"""provide methods for training and prediction"""
import os
import sys
import pandas

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
import data_loader
import feature_importance
from classify import *
from regression import *
from numpy import nan


def train_models():
    if config.is_trained:
        return

    data_loader.init_onehot_features()

    feature_importance.calculate_feature_importance()
    feature_importance.calculate_correlation()

    feature_importance.frequency_selection()
    feature_importance.chi_selection()

    data = data_loader.load_data_raw(config.training_data_path, transform=False)
    # train data and test data
    x_features = list(data.columns.values)
    x_features.remove("Class")
    x = data[x_features].values
    y = data["Class"].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=None, train_size=0.8)

    train_data = pandas.DataFrame(x_train.copy(), index=range(x_train.shape[0]), columns=config.all_features)
    train_data["Class"] = y_train.copy()
    test_data = pandas.DataFrame(x_test.copy(), index=range(x_test.shape[0]), columns=config.all_features)
    test_data["Class"] = y_test.copy()
    config.train_set = train_data
    config.test_set = test_data

    x_train = data_loader.load_data_onehot(x_train, load_class=False).values
    x_test = data_loader.load_data_onehot(x_test, load_class=False).values
    y_train = y_train - 1
    y_test = y_test - 1

    # train
    classify_train(x_train, x_test, y_train, y_test, test_data)
    regression_train(x_train, x_test, y_train, y_test, test_data)

    config.is_trained = True
    train_data.to_csv(config.train_data_path, index=True, index_label="id")
    test_data.to_csv(config.test_data_path, index=True, index_label="id")


# print result
# single result is a number
# batch result is an array
def __show_result(result):
    classify_result = result[0]
    regression_result = result[1]
    print("-----classify_result-----")
    for r in classify_result.keys():
        print("%-27s:" % r)
        print(classify_result[r])
    print("-----regression_result-----")
    for r in regression_result.keys():
        print("%-27s:" % r)
        print(regression_result[r])
    print("Finaly result is:")
    print(result[2])


def __cal_final_result(result):
    class2weight = {1: [], 2: [], 3: []}
    std_num = result.values().__iter__().__next__().__len__()
    for stu_id in range(std_num):
        for key in result.keys():
            for i in range(1, 4):
                class2weight[i].append(0)
            class2weight[result[key][stu_id]][stu_id] += config.model2accuracy[key]
    final_result = []
    for stu_id in range(std_num):
        max_index = None
        max_weight = 0
        for key in class2weight.keys():
            if max_weight < class2weight[key][stu_id]:
                max_index = key
                max_weight = class2weight[key][stu_id]
        final_result.append(max_index)
    return final_result


# return result predicted by classifiers and regressors respectively
def __predict(data):
    result_c, result_r = classify_predict(data), regression_predict(data)
    result = __cal_final_result({**result_c, **result_r})
    return result_c, result_r, result


def __fill_data(x_data):
    return x_data.fillna(0)


# predict one student's class according to given info, which is passed as args
def predict_single_student(gender=nan,
                           Nationality=nan,
                           PlaceofBirth=nan,
                           StageID=nan,
                           GradeID=nan,
                           SectionID=nan,
                           Topic=nan,
                           Semester=nan,
                           Relation=nan,
                           raisedhands=nan,
                           VisitedResources=nan,
                           AnnouncementsView=nan,
                           Discussion=nan,
                           ParentAnsweringSurvey=nan,
                           ParentschoolSatisfaction=nan,
                           StudentAbsenceDays=nan):
    if not config.is_trained:
        raise Exception("Model isn't trained yet!")
    if pandas.isnull(StudentAbsenceDays) or pandas.isnull(VisitedResources) or \
            pandas.isnull(raisedhands) or pandas.isnull(Discussion) or \
            pandas.isnull(AnnouncementsView):
        raise Exception("Must input StudentAbsenceDays, VisitedResources,"
                        "raisedHands AnnouncementsView and Discussion, "
                        "otherwise prediction is meaningless!")

    columns = config.discrete_features + config.continuous_features

    data = pandas.DataFrame([[gender, Nationality, PlaceofBirth,
                              nan if pandas.isnull(GradeID) else int(GradeID[2:4]),
                              SectionID, Topic, Semester, Relation,
                              nan if pandas.isnull(raisedhands) else int(raisedhands),
                              nan if pandas.isnull(VisitedResources) else int(VisitedResources),
                              nan if pandas.isnull(AnnouncementsView) else int(AnnouncementsView),
                              nan if pandas.isnull(Discussion) else int(Discussion),
                              ParentAnsweringSurvey, ParentschoolSatisfaction,
                              StudentAbsenceDays]], columns=config.all_features)
    data = data[columns]
    data = pandas.get_dummies(data, columns=config.discrete_features)
    data = data_loader.fix_data(data)
    data = __fill_data(data)
    result = __predict(data)
    # __show_result(result)
    data["predicting_class"] = numpy.asarray(result[2], dtype=int)
    return result, data


# predict a batch of students' class, info is passed as path of .csv
def predict_batch_student(data_path):
    if not config.is_trained:
        raise Exception("Model isn't trained yet!")
    data = data_loader.load_data_onehot(data_path, load_class=False)
    if data["StudentAbsenceDays_Under-7"].isnull().any() or \
            data["VisitedResources"].isnull().any() or \
            data["raisedhands"].isnull().any() or \
            data["Discussion"].isnull().any() or \
            data["AnnouncementsView"].isnull().any():
        raise Exception("Must input StudentAbsenceDays, VisitedResources,"
                        "raisedHands AnnouncementsView and Discussion, "
                        "otherwise prediction is meaningless!")
    data = __fill_data(data)
    result = __predict(data)
    # __show_result(result)
    data["predicting_class"] = numpy.asarray(result[2], dtype=int)
    return result, data
