from django.contrib import admin
from droughtApp.models import testdatamodel,  cropPeriod, growthStage, soilCondition, soilDrainageGroup, soilMoisture, unitConversion  # , userField
from droughtApp.models import cropType, soilType, hydrologicGroup, user, field, irrigation

# Register your models here.


admin.site.register(cropPeriod)
admin.site.register(growthStage)
admin.site.register(soilCondition)
admin.site.register(soilDrainageGroup)
admin.site.register(soilMoisture)
admin.site.register(unitConversion)
# admin.site.register(userField)

admin.site.register(cropType)
admin.site.register(hydrologicGroup)
admin.site.register(soilType)
admin.site.register(user)
admin.site.register(field)
admin.site.register(irrigation)
