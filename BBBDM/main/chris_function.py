"""
Mine
"""
import pandas as pd
import logging
from functools import reduce

logging.basicConfig(filename='functions.log', encoding='utf-8', level=logging.DEBUG)

def join_dataframe_firmid(*data_frames:pd.DataFrame) -> pd.DataFrame | bool:
    """
    Pass in dataframes and merge them on the FirmID column
    Remove any duplicate columns also
    """
    try:
        x = data_frames[0]['FirmID']
    except Exception as e:
        logging.exception(e)
        logging.exception("Did the dataframes have FirmID?")
        return False
    logging.debug("Merging dataframes - Success")
    #Merges multiple dataframes on FirmID via the amazing reduce function and the merge with the lambda to iterate over it
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['FirmID'], how='outer'), data_frames)

    df = df_merged.loc[:,~df_merged.columns.duplicated()]
    return df