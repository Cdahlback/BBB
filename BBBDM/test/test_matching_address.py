import pandas as pd
import importlib.util
from pathlib import Path

# Import the matching_address module from your code
modular = importlib.util.spec_from_file_location("matching_address", str(Path(__file__).parent.parent / 'data_processing/matching_address.py'))
matching_address = importlib.util.module_from_spec(modular)
modular.loader.exec_module(matching_address)

def test_matching_address_with_same_address():
    historical_addresses = ['123 Main St, Springfield, USA', '456 Pine St, Boston, USA', '789 Oak St, Los Angeles, USA']
    new_addresses = ['123 Main St, Springfield, USA', '456 Pine St, Boston, USA', '789 Oak St, Los Angeles, USA']
    expected_output = pd.DataFrame({
        'historical_address': historical_addresses,
        'found_address': new_addresses,
        'match_found': [1, 1, 1],
        'distance': ['N/A', 'N/A', 'N/A']
    })
    actual_output = matching_address.address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)

def test_matching_address_with_different_address_same_cities():
    historical_addresses = ['1340 Warren St, Mankato, USA', '80 S 9th St, Minneapolis, USA', '283 Oxford St, Rochester, USA']
    new_addresses = ['200 Briargate Rd, Mankato, USA', '80 S 9th St, Minneapolis, USA', '99 Court St, Rochester, USA']
    expected_output = pd.DataFrame({
        'historical_address': historical_addresses,
        'found_address': new_addresses,
        'match_found': [2, 2, 2],
        'distance': [0.465496, 0.220778, 1.107833]
    })
    actual_output = matching_address.address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)

def test_matching_address_with_different_address_different_cities():
    historical_addresses = ['123 Main St, Springfield, USA', '456 Pine St, Boston, USA', '789 Oak St, Los Angeles, USA']
    new_addresses = ['456 Maple St, California, USA', '789 Oak St, California, USA', '555 Elm St, Chicago, USA']
    expected_output = pd.DataFrame({
        'historical_address': historical_addresses,
        'found_address': new_addresses,
        'match_found': [0, 0, 0],
        'distance': ['N/A', 'N/A', 'N/A']
    })
    actual_output = matching_address.address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)

def test_matching_address_with_mixed_examples():
    historical_addresses = ['123 Main St, Springfield, USA', '456 Pine St, Boston, USA', '283 Oxford St, Rochester, USA']
    new_addresses = ['123 Main St, Springfield, USA', '789 Oak St, California, USA', '99 Court St, Rochester, USA']
    expected_output = pd.DataFrame({
        'historical_address': historical_addresses,
        'found_address': new_addresses,
        'match_found': [1, 0, 2],
        'distance': ['N/A', 'N/A', 1.107833]  
    })
    actual_output = matching_address.address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)