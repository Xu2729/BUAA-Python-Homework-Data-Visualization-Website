"""regression models in sklearn, provide training and predicting methods"""
import os
import sys
import numpy
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
import config
from util import get_model_name


def regression_train(data):
    # train data and test data
    all_features = list(data.columns.values)
    all_features.remove("Class")
    x = data[all_features].values
    y = data["Class"].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0, train_size=0.8)

    # regression
    print("-----regression_train-----")
    for model in config.regression_models:
        model.fit(x_train, y_train)

        # predict
        expected = y_test
        predicted = model.predict(x_test)
        for i in range(predicted.__len__()):
            predicted[i] = int(round(predicted[i]))

        # evaluate
        accuracy_val = accuracy_score(expected, predicted)
        config.model2accuracy[get_model_name(model)] = accuracy_val
        print("%s:\naccuracy = %.2f%%\n" % (get_model_name(model), accuracy_val * 100))


def regression_predict(x_data):
    x_data = x_data.values
    result = {}
    for model in config.regression_models:
        predicted = model.predict(x_data)
        for i in range(predicted.__len__()):
            predicted[i] = int(round(predicted[i])) + 1
        predicted = list(numpy.ndarray.astype(predicted, int))
        result[get_model_name(model)] = predicted
    return result
