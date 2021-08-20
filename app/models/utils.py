from app.models import models
import shlex

def get_filters (text):
    ''' 
    Function for getting SQLAlchemy filters for each subword of the search text
    '''
    search_words = shlex.split(text)
    filters_list = []
    for word in search_words:
        filters_list.append(models.Professor.name.ilike("%" + word + "%"))
        filters_list.append(models.Professor.keywords.ilike("%" + word + "%"))
        filters_list.append(models.Professor.department.ilike("%" + word + "%"))

    return filters_list

def listify_file (filename):
    content = []
    with open(filename) as f:
        lines = f.readlines()
        content = [x.strip() for x in lines] 

    return content