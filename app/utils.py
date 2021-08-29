def listify_string (text):
    ''' 
    This function works for lists of shape (n,2), which works for projects/fingerprints/research
    '''
    text = text.replace('\',','],')
    text = text.replace('\",','],')
    res = text.split('],')
    for i in range(len(res)):
        res[i] = res[i].replace(']','')
        res[i] = res[i].replace('[','')
        res[i] = res[i].replace('%','')
        res[i] = res[i].replace('\'','')
        res[i] = res[i].replace('\"','')

    lst = []
    for i in range(len(res)//2):
        lst.append([res[2*i], res[2*i+1]])
    return lst

def get_courses (text):
    ''' 
    This function works for lists of shape (n,1), which works for projects/fingerprints/research
    '''
    text = text.replace(', ',',')
    text = text.replace('\'','')
    text = text.replace('\"','')
    text = text.replace('[','')
    text = text.replace(']','')
    res = text.split(',')

    lst = []
    for i in range(len(res)):
        lst.append(res[i])
    return lst

def get_keywords (text):
    ''' 
    This function works for lists of shape (n,2), which works for projects/fingerprints/research
    '''
    text = text.replace('\',','],')
    text = text.replace('\",','],')
    res = text.split('],')
    for i in range(len(res)):
        res[i] = res[i].replace(']','')
        res[i] = res[i].replace('[','')
        res[i] = res[i].replace('%','')
        res[i] = res[i].replace('\'','')
    
    str = ""
    for i in range(len(res)//2):
        str += res[2*i] + ','
    
    return str

def get_website (name, netid, dep):
    name = name.split(' ')
    if dep == 'ARC': 
        return 'https://soa.princeton.edu/content/' + name[0] + '-' + name[-1]
    elif dep == 'AOS': 
        return 'https://aos.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'AST': 
        return 'https://astro.princeton.edu/~' + netid
    elif dep == 'CBE': 
        return 'https://cbe.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'CEE': 
        return 'https://cee.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'CHM': 
        return 'https://chemistry.princeton.edu/people/' + name[-1]
    elif dep == 'CHV': 
        return 'https://uchv.princeton.edu/' + name[0] + '-' + name[-1]
    elif dep == 'COS': 
        return 'https://cs.princeton.edu/~' + netid
    elif dep == 'ECE': 
        return 'https://ece.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'ECO': 
        return 'https://jrc.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'ENT': 
        return 'https://kellercenter.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'EEB': 
        return 'https://eeb.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'GEO': 
        return 'https://geosciences.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'MAE': 
        return 'https://mae.princeton.edu/people/faculty/' + name[-1]
    elif dep == 'MATH': 
        return 'https://math.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'MOL': 
        return 'https://molbio.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'BIO': 
        return 'https://molbio.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'MSE': 
        return 'https://materials.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'NEU': 
        return 'https://pni.princeton.edu/directory/' + name[0] + '-' + name[-1]
    elif dep == 'ORF': 
        return 'https://orfe.princeton.edu/people/faculty/' + name[0] + '-' + name[-1]
    elif dep == 'PHY': 
        return 'https://phy.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'POL': 
        return 'https://politics.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'PSY': 
        return 'https://psych.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'SML': 
        return 'https://csml.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'SOC': 
        return 'https://sociology.princeton.edu/people/' + name[0] + '-' + name[-1]
    elif dep == 'SPI': 
        return 'https://spia.princeton.edu/faculty/' + netid
    else: 
        return 'N/A'