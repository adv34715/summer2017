import yaml
import pandas as pd

def extractSub(data,data_list):
    for d in data:
        d['bioguide'] = bioguide
        temp = d.copy()
        for k in d:
            if type(d[k]) is list:
                for l in d[k]:
                    del temp[k]
                    temp[k] = l
                    data_list.append(temp)
                    temp = d.copy()
        data_list.append(d)

# because every legislator has different number of terms, so divide into 2 tables.
# one is bio info, one is term info. each legislator has own unique bioguide_id.
def transferInfo(data):
    bio_list = []
    term_list= []
    #terms_len = 0
    for d in data:
        temp_bio = {}
        bioguide = d['id']['bioguide']
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
                    term['bioguide'] = bioguide
                    # 'party_affiliations' is list, so split it into different records, only 2 people has that
                    if 'party_affiliations' in term:
                        for aff in term['party_affiliations']:
                            temp_term = term.copy()
                            del temp_term['party_affiliations']
                            temp_term['party_affiliations'] = aff
                            term_list.append(temp_term)
                    else:
                        term_list.append(term)
                    #term['bioguide'] = bioguide
                    #term_list.append(term)
        bio_list.append(temp_bio)
        
        # 
    if len(data)!= len(bio_list):
        print('missiing bio data. Should be %s, but only %d' %(len(data),len(bio_list)))
        
    #print('There totally are %d terms data' %len(term_list))
        
    df_bio = pd.DataFrame(bio_list)
    df_term = pd.DataFrame(term_list)
    return (df_bio,df_term)

def writeToCsv(df,file_name):
    file = 'datasets/'+file_name+'.csv'
    df.to_csv(file,index=False)

def runAll():
    with open('govtrack 2/congress-legislators/legislators-current.yaml','r') as f:
        current = yaml.load(f)
    df_cur,df_cur_term = transferInfo(current)
    writeToCsv(df_cur,'legislators-current')
    writeToCsv(df_cur_term,'legislators-current-terms')
    with open('govtrack 2/congress-legislators/legislators-historical.yaml','r') as f:
        historical = yaml.load(f)
    df_his,df_his_term = transferInfo(historical)
    writeToCsv(df_his,'legislators-historical')
    writeToCsv(df_his_term,'legislators-historical-terms')

runAll()