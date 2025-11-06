#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 11:47:48 2025

@author: bruh
"""

import os
import pandas as pd

def average_data_in_range(folder_path, output_csv):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    results = []

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, skiprows=20, header=None)


        time_col = df.iloc[:, 0]
        df_filtered = df[(time_col >= 0) & (time_col <= 1e-3)]

        # Calculate Arc Power for the filtered data
        arc_power = df_filtered.iloc[:, 7] * df_filtered.iloc[:, 3]

        # Calculate averages
        avg_ch3 = df_filtered.iloc[:, 3].mean()
        avg_math1 = df_filtered.iloc[:, 7].mean()
        avg_power = arc_power.mean()

        results.append([file, avg_ch3, avg_math1, avg_power])

    # Create a DataFrame and save to CSV
    results_df = pd.DataFrame(results, columns=['Filename', 'Avg_CH3', 'Avg_MATH1', 'Avg_Arc_Power'])
    results_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")


# Example usage
folder_path = '/media/sf_Junk.Paul/Measurements/Massspec2/oscilloscope data'  # Replace with your folder path
output_csv = '/home/bruh/Documents/electrical power.csv'  # Output file
average_data_in_range(folder_path, output_csv)
