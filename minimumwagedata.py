import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("Minimum Wage Data.csv", encoding="latin")
sdf.to_csv("minwage.csv", encoding="utf-8")  # typically encoding is in utf-8, when reading datasets, so we're making it convenient.

# Groupby

gb = df.groupby("State")
print(gb.get_group("Alabama").set_index("Year").head())

act_min_wage = pd.DataFrame()
for name, group in df.groupby("State"):     # "name" iterates over things we group by and "group" is the required dataframe in that
    if act_min_wage.empty:
        # For each group, we're going to set the index of categorisation to be "Year"
        # Since we're intereseted mainly in "Low.2018", that's the column, we'll extract it.
        # Since we know that "Low.2018" is what we're extracting, we'll rename that column to indicate the grouping.
        act_min_wage = group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name})    

    else:
        act_min_wage = act_min_wage.join(group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name}))        

print(act_min_wage.describe())  # Print out stats

min_wage_corr = act_min_wage.replace(0, np.NaN).dropna(axis=1).corr() # Removes all columns with NaN data (in this particular dataset, 0 was used to indicate NaN)

print(min_wage_corr.head(10))

labels = [c[:2] for c in min_wage_corr.columns]  # get abbv state names.

fig = plt.figure(figsize=(12,12))  # figure so we can add axis
ax = fig.add_subplot(111)  # define axis, so we can modify
ax.matshow(min_wage_corr, cmap=plt.cm.RdYlGn)  # display the matrix
ax.set_xticks(np.arange(len(labels)))   # By default, only some names are printed. This makes sure to print all names.
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels(labels)  # Setting state abbreviations.
ax.set_yticklabels(labels)  # Setting state abbreviations

plt.show()

