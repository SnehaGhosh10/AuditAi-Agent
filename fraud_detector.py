import pandas as pd
import numpy as np

def detect_fraud(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic fraud detection based on:
    - unusually high amounts (mean + 2*std)
    - missing/null values in any column

    Adds an 'is_fraud' column to the DataFrame.
    """
    df = df.copy()

    # Identify the amount column
    amount_col = next((col for col in df.columns if 'amount' in col.lower()), None)

    # Initialize is_fraud column
    df['is_fraud'] = False

    if amount_col and pd.api.types.is_numeric_dtype(df[amount_col]):
        # Calculate threshold
        threshold = df[amount_col].mean() + 2 * df[amount_col].std()

        # Flag rows with unusually high amounts
        df['is_fraud'] = df[amount_col] > threshold

    # Flag rows with missing values
    df['is_fraud'] = df['is_fraud'] | df.isnull().any(axis=1)

    # Ensure is_fraud is boolean
    df['is_fraud'] = df['is_fraud'].astype(bool)

    return df
