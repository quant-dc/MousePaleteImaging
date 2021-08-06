from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
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

# %% ORGANISE DATA FOR T(in vivo)-T0

data = data.reset_index()
data = data.loc[
       data['Stage'].str.contains('E13.5') &
       (data['CultureTime'] == 0)
, :]

data['Dissection'] = np.where(data.Sample.str.contains('Fix', regex=False), 'Tongue + mandible in situ', 'Tongue + mandible removed')

# %% PLOT GRAPH

ax = sns.barplot(
    data=data,
    x='AP',
    y='Angle',
    hue='Dissection',
    hue_order=['Tongue + mandible in situ', 'Tongue + mandible removed'],
    order=['ant','mid','post'],
    palette="Blues",
    saturation=0.8,
    ci=95,
    errwidth=1.5,
    capsize=0.06
)

ax = sns.stripplot(
    data=data,
    x="AP",
    y="Angle",
    hue="Dissection",
    hue_order=['Tongue + mandible in situ', 'Tongue + mandible removed'],
    order=['ant', 'mid', 'post'],
    palette="Blues",
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
    title=None,
    loc='upper left',
    frameon=True,
    fontsize=14,
    title_fontsize=14
)

sns.despine(top=True, right=True, left=True, bottom=False)
plt.tight_layout()
plt.show()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% T TEST

data1_ant = data.loc[((data['Dissection'] == 'Tongue + mandible in situ') & (data['AP'] == 'ant')), 'Angle']
data1_mid = data.loc[((data['Dissection'] == 'Tongue + mandible in situ') & (data['AP'] == 'mid')), 'Angle']
data1_post = data.loc[((data['Dissection'] == 'Tongue + mandible in situ') & (data['AP'] == 'post')), 'Angle']
data2_ant = data.loc[((data['Dissection'] == 'Tongue + mandible removed') & (data['AP'] == 'ant')), 'Angle']
data2_mid = data.loc[((data['Dissection'] == 'Tongue + mandible removed') & (data['AP'] == 'mid')), 'Angle']
data2_post = data.loc[((data['Dissection'] == 'Tongue + mandible removed') & (data['AP'] == 'post')), 'Angle']

print(ttest_ind(data1_ant, data2_ant, equal_var=False))
print(ttest_ind(data1_mid, data2_mid, equal_var=False))
print(ttest_ind(data1_post, data2_post, equal_var=False))