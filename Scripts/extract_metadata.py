
from pathlib import Path
import gzip
import csv

project = Path(__file__).resolve().parent.parent
raw = project / "data" / "raw"
processed = project / "data" / "processed"
processed.mkdir(parents=True, exist_ok=True)

records = []

for accession, group in [
    ("GSE5624", "Drought"),
    ("GSE5620", "Control")
]:
    path = raw / f"{accession}_series_matrix.txt.gz"

    metadata = {}

    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break

            if line.startswith("!Sample_geo_accession") or line.startswith("!Sample_title"):
                parts = next(csv.reader([line], delimiter="\t"))
                metadata[parts[0]] = parts[1:]

    ids = metadata.get("!Sample_geo_accession", [])
    titles = metadata.get("!Sample_title", [])

    for sample_id, title in zip(ids, titles):
        records.append({
            "dataset": accession,
            "group": group,
            "sample_id": sample_id,
            "sample_title": title
        })

output = processed / "sample_metadata.csv"

with open(output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["dataset", "group", "sample_id", "sample_title"]
    )
    writer.writeheader()
    writer.writerows(records)

print(f"Saved {len(records)} sample records.")
print(f"File: {output}")

print("\nFirst 10 samples:")
for record in records[:10]:
    print(record["sample_id"], record["sample_title"])
