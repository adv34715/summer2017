
# coding: utf-8

import json
import requests
import pandas as pd

def request():
    root = "https://api.ons.gov.uk/dataset"
    rep = requests.get(root) 
    count = rep.json()['totalItems']
    
    data = []
    page = int(count/100) + 1
    
    for i in range(page):
        url = "https://api.ons.gov.uk/dataset?limit=100&start=%d" %(i*100)
        response = requests.get(url) 
        data += response.json()['items']
    if(count==len(data)):
        print("Got %d records." %count)
    else:
        print("data is missing.")
    return data

def storeJson(name = 'NationalSatistics.json'):
    with open(name, 'w') as outfile:
        json.dump(data, outfile)

def extractSub(data,data_dict):
    if type(data) is dict:
        for k in data:
            if type(data[k]) is dict:
                extractSub(data[k],data_dict)
            elif type(data[k]) ==type([]):
                data_dict[k] = ','.join(data[k])
            else:
                data_dict[k] = data[k]

def deleteEndSpace(string):
    if len(string)>0 and string[-1]==' ':
        string = string[:-1]
    return (string)

def checkSimilarity(attr1,attr2,data_dict):
    if (attr1 in data_dict) and (data_dict[attr1] != data_dict[attr2]):
        data_dict[attr1] = deleteEndSpace(data_dict[attr1])
        data_dict[attr2] = deleteEndSpace(data_dict[attr2])
            
        lenm = len(data_dict[attr1])
        lens = len(data_dict[attr2])
            
        length = min(lenm,lens)
        if lenm != 0: 
            length -= 1
            if data_dict[attr1][length] == data_dict[attr2][length]:
                if lenm > lens:
                    data_dict[attr2] = data_dict[attr1]
            else:
                if lens<lenm:
                    # if the first word or last word match, then they are the same. 
                    #(because I have look through all cases, and this is the truth.)
                    if data_dict[attr1].split(' ')[0] == data_dict[attr2].split(' ')[0] or data_dict[attr2].split(' ')[-1] ==data_dict[attr1].split(' ')[-1]:
                        data_dict[attr2] = data_dict[attr1]
                    # else, combine them together.
                    else:
                        data_dict[attr2] = data_dict[attr2] + '. ' + data_dict[attr1]
    data_dict[attr1] = float('nan')
    return(data_dict)

def getSummary(attr,data,attr_to):
    if attr in data:
        if len(data[attr]) > 1:
            data[attr].replace('\n','')
            string = "%s: %s. " %(attr,data[attr])
            data[attr_to] += (string)
    return(data[attr_to])

def cleanDict(data):
    data_dict = {}
    for i in range(len(data)):
        record = data[i] # data[0]
        data_dict[i] = {}
        for attr in record: # data[0]['description]
            if type(record[attr]) ==type({}):
                extractSub(record[attr],data_dict[i])
            elif type(record[attr]) ==type([]):
                data_dict[i][attr] = ','.join(record[attr])
            else:
                data_dict[i][attr] = record[attr]
        
        # give unique title using uri
        data_dict[i]['uniqueTitle'] = data_dict[i]['uri'].split('datasets/')[-1].replace('/','-')
        
        # merge 'metaDescription'& 'summary'
        data_dict[i] = checkSimilarity('metaDescription','summary',data_dict[i])
        
        
        data_dict[i]['releaseDate'] = data_dict[i]['releaseDate'][:10]
        
        #uri_appendix = '/'+data_dict[i]['uri'].split('/')[-1]
        data_dict[i]['landingPage'] = 'https://www.ons.gov.uk' + data_dict[i]['uri']#.replace(uri_appendix,'')
        
        # rename contact info
        if 'name' in data_dict[i]:
            data_dict[i]['contactName'] = data_dict[i].pop('name')
            data_dict[i]['contactEmail'] = data_dict[i].pop('email')
            data_dict[i]['contactPhone'] = data_dict[i].pop('telephone')
        
        data_dict[i]['totalSummary'] = ''
        
        keys = ['versionLabel','edition','releaseDate','nextRelease','searchBoost','contactPhone', 'contactEmail','contactName']
        for key in keys:
            data_dict[i]['totalSummary'] = getSummary(key,data_dict[i],'totalSummary')
            
        '''for keys in data_dict[i]:
            #print(keys)
            # nationalStatistic what means?
            if (keys not in ['preUnit','source','unit','type','sampleSize','uri','datasetId','metaDescription','title','uniqueTitle','totalSummary','nationalStatistic']): # ,'versionLabel'?
                if len(data_dict[i][keys])>1:
                    data_dict[i]['totalSummary']+=(keys +': '+ str(data_dict[i][keys]))'''
        
    return(data_dict)

def showUnique(df):
    columns = df.columns.values
    for col in columns:
        l = len(df[col].unique())
        if  l> 10:
            print(col,': ',l)
        else:
            print(col,': ',df[col].unique())

data = request()
data_dict = cleanDict(data)

df = pd.DataFrame.from_dict(data_dict,orient='index')
df.head()

df.rename(columns={'summary': 'Description', 'title': 'headline','keywords':'tags','totalSummary':'summary','uniqueTitle':'title'}, inplace=True)
df.drop(['preUnit','source','unit','type','sampleSize','metaDescription','versionLabel','releaseDate','nextRelease','searchBoost','contactPhone', 'contactEmail','contactName'],axis = 1, inplace=True)
df.head()

df['titleCounts'] = df['title'].str.len()
df['headCounts'] = df['headline'].str.len()

df_csv = df[['title','titleCounts','headline','headCounts','Description','summary','tags','landingPage']]
df_csv.to_csv('nationalStatistics.csv',index=False)
