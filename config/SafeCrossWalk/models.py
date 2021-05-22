from django.db import models

# Create your models here.

class Drivers(models.Model):
    id=models.IntegerField(primary_key=True)

class User(models.Model):
    id=models.IntegerField(primary_key=True)

class Crosswalk(models.Model):
    wuido=models.FloatField()
    gyeondo=models.FloatField()
