#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:18:01 2021

@author: adam
"""

from netpyne import specs
import numpy as np
#import math
import random
#import sys





try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from t42_cfg import cfg  # if no simConfig in parent module, import directly from tut8_cfg module


netParams = specs.NetParams()  
    

np.random.seed(cfg.seedval)
random.seed(cfg.seedval)




somator=True

if cfg.pvbcpopsize>0:

    netParams.importCellParams(label='PVBC_rule', conds= {'cellType': 'PVBC', 'cellModel': 'PVBC'},
          	fileName='pvbc.hoc',cellName='cNACnoljp', somaAtOrigin=somator)
    
    netParams.popParams['PVBC_pop'] = {'cellType': 'PVBC', 
                                       'numCells': cfg.pvbcpopsize, 
                                       'cellModel': 'PVBC'}



if cfg.olmpopsize>0:
    
    netParams.importCellParams(label='OLM_rule', conds= {'cellType': 'OLM', 'cellModel': 'OLM'},
       	fileName = 'olm.hoc', cellName='INT_cAC_noljp', somaAtOrigin=somator)
        
              
    netParams.popParams['OLM_pop'] = {'cellType': 'OLM',
                                          'numCells': cfg.olmpopsize, 
                                          'cellModel': 'OLM'}       

 
if cfg.pyrpopsize>0:
    netParams.importCellParams(label='PYR_rule', conds= {'cellType': 'PYR', 'cellModel': 'PYR'},
          	fileName='pyr.hoc', cellName ='CA1_PC_cAC_sig', somaAtOrigin=somator)
    
    
    netParams.popParams['PYR_pop'] = {'cellType': 'PYR', 
                                   'numCells': cfg.pyrpopsize,  'cellModel': 'PYR'}


SCsecList = []
SCsomaDist = [100,350]
OLMsecList = []
OLMsomaDist = cfg.OLMsomaDist
PVBCsomaDist = cfg.PVBCsomaDist #50
PVBCsecList = []    
    
     
    
for secName, sec in netParams.cellParams['PYR_rule'].secs.items():
      if 'pt3d' in sec['geom']:    
         pt3d = sec['geom']['pt3d']
         midpoint = int(len(pt3d)/2)                  
         x,y,z = pt3d[midpoint][0:3]
         #print(x,y,z)
         distSec = np.linalg.norm(np.array([x,y,z]))
         #print(secName, distSec, sec['geom']['diam'])
         if secName[0:4] == 'apic':
             if distSec >= SCsomaDist[0] and distSec <= SCsomaDist[1] \
             and sec['geom']['diam'] < 2:
                SCsecList.append(secName)
                #print(secName, distSec, sec['geom']['diam'])
             if distSec > OLMsomaDist:
                OLMsecList.append(secName)
         if secName[0:4] == 'dend' or secName[0:4] == 'soma':
             if distSec < PVBCsomaDist:
                PVBCsecList.append(secName)          
                               



netParams.synMechParams['PC-OLM'] = {'mod': 'DetAMPANMDA', 
                                     'tau_d_AMPA': 1.7, 
                                          'tau_d_NMDA': 148.5,
                                          'Use': cfg.pc_olm_use,
                                          'Dep': cfg.olmdepfact,
                                          'Fac': cfg.olmfacfact, 
                                          'NMDA_ratio': 0.28}


netParams.synMechParams['PC-PVBC'] = {'mod': 'DetAMPANMDA', 
                                      'tau_d_AMPA': 4.12, 
                                          'tau_d_NMDA': 298.75,
                                          'Use':  0.32,
                                          'Dep': cfg.pvbcdep, 
                                          'Fac': cfg.pvbcfac, 
                                          'NMDA_ratio': 0.28}




 
netParams.synMechParams['PC-PC'] = {'mod': 'DetAMPANMDA', 'tau_d_AMPA': 3, 
                                          'tau_d_NMDA': 148.5,
                                          'Use': 0.5, 
                                          'Dep': 671,
                                          'Fac': 17,
                                          'NMDA_ratio': 1.22} 

netParams.synMechParams['PC-PCzero'] = {'mod': 'DetAMPANMDA', 'tau_d_AMPA': 3, 
                                          'tau_d_NMDA': 148.5,
                                          'Use': 0.5, 
                                          'Dep': 0,
                                          'Fac': 0,
                                          'NMDA_ratio': 1.22} 


netParams.synMechParams['OLM-PC'] = {'mod': 'DetGABAAB',
                                     'tau_d_GABAA': cfg.olm_pc_gaba_tau, 
                                          'Use': 0.3, 
                                          'Dep': cfg.olm2pcDep, 
                                          'Fac': cfg.olm2pcFac,
                                          }



netParams.synMechParams['PVBC-PC'] = {'mod': 'DetGABAAB',
                                      'tau_d_GABAA': 5.94*cfg.pv_pc_gaba_tau_fact, 
                                          'Use': 0.16, 
                                          'Dep': cfg.pvbc2pcDep, 'Fac': cfg.pvbc2pcFac}



netParams.synMechParams['PVBC-PVBC'] = {'mod': 'DetGABAAB', 'tau_d_GABAA': 2.67, 
                                          'Use': 0.26, 
                                          'Dep': 930, 
                                          'Fac': 1.6 
                                          }


                                          
netParams.np_pc_olm_hibound = cfg.pc_olm_hibound
netParams.np_pc_olm_lowbound = cfg.pc_olm_lowbound
netParams.np_pc_olm_wei = cfg.pc_olm_wei
netParams.pc_olm_conprob = cfg.pc_olm_conprob
netParams.pc_olm_synfact = cfg.pc_olm_synfact

netParams.pc_pc_synfact = cfg.pc_pc_synfact
netParams.pc_pc_conprob = cfg.pc_pc_conprob #0.35



netParams.np_pc_pv_wei = cfg.pc_pv_wei

netParams.pc_pv_conprob = cfg.pc_pv_conprob
netParams.pc_pv_synfact = cfg.pc_pv_synfact



netParams.np_olm_pc_wei = cfg.olm_pc_wei #* 6 #olm-pc

netParams.olm_pc_synfact = cfg.olm_pc_synfact
netParams.olm_pc_conprob = cfg.olm_pc_conprob

netParams.np_olm_pc_lobound = cfg.olm_pc_lobound
netParams.np_olm_pc_hibound = cfg.olm_pc_hibound


netParams.olmscalenum = cfg.olmscalenum

    
netParams.np_pv_pc_wei = cfg.pv_pc_wei # * 6 # pv-pc    
    
netParams.pv_pc_conprob = cfg.pv_pc_conprob
netParams.pv_pc_synfact = cfg.pv_pc_synfact

netParams.pvscalenum = cfg.pvscalenum
netParams.pcscalenum = cfg.pcscalenum

netParams.pvbc_pvbc_conprob = cfg.pvbc_pvbc_conprob # 0.35
netParams.pvbc_pvbc_synfact = cfg.pvbc_pvbc_synfact
  

if cfg.connectPCOLM: 
    netParams.connParams['PC-OLM'] = {
     	'preConds': {'pop': 'PYR_pop'}, 
    'postConds': {'pop': 'OLM_pop'},  #  PYR -> PYR random
    'synMech': 'PC-OLM',
    'synsPerConn': 
    'int(binomial(int(pcscalenum*5*pc_olm_synfact),pc_olm_conprob))',
     	'weight': 'uniform(np_pc_olm_lowbound,np_pc_olm_hibound)*np_pc_olm_wei',
     	'delay': 'uniform(0.5,2)', 
     	'sec': cfg.pc_olm_sec
     }				


    
    
    
    
if cfg.connectPCPVBC:
    netParams.connParams['PC-PVBC'] = {
 	'preConds': {'pop': 'PYR_pop'}, 
    'postConds': {'pop': 'PVBC_pop'}, 
    'synMech': 'PC-PVBC',
    'synsPerConn': 
        'int(binomial(int(pcscalenum*6*pc_pv_synfact),pc_pv_conprob))',
    'weight': 'uniform(0.3,0.7)*np_pc_pv_wei',
 	'sec': 'basal'
     }




if cfg.connectOLMPC and cfg.pyrpopsize>0:
    netParams.connParams['OLM-PC'] = {
 	'preConds': {'pop': 'OLM_pop'}, 
    'postConds': {'pop': 'PYR_pop'}, 
    'synMech': 'OLM-PC',
    'synsPerConn': 'int(binomial(int(olmscalenum*13*olm_pc_synfact),olm_pc_conprob))',
    'weight': 'uniform(np_olm_pc_lobound,np_olm_pc_hibound)*np_olm_pc_wei', 
 	'delay': 'uniform(0.5,1)',
    'sec': OLMsecList
     }			



if cfg.connectPVBCPC and cfg.pyrpopsize>0:
    netParams.connParams['PVBC-PC'] = {
 	'preConds': {'pop': 'PVBC_pop'}, 
    'postConds': {'pop': 'PYR_pop'}, 
    'synMech': 'PVBC-PC',
    'synsPerConn': 
    'int(binomial(int(pvscalenum*11*pv_pc_synfact),pv_pc_conprob))',
 	'weight': 'uniform(1,1.2)*np_pv_pc_wei',	
 	'delay': 'uniform(0.5,2)', 				
    'sec': PVBCsecList,
     }			
    


if cfg.connectPVBC2PVBC:
    netParams.connParams['PVBC-PVBC'] = {
    'preConds': {'pop': 'PVBC_pop'}, 
    'postConds': {'pop': 'PVBC_pop'},    
    'synMech': 'PVBC-PVBC',
    'synsPerConn': 'int(binomial(int(pvscalenum*5*pvbc_pvbc_synfact),pvbc_pvbc_conprob))',
    'weight': 'uniform(4.2,4.8)',
 	'delay': 'uniform(0.5,1)',
 	'sec': 'basal'
     }				



if cfg.connectPC2PC:    
   netParams.connParams['PC-PC'] = {
 	'preConds': {'pop': 'PYR_pop'}, 
   'postConds': {'pop': 'PYR_pop'}, 
  'synMech': 'PC-PC',
  'synsPerConn': 
  'int(binomial(int(pcscalenum*3*pc_pc_synfact),pc_pc_conprob))',
    'weight': 'uniform(0.5,0.7)',
   'delay': 'uniform(0.5,1)',	
  'sec': SCsecList,
   }			
   
       
      

if cfg.doAlvstim:
    
    scanz_starttime = cfg.starttime
    netParams.stimSourceParams['alv_bkg'] = {'type': 'NetStim', 
                                            'interval': cfg.scanz_fval, 
                                            'number': cfg.scanz_stimtotnum, 
                                                'start': scanz_starttime}

    if cfg.pvbcpopsize>0:

      
       netParams.stimTargetParams['PVBC_alv'] = {'source': 'alv_bkg', 'synMech': 'PC-PVBC',
                                        'conds': {'pop': 'PVBC_pop'},                  
                                        'weight': 'uniform(0.35,0.63)',
                                        'delay': 1, 
                                        'sec': 'basal', 
                                        'loc': 0.5, 
                                        'synsPerConn': 6*int(cfg.alv_pv_synfact/4)}
       
       netParams.stimTargetParams['PVBC_alv2'] = {'source': 'alv_bkg', 'synMech': 'PC-PVBC',
                                        'conds': {'pop': 'PVBC_pop'},                  
                                        'weight': 'uniform(0.35,0.63)',
                                        'delay': 1, 
                                        'sec': 'basal', 
                                        'loc': 0.5, 
                                        'synsPerConn': 6*int(cfg.alv_pv_synfact/4)}
           
       netParams.stimTargetParams['PVBC_alv3'] = {'source': 'alv_bkg', 'synMech': 'PC-PVBC',
                                        'conds': {'pop': 'PVBC_pop'},                  
                                        'weight': 'uniform(0.35,0.63)',
                                        'delay': 1, 
                                        'sec': 'basal', 
                                        'loc': 0.5, 
                                        'synsPerConn': 6*int(cfg.alv_pv_synfact/4)}
       
       netParams.stimTargetParams['PVBC_alv4'] = {'source': 'alv_bkg', 'synMech': 'PC-PVBC',
                                        'conds': {'pop': 'PVBC_pop'},                  
                                        'weight': 'uniform(0.35,0.63)',
                                        'delay': 1, 
                                        'sec': 'basal', 
                                        'loc': 0.5, 
                                        'synsPerConn': 6*int(cfg.alv_pv_synfact/4)  + 6*int(cfg.alv_pv_synfact % 4)}
                  
           
           
       

    if cfg.olmpopsize>0:
  
       netParams.stimTargetParams['OLM_alv'] = {'source': 'alv_bkg', 'synMech': 'PC-OLM',
                                                 'conds': {'pop': 'OLM_pop'},							   
                                                 'weight': 'uniform(0.275,0.325)',
                                                 'delay': 1,
                                                 'sec': 'basal', 
                                                 'loc': 0.5, 
                                                 'synsPerConn': 5*int(cfg.alv_olm_synfact/3)}
           
       netParams.stimTargetParams['OLM_alv2'] = {'source': 'alv_bkg', 'synMech': 'PC-OLM',
                                                 'conds': {'pop': 'OLM_pop'},							   
                                                 'weight': 'uniform(0.275,0.325)',
                                                 'delay': 1,
                                                 'sec': 'basal', 
                                                 'loc': 0.5, 
                                                 'synsPerConn': 5*int(cfg.alv_olm_synfact/3)}
       
       netParams.stimTargetParams['OLM_alv3'] = {'source': 'alv_bkg', 'synMech': 'PC-OLM',
                                                 'conds': {'pop': 'OLM_pop'},							   
                                                 'weight': 'uniform(0.275,0.325)',
                                                 'delay': 1,
                                                 'sec': 'basal', 
                                                 'loc': 0.5, 
                                                 'synsPerConn': 5*int(cfg.alv_olm_synfact/3)
                                                  + 5*int(cfg.alv_olm_synfact % 3)
                                                 }

if cfg.doAlvPYRclamp:
        
    doIclampsoma = True
    doIclampdend = True
    
    
    
    if doIclampsoma:
     
        netParams.stimSourceParams['I1'] = {'type': 'IClamp', 'del': 0, 
                                        'dur': cfg.duration, 'amp': cfg.alvsomaclampamp}
        
        netParams.stimTargetParams['I1targ'] = {'source': 'I1', 
                                           'conds': {'cellType': cfg.alvclamptarg, 
                                                     'cellModel': cfg.alvclamptarg}, 
      									   'sec': 'soma_0', 'loc': 0.5}
    
    if doIclampdend:
        
        dendclampamp = 0.01
        dendclapsec = ['apic_10', 'apic_20', 'apic_30', 'apic_40', 'apic_50']
          
        netParams.stimSourceParams['I2'] = {'type': 'IClamp', 'del': 0, 
                                        'dur': cfg.duration, 'amp': dendclampamp}
        
        for x in dendclapsec:
            netParams.stimTargetParams['I2targ_' + x] = {'source': 'I2', 
                                               'conds': {'cellType': cfg.alvclamptarg, 
                                                         'cellModel': cfg.alvclamptarg}, 
          									   'sec': x, 'loc': 0.5}