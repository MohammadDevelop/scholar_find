import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','schfind.settings')
django.setup()
from schrest.models import Expertise
from django.utils import timezone

import requests
from bs4 import BeautifulSoup
import re
import nltk


link = "https://en.wikipedia.org/wiki/List_of_academic_fields"
f = requests.get(link)
print(link)


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

all_rows=BeautifulSoup(f.text, "lxml").find_all("li")


for row in all_rows:
    if not "\n" in str(row) and not cleanhtml(str(row))=='':
        print(cleanhtml(str(row)))
        try:
            ex= Expertise.objects.get_or_create(title=cleanhtml(str(row)).strip())[0]
            ex.save()

        except Exception as e:
            print("Insertion: " + str(e))

