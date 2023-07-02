import pandas as pd

# Read the original Excel sheet with 30-minute intervals, read in only the time and pressure to the df
# names = ['Date Time, GMT-06:00', 'Abs Pres, kPa (LGR S/N: 21382046, SEN S/N: 21382046)']

df_original = pd.read_csv('LowerWeir_20230612.csv', usecols= [1,2])

#print(df_original.columns + '\n')

# Set the 'Date Time, GMT-06:00' column as the index
df_original.set_index('Date Time, GMT-06:00', inplace=True)

# Convert the index to datetime type
df_original.index = pd.to_datetime(df_original.index,  format='%m/%d/%y %I:%M:%S %p')
#print(df_original)
# Resample the data to 15-minute intervals and calculate the mean
df_15_min_mean = df_original.resample('15T').mean()

# Interpolate the missing values to fill in the gaps
df_final = df_15_min_mean.interpolate()
# Resample the data to 15-minute intervals and calculate the original values of the other data column
#df_15_min_other_col = df_original['Abs Pres, kPa (LGR S/N: 21382047, SEN S/N: 21382047)'].resample('15T').first()
#print(df_15_min_other_col)
# Merge the 15-minute averaged values and the original values of the other data column
#df_final = pd.merge(df_15_min_mean_interpolated, df_15_min_other_col, left_index=True, right_index=True)
print(df_final)
# Write the new DataFrame to a new csv
df_final.to_csv('weir_15_pressure.csv')