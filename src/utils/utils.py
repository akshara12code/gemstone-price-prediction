import os
import sys
import pickle
import numpy as np
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
        for i in range(len(models)):
            model = list(models.values())[i]
            # Train model
            model.fit(X_train, y_train)
            
            # Predict Testing data
            y_test_pred = model.predict(X_test)
            
            # Get R2 scores for test data
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score
            
        return report
        
    except Exception as e:
        logging.error('Exception occurred during model training')
        raise customexception(e, sys)
    
def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, 'rb') as file_obj:
            obj = pickle.load(file_obj)
            
        logging.info(f"Object loaded successfully from {file_path}")
        return obj
        
    except Exception as e:
        logging.error(f'Exception Occurred in load_object function: {str(e)}')
        raise customexception(e, sys)
