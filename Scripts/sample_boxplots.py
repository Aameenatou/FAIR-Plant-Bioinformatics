
from pathlib import Path
import gzip
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

project = Path(__file__).resolve().parent.parent
raw = project / "data" / "raw"
figures = project / "figures"
figures.mkdir(exist_ok=True)

def load_expression(accession):
    path = raw / f"{accession}_series_matrix.txt.gz"

    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip() == "!series_matrix_table_begin":
                break
        else:
            raise ValueError("Expression table not found")

        return pd.read_csv(
            f, sep="\t", index_col=0, comment="!"
        ).apply(pd.to_numeric, errors="coerce")

control = load_expression("GSE5620")
drought = load_expression("GSE5624")

combined = pd.concat([control, drought], axis=1)

# Exploratory transformation
log_expression = np.log2(combined + 1)

plt.figure(figsize=(16, 7))
plt.boxplot(
    [log_expression[col].dropna() for col in log_expression.columns],
    showfliers=False
)

plt.title("Sample-Level Expression Distributions")
plt.xlabel("Samples")
plt.ylabel("Log2(Expression + 1)")
plt.xticks([])
plt.tight_layout()

output = figures / "sample_boxplots.png"
plt.savefig(output, dpi=300)
plt.show()

print("Saved:", output)
