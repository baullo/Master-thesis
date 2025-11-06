#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 11:32:04 2025

@author: bruh
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load your data
data = pd.read_csv('/home/bruh/Documents/ioncurrent+mass.csv')

# Create a 3D scatter plot
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot with Pressure as color and Mass as z
sc = ax.scatter(
    data['Distance (cm)'],
    data['MagField (T)'],
    data['IonCurrent (A)']*1e3,
    c=data['Pressure (Pa)'],
    cmap='viridis',
    s=50
)

# Label the axes
ax.set_xlabel('Distance (cm)', fontsize=14)
ax.set_ylabel('Magnetic Field (T)', fontsize=14)
ax.set_zlabel('Ion Current (mA)', fontsize=14)
ax.view_init(elev=15, azim=315)

cbar = plt.colorbar(sc, ax=ax, pad=0.1, shrink=0.75)
cbar.set_label('Pressure (Pa)', fontsize=14)

ax.grid(True, linestyle='--', alpha=0.5)
fig.set_facecolor('white')

fig.suptitle('Ion Current (mA) vs. Distance (cm), Magnetic Field (T) and Pressure (Pa)', y=0.83, fontsize= 20)
plt.tight_layout(rect=[0, 0, 0.95, 0.95])
fig.savefig('3Dion.png', dpi=500)
