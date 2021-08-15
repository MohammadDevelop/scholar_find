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

all_expertises = Expertise.objects.all()

for x in all_expertises:
    if len(str(x.title).lower().strip().split(" ")) >7:
        x.delete()
        print(x.title+" deleted!")
    # if str(x.title)[0] ==' ':
    #     x.title=x.title.strip()
    #     x.save()
    #     print(x.title+" modified!")
