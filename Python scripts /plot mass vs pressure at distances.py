#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 11:38:39 2025

@author: bruh
"""

import matplotlib.pyplot as plt
import pandas as pd

# Load your data
df_correct = pd.read_csv('/home/bruh/Documents/ioncurrent+mass.csv')

mag_field = 0.25
df_data = df_correct[df_correct['MagField (T)'] == mag_field].copy()

# Convert mass to nanograms
df_data['Mass (ng)'] = df_data['Mass (g)'] * 1e9

# Get unique distances
distances = sorted([10, 12, 20])

# Plot Mass (ng) vs Pressure (Pa) for each distance at 0.25 T
fig, ax = plt.subplots(figsize=(9, 6))
colors = plt.cm.tab10.colors

for i, distance in enumerate(distances):
    df_subset = df_data[df_data['Distance (cm)'] == distance]
    ax.plot(df_subset['Pressure (Pa)'], df_subset['Mass (ng)'],
            color=colors[i], linestyle='-', marker='o', label=f'{distance} cm')

ax.set_xlabel('Pressure (Pa)', fontsize=16)
ax.set_ylabel('Mass (ng)', fontsize=16)
ax.tick_params(axis='both', labelsize=14)
ax.grid(True)
ax.legend(title='Distance (cm)', fontsize=12)
ax.set_title(f'Mass vs Pressure at a Magnetic field strength of {mag_field} T', fontsize=18)
fig.tight_layout()
plt.ylim(0, 1400)
plt.savefig('mass_vs_pressure_0,25T', dpi=300)
plt.show()
