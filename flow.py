#Calculate stream flow at 15 minute intervals over the interval that a hand measurment is applicable using a met tower csv and a weir logger csv 
#requires manual edit of the sheet at logger removals, only returns where an error occurs
#Weir hand measurements must be in meters
#25 degree equation from King, 1916,1954)
#90 degree equation from university of washington

import pandas as pd
import math
import datetime as dt
import numpy as np

df_air = pd.read_csv('middletower_data_r.csv', usecols=[0,7])
df_weir = pd.read_csv('LowerWeir_20230612.csv', usecols= [1,2])

df_air['Timestamp_15'] = pd.to_datetime(df_air['Datetime'], format='mixed')
df_weir['Timestamp_15'] = pd.to_datetime(df_weir['Date Time, GMT-06:00'], format='mixed')

#boolean, true if two timestamps are within time_dif of one another
def within_time_delta(time_dif, time1, time2):
    time_difference = abs((time1 - time2).total_seconds()) 
    return (time_difference <= (time_dif*60))

#find indices to continue iterating from, if there is a gap in the data, or from the beginning
#of the calculation, dont iterate past end_date
#indicies are row numbers, starting from weir_index and row_index
#returns a tuple containing updated weir_index and air_index
def find_indices(weir_index, air_index, end_date):
    i = 0 # how much  the air index is incremented forward from function call 
    j = 0 #weir
    new_air = df_air.loc[air_index, "Timestamp_15"]  #variable that contains time at row air + i
    new_weir = df_weir.loc[weir_index, "Timestamp_15"]
   
    bool = False #initialize time diff boolean
    while new_air <= end_date and new_weir <= end_date: #after every increment and bool check ensure in date bounds 
        new_air = df_air.loc[air_index+i, "Timestamp_15"] 
        new_weir = df_weir.loc[weir_index+j, "Timestamp_15"] 
        if new_air > new_weir: #if new air is later then iterate through weir data to find a matching time
            new_air = df_air.loc[air_index+i, "Timestamp_15"] #so as to not add i multiple times
            new_weir = df_weir.loc[weir_index+j, "Timestamp_15"]
            bool = within_time_delta(14, new_weir, new_air)
            
            if bool == True:
                air_index = air_index + i #if the vzlues are within the correct difference increment both and return
                
                weir_index = weir_index +j
                
                return [air_index, weir_index]

            else:
                j+=1
        
        if new_weir > new_air:
            new_air = df_air.loc[air_index+i, "Timestamp_15"] #so as to not add i multiple times
            new_weir = df_weir.loc[weir_index+j, "Timestamp_15"]
            bool = within_time_delta(14, new_weir, new_air)
            if bool == True:
                weir_index = weir_index + j
                air_index = air_index +i
                return [air_index, weir_index]
            else:
                i+=1
                
#if there is a jump in the logger data which suggests it was removed from the stream return False
def weir_accurate(weir_index):
    dif = df_weir.loc[weir_index,  'Abs Pres, kPa (LGR S/N: 21382046, SEN S/N: 21382046)'] -  df_weir.loc[weir_index - 1,  'Abs Pres, kPa (LGR S/N: 21382046, SEN S/N: 21382046)'] 
    if weir_index == 0:
        return True
    elif dif.abs() >  1:
            return False
    else:
        return True
    
#calculate the water height between the transducer and the notch, assumed to be static within a single run of the function
def h_wat_base(hand_notch_height,weir_cal,tower_cal):
    # Hydrostatic Pressure
    hyd_press = weir_cal - tower_cal # kPa

    # Water Depth (Transducer to Surface) : P = pgh
    h_water = (hyd_press*1000) / (9.81 * 997) # m

    # Baseline depth from transducer to bottom of Vnotch
    return h_water-hand_notch_height

def flow_15(weir_angle, h_wat_base, write_to_csv, start_date_time, end_date_time):
    flow = 0
    df_write_flow = pd.DataFrame({})
    end_date_time = pd.to_datetime(end_date_time)
    
    #weir index/air index = row number where timestamp15 col has value closest to start_date_time
    weir_index = np.searchsorted(df_weir['Timestamp_15'], start_date_time)
    air_index = np.searchsorted(df_air['Timestamp_15'], start_date_time)
    
    while weir_index < len(df_weir) and air_index < len(df_air):
        #if inaccurate find a new spot to perform calculations within the sheet
        if within_time_delta(14, df_weir.at[weir_index, 'Timestamp_15'], df_air.at[air_index, 'Timestamp_15']) == False:
            tuple = find_indices(weir_index, air_index, end_date_time)
            print('gap start aw: ', air_index, weir_index)
            air_index = tuple[0]
            weir_index = tuple[1]
            print('gap end: ', air_index, weir_index)
            #check time stamps are within 30 minutes of each other
        if weir_accurate == False:
            print("fix weir inaccuracy at index" + weir_index)
            
        else:
            #Calculate flow
            time1 = df_air.loc[air_index, 'Timestamp_15']
            atmos_press = df_air.loc[air_index, 'AirPress'] / 10 #milibars -> kPa
            water_press = df_weir.loc[weir_index, 'Abs Pres, kPa (LGR S/N: 21382046, SEN S/N: 21382046)']
            #calc hydrostatic pressure above transducer
            hydrostatic =  water_press - atmos_press 
            #calc water depth above transducer
            water_depth = (hydrostatic *1000) / (9.81 *997)            
            # calc water depth above vnotch
            h_water_notch = water_depth-h_wat_base
            
            if weir_angle == 22.5:
                coefficient = .586/(h_water_notch**.07)
                flow = (8/15) * math.sqrt(2 *9.81)*coefficient *(math.tan(weir_angle/2))*(h_water_notch**5/2)
                new_row = pd.DataFrame({'Date Time': time1, 'Flow': flow }, index =[0])
                df_write_flow = pd.concat([df_write_flow, new_row])
        
            #Q = 2.49 H ^2.48 
            if weir_angle == 90:
                flow = 2.49 * (h_water_notch)**2.48
                new_row = pd.DataFrame({'Date Time': time1, 'Flow': flow }, index =[0])
                df_write_flow = pd.concat([df_write_flow, new_row])

            else:
                print("no weir equation for given angle")
                
        # iterate to next time stamp
        weir_index += 1
        air_index += 1
    df_write_flow.to_csv(write_to_csv, index=False)

NOTCH_HEIGHT = 0.079375
WEIR_CAL = 71.984
TOWER_CAL = 721.35 /10

h_wat = h_wat_base(NOTCH_HEIGHT, WEIR_CAL, TOWER_CAL)
flow_15(90, h_wat, 'weir_calc.csv', '09/23/2022 11:08', '05/07/23 09:30:00') 
#weir index is not changing where expected
#pressure at time of hand notch