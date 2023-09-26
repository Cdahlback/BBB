"""
Mine
"""
import pandas as pd

def join_dataframe_firmid(*dataframes:pd.DataFrame) -> pd.DataFrame:
    """
    Pass in dataframes and merge them on the FirmID column
    Remove any duplicate columns also
    """
    try:
        x = dataframes[0]['FirmID']
    except Exception as e:
        return f"Expection {e} occurred, did the dataframes have FirmID?"
    df = pd.join(dataframes, on='FirmID', how='outer')
    df = df.loc[:,~df.columns.duplicated()]
    return df