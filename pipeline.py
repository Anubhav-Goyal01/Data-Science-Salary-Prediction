from src.config.configuration import Configuration
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


config = Configuration()

data_ingestion_config = config.get_data_ingestion_config()
data_validation_config = config.get_data_validation_config()
data_transformation_config = config.get_data_transformation_config()
model_trainer_config = config.get_model_trainer_config()

data_ingestion_artifact = DataIngestion(data_ingestion_config).initiate_data_ingestion_artifact()
data_validation_artifact = DataValidation(data_validation_config, data_ingestion_artifact).initital_data_validation()
data_transformation_artifact = DataTransformation(data_transformation_config, data_ingestion_artifact, data_validation_artifact).initiate_data_transformation()
model_trainer_artifact = ModelTrainer(model_trainer_config, data_transformation_artifact).initiate_model_trainer()