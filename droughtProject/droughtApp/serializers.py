from rest_framework import serializers
from .models import growthStage, unitConversion
from .models import cropType, soilType, hydrologicGroup, user, field, irrigation
from .models import cropPeriod1, soilMoisture1, drainageType


class cropTypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cropType
        fields = '__all__'


class cropTypes2Serializer(serializers.ModelSerializer):
    class Meta:
        model = cropType
        fields = '__all__'


class growthStageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = growthStage
        fields = '__all__'


class unitConversionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = unitConversion
        fields = '__all__'


class cropPeriod1Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cropPeriod1
        fields = '__all__'


class cropPeriod12Serializer(serializers.ModelSerializer):
    class Meta:
        model = cropPeriod1
        fields = '__all__'


class soilMoisture1Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = soilMoisture1
        fields = '__all__'


class soilMoisture12Serializer(serializers.ModelSerializer):
    class Meta:
        model = soilMoisture1
        fields = '__all__'


class soilTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = soilType
        fields = '__all__'


class soilType2Serializer(serializers.ModelSerializer):
    class Meta:
        model = soilType
        fields = '__all__'


class drainageTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = drainageType
        fields = '__all__'


class drainageType2Serializer(serializers.ModelSerializer):
    class Meta:
        model = drainageType
        fields = '__all__'


class hydrologicGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = hydrologicGroup
        fields = '__all__'


class hydrologicGroup2Serializer(serializers.ModelSerializer):
    class Meta:
        model = hydrologicGroup
        fields = '__all__'


class userSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class user2Serializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class fieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = field
        fields = '__all__'


class field2Serializer(serializers.ModelSerializer):
    class Meta:
        model = field
        fields = '__all__'


class irrigationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = irrigation
        fields = '__all__'


class irrigation2Serializer(serializers.ModelSerializer):
    class Meta:
        model = irrigation
        fields = '__all__'
