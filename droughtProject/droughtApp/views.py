from django.shortcuts import render
from rest_framework import viewsets
from droughtApp.serializers import testmodelSerializer 
from .models import testdatamodel 

class testmodelViewSet(viewsets.ModelViewSet): 
    queryset = testdatamodel.objects.all().order_by('id') 
    serializer_class = testmodelSerializer   

##new class