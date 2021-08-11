from django.db import models

import requests
from bs4 import BeautifulSoup
import re

class Link(models.Model):
    link_url = models.CharField(max_length=200)
    link_title = models.CharField(max_length=200,null=True, blank=True)
    link_icon = models.CharField(max_length=200,null=True, blank=True)

class Laboratory(models.Model):
    laboratory_title = models.CharField(max_length=200,null=True, blank=True)
    laboratory_icon = models.CharField(max_length=200,null=True, blank=True)

class Collegiate(models.Model):
    full_name = models.CharField(max_length=200)
    field = models.CharField(max_length=200,null=True, blank=True)
    email = models.CharField(max_length=200,null=True, blank=True)
    faculty = models.CharField(max_length=200,null=True, blank=True)
    position = models.CharField(max_length=200,null=True, blank=True)
    phone_number = models.CharField(max_length=200,null=True, blank=True)
    profile_picture = models.CharField(max_length=200,null=True, blank=True)
    bio = models.TextField()
    create_date = models.DateTimeField('date created')

    #Relations
    links= models.ManyToManyField(Link, blank=True)
    laboratories= models.ManyToManyField(Laboratory, blank=True) #list of labs collegiate attends.

    def __str__(self):
        return self.full_name


class Expertise(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200,null=True, blank=True)

    #Relations
    collegiates= models.ManyToManyField(Collegiate, blank=True)

    def __str__(self):
        return self.title

class Institute(models.Model):
    InstituteName = models.CharField(max_length=200)
    InstituteAddress = models.CharField(max_length=200,null=True, blank=True)

    #Relations
    collegiates= models.ManyToManyField(Collegiate, blank=True) #list of all collegiates/scholars attend to this institute/university.
    laboratories= models.ManyToManyField(Laboratory, blank=True) #list of all labs located or in collaborate with this institute/university.

    def __str__(self):
        return self.InstituteName