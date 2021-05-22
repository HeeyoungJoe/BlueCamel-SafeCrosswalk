from django.shortcuts import render
from django.http import JsonResponse

def index(req):
  # to FE : "give a unique id for each user"
  
  # get : UniqueID / Lan / Long

  # save (overwrite) user to server

  # Send notification to nearby cars
  cars = collect_cars()

  return JsonResponse('foo':'bar', "hello": "world", "nested" : {"a":1, "b":2 } } ) 

def collect_cars():
  pass
