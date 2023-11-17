import sys
from pathlib import Path

import pandas as pd
import pytest

data_processing_path = str(Path(__file__).parent.parent / "main")

print(data_processing_path)
# Append the 'data_processing' directory to sys.path
sys.path.append(data_processing_path)

# sys.path.append(str(Path(__file__).parent.parent / "runtime"))

@pytest.fixture()
def sample_dataframe():
    # Sample dataframe for testing
    data = {
        "Email": ["johndoe@example.com", "invalidemail", "alice.smith@gmail.com"],
        "Phone Number": ["123-456-7890", "invalid phone", "9876543210"],
        "Zipcode": ["12345", "ABCDE", "54321"],
    }
    data = pd.DataFrame(data)
