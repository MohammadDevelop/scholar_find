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

base="http://www.sfu.ca"
link = base+"/mechatronics/people/faculty.html"
f = requests.get(link)
print(link)

uni="Simon Fraser University"
dep="Mechatronic Systems Engineering"

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

#all_rows=BeautifulSoup(f.text, "lxml").find_all(attrs={"class": "a"})
all_rows=BeautifulSoup(f.text, "lxml").find_all("a")
#print(all_rows)
all_people=[]
for row in all_rows:
    try:
        #print(cleanhtml(str(row))+"----->"+row['href'])
        #if cleanhtml(str(row))=="Profile &amp; Contact Information":
        if str(row['href']).startswith("/mechatronics/people/faculty"):
            all_people.append(row['href'])
    except Exception as e:
        print(".")

print(all_people)


#all_people=all_people[1:]
for plink in all_people:
    print(base+plink)
    try:
        read_single = requests.get(base + plink)

    #Capture Name
        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "title"})
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
            sp=BeautifulSoup(read_single.text, "lxml").find_all("td")
            for spx in sp:
                chunk=cleanhtml(str(spx)).replace("\n"," ")
                #print(chunk)
                if chunk.strip().startswith("Email"):
                    email=chunk.strip().split(":")[1]
                    print("Email Captured: "+email.strip())
                if chunk.strip().startswith("Tel"):
                    phone=chunk.strip().split(":")[1]
                    print("Phone Captured: "+phone)
                if chunk.strip().lower().startswith("web"):
                    web=chunk.strip().split(":")[1]
                    print("WEB Captured: "+web.strip())
        except Exception as e:
            department=""
            print("Department: "+str(e))


    #Capture Intrested , Educations
        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "listed"})
            for spx in sp:
                bio = cleanhtml(str(spx)).strip()
                spl=bio.split("\n")
                if spl[0]=="Research interests":
                    interests=spl[1:]
                    print("INTEREST Captured: ")
                    print(interests)
                if spl[0]=="Education":
                    education=spl[1:]
                    print("EDU Captured: ")
                    print(education)
            if len(sp)==0:
                sp = BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "ruled"})
                for spx in sp:
                    bio = cleanhtml(str(spx)).strip()
                    spl = bio.split("\n")
                    if spl[0] == "Research interests":
                        interests = spl[1:]
                        print("INTEREST Captured: ")
                        print(interests)
                    if spl[0] == "Education":
                        education = spl[1:]
                        print("EDU Captured: ")
                        print(education)
        except Exception as e:
            bio=""
            print("BIO: "+str(e))

    #Capture ProfilePic
        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "image"})
            profile_pic = base+str(sp[0].find("img")['src'])
            print("ProfilePic Captured: "+profile_pic)
        except Exception as e:
            department=""
            print("ProfilePic: "+str(e))




        try:
            clg= Collegiate.objects.get_or_create(full_name=name.strip() , create_date = timezone.now())[0]
            #clg.position = position.strip()
            #clg.field = department.strip()
            #clg.phone_number = phone.strip()
            clg.email = email.strip()
            clg.faculty= dep
            #clg.bio = bio.strip()
            education_str=""
            for edu in education:
                education_str=education_str+"\n"
            clg.educations= education_str
            clg.main_page= base+plink
            clg.profile_picture= profile_pic
            clg.save()

            ins = Institute.objects.get_or_create(InstituteName=uni)[0]
            ins.collegiates.add(clg)
            ins.save()

            for it in interests:
                if not it=='':
                    exp = Expertise.objects.get_or_create(title=it)[0]
                    exp.collegiates.add(clg)
                    exp.save()

        except Exception as e:
            print("Insertion: " + str(e))
    except Exception as e:
        print("ALL: " + str(e))
