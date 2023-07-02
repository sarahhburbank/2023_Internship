import pandas as pd
import matplotlib.pyplot as plt

from pykrige import OrdinaryKriging
import numpy as np
df = pd.read_csv("6:13_krig.csv")
#basic plot no krigging
cm = plt.colormaps['viridis_r']
#fig, ax = plt.subplots(1,3, figsize=(10,10))
plt.figure(figsize=(10,10))
scatter = plt.scatter(df['Longitude'], df['Latitude'], c=df['%VWC'], cmap=cm, s=50)
#scatter = ax[0].scatter(df['Longitude'], df['Latitude'], c=df['%VWC'], cmap=cm, s=50)
plt.colorbar(scatter)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()


#tery different models
OK = OrdinaryKriging(x=df['Longitude'],
y=df['Latitude'],
z=df['%VWC'],
variogram_model='linear',
verbose=True, enable_plotting=True,
coordinates_type='geographic')
print("1")
#make data grid to show uncertanity and range in data
#may modify step
grid_lat = np.arange(38.924, 38.926, 0.01, dtype='float64')
grid_long = np.arange(-106.977, -106.973 , 0.01,dtype='float64')
print("2")
#zstar, ss = OK.execute('grid', grid_long, grid_lat)
print("3")
#plt data in grif
fig, ax = plt.subplots(figsize=(10,10))
print("4")
image = ax.imshow(zstar, extent=(1.5, 4.5, 57.5, 62), origin='lower')
print("5")
ax.set_xlabel('Longitude', fontsize=14, fontweight='bold')
print("6")
ax.set_ylabel('Latitude', fontsize=14, fontweight='bold')
scatter = ax.scatter(x=df['Longitude'], y=df['Latitude'], color='black')
print("7")
colorbar = fig.colorbar(image)
colorbar.set_label('%VWC', fontsize=14, fontweight='bold')
print("8")
plt.show()
print("9")
#plt uncertainty in grid
fig, ax = plt.subplots(figsize=(10,10))
image = ax.imshow(ss, extent=(1.5, 4.5, 57.5, 62), origin='lower')
ax.set_xlabel('Longitude', fontsize=14, fontweight='bold')
ax.set_ylabel('Latitude', fontsize=14, fontweight='bold')
scatter = ax.scatter(x=df['Longitude'], y=df['Latitude'], color='black')
colorbar = fig.colorbar(image)
colorbar.set_label('DTC (us/ft)', fontsize=14, fontweight='bold')
plt.show()