import datetime
from django.db import models

# Create your models here.


class testdatamodel(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name


class cropInfo(models.Model):
    crops = models.CharField(max_length=20)
    indicator = models.IntegerField()
    lengthOfGrowingPeriodDays = models.IntegerField()
    maxRootDepthInches = models.IntegerField()
    maxAlllowableDeplitionPercentage = models.IntegerField()
    columnForKc = models.IntegerField()
    columnForDAP = models.IntegerField()
    dAPforMaxRootDepth = models.IntegerField()

    def __str__(self):
        return str(self.indicator)+" "+self.crops


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
    a = models.IntegerField()
    b = models.IntegerField()
    c = models.IntegerField()
    d = models.IntegerField()

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
    cropType = models.ForeignKey(cropInfo, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
