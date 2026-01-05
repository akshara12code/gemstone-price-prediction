import pandas as pd
import numpy as np
from src.logger.logger import logging
from src.exception.exception import CustomException
import os
import sys
from dataclasses import dataclass
from pathlib import Path


from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler

from src.utils.utils import save_object

@dataclass
class DataTransformationConfig:
    def __init__(self):
        pass

class DataTransformation:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        try:
        
           pass

        except Exception as e:
            logging.info('Exception occured in data ingestion component')   
            raise CustomException(e, sys)