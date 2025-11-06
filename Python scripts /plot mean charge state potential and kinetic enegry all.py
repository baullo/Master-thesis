import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define the output directory
output_dir = '/home/bruh/Documents/massspec 60v/mean charge kinetic potential energy plots'
# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

data = pd.read_csv('/home/bruh/Documents/massspec 60v/combined_analysis_results.csv')

# Filter the data to remove rows with missing values in specific columns
filtered_data = data.dropna(subset=['Mean Charge State', 'Average Potential Energy (eV)', 'Average Kinetic Energy (eV)'])

def plot_trends(data, vary, constant1, constant2, constant1_value, constant2_value, filename):
    # Filter data based on constant values
    filtered = data[(data[constant1] == constant1_value) & (data[constant2] == constant2_value)]
    if filtered.empty:
        print(f"No data available for {constant1}={constant1_value} and {constant2}={constant2_value}.")
        return
    # Group by the varying variable and element to calculate mean and standard deviation
    grouped = filtered.groupby([vary, 'Element']).agg({
        'Mean Charge State': ['mean', 'std', 'count'],
        'Average Potential Energy (eV)': ['mean', 'std', 'count'],
        'Average Kinetic Energy (eV)': ['mean', 'std', 'count']
    }).reset_index()
    # Create a figure with subplots
    plt.figure(figsize=(14, 6))
    # Get unique elements and create a color map
    elements = sorted(filtered['Element'].unique())
    palette = sns.color_palette('tab10', n_colors=len(elements))
    color_map = {element: palette[i] for i, element in enumerate(elements)}

    # Plot Mean Charge State
    plt.subplot(1, 3, 1)
    for element in elements:
        subset = grouped[grouped['Element'] == element]
        subset = subset.sort_values(by=vary)  # Sort by the varying variable
        x_values = subset[vary]
        y_values = subset[('Mean Charge State', 'mean')]
        y_errors = subset[('Mean Charge State', 'std')]
        if len(x_values) > 1:
            plt.errorbar(x_values, y_values, yerr=y_errors, fmt='o-', color=color_map[element], capsize=5, capthick=2)
        else:
            plt.scatter(x_values, y_values, color=color_map[element])
    plt.ylim(0.9, 3)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f'Mean Charge State vs {vary}')
    plt.xlabel(vary)
    plt.ylabel('Mean Charge State')
    # Create custom legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[element], markersize=10, label=element) for element in elements]
    plt.legend(handles=handles)

    # Plot Average Potential Energy
    plt.subplot(1, 3, 2)
    for element in elements:
        subset = grouped[grouped['Element'] == element]
        subset = subset.sort_values(by=vary)  # Sort by the varying variable
        x_values = subset[vary]
        y_values = subset[('Average Potential Energy (eV)', 'mean')]
        y_errors = subset[('Average Potential Energy (eV)', 'std')]
        if len(x_values) > 1:
            plt.errorbar(x_values, y_values, yerr=y_errors, fmt='o-', color=color_map[element], capsize=5, capthick=2)
        else:
            plt.scatter(x_values, y_values, color=color_map[element])
    plt.ylim(-5, 40)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f'Average Potential Energy vs {vary}')
    plt.xlabel(vary)
    plt.ylabel('Average Potential Energy (eV)')
    # Create custom legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[element], markersize=10, label=element) for element in elements]
    plt.legend(handles=handles)

    # Plot Average Kinetic Energy
    plt.subplot(1, 3, 3)
    for element in elements:
        subset = grouped[grouped['Element'] == element]
        subset = subset.sort_values(by=vary)  # Sort by the varying variable
        x_values = subset[vary]
        y_values = subset[('Average Kinetic Energy (eV)', 'mean')]
        y_errors = subset[('Average Kinetic Energy (eV)', 'std')]
        if len(x_values) > 1:
            plt.errorbar(x_values, y_values, yerr=y_errors, fmt='o-', color=color_map[element], capsize=5, capthick=2)
        else:
            plt.scatter(x_values, y_values, color=color_map[element])
    plt.ylim(-10, 120)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f'Average Kinetic Energy vs {vary}')
    plt.xlabel(vary)
    plt.ylabel('Average Kinetic Energy (eV)')
    # Create custom legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[element], markersize=10, label=element) for element in elements]
    plt.legend(handles=handles)

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
