from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from .models import User,Drivers,Crosswalk
from django.contrib import messages
def chooseCars():
  pass
def signal_cars(req):
  messages.add_message(req,messages.INFO,"You must slow down. Pedestrian about to cross!")
 pass
def collect_cars():
  #get car sets that are closer than ??
  #get car speed
  #get car 제동거리
  # determine if the cars need signal
  chooseCars()
  #select cars that need signal
  selected_drivers=Drivers.objects.get(signal=True)
  #add message inside shared message
  try:
    signal_cars(selected_drivers)
  except(messages.WARNING.)
  #delete message
  #return cars that are signaled
  return JsonResponse({'drivers':selected_drivers})

def index(req):
  # to FE : "give a unique id for each user"
  if(req.method=='POST'):
    #register user info
    user=User.objects.create(req.readlines())
  # get : UniqueID / Lan / Long
  if(req.method=='GET'):
    user=User.objects.filter(id==req.id)
  # save (overwrite) user to server
  user.save()
  # Send notification to nearby cars
  cars = collect_cars()

  return JsonResponse( {} )


