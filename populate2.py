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

base="https://www.royalroads.ca"
link = base+"/faculty-directory?field_program_area_target_id=All&field_faculty_type_target_id=All&sort_by=field_first_name_value&combine=&page=33"
f = requests.get(link)
print(link)

uni="Royal Roads University"


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

all_rows=BeautifulSoup(f.text, "lxml").find_all(attrs={"class": "profile-listing-view__content"})

all_people=[]
for row in all_rows:
    all_people_a=row.find_all('a')
    for a in all_people_a:
        all_people.append(a['href'])

print(all_people)


all_people=all_people[1:]
for plink in all_people:
    print(base+plink)
    read_single = requests.get(base + plink)

#Capture Name
    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "page-title"})
        name = cleanhtml(str(sp[0]))
        print("Name Captured: "+name)
    except Exception as e:
        first_name=last_name=name=""
        print("Name: "+str(e))

#Capture Position
    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "position-title-wrapper-content"})
        position = cleanhtml(str(sp[0])).strip()
        print("Position Captured: "+position)
    except Exception as e:
        position=""
        print("Position: "+str(e))

#Capture Department
    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field_testimonial_program"})
        department = cleanhtml(str(sp[0])).strip()
        print("Department Captured: "+department)
    except Exception as e:
        department=""
        print("Department: "+str(e))

#Capture Education
    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field_education_wrapper_content"})
        education = cleanhtml(str(sp[0])).strip()
        #print("Education Captured: "+education)
    except Exception as e:
        education=""
        print("Education: "+str(e))

#Capture BIO
    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field_biography"})
        sp2=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field_experience"})
        bio = cleanhtml(str(sp[0])).strip() + "\n" + cleanhtml(str(sp2[0])).strip()
        print("BIO Captured: "+bio)
    except Exception as e:
        bio=""
        print("BIO: "+str(e))

#Capture ProfilePic
    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "profile__info"})
        profile_pic = base+str(sp[0].find("img")['src'])
        print("ProfilePic Captured: "+profile_pic)
    except Exception as e:
        department=""
        print("ProfilePic: "+str(e))




    try:
        clg= Collegiate.objects.get_or_create(full_name=name.strip() , create_date = timezone.now())[0]
        clg.position = position.strip()
        clg.field = department.strip()
        #clg.phone_number = phone.strip()
        #clg.email = email.strip()
        clg.bio = bio.strip()
        clg.educations= education.strip().replace("n.d.","\n")
        clg.main_page= base+plink
        clg.profile_picture= profile_pic
        clg.save()

        ins = Institute.objects.get_or_create(InstituteName=uni)[0]
        ins.collegiates.add(clg)
        ins.save()

        for exp in all_expertises:
            if exp.title.lower() in bio.lower():
                print("-"*5+" add "+exp.title.lower()+" to "+clg.full_name)
                exp.collegiates.add(clg)
                exp.save()

    except Exception as e:
        print("Insertion: " + str(e))

