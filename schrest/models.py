from django.db import models

import requests
from bs4 import BeautifulSoup
import re


class Laboratory(models.Model):
    laboratory_title = models.CharField(max_length=200,null=True, blank=True)
    laboratory_icon = models.CharField(max_length=200,null=True, blank=True)

    class Meta:
        verbose_name_plural = "Laberatories"

class Collegiate(models.Model):
    full_name = models.CharField(max_length=200 , unique=True)
    field = models.CharField(max_length=200,null=True, blank=True)
    email = models.CharField(max_length=200,null=True, blank=True)
    faculty = models.CharField(max_length=200,null=True, blank=True)
    position = models.CharField(max_length=200,null=True, blank=True)
    phone_number = models.CharField(max_length=200,null=True, blank=True)
    profile_picture = models.CharField(max_length=500, null=True, blank=True, default="/static/images/scholar.png")
    bio = models.TextField(null=True, blank=True)
    educations = models.TextField(null=True, blank=True)
    main_page = models.URLField(null=True, blank=True)
    create_date = models.DateTimeField('date created')

    #Relations
    laboratories= models.ManyToManyField(Laboratory, blank=True) #list of labs collegiate attends.

    def __str__(self):
        return self.full_name


class Expertise(models.Model):
    title = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200,null=True, blank=True)

    #Relations
    collegiates= models.ManyToManyField(Collegiate, blank=True)

    def __str__(self):
        return self.title

class Institute(models.Model):
    InstituteName = models.CharField(max_length=200 , unique=True)
    InstituteAddress = models.CharField(max_length=200,null=True, blank=True)

    #Relations
    collegiates= models.ManyToManyField(Collegiate, blank=True) #list of all collegiates/scholars attend to this institute/university.
    laboratories= models.ManyToManyField(Laboratory, blank=True) #list of all labs located or in collaborate with this institute/university.

    def __str__(self):
        return self.InstituteName


class Link(models.Model):
    link_url = models.URLField()
    link_title = models.CharField(max_length=200, null=True, blank=True)
    link_icon = models.CharField(max_length=200, null=True, blank=True)

    # Relations
    owner = models.ForeignKey(Collegiate, on_delete=models.CASCADE , null=True)

    def __str__(self):
        return self.link_title+" of "+self.owner.name