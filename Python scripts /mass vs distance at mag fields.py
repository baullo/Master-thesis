#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 13:50:32 2025

@author: bruh
"""

import matplotlib.pyplot as plt
import pandas as pd

# Load your data
df_correct = pd.read_csv('/home/bruh/Documents/ioncurrent+mass.csv')

pressure = 0.3
df_data = df_correct[df_correct['Pressure (Pa)'] == pressure].copy()

# Convert mass to nanograms
df_data['Mass (ng)'] = df_data['Mass (g)'] * 1e9

# Get unique distances
mag_field = sorted([0, 0.15, 0.25])

# Plot Mass (ng) vs distance (cm) for each distance at 0.25 T
fig, ax = plt.subplots(figsize=(9, 6))
colors = plt.cm.tab10.colors

for i, mag_field in enumerate(mag_field):
    df_subset = df_data[df_data['MagField (T)'] == mag_field]
    ax.plot(df_subset['Distance (cm)'], df_subset['Mass (ng)'],
            color=colors[i], linestyle='-', marker='o', label=f'{mag_field} T')

ax.set_xlabel('Distance (cm)', fontsize=16)
ax.set_ylabel('Mass (ng)', fontsize=16)
ax.tick_params(axis='both', labelsize=14)
ax.grid(True)
ax.legend(title='Magnetic Field (T)', fontsize=12)
ax.set_title(f'Mass vs Distance at a nitrogen pressure of {pressure} Pa', fontsize=18)
fig.tight_layout()
plt.ylim(0, 1300)
plt.savefig('mass_vs_distance_0.3Pa.png', dpi=300)
plt.show()
