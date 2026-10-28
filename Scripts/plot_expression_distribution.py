
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

# Log2 transform for exploratory visualization only
control_log = np.log2(control + 1)
drought_log = np.log2(drought + 1)

plt.figure(figsize=(10, 6))

plt.hist(
    control_log.to_numpy().ravel(),
    bins=100,
    density=True,
    alpha=0.5,
    label="Control"
)

plt.hist(
    drought_log.to_numpy().ravel(),
    bins=100,
    density=True,
    alpha=0.5,
    label="Drought"
)

plt.title("Distribution of Arabidopsis Gene Expression Values")
plt.xlabel("Log2(Expression + 1)")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()

output = figures / "expression_distribution.png"
plt.savefig(output, dpi=300)
plt.show()

print("Figure saved to:", output)
