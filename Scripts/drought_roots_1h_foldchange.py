from pathlib import Path
import gzip
import numpy as np
import pandas as pd

# Locate project folders
project = Path(__file__).resolve().parent.parent
raw = project / "data" / "raw"
processed = project / "data" / "processed"
processed.mkdir(parents=True, exist_ok=True)

# Read the expression matrices
def load_expression(accession):
    path = raw / f"{accession}_series_matrix.txt.gz"

    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip() == "!series_matrix_table_begin":
                break
        else:
            raise ValueError("Expression table not found")

        df = pd.read_csv(
            f,
            sep="\t",
            index_col=0,
            comment="!"
        )

    return df.apply(pd.to_numeric, errors="coerce")


# Load control and drought datasets
control = load_expression("GSE5620")
drought = load_expression("GSE5624")

# Root samples collected after one hour
control_ids = ["GSM131237", "GSM131238"]
drought_ids = ["GSM131341", "GSM131342"]

# Select the four samples
control_roots = control[control_ids]
drought_roots = drought[drought_ids]

# Calculate average expression per probe
control_mean = control_roots.mean(axis=1)
drought_mean = drought_roots.mean(axis=1)

# Calculate exploratory fold changes
# Small pseudocount prevents division by zero
pseudocount = 1.0

log2_fc = np.log2(
    (drought_mean + pseudocount) /
    (control_mean + pseudocount)
)

# Create results table
results = pd.DataFrame({
    "control_mean": control_mean,
    "drought_mean": drought_mean,
    "log2_fold_change": log2_fc
})

results.index.name = "probe_id"

# Sort by absolute fold change
results = results.reindex(
    results["log2_fold_change"].abs()
    .sort_values(ascending=False).index
)

# Save results
output = processed / "drought_roots_1h_foldchange.csv"
results.to_csv(output)

print("Analysis completed successfully!")
print("Number of probes:", len(results))

print("\nTop 10 probes by absolute log2 fold change:")
print(results.head(10).to_string())

print("\nResults saved to:", output)