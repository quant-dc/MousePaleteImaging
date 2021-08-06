from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from numpy.random import normal
import seaborn as sns


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
#
# data_roller = data.loc[
#               data['Stage'].str.contains('E13.5') &
#               #data['AP'].str.contains('post') &
#               (((data['Sample'].str.contains('Cul')) & (~data['Sample'].str.contains('CulIk')) & (data['CultureTime'] == 3)) |
#               ((data['CultureTime'] == 0)))
#         , :]
#
# # %% IKEMOTO CULTURE DATA
#
# data_ikemoto = data.loc[
#                data['Stage'].str.contains('E13.5') &
#                #data['AP'].str.contains('post') &
#                (((data['Sample'].str.contains('CulIk'))) |
#                 ((data['Sample'].str.contains('Cul')) & (data['CultureTime'] == 0)))
#         , :]


def create_regression_results(roller, ikemoto):
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% REGRESSION

    model_roller = smf.ols('Length ~ CultureTime', data=roller).fit()
    model_ikemoto = smf.ols('Length ~ CultureTime', data=ikemoto).fit()

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PERCENTAGE CHANGE

    model_ikemoto_adj = smf.ols(
        'Length ~ CultureTime',
        data=ikemoto.assign(Length=ikemoto['Length'] / model_ikemoto.params['Intercept'])
    ).fit()

    model_roller_adj = smf.ols(
        'Length ~ CultureTime',
        data=roller.assign(Length=roller['Length'] / model_roller.params['Intercept'])
    ).fit()

    rates = pd.DataFrame(
        data=[
            [model_ikemoto_adj.params['CultureTime'], model_ikemoto_adj.bse['CultureTime'], model_ikemoto_adj.nobs],
            [model_roller_adj.params['CultureTime'], model_roller_adj.bse['CultureTime'], model_roller_adj.nobs],
        ],
        index=['Ikemoto', 'Roller'],
        columns=['Growth Rate', 'Standard Error', 'N']
    )

    rates['Standard Deviation'] = rates['Standard Error'] * rates['N'].pow(.5)
    return rates

stage = ['E12.5', 'E13.5']

growth_rates = {
    level: create_regression_results(
        roller=data.loc[
                  data['Stage'].str.contains(level) &
                  (((data['Sample'].str.contains('Cul')) & (~data['Sample'].str.contains('CulIk')) & (data['CultureTime'] == 3)) |
                  ((data['CultureTime'] == 0)))
            , :],
        ikemoto=data.loc[
                   data['Stage'].str.contains(level) &
                    (((data['Sample'].str.contains('CulIk'))) |
                    ((data['Sample'].str.contains('Cul')) & (data['CultureTime'] == 0)))
            , :]
    ) for level in stage
}
#
# e_125_growth_rates = create_regression_results(
#     roller=data.loc[
#               data['Stage'].str.contains('E12.5') &
#               #data['AP'].str.contains('post') &
#               (((data['Sample'].str.contains('Cul')) & (~data['Sample'].str.contains('CulIk')) & (data['CultureTime'] == 3)) |
#               ((data['CultureTime'] == 0)))
#         , :],
#     ikemoto=data.loc[
#                data['Stage'].str.contains('E12.5') &
#                #data['AP'].str.contains('post') &
#                (((data['Sample'].str.contains('CulIk'))) |
#                 ((data['Sample'].str.contains('Cul')) & (data['CultureTime'] == 0)))
#         , :]
# )
#
#
# e_135_growth_rates = create_regression_results(
#     roller=data.loc[
#               data['Stage'].str.contains('E13.5') &
#               #data['AP'].str.contains('post') &
#               (((data['Sample'].str.contains('Cul')) & (~data['Sample'].str.contains('CulIk')) & (data['CultureTime'] == 3)) |
#               ((data['CultureTime'] == 0)))
#         , :],
#     ikemoto=data.loc[
#                data['Stage'].str.contains('E13.5') &
#                #data['AP'].str.contains('post') &
#                (((data['Sample'].str.contains('CulIk'))) |
#                 ((data['Sample'].str.contains('Cul')) & (data['CultureTime'] == 0)))
#         , :]
# )


simulated_data = pd.DataFrame({
    (sample, name): normal(
        data.loc[name, 'Growth Rate'],
        data.loc[name, 'Standard Deviation'],
        1000000
    )
    for sample, data in growth_rates.items()
    for name in data.index
})

simulated_data = simulated_data.stack([0,1]).droplevel(0).to_frame(name='Growth Rate')
simulated_data.index.names = ['Stage', 'Culture System']

pd.set_option('max_columns', 10)
print(pd.concat(growth_rates, axis=1).T)

sns.violinplot(
    data=simulated_data.reset_index(),
    hue='Culture System',
    x='Stage',
    y='Growth Rate',
    split=True,
    inner='quartile'
)
plt.show()