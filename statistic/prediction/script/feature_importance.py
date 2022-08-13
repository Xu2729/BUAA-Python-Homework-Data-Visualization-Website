"""provide methods to evaluate feature importance and fill out unimportant features"""
import os
import sys
from scipy.stats import chi2_contingency
import numpy

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
import config
import data_loader


# if the number of students with a certain feature is less than 2, drop that feature
def frequency_selection():
    data = data_loader.load_data_onehot(config.training_data_path)
    for feature in config.onehot_features:
        if sum(data[feature]) < 5:
            # print("drop %-30s: frequency = %d" % (feature, sum(data[feature])))
            config.drop_feature(feature)


# used to fill out onehot features
def chi_selection():
    data = data_loader.load_data_onehot(config.training_data_path)
    col_n = 3
    dropped_features = []
    for feature in config.onehot_features + config.continuous_features:
        row_n = max(data[feature].values) + 1
        kf_data = numpy.zeros(shape=(row_n, col_n), dtype=int)
        for i in range(len(data[feature].values)):
            kf_data[data[feature].values[i]][data["Class"].values[i]] += 1
        kf = chi2_contingency(kf_data)
        if kf[1] > 0.02:
            dropped_features.append(feature)
            # print('%-30s: p-value = %.3f' % (feature, kf[1]))
    for feature in dropped_features:
        config.drop_feature(feature)


# feature importance is evaluated by p-value of chi2 test
def calculate_feature_importance():
    data = data_loader.load_data_onehot(config.training_data_path)
    col_n = 3
    for feature in config.onehot_features + config.continuous_features:
        row_n = max(data[feature].values) + 1
        kf_data = numpy.zeros(shape=(row_n, col_n), dtype=int)
        for i in range(len(data[feature].values)):
            kf_data[data[feature].values[i]][data["Class"].values[i]] += 1
        kf = chi2_contingency(kf_data)
        config.feature2chi2_p_value[feature] = numpy.log10(kf[1])


# correlation matrix between continuous features
def calculate_correlation():
    data = data_loader.load_data_raw(config.training_data_path)[config.continuous_features]
    config.corr = numpy.asarray(data.corr(), dtype=float)
