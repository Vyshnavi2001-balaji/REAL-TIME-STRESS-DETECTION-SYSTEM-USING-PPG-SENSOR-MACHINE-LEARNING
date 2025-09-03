import serial
import numpy as np
import time
import joblib
import pandas as pd
from scipy.signal import butter, filtfilt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Config ===
COM_PORT = 'COM3'  # Your Arduino COM port
BAUD_RATE = 115200
SAMPLES_PER_WINDOW = 100
MODEL_FILE = "stress_model.pkl"

# === Email Config ===
EMAIL_ADDRESS = "spooyadav123@gmail.com"      # Your Gmail address (sender)
EMAIL_PASSWORD = "gipc kzpc gxcr garw"        # Gmail app password
EMAIL_TO = "syadavmanjunath@gmail.com"        # Where to send the alert

def send_stress_email():
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_TO
        msg['Subject'] = "Stress Alert from PPG Sensor"

        body = "⚠️ Stress detected! Please take a break and relax."
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_TO, msg.as_string())
        server.quit()
        print("✅ Stress alert email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# === Load Model ===
model = joblib.load(MODEL_FILE)
print("✅ Loaded ML model:", MODEL_FILE)

# === Signal Processing ===
def butter_lowpass_filter(data, cutoff=2.5, fs=20.0, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, cutoff / nyq, btype='low')
    return filtfilt(b, a, data)

def extract_features(segment):
    segment = np.array(segment)
    return [
        np.mean(segment),
        np.std(segment),
        np.max(segment) - np.min(segment),
        np.median(segment)
    ]

# === Connect to Arduino ===
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print(f"📡 Connected to Arduino on {COM_PORT}")

try:
    print("Starting continuous stress prediction session. Press Ctrl+C to quit.")
    while True:
        window = []
        start_time = time.time()
        timeout_seconds = 10
        print(f"\n⏳ Collecting {SAMPLES_PER_WINDOW} PPG samples...")
        
        while len(window) < SAMPLES_PER_WINDOW and (time.time() - start_time) < timeout_seconds:
            if ser.in_waiting:
                line = ser.readline().decode(errors='ignore').strip()
                if line.isdigit():
                    window.append(int(line))
        
        if len(window) < SAMPLES_PER_WINDOW:
            print(f"⚠️ Only {len(window)} samples collected due to timeout.")

        filtered = butter_lowpass_filter(window)
        features = extract_features(filtered)
        feature_names = ["mean", "std", "range", "median"]
        features_df = pd.DataFrame([features], columns=feature_names)

        prediction = model.predict(features_df)[0]

        if prediction == 0:
            print("🟢 You are CALM.")
            ser.write(b'CALM\n')
        else:
            print("🔴 You are STRESSED! Take a break or relax.")
            ser.write(b'STRESS\n')
            send_stress_email()

except KeyboardInterrupt:
    print("\nExiting on user interrupt (Ctrl+C)...")

except Exception as e:
    print("Error:", e)

finally:
    ser.close()
    print("Serial port closed.")
