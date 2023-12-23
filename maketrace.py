#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 13:22:12 2020

@author: adam
"""
import os.path
import json
import matplotlib.pyplot as plt
import numpy as np

dirs1 = 't42_data'

ndends = 1 + 20

apicnum = 6 


starttime = 300

asBatch = False

if asBatch:
   filename1 = dirs1 + '/t42_0' + '.json'
else:   
   filename1 = 'model_output.json'



if os.path.isfile(filename1):
    with open(filename1) as f:
      data = json.load(f)
      
      pyrind = data['net']['pops']['PYR_pop']['cellGids'][0]
      x1 = np.array(data['simData']['V_soma']['cell_' + str(pyrind)])
      x1all = np.zeros(x1.shape[0]*ndends).reshape(x1.shape[0],ndends)
      x1all[:,0] =  x1all[:,0] + x1
      l1 = [key for key, val in data['simData'].items() 
        if (key[0:6]=='V_apic' and 'cell_' + str(pyrind) in val)]

      for x, xval1 in enumerate(l1):
           x1 = np.array(data['simData'][xval1]['cell_' + str(pyrind)])
           x1all[:,x+1] =  x1all[:,x+1] + x1
 
      x1all = x1all - x1all[int(starttime-1),:]

      plt.figure('traces2')
      plt.xlim(0,200)
      plt.plot(x1all[int(starttime-20):,0], 'k' , linewidth = 6, label = 'soma')
      plt.plot(x1all[int(starttime-20):,apicnum], 'xkcd:light blue',  linewidth = 6, label = 'apical')
      pltaxis = True
      
      if pltaxis:
        plt.grid(b=True, which='major')
        plt.minorticks_on()
        plt.grid(b=True, which='minor')
        plt.ylabel('membrane potential (mV)')
        plt.xlabel('time (ms)')
      else:
        plt.axis('off')
    
      if asBatch:
         plt.savefig(dirs1 + '/traces2' +  '.png', transparent  = True)
      else:
         plt.savefig('traces2' +  '.png', transparent  = True)  
