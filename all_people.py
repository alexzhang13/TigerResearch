import requests
from bs4 import BeautifulSoup
import csv
import re
import glob

# checks the field and fills it N/a if empty
def check(field, person_info):
    if(field not in person_info.keys()):
        person_info[field] = "N/a"

# data with names and website from database
data_path = "people/"
flist = glob.glob(data_path+"*.csv")
majors = []

# dictionary with respective major and its abbreviation 
with open('majors.csv', mode='r') as infile:
    reader = csv.reader(infile)
    majors = {rows[1]:rows[0] for rows in reader}


with open('all_people.csv', mode='w') as all_people:
    # all the data we need scraped
    fieldnames = ["name",
              "netid",
              "department", 
              "fingerprints",
              "projects",
              "research",
              "citations",
              "h_index",
              "similar",
              "picture",
              "URL"
    ]
    writer=csv.DictWriter(all_people, fieldnames=fieldnames)
    writer.writeheader();

    for file in flist:
        with open(file, mode='r') as csv_file:
            #reads teh
            reader = csv.DictReader(csv_file)

            for row in reader:
                # for every person, we get all their data and write to the csv
                person_info = {}

                # adds name and url (already have)
                person_info["name"] = row["Name"]
                person_info["URL"] = row["URL"]
                
                names = person_info["name"].split()
                first_name = names[0]
                last_name = names[-1]

                # requests the princeton advanced search to get netid
                url = f"https://www.princeton.edu/search/people-advanced?f={first_name}&ff=c&l={last_name}&lf=c"
                page = requests.get(url)
                soup = BeautifulSoup(page.content, "html.parser")

                # truncates data and searches for netid
                for i in soup.find_all('div'):
                    trun_data = re.search('<div class="columns small-12 medium-6 large-3 js-hideshow">', str(i))
                    if(trun_data):
                        trun_data = re.search('<h4 class="expanded-details-label subheader">NetID</h4>', trun_data.string)
                        if(trun_data):
                            idx = trun_data.span()[0]
                            trun_data = re.search(r'(?<=<span class="expanded-details-value">)(.*?)(?=</)', trun_data.string[idx:])
                            if (trun_data):
                                person_info["netid"] = trun_data.group()
                                break
                
                # now accesses database
                page = requests.get(row["URL"])
                soup = BeautifulSoup(page.content, "html.parser")

                # gets picture
                for i in soup.find_all("img"):
                    trun_data = re.search(r'(/files-asset/)(.*?)(jpg)', str(i))
                    if(trun_data):
                        pic_url = 'https://collaborate.princeton.edu/' + trun_data.group()
                        person_info["picture"] = pic_url
                
                # list of all their projects and research
                all_projects = []
                all_research = []

                for i in soup.find_all("a"):
                    # finds department
                    trun_data = re.search('<a class="link department" href=', str(i))
                    if(trun_data):
                        trun_data = re.search(r'(?<=">)(.*?)(?=</)', trun_data.string)
                        dept = trun_data.group()[6:]

                        # if abbreviation exists use that otherwise keep it
                        if(dept in majors.keys()):
                            person_info["department"] = majors[dept]
                        else:
                            person_info["department"] = dept

                    # finds projects
                    projects = []
                    trun_data = re.search(r'(?<=<a class="link" href=)(.*?)(?=rel="UPMProject">)', str(i))
                    if(trun_data):
                        project_data = re.search(r'(?<=<span>)(.*?)(?=</span>)', trun_data.string)
                        try:
                            projects.append(project_data.group())
                        except AttributeError:
                            continue
                        project_website_data = re.search(r'(?<=href=")(.*?)(?=" rel="UPMProject">)', trun_data.string)
                        projects.append(project_website_data.group())

                    if(projects):
                        all_projects.append(projects)

                    # finds research
                    research = []
                    trun_data = re.search(r'(?<=<a class="link" href=)(.*?)(?=rel="ContributionToJournal">)', str(i))

                    if(trun_data):
                        research_data = re.search(r'(?<=<span>)(.*?)(?=</span>)', trun_data.string)
                        try:
                            research.append(research_data.group())
                        except AttributeError:
                            continue
                        research_website_data = re.search(r'(?<=href=")(.*?)(?=" rel="ContributionToJournal">)', trun_data.string)
                        research.append(research_website_data.group())

                    if(research):
                        all_research.append(research)

                

                all_fingerprints = []
                count = 0
                count_2 = 0
                for i in soup.find_all("span"):
                    
                    # finds fingerprint
                    fingerprint = []
                    trun_data = re.search('<span class="concept-wrapper"', str(i))
                    if(trun_data):
                        # only finds first 8 fingerprint
                        if(count == 8):
                            break
                        fingerprint_data = re.search(r'(?<="concept">)(.*?)(?=</)', trun_data.string)
                        value_data = re.search(r'(?<="value sr-only">)(.*?)(?=</)', trun_data.string)
                        try:
                            fingerprint.append(fingerprint_data.group())
                            fingerprint.append(value_data.group())
                        except AttributeError:
                            continue
                        
                        count += 1

                    if(fingerprint):
                        all_fingerprints.append(fingerprint)
                    
                    #citations
                    trun_data = re.search('<span class="count increment-counter">', str(i))
                    if(trun_data):
                        citation_data = re.search(r'(?<=">)(.*?)(?=</)', trun_data.string)

                        # first tag is citations
                        if(count_2 % 2 == 0):
                            person_info["citations"] = citation_data.group()
                        # second tag is h_index
                        else:
                            person_info["h_index"] = citation_data.group()
                        count_2+=1

                
                # finds similar people
                all_similar = []
                page = requests.get(row["URL"] + "/similar")
                soup = BeautifulSoup(page.content, "html.parser")

                for i in soup.find_all("a"):
                    trun_data = re.search(r'(?<=<a class="link person" href=)(.*?)(?=>)', str(i))
                    similar = []

                    if(trun_data):
                        similar_people_data = re.search(r'(?<=<span>)(.*?)(?=</span>)', trun_data.string)
                        similar.append(similar_people_data.group())

                        similar_website_data = re.search(r'(?<=href=")(.*?)(?=" rel="Person">)', trun_data.string)
                        similar.append(similar_website_data.group())
                    if(similar):
                        all_similar.append(similar)

                # adds scraped data to person
                person_info["projects"] = all_projects
                person_info["research"] = all_research
                person_info["fingerprints"] = all_fingerprints
                person_info["similar"] = all_similar

                # check if its filled
                check("department", person_info)
                check("netid", person_info)
                check("picture", person_info)
                check("citations", person_info)
                check("h_index", person_info)

                writer.writerow(person_info)                                    