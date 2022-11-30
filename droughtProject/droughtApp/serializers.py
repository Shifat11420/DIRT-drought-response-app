from rest_framework import serializers
from .models import testdatamodel, cropInfo 

class testmodelSerializer(serializers.HyperlinkedModelSerializer): 
    class Meta: 
        model = testdatamodel 
        fields = ('id', 'name', 'alias', 'date')   


class cropInfoSerializer(serializers.HyperlinkedModelSerializer): 
    class Meta: 
        model = cropInfo
        fields = '__all__'