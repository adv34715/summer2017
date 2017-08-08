import pandas as pd
df = pd.read_csv('UCI ingest.csv - UCI ingest.csv')

def req(s):
    if "# Citation Request:" in s:
        if ('Please refer to the Machine Learning Repository\'s citation policy' in s):
            index1 = s.index('Please refer to the Machine Learning Repository\'s citation policy')
            index2 = s.find('.',index1)+1
            s = s[:index1] + 'Please refer to the Machine Learning [Repository\'s citation policy.](http://archive.ics.uci.edu/ml/citation_policy.html)' + s[index2:]
            
        if "Please refer to the Machine Learning \nRepository's citation policy" in s:
            s = s.replace("Please refer to the Machine Learning \nRepository's citation policy",'Please refer to the Machine Learning [Repository\'s citation policy.](http://archive.ics.uci.edu/ml/citation_policy.html)\n')
    return(s)

def cite(s):
    if "# Papers That Cite This Data Set" in s:
        index1 = s.index("# Papers That Cite This Data Set")
        index2 = s.find('\n',index1)
        index3 = s.find('\n#',index2)
        temp = s[index2:index3]
        temp = temp.replace(' \n','\n * ')
        if temp.endswith('\n * '):
            temp = temp[:-3]
        s = s[:index2]+temp+s[index3:]
    return(s)
def ref(s):
    if "# Relevant Papers:" in s:
        index1 = s.index("# Relevant Papers:")
        index2 = s.find('\n',index1)+1
        index3 = s.find('\n#',index2)
        temp = s[index2:index3]
        temp = temp.replace('[','\n').replace(']','.')
        s = s[:index2]+temp+s[index3:]
    return(s)
for i in range(len(df)):
    if type(df.iloc[i,6]) != type(''):
        continue
    df.iloc[i,6] = df.iloc[i,6].replace('  ',' ')
    
    if df.iloc[i,6].startswith('\n'):
        df.iloc[i,6] = df.iloc[i,6][1:]
    df.iloc[i,6] = req(df.iloc[i,6])
    df.iloc[i,6] = cite(df.iloc[i,6])
    df.iloc[i,6] = ref(df.iloc[i,6])

##################
# Shorten Headline
##################
def deleteParenthesis(s):
    while "(" in s and ')' in s:
        s = s[:s.index("(")]+s[(s.index(")")+1):]
    return(s)  

def deleteLast(s):
    cur = 0
    old = 0
    count = 0
    decima = 0
    for i in range(len(s)):
        if s[i] == '.':
            old = cur
            cur = i
            if cur - old > 9:
                count += 1
                decima = old
    if count > 1:
        s = s[:decima]
    return(s)

def deleteIn(s):
    word = s.split(' ')
    for i in range(len(word)-1,len(word)-7,-1):
        if word[i] == 'in':
            return(' '.join(word[:i]+'.'))
    return(' '.join(word))
for i in range(len(df)):
    t = 0
    try:
        if df.iloc[i,5]>120:
            df.iloc[i,6] = df.iloc[i,4]+'\n'+df.iloc[i,6]
            df.iloc[i,4] = deleteParenthesis(df.iloc[i,4])
        while len(df.iloc[i,4])>120 and t < 2:
            df.iloc[i,4] = deleteLast(df.iloc[i,4])
            t += 1
        if len(df.iloc[i,4])>120:
            df.iloc[i,4] = deleteIn(df.iloc[i,4])
        df.iloc[i,5] = len(df.iloc[i,4])
    except:
        print(df.iloc[i,2])

df.to_csv('UCIFinal.csv',index=False)