## crosswalk search function 사용 방법

### simple guide
- This function is implemented by NN algorithm
- 사용 방법
 
 ```Python

from search_crosswalk import getNearestCrossWalk

current_loc = [37.644785, 126.918867]
crlocations = np.load("./test_vectorset.npy")  #crosswalk location dataset (about seoul city)

distance = getNearestCrossWalk([current_loc], crlocations) # return distance (m) to nearset CrossWalk 
```

### TO-DO
- [ ] 인덱스 파일, 벡터 데이터셋 이름 바꾸기
 