from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% LOAD SECTIONS DATA i.e. ALL CSV FILES

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

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ORGANISE DATA FOR GROWTH

data = data.loc[
       data['Stage'].str.contains('E12.5') &
       (((data['Sample'].str.contains('CulIk'))) |
       ((data['Sample'].str.contains('Cul')) & (data['CultureTime'] == 0)))
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
ax.set_xlabel('Time in Ikemoto Culture (hours)', fontsize=14)
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

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SHELF ELEVATION

# %% PLOT GRAPH

# ax = sns.barplot(
#     data=data,
#     x='AP',
#     y='Angle',
#     hue='CultureTime',
#     hue_order=['0', '48'],
#     order=['ant', 'mid', 'post'],
#     ci=95,
#     errwidth=2,
#     capsize=.08,
#     palette="Blues",
#     saturation=0.8,
# )
#
# ax.set_xlabel('Palatal shelf region, E12.5', fontsize=14)
# ax.set_ylabel('Palatal Shelf Angle (degrees)', fontsize=14)
#
# plt.legend(title='Time in culture (hours)', fontsize=12)
# sns.despine(left=True)
# plt.tight_layout()
# plt.show()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% COMPARE GROWTH RATES

# df = data.drop(columns=['Angle']).set_index(['Stage', 'Sample', 'AP', 'CultureTime']).unstack(3)
#
# df = data.groupby(['Stage', 'CultureTime']).Length.mean().unstack().T
#
# print(df.pct_change())
#
# # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% REGRESSION
#
# model = smf.ols('Length ~ CultureTime', data=data)
# model = model.fit()
#
# model.summary()