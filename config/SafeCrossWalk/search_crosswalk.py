import faiss
import numpy as np
from haversine import haversine

def getNearestVectorId(index, query, k=1):
    if len(query.shape) ==1:
        query = np.expand_dims(query,axis=0)

    distances, idxvectorids = index.search(query, k)

    #vectorids = ivindex[idxvectorids[:]]
    return idxvectorids

def getNearestCrossWalk(current_location, CRlocations, city = "Seoul"):
    assert city=="Seoul", "Other cities other than Seoul have not been implemented."
    queries = np.array(current_location, dtype=np.float32)
    index = faiss.read_index("./crosswalk_index_"+city.lower()+".index")

    vectorids = np.concatenate(getNearestVectorId(index,queries))
    print(vectorids)
    print([CRlocations[id] for id in vectorids])

    distances = [haversine(current_location, CRlocations[id] ) for current_location, id in zip(current_location,vectorids) ]

    return distances*1000


if __name__ == "__main__":
    testset = np.load("./test_vectorset.npy")
    ivindex = np.load("./inverted_index.npy")

    index = faiss.read_index("./crosswalk_index_seoul.index")

    testqueries = testset[10]
    testqueries = np.array([37.644785, 126.918867], dtype=np.float32)
 #    vectorids = getNearestCrossWalk(index, ivindex, testqueries, k = 1)
   # targetids = np.concatenate(vectorids)

    current_loc = np.mean(testset, axis = 0)
    print(getNearestCrossWalk(current_location=[[37.644785, 126.918867]], CRlocations=testset))
