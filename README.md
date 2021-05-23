# :camel::blue_heart:BlueCamel-SafeCrosswalk


## (ENG)
It is a long known fact people with difficulty walking fast from pregnant mothers to people with a chronic disability face pressure by the blinking lights of crosswalk traffic signals that often turn red too fast for them to get across. However, reconstructing all crosswalk environment is anticipated to take a long time. Even Seoul started the reconstruction concerning the subject just last year to fix over 10 thousand cases within Gangbook, the upper side of the city.
Blue Camel proposes SafeCrosswalk, a project that ensuress the safety of pedestrians, especially those who are either temporarily or chronically facing difficulty in moving. 


### Here's how it works 🖱️

We aim to resolve three main criteria
* Avoid the situation where car owners are unaware of a pedestrian attempting to use a crosswalk without traffic signals
* Ensure safer crossing in case of rural areas where no crosswalk prepared
* Suggest regulations between a pedestrian and drivers at places where all traffic light is either temporarily or always replaced with flashing orange light

(User GUI 사진 업로드)

#### Pedestrian side
To ensure safety, the user simply can press the 'Notify' button to alert nearby cars that he or she is about to cross the road. However, if the system analyzes that the car is unable to stop before the pedestrian, it will alert the user to stop and wait for the car to pass for a remote minute. Also, if the user attempts cross roads where it is not a crosswalk, a verbal message will suggest the user to go look for the nearest crosswalk with the distance to the area unless it is a rural area with no crosswalk equipped. 

#### Driver side
Whenever a driver comes within 500m boundary crosswalk and if a pedestrian has notified to cross roads, a verbal message will explain the driver to reduce speed with the distance between the vehicle and the pedestrian. 


## The APIs

### UserView
UserView is a class-based view that inherits 
'''from django.views.generic.base import View'''


## (KOR)

아이, 임산부 및 장애인들 중에는 짧은 횡단보도 신호에 민감할 수밖에 없습니다. 게다가 2021년을 기점으로도 전국 각지에 횡단보도용 신호등이 없는 횡단보도가 많으며, 음성 신호기와 같은 적절한 barrier-free 시설이 갖추어지지 않은 곳이 많습니다. Blue Camel은 자동차와 보행자, 그리고 주변 환경의 정보를 이용하여 횡단보도 이용시 특히 위험에 처할 가능성이 높은 보행자들의 안전을 지키는 서비스를 제안합니다. SafeCrosswalk을 통해서라면 교통 약자들의 이동에 대한 불안과 위험을 덜 수 있을 것입니다.


### 어떻게 쓰이나요? 🖱️

세 가지 중점적인 문제점을 해결하고자 합니다
* Avoid the situation where car owners are unaware of a pedestrian attempting to use a crosswalk without traffic signals
* Ensure safer crossing in case of rural areas where no crosswalk prepared
* Suggest regulations between a pedestrian and drivers at places where all traffic light is either temporarily or always replaced with flashing orange light


#### Pedestrian side
To ensure safety, the user simply can press the 'Notify' button to alert nearby cars that he or she is about to cross the road. However, if the system analyzes that the car is unable to stop before the pedestrian, it will alert the user to stop and wait for the car to pass for a remote minute. Also, if the user attempts cross roads where it is not a crosswalk, a verbal message will suggest the user to go look for the nearest crosswalk with the distance to the area unless it is a rural area with no crosswalk equipped. 

#### Driver side
Whenever a driver comes within 500m boundary crosswalk and if a pedestrian has notified to cross roads, a verbal message will explain the driver to reduce speed with the distance between the vehicle and the pedestrian. 

## API 설명서 

### UserView
'''from django.views.generic.base import View'''를 바탕으로 한 클래스형 view입니다. 

def get(self, req)

의도: 앱 실행시 보이는 user 근처(500m근방)의 차량 위경도를 전달하기 위해 차량 객체를 필터해서 serialize한 후 Json형태로 변환합니다.

	input: user의 lattitude, longitude가 들어가야한다.
	return: HttpResponse(serializers.serialize('json', cars),content_type="application/json")
	* cars는 user 500m근방의 모든 차를 serialize한 것이다. 


def post(self, req)

의도: user가 'Notify' 버튼을 눌렀을 때 이어지는 화면과 관련이 있습니다. 유저와 횡단보도 사이의 거리를 바탕으로 유저에게 보낼 메세지를 조작하고, 근처에 있고 다가오는 차량들을 필터링 해 메세지를 보낼 객체 내부에 메세지를 저장해놓습니다. 

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
    



### DriverView
'''from django.views.generic.base import View'''를 바탕으로 한 클래스형 view입니다. 

def get(self,req)
  
의도: 차량의 위경도를 받아 객체에 존재하는 prevlat, prevlon, curlat, curlon을 업데이트하고, 차량 화면에 띄울 메세지가 존재할 시 Json 형태로 줍니다.

    input: car의 latitude, longitude가 들어가야한다. 
    return:
    만약 user/pedestrian이 driver에게 메세지를 보낸 상황이라면
      JsonResponse({'car_msg':signal_msg}, content_type="application/json")
      *signal_msg는 CharField(manx_length=100)으로 받은 string입니다.
    만약 보낼 메세지가 없다면
      return JsonResponse({}, content_type="application/json") 


  

