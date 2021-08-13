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


link = "https://expertisefinder.com/find-an-expert/"
f = requests.get(link)
print(link)


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

all_rows=BeautifulSoup(f.text, "lxml").find_all("li")

all_links=[]
for row in all_rows:
    if not "\n" in str(row) and not cleanhtml(str(row))=='':
        all_rows_a=row.find('a')
        if len(str(all_rows_a).split('\"')) > 1:
            if "https" in str(all_rows_a).split('\"')[1]:
                all_links.append(str(all_rows_a).split('\"')[1])

all_links=all_links[1043:]
for plink in all_links:
    print(plink)
    read_single = requests.get(plink)

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "notxtstyle"})

        for s in sp:
            title_=cleanhtml(str(s))
            ex= Expertise.objects.get_or_create(title=title_)[0]
            ex.save()
    except Exception as e:
        print(str(e))
