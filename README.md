# ==========================================================
# One-Week Solar PV Power Output Analysis
# Author: Arslan Abbas
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# -----------------------------
# 1. Simulation Parameters
# -----------------------------
np.random.seed(42)

hours = 168  # 7 Days × 24 Hours

time = pd.date_range(
    start="2026-01-01",
    periods=hours,
    freq="H"
)

# -----------------------------
# 2. Simulate Solar Irradiance
# -----------------------------
irradiance = []

for hour in range(hours):

    h = hour % 24

    # Daylight from 6 AM to 6 PM
    if 6 <= h <= 18:

        value = 900 * np.sin(np.pi * (h - 6) / 12)

        value += np.random.normal(0, 40)

        value = max(value, 0)

    else:

        value = 0

    irradiance.append(value)

irradiance = np.array(irradiance)

# -----------------------------
# 3. Simulate Temperature
# -----------------------------
temperature = (
    25
    + 8 * np.sin(np.linspace(0, 7 * np.pi, hours))
    + np.random.normal(0, 1.5, hours)
)

# -----------------------------
# 4. PV System Parameters
# -----------------------------
pv_capacity = 5        # kW
efficiency = 0.20

# Simple PV Output Model
power_output = (
    irradiance / 1000
) * pv_capacity * efficiency

# Temperature effect
power_output *= (
    1 - 0.004 * (temperature - 25)
)

power_output = np.clip(power_output, 0, None)

# -----------------------------
# 5. Create DataFrame
# -----------------------------
df = pd.DataFrame({

    "DateTime": time,

    "Irradiance (W/m²)": irradiance,

    "Temperature (°C)": temperature,

    "PV Power (kW)": power_output

})

# -----------------------------
# 6. Daily Energy
# -----------------------------
df["Date"] = df["DateTime"].dt.date

daily_energy = df.groupby("Date")["PV Power (kW)"].sum()

weekly_energy = daily_energy.sum()

# -----------------------------
# 7. Statistics
# -----------------------------
print("\n========== PV SYSTEM REPORT ==========\n")

print(f"Average Power : {power_output.mean():.2f} kW")

print(f"Maximum Power : {power_output.max():.2f} kW")

print(f"Minimum Power : {power_output.min():.2f} kW")

print(f"Weekly Energy : {weekly_energy:.2f} kWh")

print(f"Standard Deviation : {power_output.std():.2f}")

# -----------------------------
# 8. Smooth Power Curve
# -----------------------------
smooth_power = savgol_filter(
    power_output,
    window_length=11,
    polyorder=2
)

# -----------------------------
# 9. Save Dataset
# -----------------------------
df.to_csv(
    "../data/solar_data.csv",
    index=False
)

# -----------------------------
# 10. Plot 1
# Hourly Power
# -----------------------------
plt.figure(figsize=(12,5))

plt.plot(
    df["DateTime"],
    power_output,
    linewidth=2
)

plt.title("Hourly Solar PV Power Output")

plt.xlabel("Time")

plt.ylabel("Power (kW)")

plt.grid(True)

plt.tight_layout()

plt.savefig("../plots/hourly_power.png")

# -----------------------------
# 11. Plot 2
# Daily Energy
# -----------------------------
plt.figure(figsize=(8,5))

daily_energy.plot(kind="bar")

plt.title("Daily Energy Generation")

plt.ylabel("Energy (kWh)")

plt.grid(axis="y")

plt.tight_layout()

plt.savefig("../plots/daily_energy.png")

# -----------------------------
# 12. Plot 3
# Smoothed Curve
# -----------------------------
plt.figure(figsize=(12,5))

plt.plot(
    df["DateTime"],
    power_output,
    alpha=0.5,
    label="Original"
)

plt.plot(
    df["DateTime"],
    smooth_power,
    linewidth=2,
    label="Smoothed"
)

plt.legend()

plt.title("Smoothed PV Power Output")

plt.xlabel("Time")

plt.ylabel("Power (kW)")

plt.grid(True)

plt.tight_layout()

plt.savefig("../plots/smoothed_power.png")

plt.show()

print("\nDataset saved successfully.")

print("Plots saved successfully.")

print("\nProject Completed.")