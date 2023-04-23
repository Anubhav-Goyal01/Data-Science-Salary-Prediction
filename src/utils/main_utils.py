import yaml
import sys
from src.exception import CustomException

def read_yaml_file(file_path: str) -> dict:

    """
    Reads a YAML file and returns the contents as as dictionary
    """

    try:
        with open(file_path, 'rb') as f:
            return yaml.safe_load(f)
        
    except Exception as e:
        raise CustomException(e, sys)
