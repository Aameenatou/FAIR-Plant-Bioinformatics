
from pathlib import Path
import gzip
import csv

project = Path(__file__).resolve().parent.parent
raw = project / "data" / "raw"

for accession in ["GSE5620", "GSE5624"]:
    path = raw / f"{accession}_series_matrix.txt.gz"

    print(f"\n{'=' * 50}")
    print(f"PROCESSING INFORMATION: {accession}")
    print(f"{'=' * 50}")

    found = set()

    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break

            if any(term in line.lower() for term in [
                "data_processing",
                "normalization",
                "scan_protocol",
                "hyb_protocol"
            ]):
                parts = next(csv.reader([line], delimiter="\t"))
                field = parts[0]

                if field not in found:
                    found.add(field)
                    print("\nFIELD:", field)
                    for value in parts[1:3]:
                        print(value[:1000])

    if not found:
        print("No processing fields found in Series Matrix.")
