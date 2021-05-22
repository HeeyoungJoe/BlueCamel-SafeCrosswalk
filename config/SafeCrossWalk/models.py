from django.db import models

# Create your models here.

class Drivers(models.Model):
    id=models.IntegerField(primary_key=True)
    signal=models.CharField(max_length=100,blank=True, null=True)
    prevlat=models.FloatField(default=0.0)
    prevlon=models.FloatField(default=0.0)
    distance=models.FloatField(default=0.0)
    curlat=models.FloatField(default=0.0)
    curlon=models.FloatField(default=0.0)
    brake=models.FloatField(default=0.0)
    is_incoming=models.BooleanField(default=0.0)



class Crosswalk(models.Model):
    lat=models.FloatField()
    lon=models.FloatField()
    has_trlight=models.BooleanField(default=True)
