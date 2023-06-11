import sys,os
import pandas as pd
from src.exception import CustomException
from src.utils.main_utils import load_object
from src.logging import logging

class PredictionPipeline:
    def __init__(self, model_dir) -> None:
        self.model_dir = "src/artifact/model_trainer"


    def get_latest_model_path(self):
        try:
            timestamps = os.listdir(self.model_dir)
            folder_name = list(map(int, timestamps))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name, "model.pkl")
            return latest_model_path
        except Exception as e:
            raise CustomException(e, sys)
        
    def predict(self, features):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(model_path)
            predicted_laptop_price = model.predict(features)
            return predicted_laptop_price
        except Exception as e:
            raise CustomException(e, sys) from e


class CustomData:

    def __init__(
      self,
      brand: str,
      processor_brand: str,
      processor_name: str,
      processor_gnrtn: str,
      ram_gb: int,
      ram_type: str,
      ssd: str,
      hdd: str,
      os: str,
      os_bit: str,
      graphic_card_gb: int,
      weight: str,
      warranty: str,
      touchscreen: str,
      msoffice: str,
      rating: str,
      num_ratings: int,
      num_reviews: int
    ) -> None:

        self.brand = brand
        self.processor_brand = processor_brand
        self.processor_name = processor_name
        self.processor_gnrtn = processor_gnrtn
        self.ram_gb = ram_gb
        self.ram_type = ram_type
        self.ssd = ssd
        self.hdd = hdd
        self.os = os
        self.os_bit = os_bit
        self.graphic_card_gb = graphic_card_gb
        self.weight = weight
        self.warranty = warranty
        self.touchscreen = touchscreen
        self.msoffice = msoffice
        self.rating = rating
        self.num_ratings = num_ratings
        self.num_reviews = num_reviews

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "brand": [self.brand],
                "processor_brand": [self.processor_brand],
                "processor_name": [self.processor_name],
                "processor_gnrtn": [self.processor_gnrtn],
                "ram_gb": [self.ram_gb],
                "ram_type": [self.ram_type],
                "ssd": [self.ssd],
                "hdd": [self.hdd],
                "os": [self.os],
                "os_bit": [self.os_bit],
                "graphic_card_gb": [self.graphic_card_gb],
                "weight": [self.weight],
                "warranty": [self.warranty],
                "Touchscreen": [self.touchscreen],
                "msoffice": [self.msoffice],
                "rating": [self.rating],
                "Number of Ratings": [self.num_ratings],
                "Number of Reviews": [self.num_reviews]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
