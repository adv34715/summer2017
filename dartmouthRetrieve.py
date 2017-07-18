import urllib.request #python3
import urllib
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

# connet to dartmouth
def connectDart():
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
    req= urllib.request.Request('http://www.dartmouthatlas.org/tools/downloads.aspx',headers=hdr)
    page= urllib.request.urlopen(req)
    return(soup.find_all('a'))

soup = BeautifulSoup(page, "lxml")
hyperlink = soup.find_all('a')
titles = soup.find_all('h3')


# get title 
def getTitle(titles):
    res = []
    for a in titles:
        res.append(a.text)
    return(res[1:])

# generate ingest doc  
def ingestData(hyperlink,titles):
    res = []
    names = getTitle(titles)
    data = None
    title_count = 0
    for a in hyperlink:
        section = ''
        if a.has_attr('name'):
            res.append(data)
            data = {}
            count = 0
            data['title'] = names[title_count]
            data['tags'] = a['name']
            title_count += 1
        elif a.has_attr('href'):
            link = a['href']
            if link.endswith('.xls') or link.endswith('.zip'):
                url = "http://www.dartmouthatlas.org"+link
                file = link.split('/')[-1]
                count += 1
                down_link = 'link%d' %count 
                down_file = 'fileNameLink%d' %count
                data[down_link] = url
                data[down_file] = file
    res.append(data)           
    return(res[1:])

# get columns names
def generateColName(df):
    lenth = int((len(df.columns.values)-2)/2)
    res = ['']*(lenth*2)
    for i in range(lenth):
        res[i]='link%d' %(i+1)
        res[i+lenth]='fileNameLink%d' %(i+1)
    return(['title','tags']+res)

data = ingestData(hyperlink,titles)
df_digest = pd.DataFrame(data)
columns = generateColName(df_digest)
df_digest = df_digest[columns]
df_digest.to_csv('Dartmouth_Data_Ingest_1.csv',index=False)

# donwload files from links
def downloadFiles(hyperlink,path):
    new_path = ''
    for a in hyperlink:
        if a.has_attr('name'):
            if new_path != '':
                print(new_path,'is done.')
            new_path = path + a['name']
            if not os.path.exists(new_path):
                os.makedirs(new_path)
        elif a.has_attr('href'):
            link = a['href']
            if link.endswith('.xls') or link.endswith('.zip'):
                url = "http://www.dartmouthatlas.org"+link
                file = link.split('/')[-1]
                file_path = new_path + '/' +file
                urllib.request.urlretrieve(url,file_path)

hyperlink = connectDart()
downloadFiles(hyperlink,'/Users/yimengz/Desktop/dataworld/dartmouth/')
