import matplotlib.pyplot as plt
import pandas as pd

# Load your data
df_correct = pd.read_csv('/home/bruh/ioncurrent+mass.csv')

# Filter data for 10 cm, 14 cm, and 20 cm at 0 Pa, 0.1 Pa, and 0.3 Pa
distances = [10, 14, 20]
dfs = {d: df_correct[(df_correct['Distance (cm)'] == d) & (df_correct['Pressure (Pa)'].isin([0, 0.1, 0.3]))] for d in distances}

# Convert ion current to milliamps for each distance
for d in distances:
    dfs[d]['IonCurrent (mA)'] = dfs[d]['IonCurrent (A)'] * 1000

# Plot for each distance
figs = []
for i, distance in enumerate(distances):
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = plt.cm.tab10.colors

    # Plot each pressure for the current distance
    for j, pressure in enumerate([0, 0.1, 0.3]):
        df_subset = dfs[distance][dfs[distance]['Pressure (Pa)'] == pressure]
        ax.plot(df_subset['MagField (T)'], df_subset['IonCurrent (mA)'],
                color=colors[j], linestyle='--', marker='s', label=f'{pressure} Pa')

    ax.set_xlabel('Magnetic Field (T)', fontsize=16)
    ax.set_ylabel('Ion Current (mA)', fontsize=16)
    ax.tick_params(axis='both', labelsize=14)
    ax.grid(True)
    ax.legend(loc='upper left', fontsize=14, title='Pressure (Pa)')
    ax.set_title(f'Ion Current vs Magnetic Field at {distance} cm, 0/0.1/0.3 Pa', fontsize=18)
    fig.tight_layout()
    figs.append(fig)

plt.show()
