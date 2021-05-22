import pandas as pd
import numpy as np
import argparse, faiss

parser = argparse.ArgumentParser()
parser.add_argument("--filepath", type=str)

def loadcsv(path):
    data = pd.read_csv(path, encoding="CP949")

    latitude = np.expand_dims(data['위도'], axis=1)
    longitude = np.expand_dims(data['경도'], axis=1)
    ids = np.expand_dims(data['순번'], axis=1)
    vectors = np.concatenate((latitude, longitude), axis=1)

    return ids, np.array(vectors, dtype=np.float32)

def indexing(vectorset, indextype = "FlatL2", dim =2):
    if indextype == "FlatL2":
        index = faiss.IndexFlatL2(dim)
    else :
        index = faiss.IndexFlatIP(dim)

    #ids = np.array(np.expand_dims(vectorset[:,0], axis=1),dtype=np.int)
    #ids = np.array(vectorset[:,0], dtype=int)
    vectors = np.array(vectorset,dtype=np.float32)
    #print(ids.shape)
    print(vectors.shape)
    index.add(vectors)
    #print(index.ntotal)
    #print(ids)
    ##print(vectors)
    #index.add_with_ids(vectors, ids)

    return index

if __name__ == "__main__":
    args = parser.parse_args()
    args.filepath = "C:/Users/leeju/PycharmProjects/BlueCamel-SafeCrosswalk/서울시 횡단보도 위치정보 (좌표계_ WGS1984) (1).csv"

    ids, vectorset = loadcsv(path = args.filepath)
    index = indexing(vectorset)
    faiss.write_index(index,"crosswalk_index_seoul.index")

    ids = np.squeeze(ids)
    np.save("./inverted_index.npy",ids)
    np.save("./test_vectorset.npy", vectorset)

    print(index.search(vectorset[1:4],1))

