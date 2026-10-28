
from pathlib import Path
import gzip
import pandas as pd

project = Path(__file__).resolve().parent.parent
raw = project / "data" / "raw"

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

control = load_expression("GSE5620")
drought = load_expression("GSE5624")

for name, df in [
    ("Control", control),
    ("Drought", drought)
]:
    values = df.stack()

    print(f"\n{name} dataset")
    print("Shape:", df.shape)
    print("Minimum:", values.min())
    print("Maximum:", values.max())
    print("Median:", values.median())
    print("Missing values:", df.isna().sum().sum())
    print("First five expression values:")
    print(values.head())

print("\nMatching probe IDs:",
      control.index.equals(drought.index))
