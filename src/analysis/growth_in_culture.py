from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")
sns.set_context('notebook')

results_folder = Path(__file__).parents[2] / 'results'

# %% Load Data

data = (
    pd.read_excel(results_folder / 'data.xlsx', sheet_name='Distances', index_col='File')
        .set_index(['Info', 'Culture', 'Time'], append=True)
        .rename_axis(columns=['Measurement'])
        .stack()
        .to_frame(name='Distance')
        .reset_index()
)

cultured = data.loc[~data.Culture.str.contains('Fix', regex=False)].copy()
cultured = cultured.loc[cultured.Info.str.contains('E12.5', regex=False), :]

# %% Plot

sns.lineplot(
    data=cultured,
    x='Time',
    y='Distance',
    hue='Measurement',
    err_style='bars'
)
plt.show()