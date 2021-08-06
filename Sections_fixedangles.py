from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# %% LOAD DATA i.e. ALL CSV FILES

data_folder = Path('./data/raw_sections')
all_files = data_folder.glob("*.csv")

data = pd.concat([
    pd.read_csv(file, index_col=0).assign(Filename=file.stem)
    for file in all_files
])

data[['Stage', 'Sample', 'AP', 'CultureTime']] = data.Filename.str.split(' ', expand=True)

data = data.groupby(['Stage', 'Sample', 'AP']).agg({'Angle': 'mean', 'Length': 'mean'})
data = data.reset_index()

data = data.loc[(data['Stage'] == 'E12.5') & (data['Sample'].str.contains('Fix')) |
                (data['Stage'] == 'E15.5') & (data['Sample'].str.contains('Fix'))]

# %% PLOT GRAPH

ax = sns.barplot(
    data=data,
    x='AP',
    y='Angle',
    hue='Stage',
    hue_order=['E12.5', 'E15.5'],
    order=['ant','mid','post'],
    palette="Blues", #{'E12.5': '#62b9dd', 'E15.5': '#0069c0'},
    saturation=0.8,
    ci=95,
    errwidth=1.5,
    capsize=0.06
)

ax = sns.stripplot(
    data=data,
    x="AP",
    y="Angle",
    hue="Stage",
    hue_order=['E12.5', 'E15.5'],
    order=['ant', 'mid', 'post'],
    palette="Blues",
    dodge=True,
    edgecolor="black",
    linewidth=.75,
    ax=ax,
)

ax.set(ylim=(-15, 100))
ax.set_xlabel('Palatal Shelf Region', fontsize=14)
ax.set_ylabel('Palatal Shelf Angle (degrees)', fontsize=14)
plt.tick_params(axis='x', labelsize=14)
plt.tick_params(axis='y', labelsize=14)

handles, labels = ax.get_legend_handles_labels()
l = plt.legend(
    handles[2:4],
    labels[2:4],
    title='Age in vivo',
    loc='upper left',
    frameon=True,
    fontsize=14,
    title_fontsize=14
)
sns.despine(top=True, right=True, left=True, bottom=False)
plt.tight_layout()
plt.show()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%% T TEST

data1_ant = data.loc[((data['Stage'] == 'E12.5') & (data['AP'] == 'ant')), 'Angle']
data1_mid = data.loc[((data['Stage'] == 'E12.5') & (data['AP'] == 'mid')), 'Angle']
data1_post = data.loc[((data['Stage'] == 'E12.5') & (data['AP'] == 'post')), 'Angle']
data2_ant = data.loc[((data['Stage'] == 'E15.5') & (data['AP'] == 'ant')), 'Angle']
data2_mid = data.loc[((data['Stage'] == 'E15.5') & (data['AP'] == 'mid')), 'Angle']
data2_post = data.loc[((data['Stage'] == 'E15.5') & (data['AP'] == 'post')), 'Angle']

print(ttest_ind(data1_ant, data2_ant, equal_var=False))
print(ttest_ind(data1_mid, data2_mid, equal_var=False))
print(ttest_ind(data1_post, data2_post, equal_var=False))