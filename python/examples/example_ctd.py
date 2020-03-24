# -*- coding: utf-8 -*-
"""
%%
% Platform:
    % Endurance Array:
	% CE01ISSM, CE01ISSP, CE02SHSM, CE02SHBP, CE02SHSP, CE04OSSM, CE04OSBP, CE06ISSM, CE06ISSP, CE07SHSM, CE07SHSP, CE09OSSM, CE09OSPM
    % CEGL386, CEGL384, CEGL383, CEGL382, CEGL381, CEGL327, CEGL326, CEGL320, CEGL319, CEGL312, CEGL311, CEGL247
	%
	% Pioneer Array:
	% CP01CNPM, CP01CNSM, CP02PMCI, CP02PMCO, CP02PMUI, CP02PMUO, CP03ISPM, CP03ISSM, CP04OSPM, CP04OSSM
	% CPGL335, CPGL336, CPGL339, CPGL340, CPGL374, CPGL375, CPGL376, CPGL379, CPGL380, CPGL387, CPGL388, CPGL389, CPGL514
%Node:
    % BUOY, NSIF, MFN, BEP, PROFILER, GLIDER
%Instrument Class:
    % ADCP, CTD, DOSTA, FDCHP, FLORT, METBK1, METBK2, METBK1-hr, METBK2-hr, MOPAK, NUTNR, OPTAA, PARAD, PCO2A, PCO2W, PHSEN, PRESF, SPKIR, VEL3D, VELPT, ZPLSC
	% WAVSS_Stats, WAVSS_MeanDir, WAVSS_NonDir, WAVSS_Motion, WAVSS_Fourier
%Method:
    % Telemetered, RecoveredHost, RecoveredInst, RecoveredCSPP, RecoveredWFP, Streamed
%%

@author: craig.risien@oregonstate.edu
"""

import matplotlib.pyplot as plt
import pandas as pd
import M2M_Toolbox
#from importlib import reload
#reload(M2M_Toolbox)

#.. set mooring metadata
platform_name = 'CE02SHSM' 
node = 'NSIF' 
instrument_class = 'CTD' 
method = 'Telemetered'

#.. set time period of interest
start_date='2016-03-01T00:00:00.000Z';
end_date='2016-06-07T23:59:59.000Z';

[uframe_dataset_name,variables] = M2M_Toolbox.M2M_URLs(platform_name,node,instrument_class,method)

# make m2m request
m2m_response = M2M_Toolbox.M2M_Call(uframe_dataset_name, start_date, end_date)

# get list of NetCDF files
nclist = M2M_Toolbox.M2M_Files(m2m_response, '.*'+instrument_class+'.*\\.nc$')

# download the data
[ctd_variables,ctd_time] = M2M_Toolbox.M2M_Data(nclist,variables)

#add time, temperature and converted time to dataframe and sort it by time
df = pd.DataFrame({ctd_variables[0].name: ctd_variables[0].data, 
                   ctd_variables[1].name: ctd_variables[1].data, 
                   'converted_time': ctd_time})
df = df.sort_values(by=[ctd_variables[0].name])

plt.plot(df.converted_time,df.temp)
plt.show()
