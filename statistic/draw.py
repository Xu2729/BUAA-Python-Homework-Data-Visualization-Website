import pandas as pd
from pyecharts.charts import Bar, Pie, Radar, Line, Page
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pandas import DataFrame


# 饼图
def draw_pie(data: DataFrame, key_name: str, group_by=None, title=None, save_filename="pie.html"):
    if title is None:
        title = key_name + " statistic"
    global_opts_dict = {"toolbox_opts": opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
        save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None, data_zoom=None, restore=None,
        magic_type=None))}
    series_opts_dict = {"label_opts": opts.LabelOpts(formatter="{b}: {c} ({d}%)")}
    if group_by is None:
        data = dict(data[key_name].value_counts())
        keys = pd.DataFrame(data.keys())
        values = pd.DataFrame(data.values())
        data = list(zip(keys[0].tolist(), values[0].tolist()))
        global_opts_dict["title_opts"] = opts.TitleOpts(title=title)
        pie = _make_pie(key_name, data, global_opts_dict, series_opts_dict)
        pie.render(save_filename)
    else:
        page = Page()
        group_keys = pd.DataFrame(dict(data[group_by].value_counts()).keys())[0].tolist()
        group_keys.sort()
        for group_key in group_keys:
            global_opts_dict["title_opts"] = opts.TitleOpts(title=title + " {}={}".format(group_by, group_key))
            temp_data = data[data[group_by] == group_key]
            temp_data = dict(temp_data[key_name].value_counts())
            keys = pd.DataFrame(temp_data.keys())
            values = pd.DataFrame(temp_data.values())
            temp_data = list(zip(keys[0].tolist(), values[0].tolist()))
            pie = _make_pie(key_name, temp_data, global_opts_dict, series_opts_dict)
            page.add(pie)
        page.render(save_filename)


def _make_pie(key_name, data, global_set: dict, series_set: dict) -> Pie:
    pie = (
        Pie(
            init_opts=opts.InitOpts(bg_color="white")
        )
            .add(key_name, data, center=["42%", "52%"])
    )
    if len(data) > 5:
        global_set["legend_opts"] = opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical",
                                                    pos_top="8%")
    pie.set_global_opts(**global_set)
    pie.set_series_opts(**series_set)
    return pie


def _make_frequency_histogram_data(data: DataFrame, key_name: str, space: int):
    arr_x = []
    arr_y = []
    max_ = data[key_name].max()
    min_ = data[key_name].min()
    i = min_
    while not i <= max_ < i + space:
        arr_x.append("[{},{})".format(i, i + space))
        temp_data = data[data[key_name].apply(lambda x: i <= x < i + space)]
        arr_y.append(int(temp_data[key_name].count()))
        i += space
    arr_x.append("[{},{}]".format(i, max_))
    temp_data = data[data[key_name].apply(lambda x: i <= x <= max_)]
    arr_y.append(int(temp_data[key_name].count()))
    return arr_x, arr_y


# 频率直方图
def draw_frequency_histogram(data: DataFrame, key_name: str, space=5, group_by=None, title=None, mark_dict=None,
                             save_filename="frequency_histogram.html"):
    if title is None:
        title = key_name + " statistic"
    global_opts_dict = {"datazoom_opts": opts.DataZoomOpts(),
                        "toolbox_opts": opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                            save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                            data_zoom=None, restore=None, magic_type=None))}
    mark_line_data, mark_point_data = _parse_mark_dict(mark_dict)
    if group_by is None:
        arr_x, arr_y = _make_frequency_histogram_data(data, key_name, space)
        global_opts_dict["title_opts"] = opts.TitleOpts(title=title)
        bar = (
            Bar(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(arr_x)
                .add_yaxis("", arr_y, category_gap="0%", markline_opts=opts.MarkLineOpts(data=mark_line_data),
                           markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
        )
        bar.set_global_opts(**global_opts_dict)
        bar.render(save_filename)
    else:
        page = Page()
        group_keys = pd.DataFrame(dict(data[group_by].value_counts()).keys())[0].tolist()
        group_keys.sort()
        sum_dict = dict(data[key_name].value_counts())
        keys = list(sum_dict.keys())
        keys.sort()
        for group_key in group_keys:
            global_opts_dict["title_opts"] = opts.TitleOpts(title=title + ": {}={}".format(group_by, group_key))
            temp_data = data[data[group_by] == group_key]
            arr_x, arr_y = _make_frequency_histogram_data(temp_data, key_name, space)
            bar = (
                Bar(
                    init_opts=opts.InitOpts(bg_color="white")
                )
                    .add_xaxis(arr_x)
                    .add_yaxis(group_key, arr_y, category_gap="0%",
                               markline_opts=opts.MarkLineOpts(data=mark_line_data),
                               markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
            )
            bar.set_global_opts(**global_opts_dict)
            page.add(bar)
        page.render(save_filename)


# 条形图
def draw_bar(data: DataFrame, key_name: str, group_by=None, use_stack=False, reverse=False, title=None, mark_dict=None,
             save_filename="bar.html"):
    if title is None:
        title = key_name + " statistic"
    mark_line_data, mark_point_data = _parse_mark_dict(mark_dict)
    global_opts_dict = {"xaxis_opts": opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
                        "title_opts": opts.TitleOpts(title=title)}
    if group_by is None:
        global_opts_dict["toolbox_opts"] = opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
            save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
            data_zoom=None, restore=None, magic_type=opts.ToolBoxFeatureMagicTypeOpts(
                type_=("line", "bar"))))
        data = dict(data[key_name].value_counts())
        keys = pd.DataFrame(data.keys())[0].tolist()
        keys.sort()
        values = [int(data.get(k, 0)) for k in keys]
        bar = (
            Bar(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(keys)
                .add_yaxis("", values, category_gap="15%", markline_opts=opts.MarkLineOpts(data=mark_line_data),
                           markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
        )
        if len(keys) > 5:
            global_opts_dict["datazoom_opts"] = opts.DataZoomOpts()
            global_opts_dict["legend_opts"] = opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical",
                                                              pos_top="8%", item_gap=3)
        bar.set_global_opts(**global_opts_dict)
        if reverse:
            bar.reversal_axis()
            bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
    else:
        global_opts_dict["toolbox_opts"] = opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
            save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
            data_zoom=None, restore=None))
        group_keys = pd.DataFrame(dict(data[group_by].value_counts()).keys())[0].tolist()
        group_keys.sort()
        tot_data = {}
        sum_dict = dict(data[key_name].value_counts())
        keys = list(sum_dict.keys())
        keys.sort()
        for group_key in group_keys:
            temp = dict(data[data[group_by] == group_key][key_name].value_counts())
            t = []
            for k in keys:
                v = int(temp.get(k, 0))
                t.append({"value": v, "percent": v / sum_dict[k]})
            tot_data[group_key] = t
        bar = (
            Bar(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(keys)
        )
        if len(keys) > 5:
            global_opts_dict["datazoom_opts"] = opts.DataZoomOpts()
            global_opts_dict["legend_opts"] = opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical",
                                                              pos_top="8%", item_gap=3)
        bar.set_global_opts(**global_opts_dict)
        if use_stack:
            for k, v in tot_data.items():
                bar.add_yaxis(k, v, stack="s1", category_gap="40%",
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
                bar.add_yaxis(k, v, category_gap="15%", markline_opts=opts.MarkLineOpts(data=mark_line_data),
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
    mark_line_data, mark_point_data = _parse_mark_dict(mark_dict)
    global_opts_dict = {"xaxis_opts": opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
                        "title_opts": opts.TitleOpts(title=title),
                        "toolbox_opts": opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                            save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                            data_zoom=None, restore=None, magic_type=opts.ToolBoxFeatureMagicTypeOpts(
                                type_=("line", "bar"))))}
    if group_by is None:
        data = dict(data[key_name].value_counts())
        keys = pd.DataFrame(data.keys())[0].tolist()
        keys.sort()
        values = [int(data.get(k, 0)) for k in keys]
        line = (
            Line(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(keys)
                .add_yaxis("", values,
                           markline_opts=opts.MarkLineOpts(data=mark_line_data),
                           markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
        )
    else:
        group_keys = pd.DataFrame(dict(data[group_by].value_counts()).keys())[0].tolist()
        group_keys.sort()
        tot_data = {}
        sum_dict = dict(data[key_name].value_counts())
        keys = list(sum_dict.keys())
        keys.sort()
        for group_key in group_keys:
            temp = dict(data[data[group_by] == group_key][key_name].value_counts())
            temp = [int(temp.get(k, 0)) for k in keys]
            tot_data[group_key] = temp
        line = (
            Line(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(keys)
        )
        for k, v in tot_data.items():
            line.add_yaxis("", v, markline_opts=opts.MarkLineOpts(data=mark_line_data),
                           markpoint_opts=opts.MarkPointOpts(data=mark_point_data))
    line.set_global_opts(**global_opts_dict)
    line.render(save_filename)


def _parse_mark_dict(mark_dict: dict):
    if mark_dict is None:
        return [], []
    mark_line_data = []
    if mark_dict["average"]:
        mark_line_data.append(opts.MarkLineItem(type_="average", name="average"))
    mark_point_data = []
    if mark_dict["max"]:
        mark_point_data.append(opts.MarkPointItem(type_="max", name="max"))
    if mark_dict["min"]:
        mark_point_data.append(opts.MarkPointItem(type_="min", name="min"))
    return mark_line_data, mark_point_data
