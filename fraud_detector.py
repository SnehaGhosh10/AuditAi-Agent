import pandas as pd
import numpy as np

def detect_fraud(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic fraud detection based on unusually high amount and missing values.
    Adds an 'is_fraud' column to the DataFrame.
    """
    df = df.copy()

    # Try to find a column that looks like 'Amount'
    amount_col = next((col for col in df.columns if 'amount' in col.lower()), None)

    if amount_col and pd.api.types.is_numeric_dtype(df[amount_col]):
        # Calculate fraud threshold: mean + 2*std deviation
        threshold = df[amount_col].mean() + 2 * df[amount_col].std()

        # Flag as fraud if amount is unusually high
        df['is_fraud'] = df[amount_col] > threshold
    else:
        # If no amount-like column, mark all as not fraudulent
        df['is_fraud'] = False

    # Also flag any rows with missing/null values
    df['is_fraud'] = df['is_fraud'] | df.isnull().any(axis=1)

    return df
