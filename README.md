# REAL-TIME-STRESS-DETECTION-SYSTEM-USING-PPG-SENSOR-MACHINE-LEARNING
This project builds a real-time stress detection system using a PPG sensor and Arduino UNO R4. Pulse data is processed in Python to extract features and predict stress with a Random Forest model. Visual (LED) and email alerts provide instant, low-cost feedback for personal stress monitoring.

# PROJECT OVERVIEW
This project presents a real-time stress detection system using a PPG (Photoplethysmogram) sensor and Arduino UNO R4. The sensor captures pulse data, which is transmitted to a Python program where features like mean, standard deviation, range, and median are extracted from 5-second windows. A trained Random Forest model classifies the user’s state as calm or stressed. If stress is detected, a sad face is shown on the Arduino's LED matrix and an alert email is sent. Calm predictions display a happy face. The system is portable, low-cost, and provides immediate visual and remote feedback, making it useful for stress monitoring and human-computer interaction projects.

# PROJECT DESIGN
## a. Data Collection:
PPG signals are collected using an Arduino UNO R4 through the A0 analog input pin. The data is continuously streamed to a Python script via the serial port (COM3). For analysis, each 5-second window—comprising 100 samples—is processed to extract key statistical features, including the mean, standard deviation, range, and median. Each data segment is then labeled as either calm (0) or stressed (1), and the resulting dataset is saved in a CSV file for further use.
## b. Model Training:
The dataset is divided into training and testing sets using an 80/20 split. A Random Forest Classifier is then trained on the extracted features from the training data. Once the model is trained, it is serialized and saved as named stress_model.pkl for future use.
## c. Real-Time Stress Prediction:
The prediction Python script continuously reads PPG data in real time and feeds it to the trained model for classification. If the model predicts a "Stressed" state, a sad face is displayed on the LED matrix, and an email alert is sent using the SMTP protocol. Conversely, if the prediction is "Calm," a happy face is shown on the LED matrix.
