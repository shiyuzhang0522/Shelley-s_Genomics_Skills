#!/usr/bin/env python3
"""Audit legacy dmcable/spacexr full/doublet CSV exports. No RCTD fitting.

CSV first column must contain barcodes (R write.csv's blank header is accepted).
Doublet compositions are emitted only for converged, subtype-resolved singlets
and certain pairs. Class-level/uncertain results are retained as metadata with
NA compositions, because a class mapping or additional interpretation is needed.
"""
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path


def read_table(path):
    with Path(path).open(newline='', encoding='utf-8-sig') as fh:
        rows = list(csv.reader(fh))
    if len(rows) < 2 or len(rows[0]) < 2:
        raise ValueError(f'{path}: need header, barcode column and data')
    header = rows[0][1:]
    if any(not x.strip() for x in header) or len(set(header)) != len(header):
        raise ValueError(f'{path}: empty or duplicate column names')
    data = {}
    for line, row in enumerate(rows[1:], 2):
        if len(row) != len(rows[0]) or not row[0].strip():
            raise ValueError(f'{path}:{line}: invalid row width or barcode')
        if row[0] in data:
            raise ValueError(f'{path}:{line}: duplicate barcode {row[0]}')
        data[row[0]] = dict(zip(header, row[1:]))
    return header, data


def number(value):
    try:
        v = float(value)
    except (ValueError, TypeError):
        raise ValueError(f'Invalid weight: {value!r}') from None
    if not math.isfinite(v) or v < 0:
        raise ValueError(f'Weight must be finite and nonnegative: {value!r}')
    return v


def boolean(value):
    if str(value).upper() in ('TRUE', 'T', '1'):
        return True
    if str(value).upper() in ('FALSE', 'F', '0'):
        return False
    raise ValueError(f'Invalid boolean: {value!r}')


def audit(mode, weights_path, classifications_path=None, expected_path=None):
    header, weights = read_table(weights_path)
    expected = None
    if expected_path:
        expected = Path(expected_path).read_text().splitlines()
        if not expected or any(not b.strip() for b in expected) or len(set(expected)) != len(expected):
            raise ValueError('Expected barcode file must contain unique nonempty lines, no header')
        unexpected = set(weights) - set(expected)
        if unexpected:
            raise ValueError(f'Unexpected result barcodes: {sorted(unexpected)[:5]}')
    excluded = [b for b in expected or [] if b not in weights]
    report = {'mode': mode, 'result_spots': len(weights),
              'expected_spots': len(expected) if expected is not None else None,
              'excluded_spots': len(excluded) if expected is not None else None,
              'units': 'cell-type RNA/count fractions, not physical cell fractions',
              'implementation': 'legacy dmcable/spacexr CSV semantics',
              'biological_validation': 'not performed'}
    fractions, statuses = {}, {}
    if mode == 'full':
        sums = []
        for b, row in weights.items():
            values = [number(row[k]) for k in header]
            total = math.fsum(values)
            if not math.isfinite(total) or total <= 0:
                raise ValueError(f'{b}: nonpositive/nonfinite full-weight sum')
            sums.append(total)
            fractions[b] = [v / total for v in values]
            statuses[b] = {'status': 'normalized_full_fit',
                           'convergence': 'not_available_in_full_export',
                           'first_type': '', 'first_class': ''}
        report.update(raw_sum_min=min(sums), raw_sum_max=max(sums),
                      composition_rows=len(fractions),
                      convergence='cannot be certified from full-mode export')
        types = header
    else:
        if set(header) != {'first_type', 'second_type'}:
            raise ValueError('Doublet weight columns must be first_type and second_type')
        if not classifications_path:
            raise ValueError('Doublet mode requires --classifications')
        cols, classes = read_table(classifications_path)
        required = {'spot_class', 'first_type', 'second_type', 'conv_all',
                    'conv_doublet', 'first_class', 'second_class'}
        if not required.issubset(cols):
            raise ValueError(f'Missing classification fields: {sorted(required-set(cols))}')
        if set(classes) != set(weights):
            raise ValueError('Classification/weight barcodes do not match exactly')
        types = sorted({r[k] for r in classes.values() for k in ('first_type','second_type')
                        if r[k] and r[k] != 'NA'})
        if not types:
            raise ValueError('No cell-type names present')
        for b, row in weights.items():
            c = classes[b]
            cl = c['spot_class']
            if cl not in {'singlet','doublet_certain','doublet_uncertain','reject'}:
                raise ValueError(f'{b}: unknown spot_class {cl!r}')
            for key in ('first_type', 'second_type'):
                label = c[key]
                if label != label.strip() or (label and not label.strip()):
                    raise ValueError(f'{b}: whitespace in {key} label')
            if cl != 'reject' and c['first_type'] in ('', 'NA'):
                raise ValueError(f'{b}: missing first type for a non-rejected call')
            if cl in {'doublet_certain', 'doublet_uncertain'} and c['second_type'] in ('', 'NA'):
                raise ValueError(f'{b}: missing second candidate type')
            pair = [number(row['first_type']), number(row['second_type'])]
            if abs(math.fsum(pair)-1) > 1e-5:
                raise ValueError(f'{b}: pair weights do not sum to one')
            ca, cd = boolean(c['conv_all']), boolean(c['conv_doublet'])
            fc, sc = boolean(c['first_class']), boolean(c['second_class'])
            status = cl
            values = None
            # Conservative policy: preserve original flags but don't certify
            # an unresolved/nonconverged composition.
            if not (ca and cd):
                status = 'nonconverged'
            elif cl in {'singlet','doublet_certain'}:
                if fc or (cl == 'doublet_certain' and sc):
                    status = 'class_mapping_required'
                else:
                    if c['first_type'] not in types:
                        raise ValueError(f'{b}: missing first type')
                    values = [0.0] * len(types)
                    if cl == 'singlet':
                        values[types.index(c['first_type'])] = 1.0
                    else:
                        if c['second_type'] not in types or c['second_type'] == c['first_type']:
                            raise ValueError(f'{b}: invalid certain pair')
                        values[types.index(c['first_type'])] = pair[0]
                        values[types.index(c['second_type'])] = pair[1]
            fractions[b] = values if values is not None else ['NA']*len(types)
            statuses[b] = {'status':status, 'original_spot_class':cl,
                           'first_type':c['first_type'], 'second_type':c['second_type'],
                           'first_class':fc, 'second_class':sc,
                           'conv_all':ca, 'conv_doublet':cd,
                           'confident_first_identity': bool(ca and cd and cl != 'reject')}
        report['status_counts'] = dict(Counter(r['status'] for r in statuses.values()))
        report['composition_rows'] = sum(all(isinstance(v,float) for v in x) for x in fractions.values())
        report['policy'] = 'NA composition for uncertain, rejected, nonconverged or class-level calls; preserve metadata'
    return types, fractions, statuses, excluded, report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode', required=True, choices=['full','doublet'])
    p.add_argument('--weights', required=True)
    p.add_argument('--classifications')
    p.add_argument('--expected-barcodes', help='One original spatial barcode per line, no header')
    p.add_argument('--outdir', required=True, help='New output directory; existing paths are refused')
    a = p.parse_args()
    out = Path(a.outdir)
    if out.exists():
        p.error('Output path already exists; use a new audit directory')
    try:
        types, fractions, statuses, excluded, report = audit(
            a.mode, a.weights, a.classifications, a.expected_barcodes)
    except (ValueError, OSError, OverflowError) as e:
        p.error(str(e))
    out.mkdir(parents=True)
    with (out/'rna_fractions.csv').open('w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['barcode']+types)
        for b, values in fractions.items(): w.writerow([b]+values)
    with (out/'statuses.csv').open('w', newline='') as fh:
        columns = list(next(iter(statuses.values())))
        w = csv.DictWriter(fh, fieldnames=['barcode']+columns)
        w.writeheader()
        for b, row in statuses.items(): w.writerow({'barcode':b, **row})
    (out/'excluded_barcodes.txt').write_text(''.join(b+'\n' for b in excluded))
    (out/'audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
