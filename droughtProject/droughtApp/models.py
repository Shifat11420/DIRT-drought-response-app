import datetime
from django.db import models


# Create your models here.
class cropType(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=20)
    GrowingPeriodDays = models.IntegerField()
    MaxRootDepth = models.IntegerField()
    MaxAlllowableDepletion = models.IntegerField()
    MaxRootDepthDaysAfterPlanting = models.IntegerField()

    def __str__(self):
        return str(self.Id)+" "+self.Name


class unitConversion(models.Model):
    flowMeterReadings = models.CharField(max_length=30)
    indicator = models.IntegerField()
    units = models.CharField(max_length=30)
    conversion = models.FloatField()

    def __str__(self):
        return self.flowMeterReadings


class cropPeriod(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=30)
    CropTypeId = models.ForeignKey(
        cropType, on_delete=models.PROTECT, null=True)
    CropCoefficient = models.CharField(max_length=30)  # CropCoefficient
    DaysAfterPlanting = models.IntegerField()  # DaysAfterPlanting

    def __str__(self):
        return str(self.Id)+" "+self.Name+" "+str(self.CropTypeId)


class soilMoisture(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=30)
    InitialSoilMoisturePercent = models.FloatField()

    def __str__(self):
        return str(self.Id)+" "+self.Name


class hydrologicGroup(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=1)

    def __str__(self):
        return str(self.Id)+" "+str(self.Name)


class drainageType(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=50)
    HydrologicGroupId = models.ForeignKey(
        hydrologicGroup, on_delete=models.PROTECT)
    DrainageValue = models.IntegerField()

    def __str__(self):
        return str(self.Id)+" "+self.Name+" "+str(self.HydrologicGroupTypeId)


class soilType(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=20)
    AveragePlantAvailableWater = models.FloatField(null=True)
    PermanentWiltingPoint = models.FloatField(null=True)
    FieldCapacity = models.FloatField(null=True)

    def __str__(self):
        return str(self.Id)+" "+self.Name


class user(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Email = models.EmailField()
    AuthenticationId = models.CharField(max_length=50)

    def __str__(self):
        return str(self.Id)+" "+self.FirstName+" "+self.LastName


class field(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=150)
    Latitude = models.DecimalField(max_digits=8, decimal_places=6)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6)
    Acreage = models.IntegerField()
    CropTypeId = models.ForeignKey(
        cropType, on_delete=models.PROTECT, blank=True, null=True)
    PlantDate = models.DateField()
    HydrologicGroupTypeId = models.ForeignKey(
        hydrologicGroup, on_delete=models.PROTECT)
    DrainageTypeId = models.ForeignKey(
        drainageType, on_delete=models.PROTECT, null=True)
    SoilTypeId = models.ForeignKey(soilType, on_delete=models.PROTECT)
    SoilMoistureId = models.ForeignKey(
        soilMoisture, on_delete=models.PROTECT, null=True)
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
