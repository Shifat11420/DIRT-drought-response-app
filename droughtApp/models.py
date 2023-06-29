import datetime
from datetime import date
from django.db import models


# Create your models here.
class cropType(models.Model):
    Name = models.CharField(max_length=20)
    GrowingPeriodDays = models.IntegerField()
    MaxRootDepth = models.IntegerField()
    MaxAllowableDepletion = models.IntegerField()
    MaxRootDepthDaysAfterPlanting = models.IntegerField()

    def __str__(self):
        return self.Name


class cropPeriod(models.Model):
    Name = models.CharField(max_length=30)
    CropTypeId = models.ForeignKey(
        cropType, on_delete=models.PROTECT, null=True)
    CropCoefficient = models.CharField(max_length=30)  # CropCoefficient
    DaysAfterPlanting = models.IntegerField()  # DaysAfterPlanting

    def __str__(self):
        return self.Name+"-"+str(self.CropTypeId)


class soilMoisture(models.Model):
    Name = models.CharField(max_length=30)
    InitialSoilMoisturePercent = models.FloatField()

    def __str__(self):
        return self.Name


class hydrologicGroup(models.Model):
    Name = models.CharField(max_length=1)

    def __str__(self):
        return str(self.Name)


class drainageType(models.Model):
    Name = models.CharField(max_length=50)
    HydrologicGroupId = models.ForeignKey(
        hydrologicGroup, on_delete=models.PROTECT)
    DrainageValue = models.IntegerField()

    def __str__(self):
        return self.Name+"-"+str(self.HydrologicGroupId)


class soilType(models.Model):
    Name = models.CharField(max_length=50)
    AveragePlantAvailableWater = models.FloatField(null=True)
    PermanentWiltingPoint = models.FloatField(null=True)
    FieldCapacity = models.FloatField(null=True)

    def __str__(self):
        return self.Name


class user(models.Model):
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Email = models.EmailField()
    AuthenticationId = models.CharField(max_length=50)

    def __str__(self):
        return self.FirstName+" "+self.LastName


class field(models.Model):
    Name = models.CharField(max_length=150)
    Latitude = models.DecimalField(max_digits=8, decimal_places=6)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6)
    Acreage = models.IntegerField()
    Elevation = models.FloatField(null=True)
    CropTypeId = models.ForeignKey(
        cropType, on_delete=models.PROTECT, blank=True, null=True)
    PlantDate = models.DateField()
    HydrologicGroupId = models.ForeignKey(
        hydrologicGroup, on_delete=models.PROTECT)
    DrainageTypeId = models.ForeignKey(
        drainageType, on_delete=models.PROTECT, null=True)
    SoilTypeId = models.ForeignKey(soilType, on_delete=models.PROTECT)
    SoilMoistureId = models.ForeignKey(
        soilMoisture, on_delete=models.PROTECT, null=True)
    GrowingPeriodDays = models.IntegerField(null=True)
    FieldCapacity = models.FloatField(null=True)
    PermanentWiltingPoint = models.FloatField(null=True)
    PlantAvailableWater = models.FloatField(null=True)
    OwnerId = models.ForeignKey(user, on_delete=models.PROTECT)

    def __str__(self):
        return self.Name


class irrigation(models.Model):
    FieldId = models.ForeignKey(field, on_delete=models.PROTECT)
    Date = models.DateField()
    Amount = models.FloatField()

    def __str__(self):
        return str(self.FieldId)+str(self.Date)


class unitConversion(models.Model):
    flowMeterReadings = models.CharField(max_length=30)
    indicator = models.IntegerField()
    units = models.CharField(max_length=30)
    conversion = models.FloatField()

    def __str__(self):
        return self.flowMeterReadings


class results(models.Model):
    FieldId = models.ForeignKey(
        field, on_delete=models.PROTECT, null=True)
    Date = models.DateField(blank=True, default=date(1111, 11, 11), null=True)
    WaterLevelStart = models.FloatField(null=True)
    WaterLevelEnd = models.FloatField(null=True)
    DeepPercolation = models.FloatField(null=True)
    SurfaceRunoff = models.FloatField(null=True)
    VolumetricWaterContent = models.FloatField(null=True)
    EffectiveIrrigation = models.FloatField(null=True)
    IrrigationEfficiency = models.FloatField(null=True)
    MaximumAvailableDepletion = models.FloatField(null=True)
    FieldCapacity = models.FloatField(null=True)
    PermanentWiltingPoint = models.FloatField(null=True)
    WaterDeficit = models.FloatField(null=True)
    IrrigationActivityAmount = models.FloatField(null=True)
    RainObservedAmount = models.FloatField(null=True)
    EffectiveRainAmount = models.FloatField(null=True)
    EvapotranporationValue = models.FloatField(null=True)
    EvapotranporationCropValue = models.FloatField(null=True)

    def __str__(self):
        return str(self.Date)+"Field : "+str(self.FieldId)
