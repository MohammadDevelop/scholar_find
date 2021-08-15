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
    path('portal/collegiate_detail/<str:pk>', views.show_collegiate_detail, name='show_collegiate_detail'),

    #expertise
    path('expertise_head', views.expertise_head, name='expertise_head'),
    path('expertise_collegiates/<str:pk>', views.expertise_collegiates, name='expertise_collegiates'),
    path('portal/expertise_detail/<str:pk>', views.show_expertise_detail, name='show_expertise_detail'),

    #institute
    path('institute_collegiates/<str:pk>', views.institute_collegiates, name='institute_collegiates'),

    #populate

]

urlpatterns = format_suffix_patterns(urlpatterns)
