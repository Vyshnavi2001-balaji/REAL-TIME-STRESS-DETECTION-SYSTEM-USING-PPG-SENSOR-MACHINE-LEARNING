import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix,
)
import joblib

# === Load Dataset ===
df = pd.read_csv("ppg_features.csv")

# === Clean Data ===
if df.isnull().any().any():
    print("Missing values detected. Cleaning data...")
    df = df.dropna()

X = df[["mean", "std", "range", "median"]]
y = df["label"]

# === Split Data ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# === Train Model ===
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# === Evaluate Model ===
y_pred = clf.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")

# === Save Model ===
joblib.dump(clf, "stress_model.pkl")
print("Model saved as 'stress_model.pkl'")

# === Plot Feature Importance ===
importances = clf.feature_importances_
features = X.columns

plt.figure(figsize=(8, 5))
plt.bar(features, importances, color='skyblue')
plt.title("Feature Importance (Random Forest)")
plt.ylabel("Importance")
plt.xlabel("Features")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()

# === Plot Prediction Distribution ===
plt.figure(figsize=(6, 4))
sns.countplot(x=y_pred, palette="coolwarm")
plt.title("Prediction Distribution: Calm vs. Stress")
plt.xticks([0, 1], ["Calm (0)", "Stress (1)"])
plt.xlabel("Predicted Label")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("prediction_distribution.png")
plt.show()

# === Plot Confusion Matrix ===
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Calm", "Stress"], yticklabels=["Calm", "Stress"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()
