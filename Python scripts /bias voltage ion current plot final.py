import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Load data
df = pd.read_csv("/home/bruh/Documents/bias_current_voltage_characteristics.csv")
x = df["Bias Voltage (V)"].values
y = df["IonCurrent (A)"].values * 1e3  # Convert A to mA

# Modified saturation model: I = I_sat*(1 - exp(-V/V_T)) + m*V
def mod_sat_func(V, I_sat, V_T, m):
    return (I_sat * (1 - np.exp(-V / V_T)) + m * V) * 1e3  # Convert A to mA

# Full saturation fit
popt, pcov = curve_fit(lambda V, I_sat, V_T, m: I_sat * (1 - np.exp(-V / V_T)) + m * V, x, y * 1e-3, p0=[0.007, 10, 1e-5])
I_sat_mA = popt[0] * 1e3
V_T = popt[1]
m_mA_per_V = popt[2] * 1e3
sat_legend_str = f"Saturation Fit: $I = {I_sat_mA:.2f} (1 - e^{{-V/{V_T:.1f}}}) + {m_mA_per_V:.3f} V$"



# Plot with semi-log y-axis
plt.figure(figsize=(8, 5))
plt.scatter(x, y, label="Data", color="blue")

# Saturation fit curve
V_fit = np.linspace(0, max(x), 100)
plt.plot(V_fit, mod_sat_func(V_fit, *popt),'g-', lw=2.5, label=sat_legend_str)


# Set semi-log y-axis
plt.yscale('log')

# Labels and legend
plt.xlabel("Bias Voltage (V)", fontsize=12)
plt.ylabel("log( Current / mA )", fontsize=12)
plt.title("Bias Voltage vs. Current", fontsize=14)
plt.legend(loc='lower right', fontsize=10)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.xlim(0, 130)
plt.ylim(2.5, 10)
plt.tight_layout()
plt.savefig('bias_current_voltage_Saturation_thesis_version.png', dpi=300)
plt.show()

# Print fit parameters
print(f"Saturation Fit Parameters: I_sat = {I_sat_mA:.2f} mA, V_T = {V_T:.1f} V, m = {m_mA_per_V:.3f} mA/V")

