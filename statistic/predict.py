from statistic.prediction.script.model import predict_single_student


def predict_class(para_dict: dict):
    result, _ = predict_single_student(**para_dict)
    methods_1 = ["RandomForestClassifier", "AdaBoostClassifier", "GradientBoostingClassifier", "ExtraTreesClassifier"]
    methods_2 = ["RandomForestRegressor", "AdaBoostRegressor", "GradientBoostingRegressor", "ExtraTreesRegressor"]
    res = {}
    for k in methods_1:
        res[k] = _num2class(int(result[0][k][0]))
    for k in methods_2:
        res[k] = _num2class(int(result[1][k][0]))
    res["IntegratedForecast"] = _num2class(int(result[2][0]))
    return res


def _num2class(num: int) -> str:
    if num == 1:
        return "Poor"
    elif num == 2:
        return "Average"
    elif num == 3:
        return "Excellent"
    else:
        return "UNKNOWN"
