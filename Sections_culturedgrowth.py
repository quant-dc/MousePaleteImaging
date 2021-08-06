from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind_from_stats

# %% LOAD DATA i.e. ALL CSV FILES

data_folder = Path('./data/raw_sections')
all_files = data_folder.glob("*.csv")

data = pd.concat([
    pd.read_csv(file, index_col=0).assign(Filename=file.stem)
    for file in all_files
])

# %% ORGANISE DATA

data[['Stage', 'Sample', 'AP', 'CultureTime']] = data.Filename.str.split(' ', expand=True)
data['CultureTime'] = data['CultureTime'].astype(float)

data = data.groupby(['Stage', 'Sample', 'AP', 'CultureTime']).agg({'Angle': 'mean', 'Length': 'mean'})

data = data.reset_index()

data = data.loc[
       data['Stage'].str.contains('E12.5') &
       (((data['Sample'].str.contains('Cul')) & (~data['Sample'].str.contains('CulIk')) & (data['CultureTime'] == 72)) |
       ((data['CultureTime'] == 0)))
, :]

data = data.sort_values('CultureTime')
data['CultureTime'] = data['CultureTime'].astype(int).astype(str)

data['AP'] = data['AP'].str.replace('ant','anterior').replace('mid','middle').replace('post','posterior')

# %% PLOT GRAPH

ax = sns.lineplot(
    data=data,
    x='CultureTime',
    y='Length',
    hue='AP',
    hue_order=['anterior', 'middle', 'posterior'],
    palette="mako_r",
    ci=95,
    err_style='bars',
    err_kws={'capsize': 8, 'elinewidth': 3, 'capthick': 2},
    lw=4
)
sns.stripplot(
    data=data,
    x='CultureTime',
    y='Length',
    hue='AP',
    hue_order=['anterior', 'middle', 'posterior'],
    palette="mako_r",
    jitter=.1,
    dodge=False,
    size=5,
    edgecolor="gray",
    linewidth=.5,
    alpha=.7,
    ax=ax,
)

ax.set(ylim=(0.25, 1.0), xlim=(-.18, 1.18))
ax.set_xlabel('Time in Culture (hours)', fontsize=14)
ax.set_ylabel('Shelf Length (mm)', fontsize=14)
plt.tick_params(axis='x', labelsize=14)
plt.tick_params(axis='y', labelsize=14)

handles, labels = ax.get_legend_handles_labels()
l = plt.legend(
    handles[0:3],
    labels[0:3],
    title='Shelf Region',
    loc='upper left',
    frameon=True,
    fontsize=14,
    title_fontsize=14
)

sns.despine(left=True)
plt.grid(axis='y', alpha=.5)
plt.tight_layout()
plt.show()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% COMPARE GROWTH RATES
#
# df = data.drop(columns=['Angle']).set_index(['Stage', 'Sample', 'AP', 'CultureTime']).unstack(3)
#
# df = data.groupby(['Stage', 'CultureTime']).Length.mean().unstack().T
#
# print(df.pct_change())

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% REGRESSION

#data['DummyTime'] = data['CultureTime'].replace(72,1)

# %% Regression based on continuous time, Length = m * CultureTime + c

model = smf.ols('Length ~ CultureTime', data=data)
model = model.fit()

model.summary()

# model = smf.ols('Length ~ DummyTime', data=data)
# model = model.fit()
# model.summary()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% WELCH'S T TEST

data1_Ro = data.loc[((data['Stage'] == 'E12.5') & (data['AP'] == 'ant')), 'Angle']
data1_Ik = data.loc[((data['Stage'] == 'E12.5') & (data['AP'] == 'post')), 'Angle']

# Calculate mean growth rate ('MEAN'), and STD for each sample

# E12.5
print(ttest_ind_from_stats(mean1='MEAN', std1='STD', nobs1='NO.OF.OBSERVATIONS', mean2='MEAN', std2='STD', nobs2='NO.OF.OBSERVATIONS', equal_var=False))
# E13.5
print(ttest_ind_from_stats(mean1='MEAN', std1='STD', nobs1='NO.OF.OBSERVATIONS', mean2='MEAN', std2='STD', nobs2='NO.OF.OBSERVATIONS', equal_var=False))