import pandas as pd
import importlib.util
from pathlib import Path
import os
modular = importlib.util.spec_from_file_location("normalize_email", str(Path(__file__).parent.parent / 'data_processing/Normalize_email.py'))

normalize_email = importlib.util.module_from_spec(modular)
modular.loader.exec_module(normalize_email)

def test_normalize_with_invalid_emails():
    emails_invalid = pd.DataFrame({'email': ['raniaanjor#gmail.com', 'Rania@.com', '@gmail.com']})
    expected_output = pd.DataFrame({'email': ['raniaanjor#gmail.com', 'Rania@.com', '@gmail.com']})
    actual_output = normalize_email.normalize_dataframe(emails_invalid)
    assert expected_output.equals(actual_output)

def test_normalize_with_valid_emails():
    emails_valid = pd.DataFrame({'email': ['W3071442@aol.com','Anjorinr1@student.iugb.edu.ci','Raniaanjor@gmail.com']})
    expected_output = pd.DataFrame({'email': ['w3071442@aol.com','anjorinr1@student.iugb.edu.ci','raniaanjor@gmail.com']})
    actual_output = normalize_email.normalize_dataframe(emails_valid)
    assert expected_output.equals(actual_output)

def test_normalize_with_mixed_emails():
    emails_mixed = pd.DataFrame({'email': [' W3071442@aol.com ','raniaanjor#gmail.com','Anjorinr1@student.iugb.edu.ci','@gmail.com']})
    expected_output = pd.DataFrame({'email': ['w3071442@aol.com','raniaanjor#gmail.com','anjorinr1@student.iugb.edu.ci','@gmail.com']})
    actual_output = normalize_email.normalize_dataframe(emails_mixed)
    assert expected_output.equals(actual_output)