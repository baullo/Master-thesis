import matplotlib.pyplot as plt
import pandas as pd

# Load your data
df_correct = pd.read_csv('/home/bruh/ioncurrent+mass.csv')

# Filter data for 0.25 T
mag_field = 0.25
df_025T = df_correct[df_correct['MagField (T)'] == mag_field]

# Convert ion current to milliamps
df_025T['IonCurrent (mA)'] = df_025T['IonCurrent (A)'] * 1000

# Get unique distances
distances = sorted(df_025T['Distance (cm)'].unique())

# Plot Ion Current (mA) vs Pressure (Pa) for each distance at 0.25 T
fig, ax = plt.subplots(figsize=(9, 6))
colors = plt.cm.tab10.colors

for i, distance in enumerate(distances):
    df_subset = df_025T[df_025T['Distance (cm)'] == distance]
    ax.plot(df_subset['Pressure (Pa)'], df_subset['IonCurrent (mA)'],
            color=colors[i], linestyle='--', marker='s', label=f'{distance} cm')

ax.set_xlabel('Pressure (Pa)', fontsize=16)
ax.set_ylabel('Ion Current (mA)', fontsize=16)
ax.tick_params(axis='both', labelsize=14)
ax.grid(True)
ax.legend(title='Distance (cm)', fontsize=12)
ax.set_title(f'Ion Current vs Pressure at {mag_field} T', fontsize=18)
fig.tight_layout()
plt.show()
