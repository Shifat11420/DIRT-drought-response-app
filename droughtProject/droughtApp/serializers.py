from rest_framework import serializers
from .models import testdatamodel,  cropPeriod, growthStage, soilMoisture, soilCondition, soilDrainageGroup, unitConversion
# cropInfo, , user, field, irrigation
from .models import cropType, soilType, hydrologicGroup


class testmodelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = testdatamodel
        fields = ('id', 'name', 'alias', 'date')


# class cropInfoSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = cropInfo
#         fields = '__all__'


# class cropInfo2Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = cropInfo
#         fields = '__all__'


#

class cropTypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cropType
        fields = '__all__'


class cropTypes2Serializer(serializers.ModelSerializer):
    class Meta:
        model = cropType
        fields = '__all__'

# #


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


class unitConversionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = unitConversion
        fields = '__all__'


# new models


class soilTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = soilType
        fields = '__all__'


class soilType2Serializer(serializers.ModelSerializer):
    class Meta:
        model = soilType
        fields = '__all__'


# class fieldSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = field
#         fields = '__all__'


# class field2Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = field
#         fields = '__all__'


class hydrologicGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = hydrologicGroup
        fields = '__all__'


class hydrologicGroup2Serializer(serializers.ModelSerializer):
    class Meta:
        model = hydrologicGroup
        fields = '__all__'


# class irrigationSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = irrigation
#         fields = '__all__'


# class irrigation2Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = irrigation
#         fields = '__all__'


# class userSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = user
#         fields = '__all__'


# class user2Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = user
#         fields = '__all__'
