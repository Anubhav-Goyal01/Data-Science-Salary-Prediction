import os, sys
from src.entity.config_entity import DataValidationConfig
from src.exception import CustomException
from src.logging import logging
from src.utils.main_utils import read_yaml_file
from src.constants import *
import pandas as pd
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

class DataValidation:

    def __init__(
            self,
            data_validation_config: DataValidationConfig,
            data_ingestion_artifact: DataIngestionArtifact
    ) -> None:
        try:
            logging.info(f"{'='*30} Data Valdaition log started. {'='*30} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(self.data_validation_config.schema_file_path)

        except Exception as e:
            raise CustomException(e, sys)
        

    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
        
        except Exception as e:
            raise CustomException(e,sys) from e
        

    def validate_dataset_schema(self, dataframe: pd.DataFrame) -> bool:
        try:
            validation_status = False

            total_cols = len(self.schema_config["columns"])
            num_cols = (self.schema_config['numerical_columns'])
            cat_cols = (self.schema_config['categorical_columns'])
            df_cols = dataframe.columns
            missing_num_cols = []
            for num_column in num_cols:
                if num_column not in df_cols:
                    missing_num_cols.append(num_column)

            logging.info(f"Missing numerical columns: [{missing_num_cols}]")

            
            missing_cat_cols = []
            for cat_column in cat_cols:
                if cat_column not in df_cols:
                    missing_cat_cols.append(cat_column)

            logging.info(f"Missing categorical columns: [{missing_cat_cols}]")
            

            if ((len(dataframe.columns) == total_cols) and (missing_num_cols == []) and (missing_cat_cols == [])):
                validation_status = True

            return validation_status

        except Exception as e:
            raise CustomException(e, sys)   


    def initital_data_validation(self) -> DataValidationArtifact:
        try:

            train_df,test_df = self.get_train_and_test_df()
            train_df_status = self.validate_dataset_schema(train_df)
            test_df_status = self.validate_dataset_schema(test_df)

            if not train_df_status:
                raise Exception("Training data did not pass the validation phase")
            if not test_df_status:
                raise Exception("Test data did not pass the validation phase")
                

            data_validation_artifact = DataValidationArtifact(
                schema_file_path= self.data_validation_config.schema_file_path,
                is_validated= True,
                message= "Data validation performed successfully"
            )
            
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)