import os
import sys
from unittest import mock

sys.path.insert(0, r"C:\Users\mvuyiso.gqwaru\OneDrive - Wabtec Corporation\Documents\MLOps\Krish Naik - End to End")

import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
import dill
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
    logging.info("A file was saved")


def evaluate_model(X_train, y_train, X_test, 
                   y_test, models, params):
    try:

        report={}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]

            gs =  GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            #mae = mean_absolute_error(y_train, y_train_pred)
            #mse = mean_squared_error(y_train, y_train_pred)
            #rmse = np.sqrt(mean_squared_error(y_train, y_train_pred)
                
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = (test_model_score)

        return report
    
    except Exception as e:
        raise CustomException(e,sys)
