from django.db import models

# Create your models here.

class Drivers(models.Model):
    id=models.IntegerField(primary_key=True)
    signal=models.BooleanField(default=False)
    class Meta:
        ordering=['id']

class User(models.Model):
    id=models.IntegerField(primary_key=True)

class Crosswalk(models.Model):
    wuido=models.FloatField()
    gyeongdo=models.FloatField()
    has_trlight=models.BooleanField(default=True)
