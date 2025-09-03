import serial
import numpy as np
from scipy.signal import butter, filtfilt
import pandas as pd
import time

# ==== CONFIG ====
COM_PORT = 'COM3'       # Update this if needed
BAUD_RATE = 115200
SAMPLES_PER_WINDOW = 100
OUTPUT_CSV = "ppg_features.csv"

# ==== Signal Filtering & Feature Extraction ====
def butter_lowpass_filter(data, cutoff=2.5, fs=20.0, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, cutoff / nyq, btype='low')
    return filtfilt(b, a, data)

def extract_features(segment):
    return [
        np.mean(segment),
        np.std(segment),
        np.max(segment) - np.min(segment),
        np.median(segment)
    ]

# ==== Load Existing Dataset ====
try:
    df = pd.read_csv(OUTPUT_CSV)
    all_features = df.values.tolist()
    print(f"📄 Loaded existing dataset with {len(all_features)} samples.")
except FileNotFoundError:
    all_features = []
    print("🆕 Starting new dataset.")

# ==== Ask for Label Once ====
label = input("Enter label for this session (0 = Calm, 1 = Stressed): ").strip()
if label not in ['0', '1']:
    print("❌ Invalid label. Exiting.")
    exit()

# ==== Connect to Arduino ====
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"📡 Connected to {COM_PORT}")
except Exception as e:
    print(f"⚠️ Failed to connect to {COM_PORT}: {e}")
    exit()

# ==== Data Collection Loop ====
try:
    while True:
        print(f"⏳ Collecting {SAMPLES_PER_WINDOW} samples...")
        window = []

        while len(window) < SAMPLES_PER_WINDOW:
            if ser.in_waiting:
                line = ser.readline().decode(errors='ignore').strip()
                if line.isdigit():
                    window.append(int(line))

        filtered = butter_lowpass_filter(window)
        features = extract_features(filtered)
        features.append(int(label))
        all_features.append(features)

        df = pd.DataFrame(all_features, columns=["mean", "std", "range", "median", "label"])
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Sample saved. Total collected: {len(all_features)}\n")

except KeyboardInterrupt:
    print("\n🛑 Data collection stopped by user.")
except Exception as e:
    print("⚠️ Error occurred:", e)
finally:
    ser.close()
    print("🔌 Serial port closed.")
