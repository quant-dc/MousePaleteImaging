from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

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
fixed = data.loc[data.Culture.str.contains('Fix', regex=False)].copy()

# %% Plot cultured timeseries

g = sns.FacetGrid(
    data=cultured.sort_values('Info'),
    col='Info',
    hue='Measurement',
    col_wrap=2,
    height=4,
    sharey=True,
    sharex=True
)
g.map(sns.lineplot, 'Time', 'Distance', err_style='bars')
sns.despine(left=True)
g.set_titles('{col_name}')
g.add_legend()
plt.suptitle('Distances of POI in Cultured Samples over time', fontweight='bold')
plt.subplots_adjust(top=.9)
plt.savefig(results_folder / 'Distances of POI in Cultured Samples over time.png', dpi=700)

# %% Culture 12 observations

twelve_cultured = pd.concat([
    cultured.loc[cultured.Info.str.contains('E12.5', regex=False), :],
    cultured.loc[cultured.Info.str.contains('E12.5', regex=False), :].copy().assign(Info='E12.5 (All Data)')
])

g = sns.FacetGrid(
    data=twelve_cultured,
    col='Info',
    hue='Measurement',
    height=4,
)
g.map(sns.lineplot, 'Time', 'Distance', err_style='bars', ci=.9)
g.set_titles('{col_name}')
g.add_legend()
sns.despine(left=True)
plt.suptitle('Distances of POI in E12.5 Cultured Samples over time', fontweight='bold')
plt.subplots_adjust(top=.85)
plt.savefig(results_folder / 'Distances of POI in E12.5 Cultured Samples over time.png', dpi=700)

# %% Fixed growth over time

fig, ax = plt.subplots(figsize=(16, 9))

sns.lineplot(
    data=fixed,
    x='Time',
    y='Distance',
    hue='Measurement',
    ax=ax,
    err_style='bars',
)
ax.set_title('Distances of POI in Fixed Samples over time', fontweight='bold', fontsize=14)
sns.despine(left=True)
plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
ax.set_ylim(0, ax.get_ylim()[1]);
plt.tight_layout()
plt.savefig(results_folder / 'Distances of POI in Fixed Samples over time.png', dpi=700)

# Model linear trend

example = fixed.loc[fixed.Measurement == 'Dist(Left, Right)', :].copy()
model = sm.OLS(example['Distance'], sm.add_constant(example['Time']))
model = model.fit()
model.summary()
