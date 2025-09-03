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
<img width="858" height="462" alt="image" src="https://github.com/user-attachments/assets/cf98bff7-4f69-47ea-8162-586d94ec4efb" />

# PLOTS
<img width="800" height="500" alt="feature_importance" src="https://github.com/user-attachments/assets/a5a59bd3-acbf-4a03-bb3f-b0f9a8b80ef5" />

This bar chart shows which features were most influential in the model’s decisions.Mean and Standard Deviation of the PPG signal were the most important, followed by range, while median had minimal impact. These insights can guide future improvements in feature engineering.
<img width="600" height="400" alt="prediction_distribution" src="https://github.com/user-attachments/assets/62f22c41-bbb8-463a-ad72-4d7614bd440b" />

This plot shows how many instances were predicted as calm vs. stressed. It visually confirms balanced performance and proper labeling in our dataset.
<img width="500" height="400" alt="confusion_matrix" src="https://github.com/user-attachments/assets/164bf189-d73c-4f17-8848-35ab4f7cb04d" />

This matrix shows our model's performance.All 16 calm instances and 9 stressed instances were classified correctly, achieving 100% accuracy on the test set.This confirms strong separation between the two classes and that the model is not overfitting.
