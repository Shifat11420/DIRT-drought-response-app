from rest_framework import serializers
from .models import testdatamodel, cropInfo, cropPeriod, growthStage, soilMoisture, soilCondition, soilDrainageGroup, unitConversion, hydrologicGroup


class testmodelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = testdatamodel
        fields = ('id', 'name', 'alias', 'date')


class cropInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cropInfo
        fields = '__all__'


class cropInfo2Serializer(serializers.ModelSerializer):
    class Meta:
        model = cropInfo
        fields = '__all__'


class cropPeriodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cropPeriod
        fields = '__all__'


class growthStageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = growthStage
        fields = '__all__'


class soilMoistureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = soilMoisture
        fields = '__all__'


class soilConditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = soilCondition
        fields = '__all__'


class soilCondition2Serializer(serializers.ModelSerializer):
    class Meta:
        model = soilCondition
        fields = '__all__'


class soilDrainageGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = soilDrainageGroup
        fields = '__all__'


class hydrologicGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = hydrologicGroup
        fields = '__all__'


class unitConversionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = unitConversion
        fields = '__all__'
