#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 13:07:59 2025

@author: bruh
"""

import matplotlib.pyplot as plt
import pandas as pd

# Load your data
df_correct = pd.read_csv('/home/bruh/Documents/ioncurrent+mass.csv')

distance = 20
df_data = df_correct[df_correct['Distance (cm)'] == distance].copy()

# Convert mass to nanograms
df_data['IonCurrent (A)'] = df_data['IonCurrent (A)'] * 1e3

# Get unique distances
pressure = sorted([0, 0.1, 0.3])

# Plot Mass (ng) vs Pressure (Pa) for each distance at 0.25 T
fig, ax = plt.subplots(figsize=(9, 6))
colors = plt.cm.tab10.colors

for i, pressure in enumerate(pressure):
    df_subset = df_data[df_data['Pressure (Pa)'] == pressure]
    ax.plot(df_subset['MagField (T)'], df_subset['IonCurrent (A)'],
            color=colors[i], linestyle='-', marker='o', label=f'{pressure} Pa')

ax.set_xlabel('Magnetic field (T)', fontsize=16)
ax.set_ylabel('Ion Current (mA)', fontsize=16)
ax.tick_params(axis='both', labelsize=14)
ax.grid(True)
ax.legend(title='Pressure (Pa)', fontsize=12)
ax.set_title(f'Mass vs Magnetic Field at {distance} cm', fontsize=18)
fig.tight_layout()
plt.ylim(0, 12.5)
plt.savefig('ions_vs_magfield_20cm.png', dpi=300)
plt.show()
