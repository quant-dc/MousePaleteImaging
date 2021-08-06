from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% LOAD DATA i.e. ALL CSV FILES

data_folder = Path('./data/raw_sections')
all_files = data_folder.glob("*.csv")

data = pd.concat([
    pd.read_csv(file, index_col=0).assign(Filename=file.stem)
    for file in all_files
])

data[['Stage', 'Sample', 'AP', 'CultureTime']] = data.Filename.str.split(' ', expand=True)

data = data.groupby(['Stage', 'Sample', 'AP']).agg({'Angle': 'mean', 'Length': 'mean'})

# %% SAVE DATA AS AN EXCEL FILE

#if __name__ == '__Sections__':
#    writer = pd.ExcelWriter('results/data_sections.xlsx')
#    data.to_excel(writer, sheet_name='data')
#    writer.save()

# %% CALCULATE Z SCORES GROUPED BY STAGE & AP

data.groupby(['Stage', 'AP']).mean()
data['Standardised Angle'] = (data['Angle'] - data.groupby(['Stage', 'AP']).Angle.transform('mean')) / data.groupby(['Stage', 'AP']).Angle.transform('std', ddof=0)
data['Standardised Length'] = (data['Length'] - data.groupby(['Stage', 'AP']).Length.transform('mean')) / data.groupby(['Stage', 'AP']).Length.transform('std', ddof=0)

data = data.drop(columns=['Angle', 'Length'])
data = data.reset_index()
data = data.set_index(['Stage', 'Sample'], append=True)

# %% PLOT GRAPH

# %% Scatter graphs against time
#with sns.axes_style('white'):
#    g = sns.jointplot(x='Time', y='Standardised AP', data=data, kind='kde');
#    g.set_axis_labels('Time (E12.5 + hours)', 'Standardised Shelf Length', fontsize=16)

#g = sns.regplot(x='Time', y='Standardised AP', data=fixed_data, color=".3", fit_reg=False, x_jitter=.1)
#g.set(xlabel='Embryonic Age (E12.5 + hours)', ylabel='Standardised Shelf Length')

# %% Scatter + histo + density graphs
g = sns.PairGrid(data, hue='AP')
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.kdeplot, lw=2, bw_method=.5)
g.add_legend()

plt.show()