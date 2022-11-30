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

