from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Collegiate, Expertise , Institute
from .serializers import CollegiateSerializer , ExpertiseSerializer



def index(request):
    context_dict={'page_title':'Main Page for Scholar Find Project !!!!'}
    return render(request,'schrest/index.html',context=context_dict)

@api_view(['GET'])
def collegiate_head(request):
    """
    :param request: None
    :return: top 5 rows of Collegiate table. (last inserted)
    """
    if request.method == 'GET':
        collegiates = Collegiate.objects.all().order_by('-create_date')[:5]
        serializer = CollegiateSerializer(collegiates, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def expertise_head(request):
    """
    :param request: None
    :return: top 5 rows of Collegiate table. (last inserted)
    """
    if request.method == 'GET':
        expertises = Expertise.objects.all().order_by('-id')[:10]
        serializer = ExpertiseSerializer(expertises, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def collegiate_detail(request,pk):
    """
    :param request: ID
    :return: all detail of Collegiate by ID.
    """
    if request.method == 'GET':
        collegiate = Collegiate.objects.get(id=pk)
        serializer = CollegiateSerializer(collegiate, many=False)
        return Response(serializer.data)

@api_view(['GET'])
def expertise_collegiates(request,pk):
    """
    :param request: ID
    :return: all Collegiates working on Expertise by ID.
    """
    if request.method == 'GET':
        expertise = Expertise.objects.get(id=pk)
        serializer = CollegiateSerializer(expertise.collegiates, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def collegiate_expertises(request,pk):
    """
    :param request: ID
    :return: all expertises that Collegiate with ID works on.
    """
    if request.method == 'GET':
        collegiate =  Collegiate.objects.get(id=pk)
        serializer = ExpertiseSerializer(collegiate.expertise_set.all(), many=True)
        return Response(serializer.data)

@api_view(['GET'])
def institute_collegiates(request,pk):
    """
    :param request: ID
    :return: list of all collegiates/scholars attend to this institute/university.
    """
    if request.method == 'GET':
        institute =  Institute.objects.get(id=pk)
        serializer = ExpertiseSerializer(institute.collegiates, many=True)
        return Response(serializer.data)

