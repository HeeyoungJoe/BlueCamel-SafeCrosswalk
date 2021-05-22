from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from django.views.generic.base import View
from .models import Drivers
from django.contrib import messages
from haversine import haversine
from django.core import serializers

Drivers.signal="A pedestrian is attempting to cross the road!"



class UserView(View):
  """
  유저가 최초에 앱을 켰을 때 호출 : 주변 500m 이내의 차량들을 JSON 형태로 제공
  """
  def get(self, req):
    # User의 lat, lon 를 받아온다
    lat = req.GET.get('lat', None)
    lon = req.GET.get('lon', None)

    cars = self._getNearCars(lat, lon, 0.5) # 0.5 km

    return HttpResponse(serializers.serialize('json', cars), content_type="application/json")

  def _getNearCars(self, user_lat, user_lon, distance):
    #제일 위험한건 제동거리가 제일 긴것
    cars = Drivers.objects.all()
    cars_arr = []

    for car in cars:
      if abs(self._getGap(car.curlat, car.curlon, user_lat, user_lon)) <= distance:
        cars_arr.append(car)

    return cars_arr

  def _getGap(self, a_lat, a_lon, b_lat, b_lon):
    start = (float(a_lat), float(a_lon)) # (lat, lon)
    goal = (float(b_lat), float(b_lon))
    return haversine(start, goal)


  """
  유저가 길을 건널 때 호출 (e.g. 버튼 클릭) : 주변 위험이 될 법한 차 중 제일 가까운 차와의 거리를 안내
  """
  def post(self, req):
    # User의 lat, lon 를 받아온다
    lat = req.GET.get('lat', None)
    lon = req.GET.get('lon', None)






    return HttpResponse(serializers.serialize('json', cars), content_type="application/json")


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


class DriverView(generic.View):
  def update(user_lat, user_lon, car_id, car_lat, car_lon):
    car = Drivers.objects.get(id=car_id)
    car.brake = 1
    car.prevlat = car_lat
    car.prevlon = car_lon
    car.distance = 1
    car.is_incoming = True
    return JsonResponse({'msg':"Okay!"})