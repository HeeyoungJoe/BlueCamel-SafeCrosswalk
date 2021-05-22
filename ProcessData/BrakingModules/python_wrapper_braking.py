import matlab.engine
import sys, os
print(os.getcwd())
#sys.path.append(os.path.join(os.getcwd(),"ProcessData"))
print(sys.path)
def getbrakinginfo(intitalv):
    eng = matlab.engine.start_matlab()
    [a, b] = eng.getBrakingInfoFromV(intitalv, nargout=2)
    return a,b

if __name__=="__main__":
    final_position, braking_time = getbrakinginfo(100.0)
    print(final_position)
    print(braking_time)