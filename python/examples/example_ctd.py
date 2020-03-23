# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 11:52:21 2020

@author: craig.risien@oregonstate.edu
"""

import matplotlib.pyplot as plt
import pandas as pd
import M2M_Toolbox
#from importlib import reload
#reload(M2M_Toolbox)

#.. set mooring metadata
mooring_name = 'CE02SHSM' 
node = 'NSIF' 
instrument_class = 'CTD' 
method = 'Telemetered'

#.. set time period of interest
start_date='2016-03-01T00:00:00.000Z';
end_date='2016-06-07T23:59:59.000Z';

[uframe_dataset_name,variables] = M2M_Toolbox.M2M_URLs(mooring_name,node,instrument_class,method)

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
