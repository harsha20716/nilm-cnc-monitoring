"""Creates a labeled dataset from the raw sensor CSV.

Input : data/7CHANNAL_DATA_1.csv  (columns assumed: spindle, coolant, hydraulic, aaxis, ...)
Output: data/labeled_data.csv

Each channel is turned into an ON/OFF flag using a threshold, then a single
machine-state label is assigned using priority rules.
EDIT the column names and thresholds below to match your data.
"""
import pandas as pd

INPUT = "data/7CHANNAL_DATA_1.csv"
OUTPUT = "data/labeled_data.csv"

THRESHOLDS = {"spindle": 0.5, "coolant": 0.3, "hydraulic": 0.3, "aaxis": 0.2}


def label_row(r):
    if r["spindle_on"] and r["coolant_on"]:
        return "MACHINING"
    if r["spindle_on"]:
        return "SPINDLE_RUNNING"
    if r["aaxis_on"]:
        return "AXIS_MOVING"
    if r["hydraulic_on"]:
        return "HYDRAULIC_ON"
    return "OFF"


df = pd.read_csv(INPUT)
for ch, th in THRESHOLDS.items():
    df[f"{ch}_on"] = (df[ch] > th).astype(int)

df["state"] = df.apply(label_row, axis=1)
df.to_csv(OUTPUT, index=False)
print(df["state"].value_counts())
print("Saved", OUTPUT)
