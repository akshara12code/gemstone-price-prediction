import os
import sys
import pandas as pd
from src.exception.exception import CustomException
from src.logger.logger import logging
from src.utils.utils import load_object

class PredictionPipeline:
    def __init__(self):
        print("PredictionPipeline initialized")
        # Load models once during initialization
        try:
            self.preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            self.model_path = os.path.join("artifacts", "model.pkl")
            
            self.preprocessor = load_object(self.preprocessor_path)
            self.model = load_object(self.model_path)
            logging.info("Models loaded successfully")
        except Exception as e:
            logging.error(f"Error loading models: {str(e)}")
            raise CustomException(e, sys)
    
    def predict(self, features):
        try:
            logging.info("Starting prediction")
            
            # Transform the input features
            scaled_data = self.preprocessor.transform(features)
            logging.info(f"Data scaled: {scaled_data}")
            
            # Make prediction
            pred = self.model.predict(scaled_data)
            logging.info(f"Prediction made: {pred}")
            
            return pred
            
        except Exception as e:
            logging.error(f"Prediction error: {str(e)}")
            raise CustomException(e, sys)

class CustomData:
    def __init__(self,
                 carat: float,
                 depth: float,
                 table: float,
                 x: float,
                 y: float,
                 z: float,
                 cut: str,
                 color: str,
                 clarity: str):
        
        self.carat = carat
        self.depth = depth
        self.table = table
        self.x = x
        self.y = y
        self.z = z
        self.cut = cut
        self.color = color
        self.clarity = clarity
    
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'carat': [self.carat],
                'depth': [self.depth],
                'table': [self.table],
                'x': [self.x],
                'y': [self.y],
                'z': [self.z],
                'cut': [self.cut],
                'color': [self.color],
                'clarity': [self.clarity]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
            
        except Exception as e:
            logging.info('Exception Occurred in prediction pipeline')
            raise CustomException(e, sys)
