import yaml
import pandas as pd

# open committee-membership-current.yaml
with open('govtrack 2/congress-legislators/committee-membership-current.yaml','r') as f:
    data = yaml.load(f)

# count how many records are in the file
def countLen(data):
    length = 0
    for key in data:
        length += len(data[key])
    print ('yaml file has %d committees' %length)

countLen(data)

#
def member(data):
    data_list = []
    for key in data:
        for i in range(len(data[key])):
            data[key][i]['thomas_id'] = key
            data_list.append(data[key][i])
    return (data_list)


data_list = member(data)
df = pd.DataFrame.from_dict(data_list)
df.to_csv('commMember.csv', index=False)

print('%d records are stored into csv file.' %len(df))


