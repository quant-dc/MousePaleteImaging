from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_style("whitegrid")
sns.set_context('notebook')

results_folder = Path(__file__).parents[2] / 'results'

# %% LOAD DATA

data = (
    pd.read_excel(results_folder / 'data.xlsx', sheet_name='Distances', index_col='File')
        .loc[:, ['Dist(Ant shelf L, Post shelf L)', 'Dist(Ant shelf R, Post shelf R)',
                 'Dist(Med shelf L, Post whis L)', 'Dist(Med shelf R, Post whis R)',
                 'Info', 'Culture', 'Time']]
       )

data['Stage/Fixed'] = np.where(
    data.Culture.str.contains('Fix', regex=False),
    'In vivo',
    data.Info.str.extract(r'(?P<capture>E[1-9\.]*)')['capture']
)
data = data.set_index(['Info', 'Culture', 'Time', 'Stage/Fixed'], append=True)

# %% calculating mean of AP distances

data['AP'] = data[['Dist(Ant shelf L, Post shelf L)', 'Dist(Ant shelf R, Post shelf R)']].mean(axis=1)

# %% calculating mean proportional ML distances

data['ML'] = data[['Dist(Med shelf L, Post whis L)', 'Dist(Med shelf R, Post whis R)']].mean(axis=1)

data = data.drop(columns=['Dist(Ant shelf L, Post shelf L)', 'Dist(Ant shelf R, Post shelf R)',
                   'Dist(Med shelf L, Post whis L)', 'Dist(Med shelf R, Post whis R)'])

# %% Z-score distances, grouped by stage/fixed & time

data.groupby(['Stage/Fixed', 'Time']).mean()
data['Standardised AP'] = (data['AP'] - data.groupby(['Stage/Fixed', 'Time']).AP.transform('mean')) / data.groupby(['Stage/Fixed', 'Time']).AP.transform('std', ddof=0)
data['Standardised ML'] = (data['ML'] - data.groupby(['Stage/Fixed', 'Time']).ML.transform('mean')) / data.groupby(['Stage/Fixed', 'Time']).ML.transform('std', ddof=0)

#data = data.rename_axis(columns=['Measurement'])
#data = data.stack()
#data = data.to_frame()
data = data.drop(columns=['AP', 'ML'])
data = data.reset_index()
data = data.set_index(['Info', 'Culture', 'Time'], append=True)

# %% Fixed or cultured datasets

cultured_data = data.loc[data['Stage/Fixed'] != 'In vivo']
fixed_data = data.loc[data['Stage/Fixed'] == 'In vivo']

# %% PLOT GRAPH

# %% Scatter graphs against time
#with sns.axes_style('white'):
#    g = sns.jointplot(x='Time', y='Standardised AP', data=data, kind='kde');
#    g.set_axis_labels('Time (E12.5 + hours)', 'Standardised Shelf Length', fontsize=16)

#g = sns.regplot(x='Time', y='Standardised AP', data=fixed_data, color=".3", fit_reg=False, x_jitter=.1)
#g.set(xlabel='Embryonic Age (E12.5 + hours)', ylabel='Standardised Shelf Length')

# %% Scatter + histo + density graphs
g = sns.PairGrid(cultured_data, hue='Stage/Fixed')
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.kdeplot, lw=2)
g.add_legend()

plt.show()




