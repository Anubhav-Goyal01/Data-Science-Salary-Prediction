import yaml
import sys, os
from src.exception import CustomException
import numpy as np
import pandas as pd
import dill
from src.constants import *

def read_yaml_file(file_path: str) -> dict:

    """
    Reads a YAML file and returns the contents as as dictionary
    """

    try:
        with open(file_path, 'rb') as f:
            return yaml.safe_load(f)
        
    except Exception as e:
        raise CustomException(e, sys)


def save_numpy_array_data(file_path: str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        with open(file_path, "wb") as f:
            np.save(f, array)
    except Exception as e:
        raise CustomException(e, sys)
    

def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)



def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as f:
            dill.load(f)

    except Exception as e:
        raise CustomException(e, sys)


def save_object(file_path: str, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        with open(file_path, "wb") as f:
            dill.dump(obj, f)
    except Exception as e:
        raise CustomException(e, sys)
    

def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    try:
        dataset_schema = read_yaml_file(file_path)
        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        df = pd.read_csv(file_path)

        for column in df.columns:
            if column in list(schema.keys()):
                df[column] = df[column].astype(schema[column])
            else:
                error_messgae = f"{error_messgae} \nColumn: [{column}] is not in the schema."

        if len(error_messgae) > 0:
            raise Exception(error_messgae)
        return df
    
    except Exception as e:
        raise CustomException(e, sys)