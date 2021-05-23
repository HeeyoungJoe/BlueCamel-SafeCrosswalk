# :camel::blue_heart:BlueCamel-SafeCrosswalk


##(ENG)
It is a long known fact people with difficulty walking fast from pregnant mothers to people with a chronic disability face pressure by the blinking lights of crosswalk traffic signals that often turn red too fast for them to get across. However, reconstructing all crosswalk environment is anticipated to take a long time. Even Seoul started the reconstruction concerning the subject just last year to fix over 10 thousand cases within Gangbook, the upper side of the city.
Blue Camel proposes SafeCrosswalk, a project that ensuress the safety of pedestrians, especially those who are either temporarily or chronically facing difficulty in moving. 


### Here's how it works 🖱️

We aim to resolve three main criteria
* Avoid the situation where car owners are unaware of a pedestrian attempting to use a crosswalk without traffic signals
* Ensure safer crossing in case of rural areas where no crosswalk prepared
* Suggest regulations between a pedestrian and drivers at places where all traffic light is either temporarily or always replaced with flashing orange light


## The APIs

### UserView
UserView is a class-based view that inherits '''
from django.views.generic.base import View'''


## (KOR)

def get(self, req)

	input: user의 lattitude, longitude가 들어가야한다.
	return: HttpResponse(serializers.serialize('json', cars),content_type="application/json")
	* cars는 user 500m근방의 모든 차를 serialize한 것이다. 


def post(self, req)

	input: user의 latitude, longitude가 들어가야한다. 
	return:
	user와 횡단보도의 거리가 20m 초과 50m 이하일 경우
		return JsonResponse({"msg":"WAIT"}, content_type="application/json")

	user와 횡단보도의 거리가 50m 초과일 경우
		JsonResponse({"msg":"INSTANT_CROSSWALK"}, content_type="application/json")

	user와 횡단보도의 거리가 20m 이하일 경우 
		사고 발생 가능성이 높다면 return JsonResponse({"msg":"STOP", "distance": distance}
		사고 발생 가능성이 낮다면/차가 없다면 JsonResponse({"msg":"GO"}, content_type="application/json")
		* distance는 float으로 user와 driver 사이의 거리를 나타낸다. 
    


###DriverView

def get(self,req)
  
    input: car의 latitude, longitude가 들어가야한다. 
    return:
    만약 user/pedestrian이 driver에게 메세지를 보낸 상황이라면
      JsonResponse({'car_msg':signal_msg}, content_type="application/json")
      *signal_msg는 CharField(manx_length=100)으로 받은 string입니다.
    만약 보낼 메세지가 없다면
      return JsonResponse({}, content_type="application/json") 


  

