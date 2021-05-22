from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from .models import Drivers
from django.contrib import messages
Drivers.signal="A pedestrian is attempting to cross the road!"

def update(user_lat,user_lon,car_id,car_lat,car_lon):
  car=Drivers.objects.get(id=car_id)
  car.brake=1
  car.prevlat=car_lat
  car.prevlon=car_lon
  car.distance=1
  car.is_incoming=True

class MyView(generic.View):
  def getCars(self,validated_data):
    filDistCars=[car for car in Drivers.objects.filter('distance') if car.distance<500]
    #제일 위험한건 제동거리가 제일
    #the one that might be the most dangerous
    return JsonResponse({'cars':filDistCars})
  def getCarAlert(self,validated_data):
    filteredCars = [car for car in Drivers.objects.filter('distance') if car.distance < 500 and car.is_incoming == True]
    most_dangerous = filteredCars.order_by('-brake')[0]
    safe=False
    #determine if it is safe

    if safe==True:
      return JsonResponse({'user_msg':0,'cars':filteredCars})
    else:
      return JsonResponse({'user_msg':1,'cars':filteredCars})
    #when safe, alert 보행자 &cars
    #when not, still alert cars but 보행자 get different message
