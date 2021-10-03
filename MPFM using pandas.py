#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 21:42:30 2017

@author: mohammedalbatati
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


#=========================================================================
#================================ PARAMETERS =============================
n = 300
m = 800
N = 5
#============================== IMPORTING ================================
'''
Using the os library this help getting the folder full path and putting the file inside the folder makes it easy to mention the name of the file only
Below code is to import the MPFM log files to the pandas dataframe 
'''
package_dir = os.path.dirname(os.path.abspath(__file__))
# the file full path is appended with the file name only
file = os.path.join(package_dir,'335.log')
# Using the sep='\t' as the dimilter since the file is a tab file
MPFM_data = pd.read_csv(file,sep='\t')
# print(MPFM_data.columns)

#========================== REMOVING BAD COLUMNS & HEADERS ===============
'''
Using the try except to remove unwanted columns from the data frame, if is needed then the below code can be removed
'''
try:
    MPFM_data.drop(['Permittivity', 'Conductivity', 'Act.OilMassRate', 'Act.WaterMassRate', 'Act.GasMassRate', 'Std.OilMassRate', 'Std.WaterMassRate', 'Std.GasMassRate', 'Std.AccumOilVol', 'AccumWaterVol', 'Std.AccumGasVol', 'Std.AccumGasVol.1', 'Unnamed: 31'], axis = 1, inplace = True)
except:
    pass

# print(MPFM_data.columns)



#========================= CONVERTING TIME AND DATE ======================
'''
Combining the two strings of date and time togather with space then using the funciton to_datetime to convert to a date time instant
'''
MPFM_data['comb_datetime'] = pd.to_datetime(MPFM_data['Date']+' '+MPFM_data['Clock'])
# MPFM_data['new_Time'] = MPFM_data['Clock'].dt.time
# print(MPFM_data)
# print(MPFM_data.describe())
# print(MPFM_data.info())

'''
#trying to make the comulative column ////// still trying
#MPFM_data['oil_cum'] = MPFM_data['Std.OilFlowrate'] + MPFM_data['Std.OilFlowrate'].shift(0)
#for i in range(0, len(MPFM_data)):
#    if i == 0:
#        MPFM_data.iloc[i]['Std.OilFlowrate'] = 0
#    else: 
#        print (MPFM_data.iloc[i]['Std.OilFlowrate']/1440 + MPFM_data.iloc[i-1]['Std.OilFlowrate'])

#print(MPFM_data['Std.OilFlowrate'])
#print(MPFM_data.columns)
'''

#============================ SUMMARY OF RESULTS ==========================
'''
Below is generating the averages for all the values needed for the report
'''
avg_P           = np.average(MPFM_data.loc[n:m,'Pressure'])
avg_T           = np.average(MPFM_data.loc[n:m,'Temperature'])
avg_dP          = np.average(MPFM_data.loc[n:m,'dP'])
avg_oilRate     = np.average(MPFM_data.loc[n:m,'Std.OilFlowrate'])
avg_waterRate   = np.average(MPFM_data.loc[n:m,'WaterFlowrate'])
avg_std_gasRate = np.average(MPFM_data.loc[n:m,'Std.GasFlowrate'])
avg_act_gasRate = np.average(MPFM_data.loc[n:m,'Act.GasFlowrate'])
avg_GOR         = np.average(MPFM_data.loc[n:m,'GOR(std)'])
avg_WC          = np.average(MPFM_data.loc[n:m,'Std.Watercut'])
avg_oilSG       = np.average(MPFM_data.loc[n:m,'OilDensity'])
avg_waterSG     = np.average(MPFM_data.loc[n:m,'WaterDensity'])
avg_gasSG       = np.average(MPFM_data.loc[n:m,'GasDensity'])
avg_dP          = np.average(MPFM_data.loc[n:m,'dP'])
first_time      = MPFM_data['comb_datetime'].iloc[1]
last_time       = MPFM_data['comb_datetime'].iloc[-1]
avg_liquid      = avg_oilRate + avg_waterRate
API             = (141.5/(avg_oilSG/1000) - 131.5)
# oil_cum         = MPFM_data.loc[n:m,'Std.OilFlowrate'].cumsum()

#============================== SUMMARY TO DATAFRAME=======================
'''
Add all the values needed for the report to a dict before moving it to a dataframe
'''
my_summary = {'From':first_time,
              'To':last_time,
              'Delta time':'??????',
              'Choke Size':'???????',
              'WHP':avg_P,
              'WHT':avg_T,
              'Diff dP':avg_dP,
              'Oil Rate':avg_oilRate,
              'Water Rate':avg_waterRate,
              'Liquid Rate':avg_liquid,
              'Gas Rate':avg_std_gasRate,
              'Actual Gas Rate':avg_act_gasRate,
              'Total GOR':avg_GOR,
              'Gas SG':avg_gasSG,
              'Oil SG':avg_oilSG,
              'Oil API':API,
              'BSW':avg_WC,
#              'Cumm Gas':last_gas_cumm,
#              'Cumm Oil':last_oil_cumm,
#              'Cumm Water':last_water_cumm
                }

summary = pd.DataFrame([my_summary]) # convert the dict to dataframe ;)

'''
This is an optional code and might not be needed
#========================== DATA REDUCING ==========================

#test_data = MPFM_data.groupby(np.arange(len(MPFM_data))//5).mean()
#test_data2 = MPFM_data.loc[::5,:]
'''


x = MPFM_data.loc[n:m,'comb_datetime']

plt.figure('Pressure vs dP vs Temp')
plt.plot(x,MPFM_data.loc[n:m,'Pressure'],'b-')
plt.plot(x,MPFM_data.loc[n:m,'dP'],'g-')
plt.plot(x,MPFM_data.loc[n:m,'Temperature'],'r-')
#plt.xticks(rotation='vertical')
plt.xticks(rotation=45)
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.05)
plt.subplots_adjust(bottom=0.15)
plt.legend('PDT')
# plt.show


plt.figure('Flow rate')
plt.plot(x,MPFM_data.loc[n:m,'Std.OilFlowrate'],'k-')
plt.plot(x,MPFM_data.loc[n:m,'GOR(std)'],'g-')
plt.plot(x,MPFM_data.loc[n:m,'WaterFlowrate'],'b-')
plt.xticks(rotation=45)
plt.legend('Test')

plt.figure('Gas rate and water cut')
plt.plot(x,MPFM_data.loc[n:m,'Std.GasFlowrate'],'y-')
plt.plot(x,MPFM_data.loc[n:m,'Std.Watercut'],'b-')
plt.xticks(rotation=45)
plt.legend()
plt.show()


#=============================  EXPORTING SUMMARY TO CSV ===================================

#MPFM_data.loc[n:m:N,['Date', 'Clock', 'Pressure', 'Temperature', 'dP', 'Std.OilFlowrate',
#       'WaterFlowrate', 'Std.GasFlowrate', 'Act.GasFlowrate', 'GOR(std)',
#       'Act.OilFlowrate', 'Std.Watercut','OilDensity', 'WaterDensity', 
#       'GasDensity']].to_csv('MPFM_Data_Report.csv',line_terminator='\n')

#============================= EXPORTING TO EXCEL =========================================

'''
The code below is to use the excel writer to output an excel sheet having the data in one sheet and the summary of data (averages) in the other sheet
'''
try:
    writer = pd.ExcelWriter('output.xlsx')
    MPFM_data.loc[n:m:N,['Date', 'Clock', 'Pressure', 'Temperature', 'dP', 'Std.OilFlowrate',
                         'WaterFlowrate', 'Std.GasFlowrate', 'Act.GasFlowrate', 'GOR(std)',
                         'Act.OilFlowrate', 'Std.Watercut','OilDensity', 'WaterDensity',
                         'GasDensity']].to_excel(writer,'sheet1')

    summary.to_excel(writer,'sheet2')

    writer.save()

except:
    print('Could not export the data to excel')
    pass


