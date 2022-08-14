import os
import sys
from pyecharts.charts import Bar, HeatMap
from pyecharts import options as opts

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from visualization import get_feature_importance, get_model_accuracy, get_correlation_matrix


def get_feature_importance_axis():
    _, axis, _, _, _ = get_feature_importance()
    return axis


def get_feature_importance_list():
    _, _, _, ans, _ = get_feature_importance()
    return ans


def get_accuracy_axis():
    _, axis, _, _, _ = get_model_accuracy()
    return axis


def get_accuracy_list():
    _, _, _, ans, _ = get_model_accuracy()
    return ans


def get_corr_mat():
    _, _, _, mat = get_correlation_matrix()
    return mat


def get_corr_axis():
    _, axis, _, _ = get_correlation_matrix()
    return axis


def _mat2data(mat):
    data = []
    for i in range(5):
        for j in range(5):
            data.append([i, j, round(float(mat[4 - j][i]), 5)])
    return data


def draw_heatmap():
    axis = get_corr_axis()
    mat = get_corr_mat()
    data = _mat2data(mat)
    heatmap = (
        HeatMap(
            init_opts=opts.InitOpts(bg_color="white", width="950px")
        )
            .add_xaxis(axis)
            .add_yaxis("", axis, data, label_opts=opts.LabelOpts(is_show=True, position="inside"))
            .set_global_opts(title_opts=opts.TitleOpts(title="Correlation Matrix of Numeric Features"),
                             xaxis_opts=opts.AxisOpts(
                                 axislabel_opts=opts.LabelOpts(font_size=9, margin=7)),
                             yaxis_opts=opts.AxisOpts(
                                 axislabel_opts=opts.LabelOpts(font_size=9, margin=1)),
                             visualmap_opts=opts.VisualMapOpts(min_=0, max_=1, is_calculable=True, pos_right="5%"),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                 save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                 data_zoom=None, restore=None, magic_type=None)))
    )
    heatmap.set_series_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(margin=3, font_size=10, rotate=-15)))
    heatmap.render("statistic/templates/Heatmap.html")


def draw_model_accuracy():
    x_axis = get_accuracy_axis()
    y_axis = get_accuracy_list()
    y_axis = list(map(lambda x: round(float(x), 5), y_axis))
    bar = (
        Bar(
            init_opts=opts.InitOpts(bg_color="white", width="970px")
        )
            .add_xaxis(x_axis)
            .add_yaxis("", y_axis, category_gap="30%",
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="average")]))
            .set_global_opts(title_opts=opts.TitleOpts(title="Model-Accuracy"),
                             yaxis_opts=opts.AxisOpts(
                                 axislabel_opts=opts.LabelOpts(font_size=7.2, margin=1)),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                 save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                 data_zoom=None, restore=None, magic_type=None)))
    )
    bar.reversal_axis()
    bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
    bar.render("statistic/templates/Model-Accuracy.html")


def draw_feature_importance():
    x_axis = get_feature_importance_axis()
    y_axis = get_feature_importance_list()
    y_axis = list(map(lambda x: round(float(x), 5), y_axis))
    bar = (
        Bar(
            init_opts=opts.InitOpts(bg_color="white", height="900px", width="970px")
        )
            .add_xaxis(x_axis)
            .add_yaxis("", y_axis, category_gap="20%",
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="average")]))
            .set_global_opts(title_opts=opts.TitleOpts(title="Features-Chi square test p-value"),
                             legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical",
                                                         pos_top="8%"),
                             yaxis_opts=opts.AxisOpts(
                                 axislabel_opts=opts.LabelOpts(position="right", font_size=6.6, margin=1,
                                                               distance="15%")),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                 save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                 data_zoom=None, restore=None, magic_type=None)))
    )
    bar.reversal_axis()
    bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    bar.render("statistic/templates/Feature_importance.html")
