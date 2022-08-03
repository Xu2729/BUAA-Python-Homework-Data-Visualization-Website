import pandas as pd
from pyecharts.charts import Bar, Pie, Radar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from django.shortcuts import redirect
from django.http import HttpRequest


# 饼图
def make_pie(data_filename: str, key_name: str, title=None, save_filename="pie.html"):
    data = pd.read_csv(data_filename)
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
                                 data_zoom=None, restore=None, magic_type=None
                             )))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )
    pie.render(save_filename)


# 条形图
def make_bar(data_filename: str, key_name: str, group_by=None, use_stack=False, title=None, save_filename="bar.html"):
    data = pd.read_csv(data_filename)
    if title is None:
        title = key_name + " statistic"
    if group_by is None:
        data = dict(data[key_name].value_counts())
        keys = pd.DataFrame(data.keys())[0].tolist()
        values = pd.DataFrame(data.values())[0].tolist()
        bar = (
            Bar(
                init_opts=opts.InitOpts(bg_color="white")
            )
                .add_xaxis(keys)
                .add_yaxis("", values, category_gap="35%")
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
                                 toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                                     save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(pixel_ratio=1.5), brush=None,
                                     data_zoom=None, restore=None, magic_type=opts.ToolBoxFeatureMagicTypeOpts(
                                         type_=("line", "bar")))))
        )
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
                                     data_zoom=None, restore=None,
                                 )))
        )
        if use_stack:
            for k, v in tot_data.items():
                bar.add_yaxis(k, v, stack="s1", category_gap="50%")
            bar.set_series_opts(
                label_opts=opts.LabelOpts(
                    position="right",
                    formatter=JsCode(
                        "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                    ),
                )
            )
        else:
            for k, v in tot_data.items():
                bar.add_yaxis(k, v, category_gap="30%")
        bar.render(save_filename)


# 雷达图
def make_radar(data_filename: str, pks: list, keyname_and_max: dict, title=None, save_filename="radar.html"):
    data = pd.read_csv(data_filename)
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
                                 data_zoom=None, restore=None, magic_type=None
                             )))
    )
    for i in pks:
        temp = list(map(int, [data.iloc[i][k] for k in keyname_and_max.keys()]))
        radar.add("student " + str(i), [{"value": temp, "name": "student " + str(i)}])
    radar.render(save_filename)


def require_login():
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            cookies = request.COOKIES
            is_login = cookies.get("is_login")
            if is_login:
                return func(request, *args, **kwargs)
            else:
                return redirect("/login/?next={}".format(request.path))

        return wrapper

    return decorator
