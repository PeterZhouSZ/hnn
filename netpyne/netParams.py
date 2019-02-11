# netParams.py - High-level specifications for network model using NetPyNE

from netpyne import specs

try:
  from __main__ import cfg  # import SimConfig object with params from parent module
except:
  from cfg import cfg  # if no simConfig in parent module, import directly from cfg module

import numpy as np


# ----------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
# ----------------------------------------------------------------------------

netParams = specs.NetParams()  # object of class NetParams to store the network parameters

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.sizeX = cfg.N_pyr_x * cfg.gridSpacing # x-dimension (horizontal length) size in um
netParams.sizeY = cfg.sizeY # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = cfg.N_pyr_y * cfg.gridSpacing # z-dimension (horizontal depth) size in um
netParams.shape = 'cuboid' 

# ----------------------------------------------------------------------------
# Cell parameters
# ----------------------------------------------------------------------------
from cellParams import cellParams  # defined in separate module for clarity
netParams.cellParams = cellParams


# ----------------------------------------------------------------------------
# Population parameters
# ----------------------------------------------------------------------------
layersE = {'L5': [0.5*cfg.sizeY, 0.5*cfg.sizeY], 'L2': [0.5*cfg.sizeY, 0.5*cfg.sizeY]}
layersI = {'L5': [0.6*cfg.sizeY, 0.6*cfg.sizeY], 'L2': [1.4*cfg.sizeY, 1.4*cfg.sizeY]}

netParams.popParams['L2Pyr'] = {'cellType': 'L2Pyr',    'cellModel': 'HH_reduced', 'yRange': layersE['L2'], 'gridSpacing': cfg.gridSpacing} 
netParams.popParams['L2Basket'] = {'cellType': 'L2Basket', 'cellModel': 'HH_simple', 'yRange': layersI['L2'], 'gridSpacing': cfg.gridSpacing} 
netParams.popParams['L5Pyr'] = {'cellType': 'L5Pyr',    'cellModel': 'HH_reduced', 'yRange': layersE['L5'], 'gridSpacing': cfg.gridSpacing} 
netParams.popParams['L5Basket'] = {'cellType': 'L5Basket', 'cellModel': 'HH_simple', 'yRange': layersI['L5'], 'gridSpacing': cfg.gridSpacing} 


#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------

netParams.synMechParams['L2Pyr_AMPA'] = {'mod':'Exp2Syn', 'tau1': cfg.L2Pyr_ampa_tau1, 'tau2': cfg.L2Pyr_ampa_tau2, 'e': cfg.L2Pyr_ampa_e}
netParams.synMechParams['L2Pyr_NMDA'] = {'mod': 'Exp2Syn', 'tau1': cfg.L2Pyr_nmda_tau1, 'tau2': cfg.L2Pyr_nmda_tau2, 'e': cfg.L2Pyr_nmda_e}
netParams.synMechParams['L2Pyr_GABAA'] = {'mod':'Exp2Syn', 'tau1': cfg.L2Pyr_gabaa_tau1, 'tau2': cfg.L2Pyr_gabaa_tau2, 'e': cfg.L2Pyr_gabaa_e}
netParams.synMechParams['L2Pyr_GABAB'] = {'mod':'Exp2Syn', 'tau1': cfg.L2Pyr_gabab_tau1, 'tau2': cfg.L2Pyr_gabab_tau2, 'e': cfg.L2Pyr_gabab_e}

netParams.synMechParams['L5Pyr_AMPA'] = {'mod':'Exp2Syn', 'tau1': cfg.L5Pyr_ampa_tau1, 'tau2': cfg.L5Pyr_ampa_tau2, 'e': cfg.L5Pyr_ampa_e}
netParams.synMechParams['L5Pyr_NMDA'] = {'mod': 'Exp2Syn', 'tau1': cfg.L5Pyr_nmda_tau1, 'tau2': cfg.L5Pyr_nmda_tau2, 'e': cfg.L5Pyr_nmda_e}
netParams.synMechParams['L5Pyr_GABAA'] = {'mod':'Exp2Syn', 'tau1': cfg.L5Pyr_gabaa_tau1, 'tau2': cfg.L5Pyr_gabaa_tau2, 'e': cfg.L5Pyr_gabaa_e}
netParams.synMechParams['L5Pyr_GABAB'] = {'mod':'Exp2Syn', 'tau1': cfg.L5Pyr_gabab_tau1, 'tau2': cfg.L5Pyr_gabab_tau2, 'e': cfg.L5Pyr_gabab_e}

netParams.synMechParams['AMPA'] = {'mod':'Exp2Syn', 'tau1': 0.5, 'tau2': 5.0, 'e': 0}
netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 1, 'tau2': 20, 'e': 0}
netParams.synMechParams['GABAA'] = {'mod':'Exp2Syn', 'tau1': 0.5, 'tau2': 5, 'e': -80}
netParams.synMechParams['GABAB'] = {'mod':'Exp2Syn', 'tau1': 1, 'tau2': 20, 'e': -80}


#------------------------------------------------------------------------------
# Local connectivity parameters 
#------------------------------------------------------------------------------

# Weight and delay distance-dependent functions (as strings) to use in conn rules
weightDistFunc = '{A_weight} * exp(-(dist_2D**2) / ({lamtha}**2))'
delayDistFunc = '{A_weight} / exp(-(dist_2D**2) / ({lamtha}**2))'

# L2 Pyr -> L2 Pyr
synParamsList = [{'synMech': 'L2Pyr_AMPA',
            'A_weight': cfg.gbar_L2Pyr_L2Pyr_ampa,
            'A_delay': 1.,
            'lamtha': 3.},

            {'synMech': 'L2Pyr_NMDA',
            'A_weight': cfg.gbar_L2Pyr_L2Pyr_nmda,
            'A_delay': 1.,
            'lamtha': 3.}]

for synParams in synParamsList:
    netParams.connParams['L2Pyr->L2Pyr'] = { 
        'preConds': {'pop': 'L2Pyr'}, 
        'postConds': {'pop': 'L2Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': ['basal_2', 'basal_3','apical_oblique', ]}
                

# L2 Basket -> L2 Pyr
synParamsList = [{'synMech': 'L2Pyr_GABAA',
            'A_weight': cfg.gbar_L2Basket_L2Pyr_gabaa,
            'A_delay': 1.,
            'lamtha': 50.},

            {'synMech': 'L2Pyr_GABAB',
            'A_weight': cfg.gbar_L2Basket_L2Pyr_gabab,
            'A_delay': 1.,
            'lamtha': 50.}]

for synParams in synParamsList:
    netParams.connParams['L2Basket->L2Pyr'] = { 
        'preConds': {'pop': 'L2Basket'}, 
        'postConds': {'pop': 'L2Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 1,
        'sec': ['soma']}


# L2 Pyr -> L2 Basket 
synParams = {'synMech': 'AMPA',
            'A_weight': cfg.gbar_L2Pyr_L2Basket,
            'A_delay': 1.,
            'lamtha': 3.}

netParams.connParams['L2Pyr->L2Basket'] = { 
    'preConds': {'pop': 'L2Pyr'}, 
    'postConds': {'pop': 'L2Basket'},
    'synMech': synParams['synMech'],
    'weight': weightDistFunc.format(**synParams),
    'delay': delayDistFunc.format(**synParams),
    'synsPerConn': 1,
    'sec': ['soma']}


# L2 Basket -> L2 Basket 
synParams = {'synMech': 'GABAA',
            'A_weight': cfg.gbar_L2Basket_L2Basket,
            'A_delay': 1.,
            'lamtha': 20.}

netParams.connParams['L2Basket->L2Basket'] = { 
    'preConds': {'pop': 'L2Basket'}, 
    'postConds': {'pop': 'L2Basket'},
    'synMech': synParams['synMech'],
    'weight': weightDistFunc.format(**synParams),
    'delay': delayDistFunc.format(**synParams),
    'synsPerConn': 1,
    'sec': ['soma']}


# L5 Pyr -> L5 Pyr
synParamsList = [{'synMech': 'L5Pyr_AMPA',
            'A_weight': cfg.gbar_L5Pyr_L5Pyr_ampa,
            'A_delay': 1.,
            'lamtha': 3.},

            {'synMech': 'L5Pyr_NMDA',
            'A_weight': cfg.gbar_L5Pyr_L5Pyr_nmda,
            'A_delay': 1.,
            'lamtha': 3.}]

for synParams in synParamsList:
    netParams.connParams['L5Pyr->L5Pyr'] = { 
        'preConds': {'pop': 'L5Pyr'}, 
        'postConds': {'pop': 'L5Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': ['basal_2', 'basal_3', 'apical_oblique']}
              

# L5 Basket -> L5 Pyr
synParamsList = [{'synMech': 'L5Pyr_GABAA',
            'A_weight': cfg.gbar_L5Basket_L5Pyr_gabaa,
            'A_delay': 1.,
            'lamtha': 70.},

            {'synMech': 'L5Pyr_GABAB',
            'A_weight': cfg.gbar_L5Basket_L5Pyr_gabab,
            'A_delay': 1.,
            'lamtha': 70.}]

for synParams in synParamsList:
    netParams.connParams['L5Basket->L5Pyr'] = { 
        'preConds': {'pop': 'L5Basket'}, 
        'postConds': {'pop': 'L5Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 1,
        'sec': ['soma']}


# L2 Pyr -> L5 Pyr
synParams = {'synMech': 'L5Pyr_AMPA',
            'A_weight': cfg.gbar_L2Pyr_L5Pyr,
            'A_delay': 1.,
            'lamtha': 3.}

netParams.connParams['L2Pyr->L5Pyr'] = { 
    'preConds': {'pop': 'L2Pyr'}, 
    'postConds': {'pop': 'L5Pyr'},
    'synMech': synParams['synMech'],
    'weight': weightDistFunc.format(**synParams),
    'delay': delayDistFunc.format(**synParams),
    'synsPerConn': 4,
    'sec': ['basal_2', 'basal_3', 'apical_tuft', 'apical_oblique']}
              

# L2 Basket -> L5 Pyr
synParams = {'synMech': 'L5Pyr_GABAA',
            'A_weight': cfg.gbar_L2Basket_L5Pyr,
            'A_delay': 1.,
            'lamtha': 50.}

netParams.connParams['L2Basket->L5Pyr'] = { 
    'preConds': {'pop': 'L2Basket'}, 
    'postConds': {'pop': 'L5Pyr'},
    'synMech': synParams['synMech'],
    'weight': weightDistFunc.format(**synParams),
    'delay': delayDistFunc.format(**synParams),
    'synsPerConn': 4,
    'sec': ['apical_tuft']}
       

# L5 Pyr -> L5 Basket 
synParams = {'synMech': 'AMPA',
            'A_weight': cfg.gbar_L5Pyr_L5Basket,
            'A_delay': 1.,
            'lamtha': 3.}

netParams.connParams['L5Pyr->L5Basket'] = { 
    'preConds': {'pop': 'L5Pyr'}, 
    'postConds': {'pop': 'L5Basket'},
    'synMech': synParams['synMech'],
    'weight': weightDistFunc.format(**synParams),
    'delay': delayDistFunc.format(**synParams),
    'synsPerConn': 1,
    'sec': ['soma']}


# L2 Pyr -> L5 Basket 
synParams = {'synMech': 'AMPA',
            'A_weight': cfg.gbar_L2Pyr_L5Basket,
            'A_delay': 1.,
            'lamtha': 3.}

netParams.connParams['L2Pyr->L5Basket'] = { 
    'preConds': {'pop': 'L2Pyr'}, 
    'postConds': {'pop': 'L5Basket'},
    'synMech': synParams['synMech'],
    'weight': weightDistFunc.format(**synParams),
    'delay': delayDistFunc.format(**synParams),
    'synsPerConn': 1,
    'sec': ['soma']}


# L5 Basket -> L5 Basket 
synParams = {'synMech': 'GABAA',
            'A_weight': cfg.gbar_L5Basket_L5Basket,
            'A_delay': 1.,
            'lamtha': 20.}

netParams.connParams['L5Basket->L5Basket'] = { 
    'preConds': {'pop': 'L5Basket'}, 
    'postConds': {'pop': 'L5Basket'},
    'synMech': synParams['synMech'],
    'weight': weightDistFunc.format(**synParams),
    'delay': delayDistFunc.format(**synParams),
    'synsPerConn': 1,
    'sec': ['soma']}


#------------------------------------------------------------------------------
# Rhythmic proximal and distal inputs parameters 
#------------------------------------------------------------------------------

''' Note: built-in ad-hoc rules from original HNN implementation -- SDB: should be part of params file??

# if stdev is zero, increase synaptic weights 5 fold to make
# single input equivalent to 5 simultaneous input to prevent spiking    <<---- SN: WHAT IS THIS RULE!?!?!?
if not d['stdev'] and d['distribution'] != 'uniform':
        for key in d.keys():
        if key.endswith('Pyramidal'):
                d[key] = (d[key][0] * 5., d[key][1])
        elif key.endswith('Basket'):
                d[key] = (d[key][0] * 5., d[key][1])

# if L5 delay is -1, use same delays as L2 unless L2 delay is 0.1 in which case use 1. <<---- SN: WHAT IS THIS RULE!?!?!?
if d['L5Pyr_ampa'][1] == -1:                                  
        for key in d.keys():
        if key.startswith('L5'):
                if d['L2Pyr'][1] != 0.1:
                d[key] = (d[key][0], d['L2Pyr'][1])
                else:
                d[key] = (d[key][0], 1.)
'''

# Location of external inputs
xrange = np.arange(cfg.N_pyr_x)
extLocX = xrange[int((len(xrange) - 1) // 2)]
zrange = np.arange(cfg.N_pyr_y)
extLocZ = xrange[int((len(zrange) - 1) // 2)]
extLocY = 1307.4  # positive depth of L5 relative to L2; doesn't affect weight/delay calculations


# External Rhythmic proximal inputs (population of 1 VecStim)
netParams.popParams['extRhythmicProximal'] = {
    'cellModel': 'VecStim',
    'numCells': 1,
    'xRange': [extLocX, extLocX],
    'yRange': [extLocY, extLocY],
    'zRange': [extLocZ, extLocZ],
    'seed': int(cfg.prng_seedcore_input_prox),
    'spikePattern': {
            'type': 'rhythmic',
            'start': cfg.t0_input_prox,
            'startStd': cfg.t0_input_stdev_prox,
            'stop': cfg.tstop_input_prox,
            'freq': cfg.f_input_prox,
            'freqStd': cfg.f_stdev_prox,
            'eventsPerCycle': cfg.events_per_cycle_prox,
            'distribution': cfg.distribution_prox,
            'repeats': cfg.repeats_prox}}


# External Rhythmic distal inputs (population of 1 VecStim)
netParams.popParams['extRhythmicDistal'] = {
    'cellModel': 'VecStim',
    'numCells': 1,
    'xRange': [extLocX, extLocX],
    'yRange': [extLocY, extLocY],
    'zRange': [extLocZ, extLocZ],
    'seed': int(cfg.prng_seedcore_input_dist),
    'spikePattern': {
            'type': 'rhythmic',
            'start': cfg.t0_input_dist,
            'startStd': cfg.t0_input_stdev_dist,
            'stop': cfg.tstop_input_dist,
            'freq': cfg.f_input_dist,
            'freqStd': cfg.f_stdev_dist,
            'eventsPerCycle': cfg.events_per_cycle_dist,
            'distribution': cfg.distribution_dist,
            'repeats': cfg.repeats_dist}}


# Rhytmic proximal -> L2 Pyr
synParamsList = [{'synMech': 'L2Pyr_AMPA',
            'A_weight': cfg.input_prox_A_weight_L2Pyr_ampa,
            'A_delay': cfg.input_prox_A_delay_L2,
            'lamtha': 100.},

            {'synMech': 'L2Pyr_NMDA',
            'A_weight': cfg.input_prox_A_weight_L2Pyr_nmda,
            'A_delay': cfg.input_prox_A_delay_L2,
            'lamtha': 100.}]

for synParams in synParamsList:
    netParams.connParams['extRhythmicProx->L2Pyr'] = { 
        'preConds': {'pop': 'extRhythmicProximal'}, 
        'postConds': {'pop': 'L2Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': ['basal_2', 'basal_3','apical_oblique']}


# Rhythmic distal -> L2 Pyr
synParamsList = [{'synMech': 'L2Pyr_AMPA',
            'A_weight': cfg.input_dist_A_weight_L2Pyr_ampa,
            'A_delay': cfg.input_dist_A_delay_L2,
            'lamtha': 100.},

            {'synMech': 'L2Pyr_NMDA',
            'A_weight': cfg.input_dist_A_weight_L2Pyr_nmda,
            'A_delay': cfg.input_dist_A_delay_L2,
            'lamtha': 100.}]

for synParams in synParamsList:
    netParams.connParams['extRhythmicDistal->L2Pyr'] = { 
        'preConds': {'pop': 'extRhythmicDistal'}, 
        'postConds': {'pop': 'L2Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': ['apical_tuft']}


# Rhythmic proximal -> L5 Pyr
synParamsList = [{'synMech': 'L5Pyr_AMPA',
            'A_weight': cfg.input_prox_A_weight_L5Pyr_ampa,
            'A_delay': cfg.input_prox_A_delay_L5,
            'lamtha': 100.},

            {'synMech': 'L5Pyr_NMDA',
            'A_weight': cfg.input_prox_A_weight_L5Pyr_nmda,
            'A_delay': cfg.input_prox_A_delay_L5,
            'lamtha': 100.}]

for synParams in synParamsList:
    netParams.connParams['extRhythmicProx->L5Pyr'] = { 
        'preConds': {'pop': 'extRhythmicProximal'}, 
        'postConds': {'pop': 'L5Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': ['basal_2', 'basal_3','apical_oblique']}


# Rhythmic distal -> L5 Pyr
synParamsList = [{'synMech': 'L5Pyr_AMPA',
            'A_weight': cfg.input_dist_A_weight_L5Pyr_ampa,
            'A_delay': cfg.input_dist_A_delay_L5,
            'lamtha': 100.},

            {'synMech': 'L5Pyr_NMDA',
            'A_weight': cfg.input_dist_A_weight_L5Pyr_nmda,
            'A_delay': cfg.input_dist_A_delay_L5,
            'lamtha': 100.}]

for synParams in synParamsList:
    netParams.connParams['extRhythmicDistal->L5Pyr'] = { 
        'preConds': {'pop': 'extRhythmicDistal'}, 
        'postConds': {'pop': 'L5Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': ['apical_tuft']}


# Rhytmic proximal -> L2 Basket
synParamsList = [{'synMech': 'AMPA',
            'A_weight': cfg.input_prox_A_weight_L2Basket_ampa,
            'A_delay': cfg.input_prox_A_delay_L2,
            'lamtha': 100.},

            {'synMech': 'NMDA',
            'A_weight': cfg.input_prox_A_weight_L2Basket_nmda,
            'A_delay': cfg.input_prox_A_delay_L2,
            'lamtha': 100.}]

for synParams in synParamsList:
    netParams.connParams['extRhythmicProx->L2Basket'] = { 
        'preConds': {'pop': 'extRhythmicProximal'}, 
        'postConds': {'pop': 'L2Basket'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': 'soma'}


# Rhytmic proximal -> L5 Basket
synParamsList = [{'synMech': 'AMPA',
            'A_weight': cfg.input_prox_A_weight_L5Basket_ampa,
            'A_delay': cfg.input_prox_A_delay_L5,
            'lamtha': 100.},

            {'synMech': 'NMDA',
            'A_weight': cfg.input_prox_A_weight_L5Basket_nmda,
            'A_delay': cfg.input_prox_A_delay_L5,
            'lamtha': 100.}]

for synParams in synParamsList:
    netParams.connParams['extRhythmicProx->L5Basket'] = { 
        'preConds': {'pop': 'extRhythmicProximal'}, 
        'postConds': {'pop': 'L5Basket'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': 'soma'}


#------------------------------------------------------------------------------
# Evoked proximal and distal inputs parameters 
#------------------------------------------------------------------------------

# Evoked proximal inputs (population of 1 VecStim)
nprox = len([k for k in cfg.__dict__ if k.startswith('t_evprox')])
ndist = len([k for k in cfg.__dict__ if k.startswith('t_evdist')])

for iprox in range(nprox):
    skey = 'evprox_' + str(i+1)
    netParams.popParams['evokedProximal'] = {
        'cellModel': 'VecStim',
        'numCells': 1,
        'xRange': [extLocX, extLocX],
        'yRange': [extLocY, extLocY],
        'zRange': [extLocZ, extLocZ],
        'seed': int(getattr(cfg, 'prng_seedcore_' + skey)),
        'spikePattern': {
                'type': 'evoked',
                'start': getattr(cfg, 't_' + skey),
                'startStd': getattr(cfg, 'sigma_t_' + skey),
                'numspikes': getattr(cfg, 'numspikes_' + skey)
                'sync': getattr(cfg, 'sync_evinput')}



# Evoked distal inputs (population of 1 VecStim)
netParams.popParams['evokedDistal'] = {
        'cellModel': 'VecStim',
        'numCells': 1,
        'xRange': [extLocX, extLocX],
        'yRange': [extLocY, extLocY],
        'zRange': [extLocZ, extLocZ],
        'seed': int(cfg.prng_seedcore_input_dist),
        'spikePattern': {
                'type': 'evoked',
                'start': cfg.t0_input_dist,
                'startStd': cfg.t0_input_stdev_dist,
                'stop': cfg.tstop_input_dist,
                'freq': cfg.f_input_dist,
                'freqStd': cfg.f_stdev_dist,
                'eventsPerCycle': cfg.events_per_cycle_dist,
                'distribution': cfg.distribution_dist,
                'repeats': cfg.repeats_dist}}

'''

        if type.startswith(('evprox', 'evdist')):
            if self.celltype in p_ext.keys():
                gid_ev = gid + gid_dict[type][0]

                # separate dictionaries for ampa and nmda evoked inputs
                nc_dict_ampa = {
                    'pos_src': pos_dict[type][gid],
                    'A_weight': p_ext[self.celltype][0], # index 0 for ampa weight
                    'A_delay': p_ext[self.celltype][2], # index 2 for delay
                    'lamtha': p_ext['lamtha_space'],
                    'threshold': p_ext['threshold'],
                    'type_src': type
                }

                nc_dict_nmda = {
                    'pos_src': pos_dict[type][gid],
                    'A_weight': p_ext[self.celltype][1], # index 1 for nmda weight
                    'A_delay': p_ext[self.celltype][2], # index 2 for delay
                    'lamtha': p_ext['lamtha_space'],
                    'threshold': p_ext['threshold'],
                    'type_src': type
                }

                if p_ext['loc'] is 'proximal':
                    self.ncfrom_ev.append(self.parconnect_from_src(gid_ev, nc_dict_ampa, self.basal2_ampa))
                    self.ncfrom_ev.append(self.parconnect_from_src(gid_ev, nc_dict_ampa, self.basal3_ampa))
                    self.ncfrom_ev.append(self.parconnect_from_src(gid_ev, nc_dict_ampa, self.apicaloblique_ampa))

                    # NEW: note that default/original is 0 nmda weight for these proximal dends
                    self.ncfrom_ev.append(self.parconnect_from_src(gid_ev, nc_dict_nmda, self.basal2_nmda))
                    self.ncfrom_ev.append(self.parconnect_from_src(gid_ev, nc_dict_nmda, self.basal3_nmda))
                    self.ncfrom_ev.append(self.parconnect_from_src(gid_ev, nc_dict_nmda, self.apicaloblique_nmda))

                elif p_ext['loc'] is 'distal':
                    self.ncfrom_ev.append(self.parconnect_from_src(gid_ev, nc_dict_ampa, self.apicaltuft_ampa))
                    self.ncfrom_ev.append(self.parconnect_from_src(gid_ev, nc_dict_nmda, self.apicaltuft_nmda))


def checkevokedsynkeys (p, nprox, ndist):
  # make sure ampa,nmda gbar values are in the param dict for evoked inputs(for backwards compatibility)
  lctprox = ['L2Pyr','L5Pyr','L2Basket','L5Basket'] # evoked distal target cell types
  lctdist = ['L2Pyr','L5Pyr','L2Basket'] # evoked proximal target cell types
  lsy = ['ampa','nmda'] # synapse types used in evoked inputs
  for nev,pref,lct in zip([nprox,ndist],['evprox_','evdist_'],[lctprox,lctdist]):
    for i in range(nev):
      skey = pref + str(i+1)
      for sy in lsy:
        for ct in lct:
          k = 'gbar_'+skey+'_'+ct+'_'+sy
          # if the synapse-specific gbar not present, use the existing weight for both ampa,nmda
          if k not in p: 
            p[k] = p['gbar_'+skey+'_'+ct]

'''

   # Create proximal evoked response parameters
    # f_input needs to be defined as 0
    for i in range(nprox):
      skey = 'evprox_' + str(i+1)
      p_unique['evprox' + str(i+1)] = {
          't0': p['t_' + skey],
          'L2_pyramidal':(p['gbar_'+skey+'_L2Pyr_ampa'],p['gbar_'+skey+'_L2Pyr_nmda'],0.1,p['sigma_t_'+skey]),
          'L2_basket':(p['gbar_'+skey+'_L2Basket_ampa'],p['gbar_'+skey+'_L2Basket_nmda'],0.1,p['sigma_t_'+skey]),
          'L5_pyramidal':(p['gbar_'+skey+'_L5Pyr_ampa'],p['gbar_'+skey+'_L5Pyr_nmda'],1.,p['sigma_t_'+skey]),
          'L5_basket':(p['gbar_'+skey+'_L5Basket_ampa'],p['gbar_'+skey+'_L5Basket_nmda'],1.,p['sigma_t_'+skey]),
          'prng_seedcore': int(p['prng_seedcore_' + skey]),
          'lamtha_space': 3.,
          'loc': 'proximal',
          'sync_evinput': p['sync_evinput'],
          'threshold': p['threshold'],
          'numspikes': p['numspikes_' + skey]
      }

    # Create distal evoked response parameters
    # f_input needs to be defined as 0
    for i in range(ndist):
      skey = 'evdist_' + str(i+1)
      p_unique['evdist' + str(i+1)] = {
          't0': p['t_' + skey],
          'L2_pyramidal':(p['gbar_'+skey+'_L2Pyr_ampa'],p['gbar_'+skey+'_L2Pyr_nmda'],0.1,p['sigma_t_'+skey]),
          'L5_pyramidal':(p['gbar_'+skey+'_L5Pyr_ampa'],p['gbar_'+skey+'_L5Pyr_nmda'],0.1,p['sigma_t_'+skey]),
          'L2_basket':(p['gbar_'+skey+'_L2Basket_ampa'],p['gbar_'+skey+'_L2Basket_nmda'],0.1,p['sigma_t_' + skey]),
          'prng_seedcore': int(p['prng_seedcore_' + skey]),
          'lamtha_space': 3.,
          'loc': 'distal',
          'sync_evinput': p['sync_evinput'],
          'threshold': p['threshold'],
          'numspikes': p['numspikes_' + skey]
      }


#------------------------------------------------------------------------------
# Poisson-distributed input sparameters 
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Gaussian-distributed inputs parameters 
#------------------------------------------------------------------------------