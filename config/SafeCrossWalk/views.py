import json
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from django.views.generic.base import View
from .models import Drivers
from django.contrib import messages
from haversine import haversine
from django.core import serializers
from SafeCrossWalk.search_crosswalk import getNearestCrossWalk
from SafeCrossWalk.simple_braking_model import simplemodel
import numpy as np
import faiss
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


Drivers.signal="A pedestrian is attempting to cross the road!"


@method_decorator(csrf_exempt, name='dispatch')
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
      if self._getGap(car.curlat, car.curlon, user_lat, user_lon) <= distance:
        cars_arr.append(car)

    return cars_arr

  def _getGap(self, a_lat, a_lon, b_lat, b_lon):
    start = (float(a_lat), float(a_lon)) # (lat, lon)
    goal = (float(b_lat), float(b_lon))
    return abs(haversine(start, goal))


  """
  유저가 길을 건널 때 호출 (e.g. 버튼 클릭) : 주변 위험이 될 법한 차 중 제일 가까운 차와의 거리를 안내
  """
  def post(self, req):
    # User의 lat, lon 를 받아온다
    lat = req.GET.get('lat', None)
    lon = req.GET.get('lon', None)

    # 근처에 횡단보도가 있다면 -> WAIT (crosswalk is near) 결과 리턴
    distance = self._getNearestCrosswalk(lat, lon)
    if type(distance) == list:
      distance = distance[0]
    print(distance)
    # distance /= 200

    if 20 < distance < 50: # 근처에 횡단보도
      return JsonResponse({"msg":"WAIT"}, content_type="application/json")

    elif 50 <= distance: # 횡단보도 없음 (instant 횡단보도)
      cars = self._collectCarToNotify(lat, lon)
      if cars != None:
        self._sendAlert(cars) # 주변에 있는 차들에게 경고를 보냄 <TODO: SECRET_MISSION>

      return JsonResponse({"msg":"INSTANT_CROSSWALK"}, content_type="application/json")

    else: # 지금 횡단보도 앞
      cars = self._collectCarToNotify(lat, lon)
      print(cars)
      if cars is None:
        print(1)
        return JsonResponse({'msg':'GO'}, content_type="application/json")

      self._sendAlert(cars)

      nearestCar = cars[0]
      isDangerous = self._isTooDangerous(nearestCar, lat, lon)
      distance = self._getGap(nearestCar.curlat, nearestCar.curlon, lat, lon) * 1000 # meter
      if isDangerous:
        print(2)
        return JsonResponse({"msg":"STOP", "distance": distance}, content_type="application/json")
      else:
        print(3)
        return JsonResponse({"msg":"GO"}, content_type="application/json")

  def _getNearestCrosswalk(self, lat, lon):
    current_loc = [float(lat), float(lon)]
    print(current_loc)
    crlocations = np.load("./test_vectorset.npy")
    return getNearestCrossWalk([current_loc], crlocations)

  # 리턴하는 리스트 안의 첫번째 인덱스가 무조건 제일 가까운 차량으로 가정한다
  def _collectCarToNotify(self, lat, lon):
    cars = Drivers.objects.all()

    result = []
    for car in cars:
      userCarDistance = self._getGap(car.curlat, car.curlon, lat, lon)
      # 500 미터 안쪽인지 && 다가오고 있는지
      if userCarDistance <= 0.5 and userCarDistance < self._getGap(car.prevlat, car.prevlon, lat, lon):
        result.append(car)

    if len(result) == 0:
      return None
    return result

  def _isTooDangerous(self, nearestCar, lat, lon):
    return self._calculateBrakeDistance(nearestCar) > self._getGap(nearestCar.curlat, nearestCar.curlon, lat, lon)

  def _calculateBrakeDistance(self, car):
    velocity = 100 #collected velocity
    braking_distance, braking_time = simplemodel(velocity)
    return braking_distance

  def _sendAlert(self, car):
    print(car.id)


###########################################################################

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

  def get(self,request):#user_lat, user_lon, car_id, car_lat, car_lon):
    car = Drivers.objects.get(id=request.car_id)

    if(car is None):
      car=Drivers.objects.create(id=request.car_id)

    car.brake = 1
    '''
    car.prevlat = car_lat
    car.prevlon = car_lon'''
    car.distance = 1
    car.is_incoming = True
    #return JsonResponse({'msg':"Okay!"})

    return JsonResponse({'msg':"Okay!"}, json_dumps_params={'ensure_ascii': True})
