from django.contrib import admin
from droughtApp.models import unitConversion
from droughtApp.models import cropType, soilType, hydrologicGroup, user, field, irrigation, cropPeriod,  soilMoisture, drainageType


# Register your models here.
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
admin.site.register(cropPeriod)
admin.site.register(soilMoisture)
admin.site.register(drainageType)
