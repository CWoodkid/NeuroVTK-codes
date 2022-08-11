
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy import signal
import operator
import scipy
from scipy.signal import find_peaks
import math
from math import atan2,degrees
from scipy.ndimage import gaussian_filter
import seaborn as sns
from scipy.spatial import distance

TestAngle = 50 #angle between the posts
TestDist = 3.0 #distance to the locust
bodylength = 0.08


def diskretize(x,y, bodylength): #discretize data into equidistant points, using body lengts (https://stackoverflow.com/questions/19117660/how-to-generate-equispaced-interpolating-values)
    tol = bodylength #10cm ,roughly 2BL 
    i, idx = 0, []
    while i < len(x):
        total_dist = 0
        for j in range(i, len(x)):
            
            total_dist += distance.euclidean([x[j],y[j]], [x[j-1],y[j-1]])
            
            #print(total_dist)
            if total_dist > tol:
                idx.append(j)
                #print(idx)
                break
        i = j+1    
    
    #xn = [x[i] for i in idx]
    #yn = [y[i] for i in idx]
    
    """
    plt.plot(x, y)
    plt.scatter(xn, yn, s=1, color ='red')
    
    
    plt.xlim(-0.4,0.4)    
    plt.ylim(-0.4,0.4)
    plt.show()
    """
    #print('NovDiskreet')

    return idx    



def AngleBtw2Points(pointA, pointB):
  changeInX = pointB[0] - pointA[0]
  changeInY = pointB[1] - pointA[1]
  return atan2(changeInY,changeInX)


def rotate_vector(x,y, angle):
    
    co = np.cos(angle)
    si = np.sin(angle)

    rotatedx=[]
    rotatedy=[]

    for i in range(len(x)):
        rotatedx.append(x[i] * co - y[i] * si)   
        rotatedy.append(x[i] * si + y[i] * co)   
    
    return rotatedx,rotatedy


def dataHandler(data):
    #print(len(data[0]))
    if len(data) <= 37500:
        resampled = scipy.signal.resample(data,37500)
    else:
        resampled = scipy.signal.resample(data,60000)

    resampled = resampled - resampled[0]     
        
    #print(len(resampled[0]))
    return resampled 



def dataHandler_old(array0,array1):

    sampledx = scipy.signal.resample(array0,60000)
    sampledy = scipy.signal.resample(array1,60000)

    diffarx = np.diff(sampledx)
    diffary = np.diff(sampledy)
    """
    plt.plot(diffarx)
    plt.title("X")
    plt.show()
    
    plt.plot(diffary)
    plt.title("Y")
    plt.show()
    """
    diffarXY= np.stack((diffarx, diffary), axis=-1)

    indikes = np.argwhere( (diffarXY<-0.1) | (diffarXY>0.1))
    

    NewX = np.delete(diffarx, indikes.T)       
    NewY = np.delete(diffary, indikes.T)       
    
    """
    plt.plot(diffarx[-10000:])
    plt.title("oldX")
    plt.show()
    
    plt.plot(NewX[-10000:])
    plt.title("NewX")
    plt.show()

    plt.plot(diffary[-10000:])
    plt.title("oldY")
    plt.show()
    
    plt.plot(NewY[-10000:])
    plt.title("NewY")
    plt.show()    
    """
#    return sampledx,sampledy 
    return np.cumsum(NewX),np.cumsum(NewY) 


def removeNoise(x,y):

    NewX  = scipy.ndimage.gaussian_filter1d(x,sigma=2)  
    NewY  = scipy.ndimage.gaussian_filter1d(y,sigma=2)  

    return NewX,NewY    

def calc_angle(List1,List2):
    w=0
    theta = []
    dot = []
    while w < len(List1)-1:
 
    
        
        Vector1 = List1[w+1]-List1[w]
        Vector2 = List2[w+1]-List2[w]
    
        UnitVector1 = Vector1 / np.linalg.norm(Vector1)
        UnitVector2 = Vector2 / np.linalg.norm(Vector2)

        dotproduct =  np.dot(UnitVector1, UnitVector2)        
        angle = np.arccos(dotproduct)
        
        dot.append(dotproduct)     
        theta.append(angle)

        w = w + 1

    #plt.plot(theta)
    #plt.show

    return np.median(theta)

def calc_eucledian(xx1,yy1):                                                   #calculates spontaneous euclidian distance over time
    w=0
    dist = []
    while w < len(xx1)-1:
        

        a = np.array(xx1[w+1],yy1[w+1])
        b = np.array(xx1[w],yy1[w])        

        euc = np.linalg.norm(a - b)
        dist.append(euc)
        w = w + 1

    return dist


"""
def dataHandlerfor1(data):
    resampled=[]
    #print(len(data[0]))
    for i in range(len(data)):
        if len(data[i]) <= 36000:
            resampled.append(scipy.signal.resample(data[i],36000))
        elif len(data[i]) <= 100000 and  len(data[i]) >= 60000: 
            resampled.append(scipy.signal.resample(data[i],100000))            
        else: 
            resampled.append(scipy.signal.resample(data[i],180000))    
            
    return resampled 


def angleRandomizerFor2(TestAngle,TestDist):
    PostDist = TestDist
    #angleRandom = round(random.uniform(0.0,6.28),2)  #random number between 0-360 degrees, 2 decimals
    angleBetween = np.deg2rad(TestAngle)/2
    angleRandom = 0.00 #random number between 0-360 degrees, 2 decimals
    posx0 = PostDist * math.cos(angleRandom + angleBetween)
    posy0 = PostDist * math.sin(angleRandom + angleBetween)
    posx1 = PostDist * math.cos(angleRandom - angleBetween)
    posy1 = PostDist * math.sin(angleRandom - angleBetween)

    newpos1 = [posx0,posy0]
    newpos2 = [posx1,posy1]

    return newpos1, newpos2


def removeNoise(x,y,px1,py1,px2,py2):

    NewX  = scipy.ndimage.gaussian_filter1d(x,sigma=2)  
    NewY  = scipy.ndimage.gaussian_filter1d(y,sigma=2)  


    NewPX1 = scipy.ndimage.gaussian_filter1d(px1 ,sigma=2)       
    NewPY1 = scipy.ndimage.gaussian_filter1d(py1, sigma=2)     

    NewPX2 = scipy.ndimage.gaussian_filter1d(px2 ,sigma=2)       
    NewPY2 = scipy.ndimage.gaussian_filter1d(py2 ,sigma=2)    
    
    #if len(NewX) != len(NewY):  
    #        print('ACHTUNG2')

    LX = NewX
    LY = NewY

    CorrX = 0.0-LX[0]
    CorrY = 0.0-LY[0]
    
    
    LocustX = [x + CorrX for x in LX]
    LocustY = [x + CorrY for x in LY]
    PostX1 = [x + CorrX for x in NewPX1]
    PostY1 = [x + CorrY for x in NewPY1]
    PostX2 = [x + CorrX for x in NewPX2]
    PostY2 = [x + CorrY for x in NewPY2]

    return LocustX, LocustY, PostX1, PostY1, PostX2, PostY2          



def removeNoisefor1(x,y,px1,py1):

    NewX  = scipy.ndimage.gaussian_filter1d(x,sigma=2)  
    NewY  = scipy.ndimage.gaussian_filter1d(y,sigma=2)  


    NewPX1 = scipy.ndimage.gaussian_filter1d(px1 ,sigma=2)       
    NewPY1 = scipy.ndimage.gaussian_filter1d(py1, sigma=2)     


    #if len(NewX) != len(NewY):  
    #        print('ACHTUNG2')

    LX = NewX
    LY = NewY

    CorrX = 0.0-LX[0]
    CorrY = 0.0-LY[0]
    
    
    LocustX = [x + CorrX for x in LX]
    LocustY = [x + CorrY for x in LY]
    PostX1 = [x + CorrX for x in NewPX1]
    PostY1 = [x + CorrY for x in NewPY1]


    return LocustX, LocustY, PostX1, PostY1   
        
            


def eventFinder(*args):
    S = np.absolute(np.diff(args[0])) + np.absolute(np.diff(args[1])) + np.absolute(np.diff(args[2])) + np.absolute(np.diff(args[3]))
    peaks, _ = find_peaks(S,prominence=3) 
    
    #plt.plot(S)
    #plt.plot(peaks, S[peaks], "x")
    #plt.show()
    
    return peaks

def eventFinderfor1(*args):
    S = np.absolute(np.diff(args[0])) + np.absolute(np.diff(args[1]))
    peaks, _ = find_peaks(S,prominence=2) 
    
    #plt.plot(S)
    #plt.plot(peaks, S[peaks], "x")
    #plt.show()

    return peaks
"""    