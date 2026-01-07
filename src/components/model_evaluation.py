import os
import sys
import mlflow
import mlflow.sklearn


from dataclasses import dataclass
import numpy as np
import pickle
from src.utils.utils import load_object
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from src.logger.logger import logging
from src.exception. exception import CustomException



@dataclass
class ModelEvaluation:
    def __init__(self):
        logging.info("Model Evaluation Config initiated")

    def eval_metrices(self,actual,pred):
        rmse=np.sqrt(mean_squared_error(actual,pred))
        mae=mean_absolute_error(actual,pred)
        r2=r2_score(actual,pred)
        logging.info(f"Model Evaluation Metrics: RMSE: {rmse}, MAE: {mae}, R2: {r2}")
        return rmse,mae,r2
    
    def initiate_model_evaluation(self,train_array,test_arry):
        try:
            
            X_test,y_test= test_arry[:,:-1],test_arry[:,-1]

           
            model_path=os.path.join("artifacts","model.pkl")

           
            model=load_object(model_path)

         
            #mlflow.set_registry_uri("")
            logging.info("MLflow registry uri set")
            tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme
            print(tracking_url_type_store)

            with mlflow.start_run():
               prediction=model.predict(X_test)
               (rmse,mae,r2)=self.eval_metrices(y_test,prediction)
               mlflow.log_metric("rmse",rmse)
               mlflow.log_metric("mae",mae)
               mlflow.log_metric("r2",r2)
                 

             # Model registry does not work with file store
               if tracking_url_type_store != "file":

                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
               else:
                    mlflow.sklearn.log_model(model, "model")

        except Exception as e:
            raise CustomException(e,sys)