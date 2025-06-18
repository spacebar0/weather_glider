import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv
from datetime import datetime

# === CONFIG ===
HOST = '192.168.4.1'
PORT = 80
CSV_FILE = f"glider_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
DURATION = 30  

# === DATA STORAGE ===
t_vals, ax_vals, ay_vals, az_vals = [], [], [], []
temp_vals, hum_vals = [], []

# === SOCKET SETUP ===
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to ESP32...")
client.connect((HOST, PORT))
print("Connected!\n")

# === PLOTTING SETUP ===
fig = plt.figure(figsize=(12, 8))
acc_ax = fig.add_subplot(2, 2, 1)
th_ax = fig.add_subplot(2, 2, 2)
ori_ax = fig.add_subplot(2, 2, 3, projection='3d')

start_time = datetime.now()

def update(frame):
    try:
        line = client.recv(128).decode().strip()
        if line:
            parts = line.split(',')
            if len(parts) == 6:
                t, ax, ay, az, temp, hum = map(float, parts)
                t /= 1000.0 
                t_vals.append(t)
                ax_vals.append(ax)
                ay_vals.append(ay)
                az_vals.append(az)
                temp_vals.append(temp)
                hum_vals.append(hum)

                # --- Acceleration Plot ---
                acc_ax.clear()
                acc_ax.plot(t_vals, ax_vals, label='Ax')
                acc_ax.plot(t_vals, ay_vals, label='Ay')
                acc_ax.plot(t_vals, az_vals, label='Az')
                acc_ax.set_title('Acceleration vs Time')
                acc_ax.set_ylabel('Accel')
                acc_ax.legend()
                acc_ax.grid(True)

                # --- Temp/Humidity Plot ---
                th_ax.clear()
                th_ax.plot(t_vals, temp_vals, label='Temp (°C)', color='red')
                th_ax.plot(t_vals, hum_vals, label='Humidity (%)', color='blue')
                th_ax.set_title('Temp & Humidity vs Time')
                th_ax.set_ylabel('Value')
                th_ax.legend()
                th_ax.grid(True)

                # --- Orientation Vector Plot ---
                ori_ax.clear()
                vec = np.array([ax, ay, az])
                if np.linalg.norm(vec) != 0:
                    vec = vec / np.linalg.norm(vec)
                ori_ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], length=1, normalize=True)
                ori_ax.set_title('3D Orientation (acceleration vector)')
                ori_ax.set_xlim([-1, 1])
                ori_ax.set_ylim([-1, 1])
                ori_ax.set_zlim([-1, 1])
                ori_ax.view_init(30, frame)  # Rotate view slowly
    except Exception as e:
        print("Error:", e)

ani = animation.FuncAnimation(fig, update, interval=100)

print(f"Collecting live data for {DURATION} seconds... (close window to interrupt)")
plt.tight_layout()
plt.show(block=False)

plt.pause(DURATION)
plt.close()
client.close()

# === SAVE TO CSV ===
with open(CSV_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Time (s)', 'Ax', 'Ay', 'Az', 'Temp (C)', 'Humidity (%)'])
    for i in range(len(t_vals)):
        writer.writerow([t_vals[i], ax_vals[i], ay_vals[i], az_vals[i], temp_vals[i], hum_vals[i]])

print(f"\n✅ Data saved to: {CSV_FILE}")

# === PLOT FROM SAVED DATA ===
plt.figure(figsize=(12, 8))

# Acceleration
plt.subplot(2, 2, 1)
plt.plot(t_vals, ax_vals, label='Ax')
plt.plot(t_vals, ay_vals, label='Ay')
plt.plot(t_vals, az_vals, label='Az')
plt.title('Final Acceleration vs Time')
plt.ylabel('Accel')
plt.grid(True)
plt.legend()

# Temp/Humidity
plt.subplot(2, 2, 2)
plt.plot(t_vals, temp_vals, label='Temp (°C)', color='red')
plt.plot(t_vals, hum_vals, label='Humidity (%)', color='blue')
plt.title('Final Temp & Humidity vs Time')
plt.ylabel('Values')
plt.grid(True)
plt.legend()

# Orientation
ax3d = plt.subplot(2, 2, 3, projection='3d')
for i in range(0, len(t_vals), max(1, len(t_vals)//20)):
    vec = np.array([ax_vals[i], ay_vals[i], az_vals[i]])
    if np.linalg.norm(vec) != 0:
        vec = vec / np.linalg.norm(vec)
    ax3d.quiver(0, 0, 0, vec[0], vec[1], vec[2], length=1, normalize=True)
ax3d.set_title("Final 3D Orientation Vectors")
ax3d.set_xlim([-1, 1])
ax3d.set_ylim([-1, 1])
ax3d.set_zlim([-1, 1])

plt.tight_layout()
plt.show()
