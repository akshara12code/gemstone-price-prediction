import os
import sys

# Fix numpy._core issue
import numpy
if not hasattr(numpy, '_core'):
    import numpy.core as _core
    numpy._core = _core

import pickle
import pandas as pd
from src.logger.logger import logging
from src.exception.exception import CustomException as customexception
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

import warnings
warnings.filterwarnings('ignore')

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        
        logging.info(f"Object saved successfully at {file_path}")
            
    except Exception as e:
        logging.error(f"Error in save_object: {str(e)}")
        raise customexception(e, sys)

def evaluate_model(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        
        for model_name, model in models.items():
            model.fit(X_train, y_train)
            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)
            report[model_name] = test_model_score
            
        return report
        
    except Exception as e:
        logging.error(f'Exception occurred during model training: {str(e)}')
        raise customexception(e, sys)

def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            error_msg = f"File not found: {file_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        with open(file_path, 'rb') as file_obj:
            obj = pickle.load(file_obj)
            
        logging.info(f"Object loaded successfully from {file_path}")
        return obj
        
    except Exception as e:
        logging.error(f'Exception occurred in load_object: {str(e)}')
        raise customexception(e, sys)
