from django.contrib import admin
# , userField, cropPeriod,
# soilDrainageGroup, soilCondition,soilMoisture,
from droughtApp.models import testdatamodel,   growthStage,    unitConversion
from droughtApp.models import cropType, soilType, hydrologicGroup, user, field, irrigation
from droughtApp.models import cropPeriod1,  soilMoisture1, drainageType  # cropType1,
# Register your models here.


# admin.site.register(cropPeriod)
admin.site.register(growthStage)
# admin.site.register(soilCondition)
# admin.site.register(soilDrainageGroup)
# admin.site.register(soilMoisture)
admin.site.register(unitConversion)
# admin.site.register(userField)


class cropTypeAdmin(admin.ModelAdmin):
    list_display = ("Id", "Name", "GrowingPeriodDays",
                    "MaxRootDepth", "MaxAlllowableDeplition", "MaxRootDepthDAP")


admin.site.register(cropType, admin.ModelAdmin)


admin.site.register(hydrologicGroup)
admin.site.register(soilType)
admin.site.register(user)
admin.site.register(field)
admin.site.register(irrigation)
admin.site.register(cropPeriod1)
admin.site.register(soilMoisture1)
admin.site.register(drainageType)
