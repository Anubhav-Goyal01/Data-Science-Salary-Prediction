from src.entity.config_entity import DataIngestionConfig
from src.exception import CustomException
import sys, os
from src.logging import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        try:
            logging.info(f"{'=' * 10} Data Ingestion started {'=' * 10}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise CustomException(e, sys)

    
    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            data_file_path = self.data_ingestion_config.raw_data_dir
            data_file_name = os.path.basename(data_file_path)
            logging.info(f"Reading CSV file: {data_file_path}")
            data = pd.read_csv(data_file_path)


            logging.info("Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits= 1, test_size= 0.2, random_state=42)

            for train_idx, test_idx in split.split(data, data['job_title']):
                strat_train_set = data.loc[train_idx]
                strat_test_set = data.loc[test_idx]

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, data_file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, data_file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Saving training dataset: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Saving test dataset: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)


            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path = train_file_path,
                test_file_path = test_file_path,
                is_ingested = True,
                message = f"Data ingestion completed successfully."
            )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact


        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_ingestion_artifact(self) -> DataIngestionArtifact:
        try:
            return self.split_data_as_train_test()
        except Exception as e:
            raise CustomException(e, sys)
        

    def __del__(self):
        logging.info(f"{'='*20} Data Ingestion log completed. {'='*20} \n\n")