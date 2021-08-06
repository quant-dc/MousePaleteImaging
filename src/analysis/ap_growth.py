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

data['CultureType'] = np.where(
    data.Culture.str.contains('CulIk', regex=False),
    'Ikemoto',
    'Normal'
)

data['Stage/Fixed'] = np.where(
     (data.Culture.str.contains('Fix', regex=False)) & (data.CultureType.str.contains('Normal', regex=False)),
     'In vivo',
     data.Info.str.extract(r'(?P<capture>E[1-9\.]*)')['capture']
 )

cultured_mapping = {
    0: 12.5,
    17: 13,
    24: 13.5,
    41: 14,
    48: 14.5,
    65: 15,
    72: 15.5
}

not_fixed = data['Stage/Fixed'] != 'In vivo'
data.loc[not_fixed, 'Time'] = data.loc[not_fixed, 'Time'].map(cultured_mapping)
data.loc[not_fixed, 'Time'] += data.loc[not_fixed, 'Stage/Fixed'].str.replace('E', '').astype(float) - 12.5
data.loc[~not_fixed, 'Time'] = data.loc[~not_fixed, 'Info'].str.replace('E', '').astype(float)

data = (
    data
        .groupby(['Info', 'Culture', 'Time', 'Stage/Fixed', 'CultureType'])['Distance']
        .mean()
        .to_frame()
        .reset_index()
)

# %% Plot

ax = sns.lineplot(
    data=(
        data.loc[data['CultureType'] != 'Ikemoto', :]
            .sort_values(
                'Stage/Fixed',
                key=lambda x: x.str.replace('In vivo', '0').str.replace('E', '').astype(float)
            )
    ),
    x='Time',
    y='Distance',
    hue='Stage/Fixed',
    hue_order=['In vivo', 'E12.5', 'E13.5'],
    err_style='bars',
    palette={'E12.5': '#f210ea', 'E13.5': '#2AA61B', 'In vivo': '#000054'},
    lw=3,
)
ax.set_xlabel('Embryonic Age (days)', fontsize=16)
ax.set_ylabel('Shelf Length (mm)', fontsize=16)
plt.tick_params(axis='x', labelsize=14)
plt.tick_params(axis='y', labelsize=14)
plt.legend(title=None, fontsize=16)
sns.despine(left=True)
plt.tight_layout()
plt.show()
