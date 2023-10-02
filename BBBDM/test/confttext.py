import sys
from pathlib import Path

data_processing_path = str(Path(__file__).parent.parent / 'main')

print(data_processing_path)
# Append the 'data_processing' directory to sys.path
sys.path.append(data_processing_path)


#sys.path.append(str(Path(__file__).parent.parent / "runtime"))