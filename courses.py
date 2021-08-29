import requests
from bs4 import BeautifulSoup
import csv
import re
import glob
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import ptonppl

#input
username = #username
password = #password

driver = webdriver.Chrome("chromedriver")
wait = WebDriverWait(driver, 10)


def login():
    driver.get("https://fed.princeton.edu/cas/login?service=https://www.princetoncourses.com/auth/verify")
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_name("submit").click()
    wait.until(EC.title_contains("Princeton Courses"))
    driver.get("https://www.princetoncourses.com/api/instructor/")


def people_search(id):
    wait.until(EC.url_contains("https://www.princetoncourses.com/api/instructor/"))
    driver.get("https://www.princetoncourses.com/api/instructor/" + id)
    wait.until(EC.url_contains("https://www.princetoncourses.com/api/instructor/" + id))
    try:
        person = requests.get(driver.current_url).json()
    except:
        person = {}
    return person

def classes(netid, term):
    classes = []
    try:
        id = ptonppl.search(netid).puid
        person = people_search(id)
        for i in person["courses"]:
            if(i["semester"]["name"] in term):
                classes.append(i["commonName"])
    except:
        pass
    return list(set(classes))

login()
term = ["Fall 2021", "Spring 2021"]
with open('all_people.csv', mode='r') as infile:
    with open("data.csv", mode='w') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, lineterminator='\n')

        people = []
        row = next(reader)
        row.append('classes')
        people.append(row)

        for row in reader:
            # searches person by their netid and term to find classes
            row.append(classes(row[1], term))
            people.append(row)
        
        writer.writerows(people)



