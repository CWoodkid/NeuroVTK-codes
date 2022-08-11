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



DATA_day0_decision = []
DATA_day0_decisionNUM = []



DATA_day1_decision = []
DATA_day1_decisionNUM = []


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
  

  
        
for it in range(len(f_decision)):
    for i in range(len(day0_decision)):
        #print(len(f_marching[it]))
        basepath = f_decision[it][i] + '\\events.dat'

        if os.path.isfile(basepath):
            #print ("File exists")
            Data = np.genfromtxt(basepath, delimiter=' ', skip_header=0) #get data 
        
            #print(Data)
            events = Data.T[1]
            events = events[~np.isnan(events)]
            
            #print(events)
            
            if len(events) == 0:
                print("no reach events")
                pass
            else:        
                preference = np.nanmean(events)
                print(preference)
                NumDecisions = len(events)

            if it == 0:
                DATA_day0_decision.append(preference)
                DATA_day0_decisionNUM.append(NumDecisions)
            else:
                DATA_day1_decision.append(preference)
                DATA_day1_decisionNUM.append(NumDecisions)            
        else:
            print ("File not found")
            pass
        
    
    



fig = plt.figure(figsize=(2,4),dpi=300)
ax = fig.add_subplot(111)

plt.hist([DATA_day0_decision,DATA_day1_decision],label=['Gregarious', 'Isolated'])
    
#plt.ylim(0,1)
#plt.xlim(-30,30)

plt.rcParams.update({'font.size': 16})
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(True)


ax.set_axisbelow(True)

#ax.set_xticks([1,2])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xticks(rotation = 45)
ax.set_xlabel('Av Decision')
ax.set_ylabel('#')
#plt.title("Object Fixation")
#plt.title("Optomotor")

plt.show()





fig = plt.figure(figsize=(2,4),dpi=300)
ax = fig.add_subplot(111)

plt.hist([DATA_day0_decisionNUM,DATA_day1_decisionNUM],label=['Gregarious', 'Isolated'])
plt.ylim(0,max([*DATA_day0_decisionNUM,*DATA_day1_decisionNUM]))
#plt.xlim(-30,30)

plt.rcParams.update({'font.size': 16})
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(True)


ax.set_axisbelow(True)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xticks([1,2,3,4],rotation = 45)
ax.set_ylabel('Locust #')
ax.set_xlabel('Decision #')
#plt.title("Object Fixation")
#plt.title("Optomotor")

plt.show()


#print("total decisions by gregarious:", sum([*DATA_day0_decisionNUM]))
#print("total decisions by solitarious:", sum([*DATA_day1_decisionNUM]))