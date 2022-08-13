"""global variables and parameters shared by all modules"""
import numpy
import pandas
from sklearn.ensemble import *

training_data_path = "statistic/prediction/data/training_data.csv"
test_data_path = "statistic/prediction/data/test.csv"

is_trained = False

# all kinds of features
usecols = [
    "gender",
    "Nationality",
    "PlaceofBirth",
    "GradeID",
    "SectionID",
    "Topic",
    "Semester",
    "Relation",
    "raisedhands",
    "VisitedResources",
    "AnnouncementsView",
    "Discussion",
    "ParentAnsweringSurvey",
    "ParentschoolSatisfaction",
    "StudentAbsenceDays",
    "Class"
]
all_features = usecols.copy()
all_features.remove("Class")
features = usecols.copy()
features.remove("Class")
discrete_features = features.copy()
continuous_features = ["raisedhands", "VisitedResources",
                       "AnnouncementsView", "Discussion", "GradeID"]
for feature in continuous_features:
    discrete_features.remove(feature)
onehot_features = []

# for continuous features, we need to segment them to make sure they won't dominate model
feature2segment_len = {
    "raisedhands": 10,
    "VisitedResources": 20,
    "AnnouncementsView": 20,
    "Discussion": 10,
    "GradeID": 4,
}


# drop feature utterly after feature selection
def drop_feature(feature):
    if usecols.__contains__(feature):
        usecols.remove(feature)
    if features.__contains__(feature):
        features.remove(feature)
    if discrete_features.__contains__(feature):
        discrete_features.remove(feature)
    if continuous_features.__contains__(feature):
        continuous_features.remove(feature)
    if onehot_features.__contains__(feature):
        onehot_features.remove(feature)


# for debug printing
pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 30)
numpy.set_printoptions(threshold=numpy.Inf)


# all models
classify_models = [RandomForestClassifier(n_estimators=1000, class_weight="balanced", max_depth=18),
                   AdaBoostClassifier(n_estimators=100, base_estimator=RandomForestClassifier(n_estimators=100, class_weight="balanced", max_depth=18)),
                   GradientBoostingClassifier(n_estimators=1000, max_depth=18),
                   ExtraTreesClassifier(n_estimators=1000, max_depth=18),
                   ]
regression_models = [RandomForestRegressor(n_estimators=1000, max_depth=18),
                     AdaBoostRegressor(n_estimators=100, base_estimator=RandomForestRegressor(n_estimators=10, max_depth=18)),
                     GradientBoostingRegressor(n_estimators=1000, max_depth=18),
                     ExtraTreesRegressor(n_estimators=1000, max_depth=18),
                     ]
models = classify_models + regression_models


# all kinds of result
feature2chi2_p_value = {}  # feature_importance
model2accuracy = {}        # accuracy of each model
corr = None                # used to draw correlation matrix
