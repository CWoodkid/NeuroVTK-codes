#%%
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

from CriticalityFuncs_align_individual import *


bodylength = 0.12

fn1 = 8
fn2 = 9 


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
DATA_day0_optomotor_distX = []
DATA_day0_optomotor_distY = []
DATA_day0_optomotor = []
DATA_day0_optomotor_dist = []
DATA_day0_optomotor_tort = []
DATA_day0_decision = []
DATA_day0_decisionNUM = []


DATA_day1_marching_distX = []
DATA_day1_marching_distY = []
DATA_day1_marching = []
DATA_day1_dist = []
DATA_day1_marching_tort = []
DATA_day1_optomotor_distX = []
DATA_day1_optomotor_distY = []
DATA_day1_optomotor = []
DATA_day1_optomotor_dist = []
DATA_day1_optomotor_tort = []
DATA_day1_decision = []
DATA_day1_decisionNUM = []
DATA_day1_optomotor_dist = []

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
  
    
  
IDs = []
for it in range(len(f_marching)):
    for i in range(len(day0_marching)):
        #print(len(f_marching[it]))
        basepath = f_decision[it][i] + '\\velocities.dat'
        IDs.append(basepath.split('\\')[fn1] + "_" + basepath.split('\\')[fn2])
        print(IDs[-1])
        

  
for it in range(len(f_marching)):
    for i in range(len(day0_marching)):
        #print(len(f_marching[it]))
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

for it in range(len(f_optomotor)):
    for i in range(len(day0_optomotor)):
        #print(len(f_marching[it]))
        basepath = f_optomotor[it][i] + '\\velocities.dat'
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
        
        diskretX = [X[i]*1 for i in newindex]
        diskretY = [Y[i]*1 for i in newindex]
        """
        plt.plot(diskretX,diskretY)
        plt.xlim(-20,20)
        plt.ylim(-20,20)
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
            DATA_day0_optomotor_distX.append(diskretX)
            DATA_day0_optomotor_distY.append(diskretY)
            DATA_day0_optomotor.append(medianAngle)
            DATA_day0_optomotor_dist.append(distX)
            DATA_day0_optomotor_tort.append(tortuosity) 
        else:
            DATA_day1_optomotor_distX.append(diskretX)
            DATA_day1_optomotor_distY.append(diskretY)
            DATA_day1_optomotor.append(medianAngle)
            DATA_day1_optomotor_dist.append(distX)
            DATA_day1_optomotor_tort.append(tortuosity) 
            
for it in range(len(f_decision)):
    for i in range(len(day0_decision)):
        #print(len(f_marching[it]))
        basepath = f_decision[it][i] + '\\events.dat'
        print(basepath)
        
        if os.path.isfile(basepath):
            #print ("File exists")
            Data = np.genfromtxt(basepath, delimiter=' ', skip_header=0) #get data 
        
            #print(Data)
            events = Data.T[1]
            events = events[~np.isnan(events)]
            
            #print(events)
            
            if len(events) == 0:
                print("no reach events")
                preference = np.nan
                NumDecisions = np.nan                
            else:        
                preference = np.nanmean(events)
                #print(preference)
                NumDecisions = len(events)

            if it == 0:
                DATA_day0_decision.append(preference)
                DATA_day0_decisionNUM.append(NumDecisions)
            else:
                DATA_day1_decision.append(preference)
                DATA_day1_decisionNUM.append(NumDecisions)            
        else:

            preference = np.nan
            NumDecisions = np.nan                   

            if it == 0:
                DATA_day0_decision.append(preference)
                DATA_day0_decisionNUM.append(NumDecisions)
            else:
                DATA_day1_decision.append(preference)
                DATA_day1_decisionNUM.append(NumDecisions)          


                print ("File not found")

        
    
    

    
def substraktor(List1,List2,List3):
    print("SUBTRAKTION: COMMENCE")
    if len(List1) != len(List2):
        print("Achtung")
    else:
        pass
    
    for i in range(len(List1)):
        d = List1[i] - List2[i]
        List3.append(d)






Diff_marching_distX = []
Diff_marching_distY = []
Diff_marching = []
Diff_dist = []
Diff_marching_tort = []
Diff_optomotor_distX = []
Diff_optomotor_distY = []
Diff_optomotor = []
Diff_optomotor_dist = []
Diff_optomotor_tort = []
Diff_decision = []
Diff_decisionNUM = []






substraktor(DATA_day0_marching,DATA_day1_marching,Diff_marching)
substraktor(DATA_day0_dist,DATA_day1_dist,Diff_dist)
substraktor(DATA_day0_marching_tort,DATA_day1_marching_tort,Diff_marching_tort)
substraktor(DATA_day0_optomotor,DATA_day1_optomotor,Diff_optomotor)
substraktor(DATA_day0_optomotor_dist,DATA_day1_optomotor_dist,Diff_optomotor_dist)
substraktor(DATA_day0_optomotor_tort,DATA_day1_optomotor_tort,Diff_optomotor_tort)
substraktor(DATA_day0_decision,DATA_day1_decision,Diff_decision)
substraktor(DATA_day0_decisionNUM,DATA_day1_decisionNUM,Diff_decisionNUM)

import pandas as pd




df = pd.DataFrame(list(zip(
    IDs,
    Diff_marching,
    Diff_dist,
    Diff_marching_tort,
    Diff_optomotor,
    Diff_optomotor_dist,
    Diff_optomotor_tort,
    Diff_decision,
    Diff_decisionNUM,
    )),
    columns =['ID','m_align','m_dist','m_tort','o_align','o_dist','o_tort','d_average','d_num'])


print(df)
df.to_csv (rt + '//data.csv', index = True, header=True, na_rep='NULL')

# %%
