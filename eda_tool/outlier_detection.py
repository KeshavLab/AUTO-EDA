import numpy as np
import pandas as pd
from scipy import stats

def detect_outliers(df, column):
    """
    Detect outliers in a specified column using IQR method.
    
    Args:
        df (pd.DataFrame): Input dataframe
        column (str): Column name to check for outliers
        
    Returns:
        tuple: (DataFrame with outliers, Summary dictionary)
    """
    # Calculate Q1, Q3, and IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Find outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    # Create summary
    summary = {
        "column": column,
        "total_rows": len(df),
        "outliers_count": len(outliers),
        "outliers_percentage": round((len(outliers) / len(df)) * 100, 2),
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR
    }
    
    return outliers, summary
