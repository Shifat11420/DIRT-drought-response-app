from rest_framework import serializers
from .models import unitConversion
from .models import cropType, soilType, hydrologicGroup, user, field, irrigation
from .models import cropPeriod, soilMoisture, drainageType


class cropTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = cropType
        fields = '__all__'


class cropTypes2Serializer(serializers.ModelSerializer):
    class Meta:
        model = cropType
        fields = '__all__'


class unitConversionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = unitConversion
        fields = '__all__'


class cropPeriodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cropPeriod
        fields = '__all__'


class cropPeriod2Serializer(serializers.ModelSerializer):
    class Meta:
        model = cropPeriod
        fields = '__all__'


class soilMoistureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = soilMoisture
        fields = '__all__'


class soilMoisture2Serializer(serializers.ModelSerializer):
    class Meta:
        model = soilMoisture
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


class fieldSerializer(serializers.ModelSerializer):
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
