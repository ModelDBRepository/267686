#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:41:05 2021

@author: adam
"""

from netpyne import specs

## Population parameters
cfg = specs.SimConfig()					# object of class SimConfig to store simulation configuration

cfg.duration = 600
cfg.starttime = 300
cfg.seedval = 42

cfg.pyrpopsize = 1
cfg.pcscalenum = 1 
cfg.pvbcpopsize = 1
cfg.pvscalenum = 1
cfg.olmpopsize = 3
cfg.olmscalenum = 1 

cfg.connectPC2PC = False # False
cfg.connectPVBC2PVBC = False # False
cfg.connectPVBCPC = True # False 
cfg.connectOLMPC = True # False
cfg.connectPCPVBC = False # False
cfg.connectPCOLM = False # False

# =============================================================================
# cfg.connectPC2PC =  False
# cfg.connectPVBC2PVBC =  False
# cfg.connectPVBCPC = False 
# cfg.connectOLMPC =  False
# cfg.connectPCPVBC =  False
# cfg.connectPCOLM =  False
# =============================================================================

cfg.PVBCsomaDist = 50
cfg.OLMsomaDist = 250


cfg.pc_olm_use  = 0.07 
cfg.olmdepfact = 38
cfg.olmfacfact = 470
cfg.pvbcdep  = 110
cfg.pvbcfac = 0 
cfg.olm_pc_gaba_tau = 18
cfg.olm2pcDep = 1770
cfg.olm2pcFac = 6
cfg.pv_pc_gaba_tau_fact = 1
cfg.pvbc2pcDep = 965
cfg.pvbc2pcFac = 8.6
cfg.pc_olm_sec = 'basal'

cfg.pc_olm_conprob = 1
cfg.pc_olm_synfact = 1
cfg.pc_pc_conprob = 1
cfg.pc_pc_synfact = 1
cfg.pc_pv_conprob = 1
cfg.pc_pv_synfact  = 1
cfg.olm_pc_conprob = 1
cfg.olm_pc_synfact  = 1
cfg.pv_pc_conprob = 1
cfg.pv_pc_synfact = 1
cfg.pvbc_pvbc_conprob = 1
cfg.pvbc_pvbc_synfact = 1

cfg.pc_olm_hibound = 0.7 
cfg.pc_olm_lowbound = 0.5 
cfg.pc_olm_wei = 0.5

cfg.pc_pv_wei = 1

cfg.olm_pc_wei = 0.25
cfg.olm_pc_lobound = 4.1
cfg.olm_pc_hibound = 5.5

cfg.pv_pc_wei = 1

#############################

    
cfg.doAlvstim = True
cfg.alv_olm_synfact = 138
cfg.alv_pv_synfact = 80

cfg.doAlvPYRclamp = True
cfg.alvsomaclampamp = 0.3 #0.3
cfg.alvclamptarg = 'PYR'

cfg.scanz_stimtotnum = 3
cfg.scanz_fval = 10



#############################

cfg.cvode_active = True
cfg.dt = 0.025
cfg.hParams = {'v_init': -65, 'celsius': 34} #, 'clamp_resist': 0.001}
cfg.verbose = False

cfg.distributeSynsUniformly = False
cfg.connRandomSecFromList = True

cfg.recordStep = 1 			# Step size in ms to save data (eg. V traces, LFP, etc)
cfg.savePickle = False 		# Save params, network and sim output to pickle file
cfg.saveFileStep = 1000 # step size in ms to save data to disk



cfg.analysis['plotRaster'] = {'include': ['artif_pyr', 'PYR_pop', 'PVBC_pop', 'OLM_pop'],
                                    'marker': 'o',
                                    'saveFig': True, 
                                    'showFig': False, 
                                    'markerSize': 6}


cfg.recordTraces['V_soma'] = {'sec':'soma_0','loc':0.5,'var':'v'}

 
    
cfg.analysis['plotTraces'] = {'include': [4],                                       
                                        'saveFig': False,
                                        'showFig': False,                                 
                                        } 

    
recordapictraces = True
if recordapictraces:
  for x1 in range(10):
    s1 = 'dend_' + str(x1*2)
    cfg.recordTraces['V_' + s1] = {'sec':s1,'loc':0.5,'var':'v'}
  for x1 in range(20):
    s1 = 'apic_' + str(x1*3)
    cfg.recordTraces['V_' + s1] = {'sec':s1,'loc':0.5,'var':'v'}



cfg.saveJson = True
cfg.seeds = {'conn': cfg.seedval + 7515, 'stim': cfg.seedval + 84331, 'loc': cfg.seedval + 943}