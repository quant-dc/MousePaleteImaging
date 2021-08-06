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

invivo = data.loc[~data.Culture.str.contains('Cul', regex=False)].copy()

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
invivo['Measurement'] = invivo.Measurement.map(measurement_name_mapping)

time_stage_mapping = {
    'E12.5': '12.5',
    'E13': '13.0',
    'E13.5': '13.5',
    'E14': '14.0',
    'E14.5': '14.5',
    'E15': '15.0',
    }

# %% Plot

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.lineplot(
    data=invivo,
    x='Info',
    y='Distance',
    hue='Measurement',
    err_style='bars',
    ax=ax
)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title='Measurement')
ax.set_xlabel('Age (days)')
ax.set_ylabel('Distance (mm)')
plt.title('Maxillary Growth In Vivo', fontweight='bold')
sns.despine(left=True)
plt.tight_layout()
plt.savefig(results_folder / 'Maxillary Growth In Vivo', dpi=700)
# plt.show()