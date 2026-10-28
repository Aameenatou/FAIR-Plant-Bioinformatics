from pathlib import Path
import pandas as pd

# Find the project folders
project = Path(__file__).resolve().parent.parent
raw = project / "data" / "raw"
processed = project / "data" / "processed"

# Find the GPL198 annotation file
files = list(raw.glob("GPL198*.txt"))

if not files:
    raise FileNotFoundError("GPL198 text file not found")

annotation_file = files[0]

print("Reading:", annotation_file.name)

# Read the annotation table
annotation = pd.read_csv(
    annotation_file,
    sep="\t",
    comment="#",
    dtype=str,
    low_memory=False
)

print("Annotation columns:")
print(annotation.columns.tolist())

# Find the probe ID column
possible_columns = ["ID", "ID_REF", "Probe Set ID"]

probe_column = next(
    (col for col in possible_columns if col in annotation.columns),
    None
)

if probe_column is None:
    raise ValueError("Probe ID column not found")

# Read our fold-change results
results_file = processed / "drought_roots_1h_foldchange.csv"

results = pd.read_csv(results_file, dtype={"probe_id": str})

# Match probes to annotations
annotation = annotation.drop_duplicates(subset=[probe_column])

merged = results.merge(
    annotation,
    left_on="probe_id",
    right_on=probe_column,
    how="left"
)

# Save the annotated results
output = processed / "drought_roots_1h_annotated.csv"

merged.to_csv(output, index=False)

print("\nAnalysis completed!")
print("Total probes:", len(merged))
print("Matched probes:", merged[probe_column].notna().sum())

print("\nTop 10 annotated probes:")
print(merged.head(10).to_string(index=False))

print("\nSaved to:", output)