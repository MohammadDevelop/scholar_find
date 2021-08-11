from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #collegiate
    path('collegiate_head', views.collegiate_head, name='collegiate_head'),
    path('collegiate_detail/<str:pk>', views.collegiate_detail, name='collegiate_detail'),
    path('collegiate_expertises/<str:pk>', views.collegiate_expertises, name='collegiate_expertises'),

    #expertise
    path('expertise_collegiates/<str:pk>', views.expertise_collegiates, name='expertise_collegiates'),

    #institute
    path('institute_collegiates/<str:pk>', views.institute_collegiates, name='institute_collegiates'),

    #populate

]

urlpatterns = format_suffix_patterns(urlpatterns)
