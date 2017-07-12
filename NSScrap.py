
# coding: utf-8
#import urllib2
import urllib.request #python3
from bs4 import BeautifulSoup
import csv
import pandas as pd

df = pd.read_csv('nationalStatistics.csv')
urls = df[['title','landingPage']]
urls['DownloadURL'],urls['DatasetTitle'],urls['FileNameLink']=None,None,None

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def getAppendix(url):
    return(url.split('/')[-1])

def getLink(url,hdr,apped):
    req= urllib.request.Request(url,headers=hdr)
    page= urllib.request.urlopen(req)
    
    soup = BeautifulSoup(page)
    
    links = soup.find_all('a',class_="btn")
                          #class_="btn btn--primary btn--thick")
    if len(links)>0:
        for i in range(len(links)):
            link = links[i]
            href = link.get('href').replace('/file?uri=','https://www.ons.gov.uk')
            if apped in href:
                name = link.get('data-ga-event-label')
                file_name = href.split('/')[-1]
                if len(name)<=len(apped):
                    name = soup.h1.text[11:-1] + ': ' + apped 
                    return(href,name,file_name)
                    break
         
    else:
        temp = getAppendix(url)
        url = url.replace(temp,'')[:-1]
        getLink(url,hdr,temp)     

urls_prob = []
for i in range(len(urls)):
    url = urls.iloc[i]['landingPage']
    if(i%100==0):
        print(i)
        
    apped = getAppendix(url)
    try:
        download,dstitle,filename=getLink(url,hdr,apped)
        urls.set_value(i,'DownloadURL',download)
        urls.set_value(i,'DatasetTitle',dstitle)
        urls.set_value(i,'FileNameLink',filename)
        
    except:
        urls_prob.append(url)


urls.to_csv('url.csv',index=False)