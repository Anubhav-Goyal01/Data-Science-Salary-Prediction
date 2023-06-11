from src.config.configuration import Configuration
config = Configuration()
data_ingestion_config = config.get_data_ingestion_config()
data_validation_config = config.get_data_validation_config()
data_transformation_config = config.get_data_transformation_config()
model_trainer_config = config.get_model_trainer_config()

from src.components.data_ingestion import DataIngestion
data_ingestion_artifact = DataIngestion(data_ingestion_config).initiate_data_ingestion_artifact()

from src.components.data_validation import DataValidation
data_validation_artifact = DataValidation(data_validation_config, data_ingestion_artifact).initital_data_validation()

from src.components.data_transformation import DataTransformation
data_transformation_artifact = DataTransformation(data_transformation_config, data_ingestion_artifact, data_validation_artifact).initiate_data_transformation()

from src.components.model_trainer import ModelTrainer
model_trainer_artifact = ModelTrainer(model_trainer_config, data_transformation_artifact).initiate_model_trainer()