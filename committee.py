import yaml
import pandas as pd

# count how many records, including subcommittees and parent committees
# opt = 0: current; 1: historical
def countLenCom(data,opt):
    length = 0
    for d in data:
        if 'subcommittees' in d:
            length += len(d['subcommittees'])+opt
        else: length += 1
    return (length)


# compare phone & address between sub and parent
def compareAddress(data):
    count_addr = 0
    count_call = 0
    for d in data:
        if 'subcommittees' in d:
            for sub in d['subcommittees']:
                if ('address' in sub):
                    addr_len = len(sub['address'])
                    if sub['address'] != d['address'][:addr_len]:
                        count_addr += 1
                if ('phone' in sub) and sub['phone'] != d['phone']:
                    count_call += 1
    print('differnt address: ',count_addr)
    print('\ndiffernt phone: ', count_call)

def currentSubProcess(data,data_list):
    for d in data:
        # d is dict
        if 'subcommittees' in d:
            appendix = d.copy()
            del appendix['subcommittees']
            for k in d:
                if k == 'subcommittees':
                    for sub in d[k]:
                        temp = sub.copy()
                        for subk in sub:
                            newk = 'sub_' + subk
                                #print(subk,newk)
                                #print(sub['name'],subk)
                            temp[newk] = temp.pop(subk)
                        temp.update(appendix)
                        data_list.append(temp)
        else:
            data_list.append(d)

def historicalPastNames(names):
    pastNames = {}
    for n in names:
        new_name = names[n]
        if new_name in pastNames:
            pastNames[new_name].append(n)
        else:
            pastNames[new_name] = [n]
    return (pastNames)

def historicalSubProcess(data,data_list):
    for d in data:
        # d is dict
        if 'subcommittees' in d:
            parent = d.copy()
            del parent['subcommittees']
            parent['pastNames'] = historicalPastNames(parent['names'])
            data_list.append(parent)
            
            for sub in d['subcommittees']:
                temp = sub.copy()
                temp['parent'] = d['name']
                temp['pastNames'] = historicalPastNames(temp['names'])
                data_list.append(temp)
        else:
            d['pastNames'] = historicalPastNames(d['names'])
            data_list.append(d)
# define a function that can extract subcommittes out from their parent committees. 
# use on current data: opt = 1; historical: opt = other.
# Historical data: parent committees have their own data. So, keep all except subcommittees; 
# for all sub, add a new attribute: parent.
# Current: combine sub and parent.
def extractSub(data,opt):
    data_list = []
    # data is list
    if opt == 0:
        currentSubProcess(data,data_list)
    else:
        historicalSubProcess(data,data_list)     
    return(data_list)              

# compare congreess and names, see if all the congress in the name
# only use on historical data
def compareCongressName(data):
    congress = []
    for h in data:
        if 'names' in h:
            if 'congresses' in h:
                for i in h['congresses']:
                    if i not in h['names']:
                        congress.append(h['name'])
            else:
                congress.append(h['name'])
    return(congress)
def transformData(file):
    if 'historical' in file:
        file_path = 'govtrack 2/congress-legislators/committees-historical.yaml'
        opt = 1
        csv_name = file_path.split('/')[-1].split('.')[0]+'.csv'
    else:
        file_path = 'govtrack 2/congress-legislators/committees-current.yaml'
        opt = 0
        csv_name = file_path.split('/')[-1].split('.')[0]+'.csv'
    with open(file_path,'r') as f:
        data = yaml.load(f)
    
    file_len = countLenCom(data,opt)
    data_new = extractSub(data,opt)
    
    df = pd.DataFrame(data_new)
    
    if opt==1:
        congress = compareCongressName(data_new)
        if(len(congress) != 0):
            print('missing congress name: ',congress)
        else:
            df.drop(['congresses','names'],inplace=True,axis=1)
    
    if(file_len!=len(df)):
        print('warning: missing data!',file_len,len(df))
    
    
    df.to_csv(csv_name,index=False)
    
    return (df)
    
df_cur = transformData('current')
df_his = transformData('historical')