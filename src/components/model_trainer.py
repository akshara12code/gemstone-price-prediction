import pandas as pd
import numpy as np
from src.logger.logger import logging
from src.exception.exception import CustomException
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from src.utils.utils import save_object,evaluate_model

from sklearn.linear_model import LinearRegression, Ridge,Lasso,ElasticNet


@dataclass
class ModelTrainingConfig:
    def __init__(self):
        pass

class ModelTraining:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        try:
        
           pass

        except Exception as e:
            logging.info('Exception occured in data ingestion component')   
            raise CustomException(e, sys)