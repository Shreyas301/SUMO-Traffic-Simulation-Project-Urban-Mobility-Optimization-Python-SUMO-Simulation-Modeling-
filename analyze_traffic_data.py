import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Load Detector Data ---
tree = ET.parse("detector_output.xml")
root = tree.getroot()

data = []
for interval in root.findall("interval"):
    data.append({
        "begin": float(interval.get("begin", 0)),
        "end": float(interval.get("end", 0)),
        "flow": float(interval.get("flow", 0)),
        "speed": float(interval.get("speed", 0)),
        "vehicles": float(interval.get("nVehContrib", 0))
    })

df = pd.DataFrame(data)

print("\n✅ Data loaded successfully!")
print(df.head())

# --- 2. Basic Stats ---
print("\n--- Traffic Summary ---")
print(f"Average Speed: {df['speed'].mean():.2f} m/s")
print(f"Average Flow: {df['flow'].mean():.2f} veh/hr")
print(f"Total Vehicles Counted: {df['vehicles'].sum():.0f}")

# --- 3. Plot Settings for Readability ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    "figure.figsize": (10,5),
    "axes.titlesize": 16,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "lines.linewidth": 2,
    "lines.markersize": 6
})

# --- 4. Flow over Time ---
plt.figure()
plt.plot(df['begin'], df['flow'], color="#1f77b4", marker='o', label='Traffic Flow (veh/hr)')
plt.title("Traffic Flow Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Flow (vehicles/hour)")
plt.legend()
plt.tight_layout()
plt.show()

# --- 5. Speed over Time ---
plt.figure()
plt.plot(df['begin'], df['speed'], color="#2ca02c", marker='s', label='Average Speed (m/s)')
plt.title("Average Speed Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
plt.legend()
plt.tight_layout()
plt.show()
