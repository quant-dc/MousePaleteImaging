from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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
cultured_mapping = {
    0: 12.5,
    17: 13,
    24: 13.5,
    41: 14,
    48: 14.5,
    65: 15,
    72: 15.5
}
data.loc[~data.Fixed, 'Time'] = data.loc[~data.Fixed, 'Time'].map(cultured_mapping)
data.loc[data.Fixed, 'Time'] = data.loc[data.Fixed, 'Info'].str.replace('E', '').astype(float)
data['Fixed'] = np.where(data.Fixed, 'In vivo', 'E12.5 culture')
data = (
    data
        .groupby(['Info', 'Culture', 'Time', 'Fixed'])['Distance']
        .mean()
        .to_frame()
        .reset_index()
)

data

# %% Plot

ax = sns.lineplot(
    data=data,
    x='Time',
    y='Distance',
    hue='Fixed',
    err_style='bars',
    palette={'E12.5 culture': '#f210ea', 'In vivo': '#000054'}
)
ax.set_xlabel('Age (days)')
ax.set_ylabel('Shelf length (mm)')
plt.title('Anteroposterior Shelf Growth Arrests in Culture', fontweight='bold')
plt.legend(title=None)
sns.despine(left=True)
plt.tight_layout()
plt.savefig(results_folder / 'Anteroposterior Shelf Growth Arrests in Culture.png', dpi=700)
# plt.show()
