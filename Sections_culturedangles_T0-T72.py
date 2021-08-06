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
data['CultureTime'] = data['CultureTime'].astype(float)

data = data.groupby(['Stage', 'Sample', 'AP', 'CultureTime']).agg({'Angle': 'mean', 'Length': 'mean'})
data = data.reset_index()

# %% ORGANISE DATA FOR T0-T72
data = data.reset_index()
data = data.loc[
       data['Stage'].str.contains('E13.5') &
       data['Sample'].str.contains('Cul') &
       ~data['Sample'].str.contains('CulIk') &
       (data['CultureTime'] != 20)
, :]
# %%%%%%%%% FOR T(IN VIVO) - T72 %%%%%%%%%%%%
data = data.loc[
       data['Stage'].str.contains('E13.5') & ~data['Sample'].str.contains('CulIk') &
       (((data['Sample'].str.contains('Cul')) & (data['CultureTime'] == 72)) |
         (data['Sample'].str.contains('Fix')))
, :]

data = data.sort_values('CultureTime')
data['CultureTime'] = data['CultureTime'].astype(int).astype(str) + ' hours'

# %% PLOT GRAPH

ax = sns.barplot(
    data=data,
    x='AP',
    y='Angle',
    hue='CultureTime',
    hue_order=['0 hours', '72 hours'],
    order=['ant','mid','post'],
    palette="Purples",
    saturation=0.8,
    ci=95,
    errwidth=1.5,
    capsize=0.06
)

ax = sns.stripplot(
    data=data,
    x="AP",
    y="Angle",
    hue="CultureTime",
    hue_order=['0 hours', '72 hours'],
    order=['ant', 'mid', 'post'],
    palette="Purples",
    dodge=True,
    edgecolor="black",
    linewidth=.75,
    ax=ax,
)

ax.set(ylim=(0, 100))
ax.set_xlabel('Palatal Shelf Region', fontsize=14)
ax.set_ylabel('Palatal Shelf Angle (degrees)', fontsize=14)
plt.tick_params(axis='x', labelsize=14)
plt.tick_params(axis='y', labelsize=14)

handles, labels = ax.get_legend_handles_labels()
l = plt.legend(
    handles[2:4],
    labels[2:4],
    title='Time after dissection',
    loc='upper left',
    frameon=True,
    fontsize=14,
    title_fontsize=14
)

sns.despine(top=True, right=True, left=True, bottom=False)
plt.tight_layout()
plt.show()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% T TEST

data1_ant = data.loc[((data['CultureTime'] == '0 hours') & (data['AP'] == 'ant')), 'Angle']
data1_mid = data.loc[((data['CultureTime'] == '0 hours') & (data['AP'] == 'mid')), 'Angle']
data1_post = data.loc[((data['CultureTime'] == '0 hours') & (data['AP'] == 'post')), 'Angle']
data2_ant = data.loc[((data['CultureTime'] == '72 hours') & (data['AP'] == 'ant')), 'Angle']
data2_mid = data.loc[((data['CultureTime'] == '72 hours') & (data['AP'] == 'mid')), 'Angle']
data2_post = data.loc[((data['CultureTime'] == '72 hours') & (data['AP'] == 'post')), 'Angle']

print(ttest_ind(data1_ant, data2_ant, equal_var=False))
print(ttest_ind(data1_mid, data2_mid, equal_var=False))
print(ttest_ind(data1_post, data2_post, equal_var=False))