from pathlib import Path

import seaborn as sns
import matplotlib.pyplot as plt

from data.ml_growth import data

results_folder = Path(__file__).parents[2] / 'results'

sns.set_style("whitegrid")
sns.set_context('notebook')

# %% Adjust the data

data = data.stack().mul(100)
data = data.reset_index()
data.columns = ['Culture', 'Age (days)', 'Percentage (%)']

# %% Plot

ax = sns.pointplot(
    data=data,
    x='Age (days)',
    y='Percentage (%)',
    color='#f210ea',
)
ax.set_ylim(0, 100)
ax.set_ylabel('Mediolateral Shelf Width \n(as a percentage of total width)')
sns.despine(left=True)
plt.subplots_adjust(top=.95)
plt.title('Mediolateral Shelf Growth occurs in Culture', fontweight='bold')
# plt.savefig(results_folder / 'Distances of POI in Cultured Samples over time.png', dpi=700)
plt.show()
