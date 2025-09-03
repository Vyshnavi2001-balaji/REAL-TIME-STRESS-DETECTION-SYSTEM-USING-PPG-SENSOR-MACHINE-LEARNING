# REAL-TIME-STRESS-DETECTION-SYSTEM-USING-PPG-SENSOR-MACHINE-LEARNING
This project builds a real-time stress detection system using a PPG sensor and Arduino UNO R4. Pulse data is processed in Python to extract features and predict stress with a Random Forest model. Visual (LED) and email alerts provide instant, low-cost feedback for personal stress monitoring.

# PROJECT OVERVIEW
This project presents a real-time stress detection system using a PPG (Photoplethysmogram) sensor and Arduino UNO R4. The sensor captures pulse data, which is transmitted to a Python program where features like mean, standard deviation, range, and median are extracted from 5-second windows. A trained Random Forest model classifies the user’s state as calm or stressed. If stress is detected, a sad face is shown on the Arduino's LED matrix and an alert email is sent. Calm predictions display a happy face. The system is portable, low-cost, and provides immediate visual and remote feedback, making it useful for stress monitoring and human-computer interaction projects.

# PROJECT DESIGN
# a. Data Collection:
