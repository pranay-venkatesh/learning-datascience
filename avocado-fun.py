"""

Fooling around with pandas and matplotlib.
Trying to learn data science for fun.

Author : Pranay Venkatesh

Learned from:
sentdex (Best dude ever)
Kaggle
pandas and matplotlib documentation


"""

import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('avocado.csv')

df = df.copy()[df['type'] == "organic"]     # This only takes the organic avocados; This is a measure to avoid a lot of computation problems later on

df['Date'] = pd.to_datetime(df['Date'])
print(df.head(3))
# print(df["region"])

albany_df = df[ df['region'] == 'Albany' ]

# print (albany_df.head())
print (albany_df.set_index("Date")) # Very weird that set_index actually returns a value :P
albany_df['AveragePrice'].plot()   # This actually returns a plot, so in Jupyter Notebook, the next line isn't needed.
plt.show()

albany_df.sort_index(inplace=True)
albany_df['AveragePrice'].rolling(25).mean().plot()
plt.show()

# Individually graphing out some separate values

df.sort_values(by="Date", ascending=True, inplace=True)

graph_df = pd.DataFrame()

for region in df['region'].unique():
    region_df = df.copy()[df['region'] == region]
    region_df.set_index("Date")
    region_df.sort_index(inplace=True)
    region_df[f"{region}_price25ma"] = region_df['AveragePrice'].rolling(25).mean()

    if graph_df.empty:                          # Adding the first element into the graph dataframe
        graph_df = region_df[[f"{region}_price25ma"]]     # Reason for putting double-brackets is because [] will give you a series while [[]] will give you a dataframe
        
    else:                                       # Adding new elements into our dataframe
        graph_df = graph_df.join(region_df[f"{region}_price25ma"])  # This line is the reason why we used df['type'] == organic, as pandas has a weird way to join stuff to dataframes


graph_df.plot(figsize=(6,7), legend=False)
plt.show()
