from django.contrib import admin 
from droughtApp.models import testdatamodel, cropInfo, cropPeriod, growthStage, soilCondition, soilDrainageGroup, soilMoisture, unitConversion 

 
# Register your models here. 

admin.site.register(testdatamodel) 
admin.site.register(cropInfo) 
admin.site.register(cropPeriod)
admin.site.register(growthStage)
admin.site.register(soilCondition)
admin.site.register(soilDrainageGroup)
admin.site.register(soilMoisture)
admin.site.register(unitConversion)
