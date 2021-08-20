def listify_string (text):
    ''' 
    This function works for lists of shape (n,2), which works for projects/fingerprints/research
    '''
    res = text.replace(']','')
    res = res.replace('[','')
    res = res.replace('%','')
    res = res.replace('\'','')
    res = res.split(',')

    lst = []
    for i in range(len(res)//2):
        lst.append([res[2*i], res[2*i+1]])
    return lst

def get_keywords (text):
    ''' 
    This function works for lists of shape (n,2), which works for projects/fingerprints/research
    '''
    res = text.replace(']','')
    res = res.replace('[','')
    res = res.replace('%','')
    res = res.replace('\'','')
    res = res.split(',')
    str = ""
    for i in range(len(res)//2):
        str += res[2*i] + ','
    
    return str