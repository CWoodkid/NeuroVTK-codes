# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 13:46:47 2022

@author: Sercan
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy import signal
import operator
import scipy
import os, glob
import math

from CriticalityFuncs_align import *


bodylength = 0.12


rt = "C:\\Users\\mcank\\OneDrive\\Masaüstü\\vtk\\VR\\can\\"

        
day0_marching = []
day0_optomotor = []
day0_decision = []

day1_marching = []
day1_optomotor = []
day1_decision = []


f_marching = [day0_marching,day1_marching]
f_optomotor = [day0_optomotor,day1_optomotor]
f_decision = [day0_decision,day1_decision]



DATA_day0_marching_distX = []
DATA_day0_marching_distY = []
DATA_day0_marching = []
DATA_day0_dist = []
DATA_day0_marching_tort = []



DATA_day1_marching_distX = []
DATA_day1_marching_distY = []
DATA_day1_marching = []
DATA_day1_dist = []
DATA_day1_marching_tort = []


for rootdir, dirs, files in os.walk(rt):
    for subdir in dirs:
        p = os.path.join(rootdir,subdir)
        s = p.split('\\')
        
        #print(s[-1].split('_'))
        if "day1" in s:
            if 'HighC' in s[-1].split('_'):
                day0_marching.append(p)
            elif "opto" in s[-1].split('_'):
                day0_optomotor.append(p)
            elif "Angle50" in s[-1].split('_'):
                day0_decision.append(p)                
        elif "day2" in s:
            if 'HighC' in s[-1].split('_'):
                day1_marching.append(p)
            elif "opto" in s[-1].split('_'):
                day1_optomotor.append(p)
            elif "Angle50" in s[-1].split('_'):
                day1_decision.append(p)      
  

  
for it in range(len(f_marching)):
    for i in range(len(day0_marching)):
        print(len(f_marching[it]))
        basepath = f_marching[it][i] + '\\velocities.dat'
        print(basepath)
        Data = np.genfromtxt(basepath, delimiter=' ', skip_header=0) #get data 
            
        X = Data.T[0]                                                       
        Y = Data.T[1]
            
        #print(len(X))
        
        #resampleX, resampleY = dataHandler(X),dataHandler(Y)
        resampleX, resampleY = dataHandler_old(X,Y)
        #print("resampled")
    
        X, Y = removeNoise(resampleX, resampleY)
        #print("noise removed")
    
        newindex = diskretize(X,Y, bodylength)
        
        diskretX = [X[i]*-1 for i in newindex]
        diskretY = [Y[i]*-1 for i in newindex]
        """
        plt.plot(diskretX,diskretY)
        plt.xlim(-20,20)
        plt.ylim(-20,20)
        plt.title(basepath)
        plt.show()    
        """
        #print("spatially handled")
        
        speedVirtualx = [0.0032]*len(diskretX) #actual value is not important for x, any positive scalar should work
        speedVirtualy = [0.0]*len(diskretY) #it must be 0.0
        
        distVirtual = np.c_[np.cumsum(speedVirtualx),np.cumsum(speedVirtualy)]
        vectordata = np.c_[diskretX,diskretY]
        
        medianAngle = 1-((calc_angle(vectordata,distVirtual)/np.pi)*2)
        distX = diskretX[-1]
        

        eucLocust = math.sqrt((diskretX[-1])**2+(diskretY[-1])**2) 
        distTraveled = bodylength * len(diskretX) 
        tortuosity = eucLocust / distTraveled
        
        if it == 0:
            DATA_day0_marching_distX.append(diskretX)
            DATA_day0_marching_distY.append(diskretY)
            DATA_day0_marching.append(medianAngle)
            DATA_day0_dist.append(distX)            
            DATA_day0_marching_tort.append(tortuosity)                     
        else:
            DATA_day1_marching_distX.append(diskretX)
            DATA_day1_marching_distY.append(diskretY)
            DATA_day1_marching.append(medianAngle)
            DATA_day1_dist.append(distX)
            DATA_day1_marching_tort.append(tortuosity) 


    
    

    
    
fig = plt.figure(figsize=(4,4),dpi=300)
ax = fig.add_subplot(111)
for i in range(len(DATA_day0_marching_distX)):
    plt.plot(DATA_day0_marching_distX[i],DATA_day0_marching_distY[i])
    
plt.ylim(-15,15)
plt.xlim(-15,15)
ax.set_xticks([-15,0,15])
ax.set_yticks([-15,0,15])
plt.rcParams.update({'font.size': 16})
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)


ax.set_axisbelow(True)

plt.title("Marching: Gregarious")
#plt.title("Optomotor")

plt.show()



    
fig = plt.figure(figsize=(4,4),dpi=300)
ax = fig.add_subplot(111)
for i in range(len(DATA_day1_marching_distX)):
    plt.plot(DATA_day1_marching_distX[i],DATA_day1_marching_distY[i])
    
plt.ylim(-15,15)
plt.xlim(-15,15)
ax.set_xticks([-15,0,15])
ax.set_yticks([-15,0,15])
plt.rcParams.update({'font.size': 16})
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)


ax.set_axisbelow(True)

plt.title("Marching: Isolated")
#plt.title("Optomotor")

plt.show()


    
    

fig = plt.figure(figsize=(2,4),dpi=300)
ax = fig.add_subplot(111)

ax.boxplot([DATA_day0_marching,DATA_day1_marching])
    
plt.ylim(-1,1)
#plt.xlim(-30,30)

plt.rcParams.update({'font.size': 16})
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(True)


ax.set_axisbelow(True)

ax.set_xticks([1,2])
ax.set_xticklabels(['Gregarious', 'Isolated'])
plt.xticks(rotation = 45)
ax.set_ylabel('Align Score')
plt.title("Marching")
#plt.title("Optomotor")

plt.show()

diffcon = []
for i in range(len(DATA_day0_marching)):
    diff = DATA_day1_marching[i]-DATA_day0_marching[i]
    diffcon.append(diff) 


fig = plt.figure(figsize=(2,4),dpi=300)
ax = fig.add_subplot(111)

ax.boxplot(diffcon)
    
plt.ylim(-1,1)
#plt.xlim(-30,30)

plt.rcParams.update({'font.size': 16})
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(True)


ax.set_axisbelow(True)
ax.set_xticklabels(['Isolated-Gregarious'])
plt.xticks(rotation = 45)
ax.set_ylabel('Delta Align Score')
plt.title("Marching")
#plt.title("Optomotor")

plt.show()




fig = plt.figure(figsize=(2,4),dpi=300)
ax = fig.add_subplot(111)

ax.boxplot([DATA_day0_dist,DATA_day1_dist])
    
plt.ylim(0,max([*DATA_day0_dist,*DATA_day1_dist]))
#plt.xlim(-30,30)

plt.rcParams.update({'font.size': 16})
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(True)


ax.set_axisbelow(True)

ax.set_xticks([1,2])
ax.set_xticklabels(['Gregarious', 'Isolated'])
plt.xticks(rotation = 45)
ax.set_ylabel('Marching Dist')
plt.title("Marching")
#plt.title("Optomotor")

plt.show()






fig = plt.figure(figsize=(2,4),dpi=300)
ax = fig.add_subplot(111)

ax.boxplot([DATA_day0_marching_tort,DATA_day1_marching_tort])
    
plt.ylim(0,1)
#plt.xlim(-30,30)

plt.rcParams.update({'font.size': 16})
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(True)


ax.set_axisbelow(True)

ax.set_xticks([1,2])
ax.set_xticklabels(['Gregarious', 'Isolated'])
plt.xticks(rotation = 45)
ax.set_ylabel('Tortuosity')
plt.title("Marching")
#plt.title("Optomotor")

plt.show()


