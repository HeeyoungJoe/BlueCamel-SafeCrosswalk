## simple braking model 사용 방법

### simple guide

 ```Python

from simple_braking_model import simplecheckBraking

velocity = 100 #collected velocity
distance = 180  #distance between car and pedestrian
safetime = 5 # time for buffering braking

braking_distance, braking_time = simplecheckBraking(velocity, distance, safetime) 
#braking_distance : distance for stopping car
#braking_time : time for stopping car
```
 