import sys
from src.entity.config_entity import *
from src.utils.main_utils import read_yaml_file
from src.constants import *
from src.exception import CustomException
from src.logging import logging


class Configuration:

    def __init__(
            self,
            config_file_path:str = CONFIG_FILE_PATH,
            current_time_stamp:str = CURRENT_TIME_STAMP
    ) -> None:
        try:
            self.config_info = read_yaml_file(config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise CustomException(e, sys)

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_pipeline_info = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(
                ROOT_DIR, 
                training_pipeline_info[TRAINING_PIPELINE_NAME_KEY],
                training_pipeline_info[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir= artifact_dir)
            logging.info(f"Training pipeline config: {training_pipeline_config}")
            return training_pipeline_config

        except Exception as e:
            raise CustomException(e, sys)


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            data_ingestion_artifact_dir = os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            raw_data_dir = os.path.join(
                ROOT_DIR,
                DATA_DIR,
                DATA_FILE_NAME
            )

            
            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_DIR_NAME_KEY]
            )

            ingested_train_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            ingested_test_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )


            data_ingestion_config = DataIngestionConfig(
                raw_data_dir= raw_data_dir,
                ingested_train_dir= ingested_train_dir, 
                ingested_test_dir= ingested_test_dir
            )

            logging.info(f"Data ingestion config: {data_ingestion_config}")
            return data_ingestion_config

        except Exception as e:
            raise CustomException(e, sys)


    def get_data_validation_config(self) -> DataValidationConfig:
        pass


    def get_data_transformation_config(self) -> DataTransformationConfig:
        pass


    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass



    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass


    def get_model_pusher_config(self) -> ModelPusherConfig: 
        pass

