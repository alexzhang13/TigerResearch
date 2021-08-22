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

    return filters_list

def get_departments (text):
    ''' 
    Function for getting exact SQLAlchemy filters for departments
    '''
    if text == "": return None

    search_words = shlex.split(text)
    filters_list = []
    for word in search_words:
        filters_list.append(models.Professor.department.like(word))

    return filters_list

def listify_file (filename):
    content = []
    with open(filename) as f:
        lines = f.readlines()
        content = [x.split(',') for x in lines] 

    return content
