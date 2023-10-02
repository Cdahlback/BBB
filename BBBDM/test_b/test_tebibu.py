import pandas as pd
import importlib.util
from pathlib import Path

modular = importlib.util.spec_from_file_location("Tebibu", str(Path(__file__).parent.parent / 'data_processing/Tebibu.py'))

Tebibu = importlib.util.module_from_spec(modular)
modular.loader.exec_module(Tebibu)

# test filtering of valid DataFrams
def test_filter_success():
    df = pd.DataFrame({
        'name': ['Company A', 'Company C'],
        'address': ['123 Main St', '456 Oak St'],
        'phone': ['5551234567', '5557891234'],
        'website': ['www.companya.com', 'www.companyc.com'],
        'email': ['email@companya.com', 'email@companyc.com']
    })
    
    valid_df, invalid_df = Tebibu.filter_dataframes(df)
    
   
    assert len(valid_df) == 2
    assert len(invalid_df) == 0
    
    
    assert all(col in valid_df.columns for col in ['name', 'address', 'phone', 'website', 'email'])
    
    assert 'Company A' in valid_df['name'].values
    assert 'Company C' in valid_df['name'].values
    

# tst filtering of invalid DataFrames
def test_filter_failure():
    df = pd.DataFrame({
        'name': ['', None],
        'address': ['', None],
        'phone': ['12345678901234567890', None],
        'website': ['', None],
        'email': ['', None]
    })
    
    valid_df, invalid_df = Tebibu.filter_dataframes(df)
    
   
    assert len(valid_df) == 0
    assert len(invalid_df) == 2
    
   
    assert all(col in invalid_df.columns for col in ['name', 'address', 'phone', 'website', 'email'])
    

