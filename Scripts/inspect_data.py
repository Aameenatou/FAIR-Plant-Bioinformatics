
from pathlib import Path
import gzip
import pandas as pd

# Locate our project folders
project = Path(__file__).resolve().parent.parent
raw_folder = project / "data" / "raw"

def inspect_dataset(accession):
    files = list(raw_folder.glob(f"*{accession}*series_matrix*.txt.gz"))
    files += list(raw_folder.glob(f"*{accession}*series_matrix*.txt"))

    if not files:
        print(f"Cannot find the matrix file for {accession}")
        return

    file_path = files[0]
    print(f"\nDataset: {accession}")
    print(f"File: {file_path.name}")

    opener = gzip.open if file_path.suffix == ".gz" else open

    with opener(file_path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
        else:
            print("Expression table not found.")
            return

        df = pd.read_csv(f, sep="\t", index_col=0, comment="!")

    print("Number of probe rows:", df.shape[0])
    print("Number of sample columns:", df.shape[1])
    print("First five probe IDs:")
    print(df.index[:5].tolist())
    print("First five sample IDs:")
    print(df.columns[:5].tolist())

inspect_dataset("GSE5624")
inspect_dataset("GSE5620")
