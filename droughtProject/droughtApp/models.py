import datetime
from django.db import models


# Create your models here.
class cropType(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=20)
    GrowingPeriodDays = models.IntegerField()
    MaxRootDepth = models.IntegerField()
    MaxAlllowableDeplition = models.IntegerField()
    MaxRootDepthDAP = models.IntegerField()

    def __str__(self):
        return str(self.Id)+" "+self.Name


class growthStage(models.Model):
    crop = models.CharField(max_length=20)
    indicator = models.IntegerField()
    emergence = models.CharField(max_length=30)
    initialMoistureCheck = models.CharField(max_length=30)
    irrigationInitiation = models.CharField(max_length=30)
    irrigationTermination = models.CharField(max_length=30)

    def __str__(self):
        return str(self.indicator)+" "+self.crop


class unitConversion(models.Model):
    flowMeterReadings = models.CharField(max_length=30)
    indicator = models.IntegerField()
    units = models.CharField(max_length=30)
    conversion = models.FloatField()

    def __str__(self):
        return self.flowMeterReadings


class cropPeriod1(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=30)
    CropTypeId = models.ForeignKey(
        cropType, on_delete=models.PROTECT, null=True)
    CropCoefficient = models.CharField(max_length=30)  # CropCoefficient
    DaysAfterPlanting = models.IntegerField()  # DaysAfterPlanting

    def __str__(self):
        return str(self.Id)+" "+self.Name+" "+str(self.CropTypeId)


class soilMoisture1(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=30)
    Ratio = models.FloatField()

    def __str__(self):
        return str(self.Id)+" "+self.Name


class hydrologicGroup(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=5)

    def __str__(self):
        return str(self.Id)+" "+str(self.Name)


class drainageType(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=50)
    HydrologicGroupTypeId = models.ForeignKey(
        hydrologicGroup, on_delete=models.PROTECT)
    ValueField = models.IntegerField()

    def __str__(self):
        return str(self.Id)+" "+self.Name+" "+str(self.HydrologicGroupTypeId)


class soilType(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=20)
    AveragePlantAvailableWater = models.FloatField(null=True)
    PermanentWiltingPoint = models.FloatField(null=True)

    def __str__(self):
        return str(self.Id)+" "+self.Name


class user(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Email = models.EmailField()
    AuthenticationInfo = models.CharField(max_length=50)

    def __str__(self):
        return str(self.Id)+" "+self.FirstName+" "+self.LastName


class field(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=50)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Acreage = models.IntegerField()
    CropTypeId = models.ForeignKey(
        cropType, on_delete=models.PROTECT, blank=True, null=True)
    PlantDate = models.DateField()
    SoilTypeId = models.ForeignKey(soilType, on_delete=models.PROTECT)
    HydrologicGroupTypeId = models.ForeignKey(
        hydrologicGroup, on_delete=models.PROTECT)
    CropPeriodId = models.ForeignKey(
        cropPeriod1, on_delete=models.PROTECT, null=True)
    SoilMoistureId = models.ForeignKey(
        soilMoisture1, on_delete=models.PROTECT, null=True)
    DrainageTypeId = models.ForeignKey(
        drainageType, on_delete=models.PROTECT, null=True)
    OwnerId = models.ForeignKey(user, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.Id)+" "+self.Name


class irrigation(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    FieldId = models.ForeignKey(field, on_delete=models.PROTECT)
    Date = models.DateField()
    Amount = models.FloatField()

    def __str__(self):
        return str(self.Id)+str(self.Date)
