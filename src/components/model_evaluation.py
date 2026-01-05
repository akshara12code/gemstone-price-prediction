import os
import sys

from dataclasses import dataclass
import numpy as np
import pickle
from src.utils.utils import load_object
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from src.logger.logger import logging
from src.exception. exception import CustomException



@dataclass
class ModelEvaluationConfig:
    def __init__(self):
        pass

class ModelEvaluation:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        try:
        
           pass

        except Exception as e:
            logging.info('Exception occured in data ingestion component')   
            raise CustomException(e, sys)