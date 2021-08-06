from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf

# %% LOAD DATA

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

data = data.sort_values('CultureTime')
data['CultureTime'] = data['CultureTime'].div(24)

# %%% ROLLER CULTURE DATA

data_roller = data.loc[
              data['Stage'].str.contains('E13.5') &
              #data['AP'].str.contains('post') &
              (((data['Sample'].str.contains('Cul')) & (~data['Sample'].str.contains('CulIk')) & (data['CultureTime'] == 3)) |
              ((data['CultureTime'] == 0)))
        , :]

# %% IKEMOTO CULTURE DATA

data_ikemoto = data.loc[
               data['Stage'].str.contains('E13.5') &
               #data['AP'].str.contains('post') &
               (((data['Sample'].str.contains('CulIk'))) |
                ((data['Sample'].str.contains('Cul')) & (data['CultureTime'] == 0)))
        , :]

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% REGRESSION
#
model_roller = smf.ols('Length ~ CultureTime', data=data_roller)
model_roller = model_roller.fit()
model_roller.params['CultureTime'] / model_roller.params['Intercept']
#model_roller.summary()

model_ikemoto = smf.ols('Length ~ CultureTime', data=data_ikemoto)
model_ikemoto = model_ikemoto.fit()
model_ikemoto.params
#model_ikemoto.summary()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PERCENTAGE CHANGE

model_roller_adj = smf.ols('Length ~ CultureTime', data=data_roller.assign(Length=data_roller['Length'] / model_roller.params['Intercept']))
model_roller_adj = model_roller_adj.fit()
model_roller_adj.summary()

model_ikemoto_adj = smf.ols('Length ~ CultureTime', data=data_ikemoto.assign(Length=data_ikemoto['Length'] / model_ikemoto.params['Intercept']))
model_ikemoto_adj = model_ikemoto_adj.fit()
model_ikemoto_adj.summary()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% WELCH'S T TEST

# E12.5
# print(ttest_ind_from_stats(
#     mean1=0.0730,
#     std1=.027 * (26 ** .5),
#     nobs1=26,
#     mean2=0.0422,
#     std2=.006 * (52 ** .5),
#     nobs2=52,
#     equal_var=False
# ))
#
# sigma_1 = (.027 * (26 ** .5))
# sigma_2 = (.006 * (52 ** .5))
# n_1 = 26
# n_2 = 52
#
# var_1 = sigma_1 ** 2
# var_2 = sigma_2 ** 2
#
# denom = ((var_1 / n_1) + (var_2 / n_2)) ** .5

# USE THIS
print(ttest_ind_from_stats(
    mean1=.1172,
    std1=.122589 * (52 ** .5),
    nobs1=52,
    mean2=.0706,
    std2=.135834 * (69 ** .5),
    nobs2=69,
    equal_var=False
))

# # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PLOT GRAPH
#
# x = np.array(['E12.5 Roller', 'E12.5 Ikemoto', 'E13.5 Roller', 'E13.5 Ikemoto'])
# y = np.array([0.0422, 0.073, 0.0302, 0.0229])
# e = np.array([0.006, 0.027, 0.007, 0.01])
# plt.errorbar(x, y, e, linestyle='None', marker='o', ecolor='green', ms=10, mfc='green', mec='green', elinewidth=3, capsize=5, capthick=3)
#
# plt.title('Coefficients of Growth w/ Standard Error', fontsize=18)
# plt.ylabel('Coefficients of Growth (mm per day)', fontsize=16)
# plt.xlabel('Palate Stage and Culture System', fontsize=16)
# plt.tick_params(axis='x', labelsize=14)
# plt.tick_params(axis='y', labelsize=14)
# #plt.xlim(-0.75, 1.75)
# sns.despine(left=True)
# plt.grid(axis='y', alpha=.5)
# plt.tight_layout()
# plt.show()