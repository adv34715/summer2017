
# coding: utf-8
# this file is to craw all the uci datasets's info. 
# First, get each dataset's page web link;
# Then, go to each dataset link, get all the files' link and name.
# Notice: rename data file to .csv; and others that are not compressed files to .txt file.
# Finish the ingest doc.
# The code require webdriver: chromedriver and selenium.

from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import numpy as np
pd.options.display.max_colwidth = 100


# get dataset page link. Require selenium and chromedriver
# xpath_max is the # of datasests 
def getLinks(xpath_max):
    res = []
    chrome_path = r"/Users/yimengz/dev/chromedriver"
    driver=webdriver.Chrome(chrome_path)
    driver.get('http://archive.ics.uci.edu/ml/datasets.html')
    for i in range(2,xpath_max+2):
        xpath = "/html/body/table[2]/tbody/tr/td[2]/table[2]/tbody/tr[%d]/td[1]/table/tbody/tr/td[2]/p/b/a" %i
        link = driver.find_elements_by_xpath(xpath)[0].get_attribute("href")
        temp = {'link':link}
        res.append(temp)
    driver.close()
    print(len(res))
    return(res)

# find all dataset's folder's sub files
def findSubs(link,sub,href_list,file_list):
    # open link and get all href
    page = urllib.request.urlopen(link)
    href = BeautifulSoup(page, "lxml").find_all('a')

    sub += 1
    for a in href:
        a = a['href']
        if re.match(r'\w', a) or a.endswith('.csv'):
            if a.endswith('/'):
                findSubs(link+a,sub,href_list,file_list)
            else:
                if not link.endswith('/'):
                    link += '/'
                a = link + a
                names = a.split('/')
                file_name = '_'.join(names[(len(names)-sub):])
                href_list.append(a)
                file_list.append(file_name)
    return(href_list,file_list)

# get dataset name and dataset files' links and names
def getDataLink(link_dict):
    link = link_dict['link']
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, "lxml")
    data_link = soup.find('a',text="Data Folder")['href']
    html = soup.find_all(text=True)
    link_dict['name'] = html[3].replace('UCI Machine Learning Repository: ','').replace(' Data Set','')
    
    if data_link.startswith('../'):
        data_link = 'http://archive.ics.uci.edu/ml/'+ data_link[3:]
    if data_link == "http://archive.ics.uci.edu/ml/machine-learning-databases/reuters_transcribed/reuters_transcribed.html-mld/":
        data_link = "http://archive.ics.uci.edu/ml/machine-learning-databases/reuters_transcribed-mld/"
    try:
        href_list,file_list = findSubs(data_link,0,[],[])
        return (data_link,href_list,file_list)
    except:
        print(data_link)

# find all data/folders in page
def processLink(link_dict):
    try:
        data_link,href_list,file_list = getDataLink(link_dict)
        for i in range(len(href_list)):
            key_link = 'Link %d' %(i+1)
            key_file = 'Link Name %d' %(i+1)

            link_dict[key_link] = href_list[i]
            if file_list[i].lower().endswith(('data','data1','data2','data-numeric','test','train')):
                file_list[i] = file_list[i]+'.csv'
            elif not file_list[i].lower().endswith(('tgz', 'xlsx','csv', 'xls', 'gz','tar','mat','rar','z','doc','gz','mod','zip','ps','bz2','html','sql','htm','jpg','gif','jpeg','pdf','png','arff','docx','txt')):
                file_list[i] = file_list[i]+'.txt'  
            link_dict[key_file] = file_list[i]
        return (link_dict)
    except:
        print("No dataset found.",link_dict['link'])
        return()

# first step to get all links
def firstLink(links):
    for l in links:
        l = processLink(l)
        if l == None:
            links.remove(l)
            print('It havs been deleted.')
    return(links)

# transfer links to data frame
def toDF(links,other_col):
    df = pd.DataFrame(links)
    file_count = int((len(df.columns.values)-other_col)/2)
    columns = []
    columns2 = []
    column_first = []
    for i in range(file_count):
        columns.append('Link %d' %(i+1))
        columns2.append('Link Name %d' %(i+1))
    for c in df.columns.values:
        if (c not in columns) and (c not in columns2):
            column_first.append(c)
    columns = column_first + columns + columns2
    df = df[columns]
    return(df)

# scrape summary columns
def getHTML(link):
    res = []
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, "lxml")
    #html = soup.find_all(class_='normal')
    html = soup.find_all(text=True)
    html = list(filter(lambda a: a != '\n', html))
    return(html[29:])

def ProcessHTML(html):
    res = {'tags': ['UCI'],'summary':''}
    start = 0 # start get source
    section = []
    summary = ''
    for h in range(len(html)):
        if h < 20:
            if html[h] == 'Abstract':
                h += 1
                res['Headline'] = html[h][2:]
                continue
            if html[h] in ['Data Set Characteristics:','Area:','Attribute Characteristics:','Associated Tasks:']:
                h += 1
                if html[h] != 'N/A':
                    res['tags'].append(html[h])
        elif html[h].startswith(' OLD CODE:'):
            continue
        elif start <2 and html[h]!='Supported By:':
            if html[h].endswith(':'):
                if html[h]==':':
                    headline = ":"
                    point = 1
                    while(len(headline)<3):
                        headline = html[h-point] + headline
                        point += 1
                    section.append(headline)
                    summary = summary[:-(len(headline)-1)] + '\n# ' + headline + '\n'
                elif html[h][:html[h].index(':')] not in section:
                    colon = html[h].index(':')
                    section.append(html[h][:colon])
                    start = 1
                    summary += '\n# '+ html[h] + '\n'
                    #print(summary,'summary:')
            elif html[h] == ' ':
                if len(summary)>1 and summary[-1] != '\n':
                    #print(summary)
                    res['summary'] += summary + '\n'
                    summary = ''
            elif html[h].endswith(': '):
                summary += html[h] + '\n'
            elif start == 1:
                html[h] = html[h].replace('\r','').replace('--','*')
                summary += html[h]
        else:
            start=2
            res['summary'] += summary + '\n'
            break
    res['summary'] = res['summary'].replace('[View Context].','\n').replace('[Web Link]','  ').replace('in collaboration \n','in collaboration').replace('Rexa.info','[Rexa.info](http://rexa.info/)')
    return(res)
def getSummary(links):
    for l in links:
        link = l['link']
        html = getHTML(link)
        res = ProcessHTML(html)
        res['tags'] = ', '.join(res['tags'])
        l.update(res)
    return (links)

# main code
links = getLinks(383)
links = firstLink(links)
links = getSummary(links)
df2 = toDF(links,4)
df2.head()
df2.to_csv('UCIDone.csv',index=False)
df2[['Headline','name']].describe(include=["O"])

