import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from src.exception import CustomException
from src.logger import logging
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        logging.info("Saving object")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        logging.info("Error in saving object")
        raise CustomException(e, sys)
    

def evaluate_models(X_train, y_train, X_test, y_test, models, parameters):
    try:
        logging.info("Evaluating models")
        report = {}

        for model_name, model in models.items():

            param = parameters[model_name]

            gs = GridSearchCV(
                estimator=model,
                param_grid=param,
                cv=3,
                scoring="r2"
            )

            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)

            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        logging.info("Error in evaluating models")
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
