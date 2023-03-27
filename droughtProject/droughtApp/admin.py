from django.contrib import admin
from droughtApp.models import testdatamodel,  cropPeriod, growthStage, soilCondition, soilDrainageGroup, soilMoisture, unitConversion, userField
# , irrigation, soilType, user, field
from droughtApp.models import cropType, hydrologicGroup

# Register your models here.

admin.site.register(testdatamodel)

admin.site.register(cropPeriod)
admin.site.register(growthStage)
admin.site.register(soilCondition)
admin.site.register(soilDrainageGroup)
admin.site.register(soilMoisture)
admin.site.register(unitConversion)
admin.site.register(userField)

admin.site.register(cropType)
admin.site.register(hydrologicGroup)

# admin.site.register(soilType)
# admin.site.register(field)
# admin.site.register(irrigation)
# admin.site.register(user)
