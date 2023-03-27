import datetime
from django.db import models

# Create your models here.


class testdatamodel(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name


class cropType(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=20)
    GrowingPeriodDays = models.IntegerField()
    MaxRootDepth = models.IntegerField()
    MaxAlllowableDeplition = models.IntegerField()
    KC = models.IntegerField()
    DAP = models.IntegerField()
    MaxRootDepthDAP = models.IntegerField()

    def __str__(self):
        return str(self.Id)+" "+self.Name


class cropPeriod(models.Model):
    period = models.CharField(max_length=30)
    kcforCorn = models.CharField(max_length=30)
    dAPforCorn = models.IntegerField()
    kcforSoybean = models.CharField(max_length=30)
    dAPforSoybean = models.IntegerField()
    kcforCotton = models.CharField(max_length=30)
    dAPforCotton = models.IntegerField()
    kcforGrainSorghum = models.CharField(max_length=30)
    dAPforSorghum = models.IntegerField()
    kcforSugarcane = models.CharField(max_length=30)
    dAPforSugarcane = models.IntegerField()

    def __str__(self):
        return str(self.period)


class growthStage(models.Model):
    crop = models.CharField(max_length=20)
    indicator = models.IntegerField()
    emergence = models.CharField(max_length=30)
    initialMoistureCheck = models.CharField(max_length=30)
    irrigationInitiation = models.CharField(max_length=30)
    irrigationTermination = models.CharField(max_length=30)

    def __str__(self):
        return str(self.indicator)+" "+self.crop


class soilCondition(models.Model):
    soilTexture = models.CharField(max_length=30)
    indicator = models.IntegerField()
    averagePlantAvailableWaterInFt = models.FloatField()
    averagePlantAvailableWaterInIn = models.FloatField()
    permanentWiltingPointInIn = models.FloatField()

    def __str__(self):
        return str(self.indicator)+" "+self.soilTexture


class soilDrainageGroup(models.Model):
    descriptionForCN = models.CharField(max_length=30)
    indicator = models.IntegerField()
    A = models.IntegerField()
    B = models.IntegerField()
    C = models.IntegerField()
    D = models.IntegerField()

    def __str__(self):
        return str(self.indicator)+" "+self.descriptionForCN


class soilMoisture(models.Model):
    initialConditions = models.CharField(max_length=30)
    indicator = models.IntegerField()
    ratio = models.FloatField()

    def __str__(self):
        return str(self.indicator)+" "+self.initialConditions


class unitConversion(models.Model):
    flowMeterReadings = models.CharField(max_length=30)
    indicator = models.IntegerField()
    units = models.CharField(max_length=30)
    conversion = models.FloatField()

    def __str__(self):
        return self.flowMeterReadings


class userField(models.Model):
    fieldId = models.IntegerField()
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    size = models.FloatField()
    plantDate = models.DateField()
    cropType = models.ForeignKey(cropType, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

# new models


class hydrologicGroup(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=5)

    def __str__(self):
        return str(self.Id)+" "+str(self.Name)



class soilType(models.Model):
    Id = models.IntegerField(primary_key=True, null=False)
    Name = models.CharField(max_length=20)

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
    CropTypeId = models.ForeignKey(cropType, on_delete=models.PROTECT)
    PlantDate = models.DateField()
    SoilTypeId = models.ForeignKey(soilType, on_delete=models.PROTECT)
    HydrologicGroupTypeId = models.ForeignKey(
        hydrologicGroup, on_delete=models.PROTECT)
    OwnerId = models.ForeignKey(user, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.Id)+" "+self.Name


# class irrigation(models.Model):
#     Id = models.IntegerField(primary_key=True, null=False)
#     FieldId = models.ForeignKey(field, on_delete=models.PROTECT)
#     Date = models.DateField()
#     Amount = models.FloatField()

#     def __str__(self):
#         return str(self.Id)
