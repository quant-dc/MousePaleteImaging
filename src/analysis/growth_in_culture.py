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

measurement_name_mapping = {
    'Dist(Ant shelf L, Post shelf L)': '1-3',
    'Dist(Ant shelf R, Post shelf R)': '2-4',
    'Dist(Post shelf L, Ant whis L)': '3-5',
    'Dist(Post shelf R, Ant whis R)': '4-6',
    'Dist(Post shelf L, Ant nare L)': '3-9',
    'Dist(Post shelf R, Ant nare R)': '4-10',
    'Dist(Ant shelf L, Post whis L)': '1-7',
    'Dist(Ant shelf R, Post whis R)': '2-8',
    'Dist(Post whis L, Post whis R)': '7-8',
    'Dist(Left, Right)': '11-12'
}
cultured['Measurement'] = cultured.Measurement.map(measurement_name_mapping)

# %% Plot

fig, ax = plt.subplots(figsize=(8,4.5))
sns.lineplot(
    data=cultured,
    x='Time',
    y='Distance',
    hue='Measurement',
    err_style='bars',
    ax=ax
)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title='Measurement')
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Distance (mm)')
plt.title('Maxillary Explant Dimension Changes in Culture', fontweight='bold')
sns.despine(left=True)
plt.tight_layout()
plt.savefig(results_folder / 'Maxillary Explant Dimension Changes in Culture', dpi=700)
# plt.show()