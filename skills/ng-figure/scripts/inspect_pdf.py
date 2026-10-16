"""Technical PDF check, not a journal-compliance certificate. Requires PyMuPDF."""
import argparse
import json
import re
import shutil
import subprocess
import sys
import fitz


def inspect(path, width_mm=None, height_mm=None):
    errors, warnings, pages = [], [], []
    with fitz.open(path) as doc:
        for i, page in enumerate(doc):
            width, height = page.rect.width * 25.4 / 72, page.rect.height * 25.4 / 72
            for label, actual, expected in [("width", width, width_mm), ("height", height, height_mm)]:
                if expected is not None and abs(actual - expected) > 0.1:
                    errors.append(f"Page {i+1}: {label} {actual:.2f} != {expected:.2f} mm")
            if width > 180.1:
                warnings.append(f"Page {i+1}: wider than 180 mm; check whether this is a caption page.")
            spans = [s for b in page.get_text("dict")["blocks"] if "lines" in b
                     for line in b["lines"] for s in line["spans"] if s["text"].strip()]
            text = page.get_text().strip()
            if not text:
                warnings.append(f"Page {i+1}: no extractable text; inspect for outlined/rasterized labels.")
            sizes = sorted({round(s["size"], 2) for s in spans})
            if any(s < 4.95 or s > 8.05 for s in sizes):
                warnings.append(f"Page {i+1}: text outside 5–8 pt; review labels and math components.")
            if any(s > 7.05 for s in sizes):
                warnings.append(f"Page {i+1}: text >7 pt; confirm these are 8 pt panel tags.")
            for span in spans:
                if not page.rect.contains(fitz.Rect(span["bbox"])):
                    warnings.append(f"Page {i+1}: text bounding box crosses page edge: {span['text'][:60]}")
            pages.append({"page": i+1, "width_mm": round(width, 3), "height_mm": round(height, 3),
                          "text_sizes_pt": sizes, "fonts": sorted({s["font"] for s in spans}),
                          "text_characters": len(text), "image_objects": len(page.get_images()),
                          "vector_paths": len(page.get_drawings())})
    font_table = None
    if shutil.which("pdffonts"):
        result = subprocess.run(["pdffonts", str(path)], text=True, capture_output=True, check=True)
        font_table = result.stdout
        for line in font_table.splitlines()[2:]:
            if re.search(r"\bType\s+3\b", line):
                errors.append("Type 3 font: " + line.strip())
            status = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line)
            if status and status[1] == "no":
                errors.append("Unembedded font: " + line.strip())
    else:
        warnings.append("pdffonts absent; embedding and Type 3 checks not performed.")
    return {"file": str(path), "pages": pages, "errors": errors, "warnings": warnings,
            "pdffonts": font_table,
            "limitations": "Needs visual review; does not test Illustrator/macOS, overlaps or accessibility."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf")
    parser.add_argument("--width-mm", type=float)
    parser.add_argument("--height-mm", type=float)
    args = parser.parse_args()
    report = inspect(args.pdf, args.width_mm, args.height_mm)
    print(json.dumps(report, indent=2))
    sys.exit(1 if report["errors"] else 0)
