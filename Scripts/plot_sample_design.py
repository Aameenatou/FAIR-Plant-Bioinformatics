
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

project = Path(__file__).resolve().parent.parent

data_file = (
    project / "data" / "processed"
    / "sample_metadata_enriched.csv"
)

figures = project / "figures"
figures.mkdir(exist_ok=True)

df = pd.read_csv(data_file)

summary = (
    df.groupby(
        ["time_hours", "group", "tissue"]
    )
    .size()
    .unstack(["group", "tissue"], fill_value=0)
)

ax = summary.plot(
    kind="bar",
    figsize=(11, 6),
    width=0.8
)

ax.set_title(
    "Arabidopsis thaliana: Experimental Sample Design"
)
ax.set_xlabel("Time after treatment (hours)")
ax.set_ylabel("Number of samples")
ax.legend(title="Treatment and tissue")

plt.xticks(rotation=0)
plt.tight_layout()

output = figures / "sample_design.png"
plt.savefig(output, dpi=300)
plt.show()

print("Figure saved to:", output)
