from django.contrib import admin
from droughtApp.models import growthStage, unitConversion
from droughtApp.models import cropType, soilType, hydrologicGroup, user, field, irrigation
from droughtApp.models import cropPeriod1,  soilMoisture1, drainageType


# Register your models here.
admin.site.register(growthStage)
admin.site.register(unitConversion)


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
