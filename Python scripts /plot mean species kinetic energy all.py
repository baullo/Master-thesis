#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:04:56 2025
@author: bruh
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the output directory
output_dir = '/home/bruh/Documents/massspec 60v/species kinetic energies'
# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

data = pd.read_csv('/home/bruh/Documents/massspec 60v/combined_analysis_results.csv')

# Drop rows where all kinetic columns are NaN
kinetic_columns = [
    'Kinetic Energy Al+', 'Kinetic Energy Al++', 'Kinetic Energy Al+++',
    'Kinetic Energy Ti+', 'Kinetic Energy Ti++', 'Kinetic Energy Ti+++', 'Kinetic Energy Ti++++',
    'Kinetic Energy N+', 'Kinetic Energy N₂+'
]
filtered_data = data.dropna(subset=kinetic_columns, how='all')

def plot_trends(data, vary, constant1, constant2, constant1_value, constant2_value, filename):
    # Filter data based on constant values
    filtered = data[(data[constant1] == constant1_value) & (data[constant2] == constant2_value)]
    if filtered.empty:
        print(f"No data available for {constant1}={constant1_value} and {constant2}={constant2_value}.")
        return
    # Create a figure with subplots
    plt.figure(figsize=(16, 10))  # Adjusted figure size for 4 subplots

    # Subplot for Al
    plt.subplot(2, 2, 1)
    element_value = 'Al'
    columns = ['Kinetic Energy Al+', 'Kinetic Energy Al++', 'Kinetic Energy Al+++']
    for col in columns:
        # Group by the varying parameter and calculate mean and std
        grouped = filtered[filtered['Element'] == element_value].groupby(vary)[col].agg(['mean', 'std', 'count']).reset_index()
        # Sort by the varying parameter
        grouped = grouped.sort_values(by=vary)
        x = grouped[vary]
        y = grouped['mean']
        y_err = grouped['std']
        # Plot error bars if there's more than one data point, otherwise plot a single point
        if grouped['count'].max() > 1:
            plt.errorbar(x, y, yerr=y_err, fmt='o-', label=col, capsize=5)
        else:
            plt.plot(x, y, 'o-', label=col)
    plt.ylim(0, 150)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f'Al Kinetic Energies vs {vary}')
    plt.xlabel(vary)
    plt.ylabel('Kinetic Energy (eV)')
    plt.legend()

    # Subplot for Ti
    plt.subplot(2, 2, 2)
    element_value = 'Ti'
    columns = ['Kinetic Energy Ti+', 'Kinetic Energy Ti++', 'Kinetic Energy Ti+++', 'Kinetic Energy Ti++++']
    for col in columns:
        grouped = filtered[filtered['Element'] == element_value].groupby(vary)[col].agg(['mean', 'std', 'count']).reset_index()
        grouped = grouped.sort_values(by=vary)
        x = grouped[vary]
        y = grouped['mean']
        y_err = grouped['std']
        if grouped['count'].max() > 1:
            plt.errorbar(x, y, yerr=y_err, fmt='o-', label=col, capsize=5)
        else:
            plt.plot(x, y, 'o-', label=col)
    plt.ylim(0, 200)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f'Ti Kinetic Energies vs {vary}')
    plt.xlabel(vary)
    plt.ylabel('Kinetic Energy (eV)')
    plt.legend()

    # Subplot for N+
    plt.subplot(2, 2, 3)
    element_value = 'N'
    columns = ['Kinetic Energy N+']
    for col in columns:
        grouped = filtered[filtered['Element'] == element_value].groupby(vary)[col].agg(['mean', 'std', 'count']).reset_index()
        grouped = grouped.sort_values(by=vary)
        x = grouped[vary]
        y = grouped['mean']
        y_err = grouped['std']
        if grouped['count'].max() > 1:
            plt.errorbar(x, y, yerr=y_err, fmt='o-', label=col, capsize=5)
        else:
            plt.plot(x, y, 'o-', label=col)
    plt.ylim(-5, 60)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f'N+ Kinetic Energies vs {vary}')
    plt.xlabel(vary)
    plt.ylabel('Kinetic Energy (eV)')
    plt.legend()

    # Subplot for N2+
    plt.subplot(2, 2, 4)
    element_value = 'N₂'
    columns = ['Kinetic Energy N₂+']
    for col in columns:
        grouped = filtered[filtered['Element'] == element_value].groupby(vary)[col].agg(['mean', 'std', 'count']).reset_index()
        grouped = grouped.sort_values(by=vary)
        x = grouped[vary]
        y = grouped['mean']
        y_err = grouped['std']
        if grouped['count'].max() > 1:
            plt.errorbar(x, y, yerr=y_err, fmt='o-', label=col, capsize=5)
        else:
            plt.plot(x, y, 'o-', label=col)
    plt.ylim(-5, 75)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f'N2+ Kinetic Energies vs {vary}')
    plt.xlabel(vary)
    plt.ylabel('Kinetic Energy (eV)')
    plt.legend()

    plt.tight_layout()
    # Save the plot to the specified directory
    full_path = os.path.join(output_dir, filename)
    plt.savefig(full_path)  # Save the plot to a file
    print(f"Plot saved to: {full_path}")
    plt.close()  # Close the plot to free memory

# Define the parameter values
distances = [10, 14, 20]
magnetic_fields = [0, 0.15, 0.25]
pressures = [0, 0.1, 0.2, 0.3]

print("Starting to generate plots...")
print(f"Plots will be saved to: {output_dir}")

# Vary Distance, keep Magnetic Field and Pressure constant
print("\nVarying Distance, keeping Magnetic Field and Pressure constant:")
for magnetic_field in magnetic_fields:
    for pressure in pressures:
        filename = f"Distance_{magnetic_field:.2f}T_{pressure:.1f}Pa.png"
        print(f"Generating plot for Magnetic Field={magnetic_field}, Pressure={pressure}...")
        plot_trends(filtered_data, 'Distance (cm)', 'Magnetic Field (T)', 'Pressure (Pa)', magnetic_field, pressure, filename)

# Vary Magnetic Field, keep Distance and Pressure constant
print("\nVarying Magnetic Field, keeping Distance and Pressure constant:")
for distance in distances:
    for pressure in pressures:
        filename = f"Magnetic_field_{distance}cm_{pressure:.1f}Pa.png"
        print(f"Generating plot for Distance={distance}, Pressure={pressure}...")
        plot_trends(filtered_data, 'Magnetic Field (T)', 'Distance (cm)', 'Pressure (Pa)', distance, pressure, filename)

# Vary Pressure, keep Distance and Magnetic Field constant
print("\nVarying Pressure, keeping Distance and Magnetic Field constant:")
for distance in distances:
    for magnetic_field in magnetic_fields:
        filename = f"Pressure_{distance}cm_{magnetic_field:.2f}T.png"
        print(f"Generating plot for Distance={distance}, Magnetic Field={magnetic_field}...")
        plot_trends(filtered_data, 'Pressure (Pa)', 'Distance (cm)', 'Magnetic Field (T)', distance, magnetic_field, filename)

print("\nFinished generating plots.")
