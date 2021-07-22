def listify_file (filename):
    content = []
    with open(filename) as f:
        lines = f.readlines()
        content = [x.strip() for x in lines] 

    return content