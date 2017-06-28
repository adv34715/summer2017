import yaml
import pandas as pd

with open('govtrack 2/congress-legislators/legislators-social-media.yaml','r') as f:
        social = yaml.load(f)

data_list = []
for row in social:
    temp = {}
    for key in row:
        for k in row[key]:
            temp[k]=row[key][k]
    data_list.append(temp)

len(data_list)

df_so = pd.DataFrame(data_list)
df_so.to_csv('datasets/legislators-social-media.csv',index=False)