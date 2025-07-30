from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_fraud(df):
    numeric_data = df.select_dtypes(include=['float64', 'int64'])
    model = IsolationForest(n_estimators=100, contamination=0.05)
    model.fit(numeric_data)
    df['fraud_flag'] = model.predict(numeric_data)
    df['fraud_flag'] = df['fraud_flag'].map({1: 'Normal', -1: 'Anomaly'})
    return df
