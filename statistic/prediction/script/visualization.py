"""provide data for visualization"""
import os
import sys

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
import config


def __dict2list(d):
    x = []
    y = []
    for key in d.keys():
        x.append(key)
        y.append(d[key])
    return x, y


def get_feature_importance():
    x, y = __dict2list(config.feature2chi2_p_value)
    return "Features-Chi square test p-value", x, "Features", y, "p-value"


def get_model_accuracy():
    x, y = __dict2list(config.model2accuracy)
    return "Model-Accuracy", x, "Model", y, "Accuracy"


def get_correlation_matrix():
    continuous_features = config.continuous_features.copy()
    if not continuous_features.__contains__("GradeID"):
        continuous_features.append("GradeID")
    return "Correlation Matrix of Numeric Features", \
           continuous_features, \
           continuous_features, \
           config.corr
