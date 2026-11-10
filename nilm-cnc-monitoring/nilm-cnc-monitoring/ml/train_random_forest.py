"""Multi-label Random Forest: predicts whether each subsystem is ON from the
main (whole-machine) current signals. This is the core NILM idea."""
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier

DATA = "data/labeled_data.csv"
FEATURES = ["main1", "main2"]                      # aggregate signals (inputs)
TARGETS = ["spindle_on", "coolant_on", "hydraulic_on", "aaxis_on"]

df = pd.read_csv(DATA)
X, Y = df[FEATURES], df[TARGETS]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = MultiOutputClassifier(RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
model.fit(X_train, Y_train)
pred = model.predict(X_test)

for i, name in enumerate(TARGETS):
    print(f"\n=== {name} ===")
    print(classification_report(Y_test[name], pred[:, i]))

joblib.dump(model, "ml/nilm_rf_model.pkl")
print("Model saved to ml/nilm_rf_model.pkl")
