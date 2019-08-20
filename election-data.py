"""

This exercise is a measure to see if we can load multiple datasets and combine values and stuff

Learned from:
Sentdex


"""


import pandas as pd
import numpy as np


# Main datasets
unemp_county = pd.read_csv("output.csv")
pres16 = pd.read_csv("pres16results.csv")

pres16.rename(columns = {"county":"County", "st":"State"}, inplace=True)    # Renaming some columns so that the datasets can be joined
pres16 = pres16[pres16['cand'] == "Donald Trump"]

df = pd.read_csv("Minimum Wage Data.csv", encoding="latin")
states_abv = pd.read_csv("states.csv") # Dataset containing the US states and their abbreviations (needed as presidential data only has abbreviations)

states_abv_dict = states_abv.to_dict()['Abbreviation']


df.to_csv("minwage.csv", encoding="utf-8") 


gb = df.groupby("State")


act_min_wage = pd.DataFrame()
for name, group in df.groupby("State"):   
    if act_min_wage.empty:
        act_min_wage = group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name})    

    else:
        act_min_wage = act_min_wage.join(group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name}))        

act_min_wage = act_min_wage.replace(0, np.NaN).dropna(axis=1)

print(act_min_wage.head())

# We're going to add minimum wage data as a column to our unemployment data

def get_min_wage(year, state):
    try:
        sumthin = act_min_wage.loc[state, year]
        return sumthin
    except:
        return np.NaN


unemp_county['min_wage'] = list(map(get_min_wage, unemp_county['Year'], unemp_county['State'])) # Adding min wage data as a column to our unemployment data

print (unemp_county.tail())

# Correlation and covariance between unemployment rate and minimum wage
print(unemp_county[["Rate", "min_wage"]].corr())
print(unemp_county[["Rate", "min_wage"]].cov())

# unemp_county is a massive dataset. We're going to extract data from Feb 2015 alone.

county_2015 = unemp_county[(unemp_county['Year'] == 2015) & (unemp_county['Month'] == "February")]
county_2015['State'] = county_2015['State'].map(states_abv_dict)

for dataframe in [county_2015, pres16]:
    dataframe.set_index(["County", "State"], inplace=True)

altogether = county_2015.merge(pres16, on=["County", "State"])  # The god dataframe with EVERYTHING
altogether.dropna(inplace=True)

print(altogether.head())
print(altogether.cov())
print(altogether.corr())
