#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 10:35:20 2025

@author: bruh
"""

import matplotlib.pyplot as plt
import pandas as pd

# Load your data into a DataFrame named `df_correct`
df_correct = pd.read_csv('/home/bruh/ioncurrent+mass.csv')

# Filter data for 0.1 Pa and 0.3 Pa, all distances
distances = [10, 12, 14, 16, 18, 20]
df_01 = {d: df_correct[(df_correct['Distance (cm)'] == d) & (df_correct['Pressure (Pa)'] == 0.1)] for d in distances}
df_03 = {d: df_correct[(df_correct['Distance (cm)'] == d) & (df_correct['Pressure (Pa)'] == 0.3)] for d in distances}

# Convert units for all datasets
for d in distances:
    df_01[d]['Mass (ng)'] = df_01[d]['Mass (g)'] * 1e9
    df_01[d]['IonCurrent (mA)'] = df_01[d]['IonCurrent (A)'] * 1000
    df_03[d]['Mass (ng)'] = df_03[d]['Mass (g)'] * 1e9
    df_03[d]['IonCurrent (mA)'] = df_03[d]['IonCurrent (A)'] * 1000

# Plot Mass (ng) vs Magnetic Field (T) at 0.1 Pa
fig1, ax1 = plt.subplots(figsize=(9, 6))
colors = plt.cm.tab10.colors
for i, d in enumerate(distances):
    ax1.plot(df_01[d]['MagField (T)'], df_01[d]['Mass (ng)'], color=colors[i], linestyle='-', marker='o', label=f'{d} cm')
ax1.set_xlabel('Magnetic Field (T)', fontsize=16)
ax1.set_ylabel('Mass (ng)', fontsize=16)
ax1.tick_params(axis='both', labelsize=14)
ax1.grid(True)
ax1.legend(loc='upper left', fontsize=14)
ax1.set_title('Mass vs Magnetic Field at 0.1 Pa, 10 cm–20 cm', fontsize=18)
fig1.tight_layout()

# Plot Ion Current (mA) vs Magnetic Field (T) at 0.1 Pa
fig2, ax2 = plt.subplots(figsize=(9, 6))
for i, d in enumerate(distances):
    ax2.plot(df_01[d]['MagField (T)'], df_01[d]['IonCurrent (mA)'], color=colors[i], linestyle='--', marker='s', label=f'{d} cm')
ax2.set_xlabel('Magnetic Field (T)', fontsize=16)
ax2.set_ylabel('Ion Current (mA)', fontsize=16)
ax2.tick_params(axis='both', labelsize=14)
ax2.grid(True)
ax2.legend(loc='upper left', fontsize=14)
ax2.set_title('Ion Current vs Magnetic Field at 0.1 Pa, 10 cm–20 cm', fontsize=18)
fig2.tight_layout()

# Plot Mass (ng) vs Magnetic Field (T) at 0.3 Pa
fig3, ax3 = plt.subplots(figsize=(9, 6))
for i, d in enumerate(distances):
    ax3.plot(df_03[d]['MagField (T)'], df_03[d]['Mass (ng)'], color=colors[i], linestyle='-', marker='o', label=f'{d} cm')
ax3.set_xlabel('Magnetic Field (T)', fontsize=16)
ax3.set_ylabel('Mass (ng)', fontsize=16)
ax3.tick_params(axis='both', labelsize=14)
ax3.grid(True)
ax3.legend(loc='upper left', fontsize=14)
ax3.set_title('Mass vs Magnetic Field at 0.3 Pa, 10 cm–20 cm', fontsize=18)
fig3.tight_layout()

# Plot Ion Current (mA) vs Magnetic Field (T) at 0.3 Pa
fig4, ax4 = plt.subplots(figsize=(9, 6))
for i, d in enumerate(distances):
    ax4.plot(df_03[d]['MagField (T)'], df_03[d]['IonCurrent (mA)'], color=colors[i], linestyle='--', marker='s', label=f'{d} cm')
ax4.set_xlabel('Magnetic Field (T)', fontsize=16)
ax4.set_ylabel('Ion Current (mA)', fontsize=16)
ax4.tick_params(axis='both', labelsize=14)
ax4.grid(True)
ax4.legend(loc='upper left', fontsize=14)
ax4.set_title('Ion Current vs Magnetic Field at 0.3 Pa, 10 cm–20 cm', fontsize=18)
fig4.tight_layout()

plt.show()
