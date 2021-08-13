# tiny populate script:
# using simple crawl pages

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','schfind.settings')
django.setup()
from schrest.models import Collegiate,Expertise ,Institute
from django.utils import timezone

import requests
from bs4 import BeautifulSoup
import re
import nltk

from nltk.parse.corenlp import CoreNLPDependencyParser

all_expertises = Expertise.objects.all()
print(len(all_expertises))

base="https://sala.ubc.ca"
link = base+"/people/faculty"
f = requests.get(link)
print(link)

dep="Aeronautics & Astronautics"
uni="Stanford University"


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

all_rows=BeautifulSoup(f.text, "lxml").find_all(attrs={"class": "salacol-xs-3"})

all_people=[]
for row in all_rows:
    all_people_a=row.find_all('a')
    for a in all_people_a:
        all_people.append(a['href'])


all_people=all_people[1:]
for plink in all_people:
    print(base+plink)
    read_single = requests.get(base + plink)

#Capture Name
    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "page-header"})
        name = cleanhtml(str(sp[0]))
        print("Name Captured: "+name)
        if len(name.split(" "))==2:
            first_name=name.split(" ")[0]
            last_name=name.split(" ")[1]
            middle_name = ""
        if len(name.split(" "))==3:
            first_name=name.split(" ")[0]
            middle_name=name.split(" ")[1]
            last_name = name.split(" ")[2]
    except Exception as e:
        first_name=last_name=name=""
        print("Name: "+str(e))

    # try:
    #     sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "su-person-email"})
    #     email = cleanhtml(str(sp[0].find('a')))
    #     print(email)
    # except Exception as e:
    #     email=""
    #     print("Email: "+str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "block-system"})
        #print(sp[0].find('a').split('"')[1])
        site = cleanhtml(str(sp[0].find_all('h5')))
        site2 = cleanhtml(str(sp[0].find_all('p')))
        print(site)
        print(site2)
        position=site2[0]

    except Exception as e:
        site=""
        print("Site: "+str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "node-stanford-person-su-person-full-title"})
        position=cleanhtml(str(sp[0]))
        position=position.split("of")[0]
        of_str=position.split("of")[1]
        print(position.split("of"))
    except Exception as e:
        position=""
        of_str=""
        print("Faculty: "+str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field-block node-stanford-person-su-person-mobile-phone block-layout-builder"})
        phone=cleanhtml(str(sp[0]))
        print(phone)
    except Exception as e:
        phone=""
        print("Phone: "+str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "su-person-education"})
        edu=cleanhtml(str(sp[0]))
        print(edu)
    except Exception as e:
        edu=""
        print("Educations: "+str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "su-person-body"})
        desc=cleanhtml(str(sp[0]))
    except Exception as e:
        desc=""
        print("Desciption: "+str(e))



    # try:
    #     clg= Collegiate.objects.get_or_create(full_name=name.strip() , create_date = timezone.now())[0]
    #     clg.position = position.strip()
    #     clg.faculty = of_str.strip()
    #     clg.phone_number = phone.strip()
    #     clg.email = email.strip()
    #     clg.bio = desc.strip()
    #     clg.educations= edu.strip()
    #     clg.main_page= site.strip()
    #     clg.save()
    #
    #     ins = Institute.objects.get_or_create(InstituteName=uni)[0]
    #     ins.collegiates.add(clg)
    #     ins.save()
    #
    #     for exp in all_expertises:
    #         if exp.title.lower() in desc.lower():
    #             print("-"*5+" add "+exp.title.lower()+" to "+clg.full_name)
    #             exp.collegiates.add(clg)
    #             exp.save()
    #
    # except Exception as e:
    #     print("Insertion: " + str(e))
    #
