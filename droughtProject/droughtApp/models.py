import datetime
from django.db import models

# Create your models here.

class testdatamodel(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    date = models.DateField(default=datetime.date.today)
   
    def __str__(self):
        return self.name