from rest_framework import serializers
from .models import unitConversion
from .models import cropType, soilType, hydrologicGroup, user, field, irrigation
from .models import cropPeriod, soilMoisture, drainageType


class cropTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = cropType
        fields = '__all__'


class cropPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = cropPeriod
        fields = '__all__'


class soilMoistureSerializer(serializers.ModelSerializer):
    class Meta:
        model = soilMoisture
        fields = '__all__'


class soilTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = soilType
        fields = '__all__'


class drainageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = drainageType
        fields = '__all__'


class hydrologicGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = hydrologicGroup
        fields = '__all__'


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class fieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = field
        fields = '__all__'


class irrigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = irrigation
        fields = '__all__'


class unitConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = unitConversion
        fields = '__all__'
