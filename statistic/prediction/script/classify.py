"""classify models in sklearn, provide training and predicting methods"""
import os
import sys
import numpy
from sklearn.metrics import accuracy_score

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
import config
from util import get_model_name


def classify_train(x_train, x_test, y_train, y_test, test_data):
    # classify
    print("-----classify_train-----")
    for model in config.classify_models:
        model.fit(x_train, y_train)

        # predict
        expected = y_test
        predicted = model.predict(x_test)
        test_data[get_model_name(model)] = predicted + 1
        test_data[get_model_name(model) + "_is_right"] = (predicted + 1) == test_data["Class"]

        # evaluate
        accuracy_val = accuracy_score(expected, predicted)
        print("%s:\naccuracy = %.2f%%\n" % (get_model_name(model), accuracy_val * 100))
        config.model2accuracy[get_model_name(model)] = accuracy_val


def classify_predict(x_data):
    x_data = x_data.values
    result = {}
    for model in config.classify_models:
        predicted = list(numpy.ndarray.astype(model.predict(x_data) + 1, dtype=int))
        result[get_model_name(model)] = predicted
    return result
