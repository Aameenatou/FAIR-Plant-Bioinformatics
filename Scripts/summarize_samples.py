
from pathlib import Path
import pandas as pd

project = Path(__file__).resolve().parent.parent
file = project / "data" / "processed" / "sample_metadata.csv"

df = pd.read_csv(file)

# Extract tissue, time, and replicate from sample titles
df["tissue"] = df["sample_title"].str.extract(
    r"(?i)(Shoots|Roots)"
)[0].str.lower()

df["time_hours"] = pd.to_numeric(
    df["sample_title"].str.extract(
        r"(?i)(\d+(?:\.\d+)?)h"
    )[0],
    errors="coerce"
)

df["replicate"] = pd.to_numeric(
    df["sample_title"].str.extract(
        r"(?i)Rep(\d+)"
    )[0],
    errors="coerce"
)

print("\nSamples by dataset:")
print(df.groupby("dataset").size())

print("\nSamples by group and tissue:")
print(df.groupby(["group", "tissue"]).size())

print("\nSamples by group, tissue and time:")
print(df.groupby(
    ["group", "tissue", "time_hours"],
    dropna=False
).size().to_string())

print("\nSamples with missing information:")
print(df[
    df[["tissue", "time_hours", "replicate"]]
    .isna().any(axis=1)
][["sample_id", "sample_title"]].to_string(index=False))

output = project / "data" / "processed" / "sample_metadata_enriched.csv"
df.to_csv(output, index=False)

print("\nSaved:", output)
