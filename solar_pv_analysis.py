# ============================================================
# Project: Solar PV Power Output Analysis (30 Days)
# Author: Arslan Abbas
# Libraries: NumPy, Pandas, Matplotlib, SciPy
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# -----------------------------
# Generate Sample Data
# -----------------------------
np.random.seed(42)

days = np.arange(1, 31)

# Solar Irradiance (W/m²)
irradiance = np.random.normal(800, 80, 30)
irradiance = np.clip(irradiance, 500, 1000)

# Temperature (°C)
temperature = np.random.normal(32, 4, 30)

# PV System Parameters
pv_capacity = 5  # kW
efficiency = 0.18

# Calculate Daily Power Output (kWh)
power_output = (
    irradiance / 1000
) * pv_capacity * 6 * efficiency + np.random.normal(0, 0.2, 30)

power_output = np.clip(power_output, 0, None)

# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame({
    "Day": days,
    "Irradiance (W/m²)": irradiance,
    "Temperature (°C)": temperature,
    "Power Output (kWh)": power_output
})

# -----------------------------
# Statistical Analysis
# -----------------------------
print("\n========== Solar PV Analysis ==========\n")

print(df)

print("\nSummary Statistics\n")
print(df.describe())

print("\nAverage Daily Energy: {:.2f} kWh".format(df["Power Output (kWh)"].mean()))
print("Maximum Energy: {:.2f} kWh".format(df["Power Output (kWh)"].max()))
print("Minimum Energy: {:.2f} kWh".format(df["Power Output (kWh)"].min()))

# -----------------------------
# Save CSV File
# -----------------------------
df.to_csv("solar_pv_data.csv", index=False)

print("\nCSV file saved as solar_pv_data.csv")

# -----------------------------
# Smooth Curve
# -----------------------------
smooth_output = savgol_filter(df["Power Output (kWh)"], 7, 2)

# -----------------------------
# Plot 1: Daily Power Output
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(df["Day"], df["Power Output (kWh)"], marker='o', label="Actual Output")
plt.plot(df["Day"], smooth_output, linewidth=2, label="Smoothed Output")
plt.title("30-Day Solar PV Power Output")
plt.xlabel("Day")
plt.ylabel("Energy (kWh)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# Plot 2: Solar Irradiance
# -----------------------------
plt.figure(figsize=(10,5))
plt.bar(df["Day"], df["Irradiance (W/m²)"])
plt.title("Daily Solar Irradiance")
plt.xlabel("Day")
plt.ylabel("Irradiance (W/m²)")
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------
# Plot 3: Temperature
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(df["Day"], df["Temperature (°C)"], marker='s')
plt.title("Daily Temperature")
plt.xlabel("Day")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------
# Plot 4: Correlation
# -----------------------------
plt.figure(figsize=(6,5))
plt.scatter(df["Irradiance (W/m²)"], df["Power Output (kWh)"])
plt.title("Irradiance vs Power Output")
plt.xlabel("Irradiance (W/m²)")
plt.ylabel("Power Output (kWh)")
plt.grid(True)
plt.tight_layout()
plt.show()

print("\nAnalysis Completed Successfully!")