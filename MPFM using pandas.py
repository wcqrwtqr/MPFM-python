#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 21:42:30 2017

@author: mohammedalbatati
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#=========================================================================
#================================ PARAMETERS =============================
n = 300
m = 1100
N = 5
#============================== IMPORTING ================================
file= '/Users/mohammedalbatati/AnacondaProjects/OilSERV/Reading csv using pandas/MPFM-python/ZB-10second.log'
MPFM_data = pd.read_csv(file,sep='\t')
#MPFM_data = pd.read_csv('ZB-10second.log',sep='\t')

#========================== REMOVING BAD COLUMNS & HEADERS ===============
#MPFM_data.drop('Unnamed: 31', axis = 1, inplace = True)
MPFM_data.drop(MPFM_data[[18,19,20,21,22,23,24,25,26,27,28,29,30,31]],axis=1, inplace = True)
MPFM_data.drop('Unnamed: 32', axis = 1, inplace = True)



#========================= CONVERTING TIME AND DATE ======================
MPFM_data['comb_datetime'] = pd.to_datetime(MPFM_data['Date']+' '+MPFM_data['Clock'])
MPFM_data['new_Time'] = MPFM_data['comb_datetime'].dt.time

#trying to make the comulative column ////// still trying
#MPFM_data['oil_cum'] = MPFM_data['Std.OilFlowrate'] + MPFM_data['Std.OilFlowrate'].shift(0)
#for i in range(0, len(MPFM_data)):
#    if i == 0:
#        MPFM_data.iloc[i]['Std.OilFlowrate'] = 0
#    else: 
#        print (MPFM_data.iloc[i]['Std.OilFlowrate']/1440 + MPFM_data.iloc[i-1]['Std.OilFlowrate'])

#print(MPFM_data['Std.OilFlowrate'])
#print(MPFM_data.columns)

#============================ SUMMARY OF RESULTS ==========================
avg_P =         np.average(MPFM_data.loc[n:m,'Pressure'])
avg_T =         np.average(MPFM_data.loc[n:m,'Temperature'])
avg_dP =        np.average(MPFM_data.loc[n:m,'dP'])
avg_oilRate =   np.average(MPFM_data.loc[n:m,'Std.OilFlowrate'])
avg_waterRate = np.average(MPFM_data.loc[n:m,'WaterFlowrate'])
avg_std_gasRate=np.average(MPFM_data.loc[n:m,'Std.GasFlowrate'])
avg_act_gasRate=np.average(MPFM_data.loc[n:m,'Act.GasFlowrate'])
avg_GOR =       np.average(MPFM_data.loc[n:m,'GOR(std)'])
avg_WC =        np.average(MPFM_data.loc[n:m,'Std.Watercut'])
avg_oilSG =     np.average(MPFM_data.loc[n:m,'OilDensity'])
avg_waterSG =   np.average(MPFM_data.loc[n:m,'WaterDensity'])
avg_gasSG =     np.average(MPFM_data.loc[n:m,'GasDensity'])
avg_dP =        np.average(MPFM_data.loc[n:m,'dP'])
first_time =    MPFM_data['Date'].iget(0) +' '+ MPFM_data.loc[n:m,'Clock'].iget(0)
last_time =     MPFM_data['Date'].iget(0) +' '+ MPFM_data.loc[n:m,'Clock'].iget(-1)
first_time =    pd.to_datetime(first_time)
last_time =     pd.to_datetime(last_time)
avg_liquid =    avg_oilRate + avg_waterRate
API =           (141.5/(avg_oilSG/1000) - 131.5)
#oil_cum =       MPFM_data.loc[n:m,'Std.OilFlowrate'].cumsum()



#============================== SUMMARY TO DATAFRAME=======================
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

#========================== DATA REDUCING ==========================

#test_data = MPFM_data.groupby(np.arange(len(MPFM_data))//5).mean()
#test_data2 = MPFM_data.loc[::5,:]

#============================= GRAPHING ==================================

x = MPFM_data.loc[n:m,'new_Time']

plt.figure()
plt.plot(x,MPFM_data.loc[n:m,'Pressure'],'b-')
plt.plot(x,MPFM_data.loc[n:m,'dP'],'g-')
plt.plot(x,MPFM_data.loc[n:m,'Temperature'],'r-')
#plt.xticks(rotation='vertical')
plt.xticks(rotation=45)
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.05)
plt.subplots_adjust(bottom=0.15)
plt.legend()
plt.show

plt.figure()
plt.plot(x,MPFM_data.loc[n:m,'Std.OilFlowrate'],'k-')
plt.plot(x,MPFM_data.loc[n:m,'GOR(std)'],'g-')
plt.plot(x,MPFM_data.loc[n:m,'WaterFlowrate'],'b-')
plt.xticks(rotation=45)
plt.legend()
plt.show

plt.figure()
plt.plot(x,MPFM_data.loc[n:m,'Std.GasFlowrate'],'y-')
plt.plot(x,MPFM_data.loc[n:m,'Std.Watercut'],'b-')
plt.xticks(rotation=45)
plt.legend()
plt.show



#=============================  EXPORTING SUMMARY TO CSV ===================================

#MPFM_data.loc[n:m:N,['Date', 'Clock', 'Pressure', 'Temperature', 'dP', 'Std.OilFlowrate',
#       'WaterFlowrate', 'Std.GasFlowrate', 'Act.GasFlowrate', 'GOR(std)',
#       'Act.OilFlowrate', 'Std.Watercut','OilDensity', 'WaterDensity', 
#       'GasDensity']].to_csv('MPFM_Data_Report.csv',line_terminator='\n')

#============================= EXPORTING TO EXCEL =========================================

writer = pd.ExcelWriter('output.xlsx')

MPFM_data.loc[n:m:N,['Date', 'Clock', 'Pressure', 'Temperature', 'dP', 'Std.OilFlowrate',
       'WaterFlowrate', 'Std.GasFlowrate', 'Act.GasFlowrate', 'GOR(std)',
       'Act.OilFlowrate', 'Std.Watercut','OilDensity', 'WaterDensity', 
       'GasDensity']].to_excel(writer,'sheet1')

summary.to_excel(writer,'sheet2')

writer.save()

# checking

