"""provide methods to load data in different ways"""
import os
import sys
import numpy
import pandas
from numpy import nan

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
import config


# divide continuous feature into segments
# eg: 0~100 -> 0-4, representing [0:20) [20:40) ... [80,100) respectively
def segment(data):
    for feature in config.continuous_features:
        segment_len = config.feature2segment_len[feature]
        max_label = max(data[feature].values)
        for i in range(len(data[feature].values)):
            if max_label % segment_len == 0 and data[feature].values[i] == max_label:
                data[feature].values[i] = max_label // segment_len - 1
            else:
                data[feature].values[i] //= segment_len
    return data


# load .csv, only change GradeID into number and Class into {0, 1, 2}
def load_data_raw(data_path, load_class=True):
    usecols = config.usecols.copy()
    if not load_class:
        usecols.remove("Class")
    data = pandas.read_csv(data_path,
                           delimiter=",",
                           usecols=usecols,
                           engine="c",
                           converters={
                               "GradeID": lambda x: nan if pandas.isnull(x) else int(x[2:4]),
                               "Class": lambda x: int(int(x) - 1)
                           })
    return data.sort_index(axis=1)


# fill out labels of data that isn't in config.onehot_features + config.continuous_features
# add labels of config.onehot_features that isn't in data to data
# added columns will be all zeros
def fix_data(data):
    dropped_features = []
    for feature in data.columns:
        if not config.continuous_features.__contains__(feature) and \
                not config.onehot_features.__contains__(feature) and \
                not feature == "Class":
            dropped_features.append(feature)
    for feature in dropped_features:
        data = data.drop(feature, axis=1)
    for feature in config.onehot_features:
        if not data.columns.__contains__(feature):
            flag = True
            for f in data.columns:
                if feature[0:3] == f[0:3]:
                    data[feature] = 0
                    flag = False
                    break
            if flag:
                data[feature] = numpy.nan
    return data.sort_index(axis=1)


# load .csv data, with discrete features in onehot form,
# load_class is False when loading test data
def load_data_onehot(data_path, load_class=True):
    labels = config.discrete_features + config.continuous_features
    if load_class:
        labels.append("Class")
    original_data = segment(load_data_raw(data_path, load_class))[labels]
    discrete_features = list(set(config.discrete_features) & set(original_data.columns))
    onehot_data = pandas.get_dummies(original_data, columns=discrete_features)
    return fix_data(onehot_data)


# initialize onehot features list in config
def init_onehot_features():
    data = segment(load_data_raw(config.training_data_path))[
        config.discrete_features + config.continuous_features + ["Class"]]
    data = pandas.get_dummies(data, columns=config.discrete_features)
    for feature in data.columns:
        if not config.continuous_features.__contains__(feature) and not feature == "Class":
            config.onehot_features.append(feature)
