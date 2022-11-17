from rest_framework import serializers
from .models import testdatamodel 

class testmodelSerializer(serializers.HyperlinkedModelSerializer): 
    class Meta: 
        model = testdatamodel 
        fields = ('id', 'name', 'alias', 'date')   