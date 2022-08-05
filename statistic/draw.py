import pandas as pd
from pyecharts.charts import Bar, Pie, Radar, Line, HeatMap
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pandas import DataFrame


# 饼图
def draw_pie(data: DataFrame, key_name: str, title=None, save_filename="pie.html"):
    data = dict(data[key_name].value_counts())
    keys = pd.DataFrame(data.keys())
    values = pd.DataFrame(data.values())
    data = list(zip(keys[0].tolist(), values[0].tolist()))
    if title is None:
        title = key_name + " statistic"
    pie = (
        Pie(
            init_opts=opts.InitOpts(bg_color="white")
        )
            .add(key_name, data, center=["42%", "52%"])
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical",
                                                         pos_top="8%"),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                 save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                 data_zoom=None, restore=None, magic_type=None)))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )
    pie.render(save_filename)


# 条形图
def draw_bar(data: DataFrame, key_name: str, group_by=None, use_stack=False, reverse=False, title=None, mark_dict=None,
             save_filename="bar.html"):
    if title is None:
        title = key_name + " statistic"
    mark_line_data, mark_point_data = parse_mark_dict(mark_dict)
    if group_by is None:
        data = dict(data[key_name].value_counts())
        keys = pd.DataFrame(data.keys())[0].tolist()
        values = pd.DataFrame(data.values())[0].tolist()
        bar = (
            Bar(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(keys)
                .add_yaxis("", values, category_gap="35%", markline_opts=opts.MarkLineOpts(data=mark_line_data),
                           markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
                                 toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                     save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                     data_zoom=None, restore=None, magic_type=opts.ToolBoxFeatureMagicTypeOpts(
                                         type_=("line", "bar")))))
        )
        if reverse:
            bar.reversal_axis()
            bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
        bar.render(save_filename)
    else:
        group_keys = pd.DataFrame(dict(data[group_by].value_counts()).keys())[0].tolist()
        tot_data = {}
        sum_dict = dict(data[key_name].value_counts())
        keys = list(sum_dict.keys())
        for group_key in group_keys:
            temp = dict(data[data[group_by] == group_key][key_name].value_counts())
            t = []
            for k in keys:
                if temp.get(k) is None:
                    v = 0
                else:
                    v = int(temp[k])
                t.append({"value": v, "percent": v / sum_dict[k]})
            tot_data[group_key] = t
        bar = (
            Bar(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(keys)
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
                                 toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                     save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                     data_zoom=None, restore=None)))
        )
        if use_stack:
            for k, v in tot_data.items():
                bar.add_yaxis(k, v, stack="s1", category_gap="50%",
                              markline_opts=opts.MarkLineOpts(data=mark_line_data),
                              markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
            if reverse:
                bar.reversal_axis()
                bar.set_series_opts(label_opts=opts.LabelOpts(position="top", formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}")))
            else:
                bar.set_series_opts(label_opts=opts.LabelOpts(position="right", formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}")))
        else:
            for k, v in tot_data.items():
                bar.add_yaxis(k, v, category_gap="30%", markline_opts=opts.MarkLineOpts(data=mark_line_data),
                              markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
            if reverse:
                bar.reversal_axis()
                bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
        bar.render(save_filename)


# 雷达图
def draw_radar(data: DataFrame, pks: list, keyname_and_max: dict, title=None, save_filename="radar.html"):
    schema = []
    for k, v in keyname_and_max.items():
        schema.append({"name": k, "max": v})
    if title is None:
        title = "students radar"
    radar = (
        Radar(
            init_opts=opts.InitOpts(bg_color="white")
        )
            .add_schema(schema)
            .set_global_opts(title_opts=opts.TitleOpts(title=title), legend_opts=opts.LegendOpts(),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                 save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                 data_zoom=None, restore=None, magic_type=None)))
    )
    for i in pks:
        temp = list(map(int, [data.iloc[i][k] for k in keyname_and_max.keys()]))
        radar.add("student " + str(i), [{"value": temp, "name": "student " + str(i)}])
    radar.render(save_filename)


# 折线图
def draw_line(data: DataFrame, key_name: str, group_by=None, title=None, mark_dict=None, save_filename="line.html"):
    if title is None:
        title = key_name + " statistic"
    mark_line_data, mark_point_data = parse_mark_dict(mark_dict)
    if group_by is None:
        data = dict(data[key_name].value_counts())
        keys = pd.DataFrame(data.keys())[0].tolist()
        values = pd.DataFrame(data.values())[0].tolist()
        line = (
            Line(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(keys)
                .add_yaxis("", values,
                           markline_opts=opts.MarkLineOpts(data=mark_line_data),
                           markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
                                 toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                     save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                     data_zoom=None, restore=None, magic_type=opts.ToolBoxFeatureMagicTypeOpts(
                                         type_=("line", "bar")))))
        )
    else:
        group_keys = pd.DataFrame(dict(data[group_by].value_counts()).keys())[0].tolist()
        tot_data = {}
        sum_dict = dict(data[key_name].value_counts())
        keys = list(sum_dict.keys())
        for group_key in group_keys:
            temp = dict(data[data[group_by] == group_key][key_name].value_counts())
            temp = [int(temp[k]) for k in keys]
            tot_data[group_key] = temp
        line = (
            Line(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(keys)
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
                                 toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                     save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                     data_zoom=None, restore=None, magic_type=opts.ToolBoxFeatureMagicTypeOpts(
                                         type_=("line", "bar")))))
        )
        for k, v in tot_data.items():
            line.add_yaxis("", v, markline_opts=opts.MarkLineOpts(data=mark_line_data),
                           markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
    line.render(save_filename)


def parse_mark_dict(mark_dict: dict):
    mark_line_data = []
    if mark_dict["average"]:
        mark_line_data.append(opts.MarkLineItem(type_="average", name="平均值"))
    mark_point_data = []
    if mark_dict["max"]:
        mark_point_data.append(opts.MarkPointItem(type_="max", name="最大值"))
    if mark_dict["min"]:
        mark_point_data.append(opts.MarkPointItem(type_="min", name="最小值"))
    return mark_line_data, mark_point_data
