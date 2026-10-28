from pathlib import Path
import pandas as pd

# Locate project folders
project = Path(__file__).resolve().parent.parent
processed = project / "data" / "processed"

# Read the top 20 probes
input_file = processed / "top_20_drought_probes.csv"
df = pd.read_csv(input_file, low_memory=False)

# Find columns automatically
def find_column(possible_names):
    for name in possible_names:
        for col in df.columns:
            if col.strip().lower() == name.lower():
                return col
    return None

columns = {
    "Probe ID": find_column(["probe_id"]),
    "ORF": find_column(["ORF"]),
    "Gene Symbol": find_column(["Gene Symbol"]),
    "Gene Title": find_column(["Gene Title"]),
    "Log2 Fold Change": find_column([
        "log2_fold_change",
        "log2 fold change",
        "log2FC",
        "log2FoldChange"
    ]),
    "Direction": find_column(["direction"])
}

# Check that all required columns exist
missing = [
    name for name, col in columns.items()
    if col is None
]

if missing:
    print("Available columns:", df.columns.tolist())
    raise ValueError(f"Missing columns: {missing}")

# Create clean summary
summary = df[[col for col in columns.values()]].copy()
summary.columns = list(columns.keys())

# Calculate ordinary fold change
summary["Fold Change"] = (
    2 ** pd.to_numeric(
        summary["Log2 Fold Change"],
        errors="coerce"
    )
)

# Save the summary
output = processed / "drought_gene_summary.csv"
summary.to_csv(output, index=False)

print("\nSummary created successfully!")
print("Total probes:", len(summary))
print("\nSummary preview:")
print(summary.head(5).to_string(index=False))
print("\nSaved to:", output)