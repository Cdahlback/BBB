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

    Parameters:
    data_frames (pd.DataFrame): Dataframes to merge

    Returns:
    pd.DataFrame | bool: Returns a dataframe if successful, False if not
    """
    #Checks if there are any dataframes to merge
    if len(data_frames) == 0:
        logging.debug("No dataframes to merge")
        return False
    #Checks if there is only one dataframe to merge
    elif len(data_frames) < 2:
        logging.debug("Not enough dataframes to merge")
        return data_frames[0]
    #Checks if the dataframes have FirmID
    try:
        x = data_frames[0]['FirmID']
    except Exception as e:
        logging.exception(e)
        logging.exception("Did the dataframes have FirmID?")
        return False
    logging.debug("Dataframe contains FirmID - Success")
    #Merges multiple dataframes on FirmID via the amazing reduce function and the merge with the lambda to iterate over it
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['FirmID'], how='outer'), data_frames)
    logging.debug("Merging dataframes - Success")
    #Removes duplicate columns
    df = df_merged.loc[:,~df_merged.columns.duplicated()]
    logging.debug("Removing duplicate columns - Success")
    return df