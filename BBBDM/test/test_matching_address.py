import pandas as pd
import importlib.util
from pathlib import Path
import os
modular = importlib.util.spec_from_file_location("matching_address", str(Path(__file__).parent.parent / 'data_processing/matching_address.py'))

matching_address = importlib.util.module_from_spec(modular)
modular.loader.exec_module(matching_address)

def test_matching_address_with_same_address():
    # Test case 1: Identical addresses, expecting match_found = 1
    historical_addresses = ['123 Main St, Springfield', '456 Pine St, Boston', '789 Oak St, Los Angeles']
    new_addresses = ['123 Main St, Springfield', '456 Pine St, Boston', '789 Oak St, Los Angeles']
    expected_output = pd.DataFrame({'historical_address': historical_addresses, 'found_address': new_addresses, 'match_found': [1, 1, 1],'city_match_name':['N/A','N/A','N/A']})
    actual_output = matching_address.address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)

def test_matching_address_with_different_address_same_cities():
    # Test case 2: Addresses with matching cities, expecting match_found = 2
    historical_addresses = ['124 Main St, Springfield', '456 Pine St, Boston', '789 Oak St, Los Angeles']
    new_addresses = ['123 Main St, Springfield', '456 Maple St, Boston', '111 Oak St, Los Angeles']
    expected_output = pd.DataFrame({'historical_address': historical_addresses, 'found_address': new_addresses, 'match_found': [2, 2, 2],'city_match_name':['Springfield','Boston','Los Angeles']})
    actual_output = matching_address.address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)
def test_matching_address_with_different_address_different_cities():
    # Test case 3: No matching addresses, expecting match_found = 0
    historical_addresses = ['123 Main St, Springfield', '456 Pine St, Boston', '789 Oak St, Los Angeles']
    new_addresses = ['456 Maple St, California', '789 Oak St, California', '555 Elm St, Chicago']
    expected_output = pd.DataFrame({'historical_address': historical_addresses, 'found_address': new_addresses, 'match_found': [0, 0, 0],'city_match_name':['N/A','N/A','N/A']})
    actual_output = matching_address.address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)

def test_matching_address_with_mixed_examples():
    historical_addresses = ['123 Main St, Springfield', '456 Pine St, Boston', '1340 Warren St, Mankato']
    new_addresses = ['123 Main St, Springfield', '789 Oak St, California', '200 Briargate Rd, Mankato']
    expected_output = pd.DataFrame({'historical_address': historical_addresses, 'found_address': new_addresses, 'match_found': [1, 0, 2],'city_match_name':['N/A','N/A','Mankato']})
    actual_output = matching_address.address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)    