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
        .loc[:, ['Dist(Ant shelf L, Post shelf L)', 'Dist(Ant shelf R, Post shelf R)', 'Info', 'Culture', 'Time']]
        .set_index(['Info', 'Culture', 'Time'], append=True)
        .rename_axis(columns=['Measurement'])
        .stack()
        .to_frame(name='Distance')
        .reset_index()
)
data['Fixed'] = data.Culture.str.contains('Fix', regex=False)
data = (
    data
        .groupby(['Info', 'Culture', 'Time', 'Fixed'])['Distance']
        .mean()
        .to_frame()
        .reset_index()
)

# %% Plot

sns.lineplot(
    data=data,
    x='Time',
    y='Distance',
    hue='Fixed',
    err_style='bars'
)
plt.show()
