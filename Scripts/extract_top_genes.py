from pathlib import Path
import pandas as pd

# Locate project folders
project = Path(__file__).resolve().parent.parent
processed = project / "data" / "processed"

# Read the annotated dataset
input_file = processed / "drought_roots_1h_annotated.csv"
df = pd.read_csv(input_file, low_memory=False)

# Find the log2 fold-change column
possible_names = [
    "log2_fold_change",
    "log2FC",
    "log2FoldChange"
]

fc_col = next(
    (name for name in possible_names if name in df.columns),
    None
)

if fc_col is None:
    print("Available columns:", df.columns.tolist())
    raise ValueError("Log2 fold-change column not found")

# Convert fold changes to numbers
df[fc_col] = pd.to_numeric(df[fc_col], errors="coerce")
df = df.dropna(subset=[fc_col])

# Extract top upregulated and downregulated probes
top_up = df[df[fc_col] > 0].nlargest(10, fc_col).copy()
top_down = df[df[fc_col] < 0].nsmallest(10, fc_col).copy()

top_up["direction"] = "Upregulated"
top_down["direction"] = "Downregulated"

# Combine the results
top_genes = pd.concat([top_up, top_down])

# Save the results
output = processed / "top_20_drought_probes.csv"
top_genes.to_csv(output, index=False)

print("Analysis completed!")
print("Upregulated probes:", len(top_up))
print("Downregulated probes:", len(top_down))
print("Saved to:", output)