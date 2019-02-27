def decrypt(b):
    from more_itertools import sliced
    import math
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    import collections
    import pandas as pd
    import numpy as np
    import string
    punctuations = '!"#$%&\'\'()*+,-./:;<=>?@[\\]^_`{|}~'    
    a=""
    for i in b:
        if i not in punctuations:
            a=a+i
    a=a.lower()

    b=dict((letter,a.count(letter)) for letter in set(a))
    
    results=collections.Counter(b)
    
    df=pd.DataFrame.from_dict(results,orient='index').reset_index()
    
    df['index'].replace(' ',np.nan,inplace=True)
    
    df.dropna(subset=['index'],inplace=True)
    
    df.columns=['col1','count__']
    
    tot=sum(df.count__)
    
    var_exp=[(i/tot) for i in
              sorted(df.count__,reverse=True)]
    
    
    df['c']=(df.count__)/sum(df.count__)*100
    
    
    total=sum(df.count__)
    
    df['u95']=100*((df.count__)/sum(df.count__)+2.25*np.sqrt(((df.count__)/sum(df.count__))*(1-((df.count__)/                        sum(df.count__)))*1/sum(df.count__)))
    
    df['l95']=100*((df.count__)/sum(df.count__)-2.25*np.sqrt(((df.count__)/sum(df.count__))*(1-((df.count__)/sum(df.count__)))*1/sum(df.count__)))
    
    d={'col1': ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],
       'col2':[8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,
    	5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074],'col3':[1000001,	1000010,1000011,1000100,1000101,		 
    1000110,1000111,1001000,1001001,1001010,1001011,1001100,	1001101,1001110,1001111,1010000,1010001,1010010,		 
    1010011,1010100,1010101,1010110,1010111,1011000,1011001,2222222]}
       
    df2=pd.DataFrame(data=d)
    
    df2['d']=pd.Series(index=df2.index)
    
    df=df.reset_index()
    
    df2=df2.sort_values('col2',ascending=False)
    
    df2=df2.reset_index()
    
    df=df.sort_values('c',ascending=False)
    
    df=df.reset_index()
    
    #taking values from col2, are they within the CI? If yes->Print If no->NA
    l=0
    df['append']=pd.Series(index=df.index)
    
    for x in df2['col2']:
        if x < df['u95'][l] and x > df['l95'][l]:
            #print(x ,df2['col1'][l])
            df['append'][l]=df2['col1'][l]      
        if x>df['u95'][l] or  x < df['l95'][l]:
            df['append'][l]="NotinCI"
        l=1+l
    
    #if column append does not eqaul cat then take value from df2[col2] and match on column a and column append
    value=pd.merge(df2[['col1','col3']],df[['col1','append']],on='col1')
    value['cipher_text_ascii']=pd.Series(index=value.index)
    
    l=0
    
    for x in value['col1']:
        if value['append'][l]!="NotinCI":
            value['cipher_text_ascii'][l]="Nomatch"
            l=l+1
    for x in range(26):
        for y in range(26):
            if value['col1'][x]==value['append'][y]:
                value['cipher_text_ascii'][y]=value['col3'][x]
                
    value=value.dropna()
    
    alphabet=pd.DataFrame(data={'col1': ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']})
    alphabet['col2']=pd.Series(index=value.index)
    l=1
    
    for i in alphabet['col2']:
        alphabet['col2'][l-1]=l
        l=l+1
    
    shift_list=pd.DataFrame()
    
    shift_list['shift']=pd.Series(index=value.index)
    ##This is the loop that finds our shift parameter Iterate through columns1 and append match columns1 from alphabet and value find corresponding number f
        #for plain text and cipher text then do modular aritmeric
    for i,j in zip(value['col1'],value['append']):
        for k in range(26):
            if alphabet['col1'][k]==i:
                x=alphabet['col2'][k]          
        for l in range(26):
            if alphabet['col1'][l]==j:
                y=alphabet['col2'][l]
                k=(x-y)%26
                shift_list=shift_list.append({'shift':k},ignore_index=True)
        shift_list=shift_list.dropna()
        shift_list=shift_list.sort_values('shift',ascending=True)
        shift_list_freq=shift_list.groupby(['shift'])['shift'].agg({"count":len}).sort_values("count",ascending=False).reset_index()
    df3=df2[['col1']]
    df3=df3.sort_values('col1',ascending=True)
    df3=df3.reset_index()
    df3['col2']=pd.Series()
    df3['col2']=pd.DataFrame(df3,columns=['col1'])
    
    k=int(shift_list_freq['shift'][0])
    
    words_list=['the', 'then', 'most', 'have']
    
    
    
    for k in shift_list_freq['shift']:
        k=int(k)
        df3['col2']=pd.DataFrame(np.roll(df3['col2'],k))
        a2=list(a)
        for k,z in zip(a2,range(len(a2))):
            for x,y in zip(df3['col2'],df3['col1']):
                if k == y:
                    a2[z]=x
        message=''.join(str(x) for x in a2)
        t=1
        for j in range(len(words_list)):
            if words_list[j] in message:
                t=t+1                
            if t==len(words_list):
                    print(message)
    


 
