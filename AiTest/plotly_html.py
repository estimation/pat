#coding:utf-8
# Get this figure: fig = py.get_figure("https://plot.ly/~wuweizuo/9/")
# Get this figure's data: data = py.get_figure("https://plot.ly/~wuweizuo/9/").get_data()
# Add data to this figure: py.plot(Data([Scatter(x=[1, 2], y=[2, 3])]), filename ="four_pie_plot", fileopt="extend")

# Get figure documentation: https://plot.ly/python/get-requests/
# Add data documentation: https://plot.ly/python/file-options/

# If you're using unicode in your file, you may need to specify the encoding.
# You can reproduce this figure in Python with the following code!

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
from plotly.graph_objs import *
#py.sign_in('username', 'api_key')
trace1 = {
  "direction": "counterclockwise",
  "domain": {
    "x": [0, 0.48],
    "y": [0, 0.49]
  },
  "hole": 0.01,
  "hoverinfo": "label+percent+name",
  "labels": ["成功数", "失败数"],
  "labelssrc": "wuweizuo:8:641249",
  "marker": {
    "colors": ["rgb(222,183,175)", "rgb(207,131,113)", "rgb(192,88,64)", "rgb(182,59,37)", "rgb(150,19,27)", "rgb(144,19,28)"],
    "line": {
      "color": "rgb(68, 68, 68)",
      "width": 0.1
    }
  },
  "name": "前台图",
  "opacity": 1,
  "pull": 0.1,
  "rotation": 0,
  "sort": True,
  "textfont": {"size": 10},
  "textinfo": "label+value+percent",
  "textposition": "inside",
  "type": "pie",
  "uid": "8ecdd5",
  "values": ["100", "0"],
  "valuessrc": "wuweizuo:8:8de04c"
}
trace2 = {
  "direction": "clockwise",
  "domain": {
    "x": [0.52, 1],
    "y": [0, 0.49]
  },
  "hole": 0.01,
  "hoverinfo": "label+percent+name",
  "labels": ["成功数", "失败数"],
  "labelssrc": "wuweizuo:8:641249",
  "marker": {
    "colors": ["rgb(222,183,175)", "rgb(207,131,113)", "rgb(192,88,64)", "rgb(182,59,37)", "rgb(150,19,27)", "rgb(144,19,28)"],
    "line": {"width": 0.1}
  },
  "name": "后台图",
  "pull": 0.1,
  "rotation": 90,
  "sort": False,
  "textfont": {"size": 10},
  "textinfo": "label+value+percent",
  "textposition": "inside",
  "type": "pie",
  "uid": "827a6f",
  "values": ["98", "2"],
  "valuessrc": "wuweizuo:8:5c9631"
}
trace3 = {
  "direction": "counterclockwise",
  "domain": {
    "x": [0, 0.48],
    "y": [0.51, 1]
  },
  "hole": 0.01,
  "hoverinfo": "label+percent+name",
  "labels": ["成功数", "失败数"],
  "labelssrc": "wuweizuo:8:641249",
  "marker": {
    "colors": ["rgb(222,183,175)", "rgb(207,131,113)", "rgb(192,88,64)", "rgb(182,59,37)", "rgb(150,19,27)", "rgb(144,19,28)"],
    "line": {"width": 0.1}
  },
  "name": "用例运行分析图",
  "pull": 0.1,
  "rotation": 90,
  "sort": True,
  "textfont": {"size": 9},
  "textinfo": "label+value+percent",
  "textposition": "inside",
  "type": "pie",
  "uid": "c9380e",
  "values": ["98", "2"],
  "valuessrc": "wuweizuo:8:722ecc"
}
trace4 = {
  "direction": "counterclockwise",
  "domain": {
    "x": [0.52, 1],
    "y": [0.51, 1]
  },
  "hole": 0.01,
  "hoverinfo": "label+percent+name",
  "labels": ["成功数", "失败数"],
  "labelssrc": "wuweizuo:8:641249",
  "marker": {
    "colors": ["rgb(222,183,175)", "rgb(207,131,113)", "rgb(192,88,64)", "rgb(182,59,37)", "rgb(150,19,27)", "rgb(144,19,28)"],
    "line": {"width": 0.1}
  },
  "name": "验证点运行分析图",
  "pull": 0.1,
  "rotation": 90,
  "sort": True,
  "textfont": {
    "family": "Open Sans",
    "size": 9
  },
  "textinfo": "label+value+percent",
  "textposition": "inside",
  "type": "pie",
  "uid": "cae88a",
  "values": ["1400", "20"],
  "valuessrc": "wuweizuo:8:79407a"
}
data = Data([trace1, trace2, trace3, trace4])
layout = {
  "annotations": [
    {
      "x": 0.18,
      "y": 1.1,
      "font": {"color": "rgb(127, 127, 127)"},
      "showarrow": False,
      "text": "<b>用例运行分析图</b>",
      "xref": "paper",
      "yref": "paper"
    },
    {
      "x": 0.82,
      "y": 1.1,
      "font": {"color": "rgb(127, 127, 127)"},
      "showarrow": False,
      "text": "<b>验证点运行分析图</b>",
      "xanchor": "right",
      "xref": "paper",
      "yref": "paper"
    },
    {
      "x": 0.21,
      "y": 0.5,
      "font": {"color": "rgb(127, 127, 127)"},
      "showarrow": False,
      "text": "<b>前台图</b>",
      "xref": "paper",
      "yref": "paper"
    },
    {
      "x": 0.78,
      "y": 0.5,
      "showarrow": False,
      "text": "<b>后台图</b>",
      "xref": "paper",
      "yref": "paper"
    },
    {
      "x": 0.5,
      "y": -0.1,
      "arrowhead": 0,
      "ax": -10,
      "ay": -30,
      "showarrow": False,
      "text": "<b>AI Autotest.</b><br>generate from the result of autotest running",
      "xanchor": "center",
      "xref": "paper",
      "yanchor": "bottom",
      "yref": "paper"
    }
  ],
  "autosize": False,
  "font": {"size": 12},
  "height": 689,
  "hovermode": "closest",
  "legend": {
    "x": 1.02,
    "y": 1.2,
    "borderwidth": 0,
    "font": {"size": 12},
    "orientation": "v",
    "traceorder": "normal",
    "xanchor": "right",
    "yanchor": "top"
  },
  "margin": {
    "r": 50,
    "t": 100,
    "b": 80,
    "pad": 0
  },
  "paper_bgcolor": "rgb(255, 255, 255)",
  "showlegend": True,
  "title": "<b>用例运行分析图</b>",
  "titlefont": {
    "color": "rgb(214, 39, 40)",
    "size": 35
  },
  "width": 943
}
fig = Figure(data=data, layout=layout)
plot_url = plotly.offline.plot(fig)