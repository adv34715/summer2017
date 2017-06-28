import yaml
import pandas as pd

def writeToCsv(df,file_name):
    file = 'datasets/'+file_name+'.csv'
    df.to_csv(file,index=False)

def runExcu():
    with open('govtrack 2/congress-legislators/executive.yaml','r') as f:
        excu = yaml.load(f)
    
    bio_list = []
    term_list= []
    #terms_len = 0
    for d in excu:
        temp_bio = {}
        #if 'bioguide' in d['id']:
            #bioguide = d['id']['bioguide']
        #else:
        govtrack = d['id']['govtrack']
        for key in d:
            # all bio info
            if type(d[key]) is dict:
                for k in d[key]:
                    new_key = k+'_'+key
                    temp_bio[new_key] = d[key][k]
            # terms
            else:
                #terms_len += len(d[key]) # count for all terms of all legislator
                
                for term in d[key]:
                    term['govtrack'] = govtrack
                    term_list.append(term)
        bio_list.append(temp_bio)
        
        # 
    if len(excu)!= len(bio_list):
        print('missiing bio data. Should be %s, but only %d' %(len(data),len(bio_list)))
        
    #print('There totally are %d terms data' %len(term_list))
        
    df_ex = pd.DataFrame(bio_list)
    df_ex_term = pd.DataFrame(term_list)

    writeToCsv(df_ex,'executive')
    writeToCsv(df_ex_term,'executive-terms')


runExcu()