#coding:utf-8
from plotly import tools
import plotly
import plotly.graph_objs as go

#line_1 = go.Scatter(x = ['a','b','c','d','e'],y = [1,3,4,5,5])

pie_1 = go.Pie(labels= ['1st', '2nd', '3rd', '4th', '5th'],values= [38, 27, 18, 10, 7],)

pie_2 = go.Pie(labels=['1st', '2nd', '3rd', '4th', '5th'],values=[38, 27, 18, 10, 7])

pie_3 = go.Pie(labels=['1st', '2nd', '3rd', '4th', '5th'],values=[38, 27, 18, 10, 7])

pie_4 = go.Pie(labels=['1st', '2nd', '3rd', '4th', '5th'],values=[38, 27, 18, 10, 7])

#data = [line_1, pie_1, pie_2, pie_3,pie_4]
data = [pie_1, pie_2, pie_3,pie_4]
# fig = tools.make_subplots(rows=3, cols=2, specs=[[{'colspan':2},None],[{}, {}], [{}, {}]],
#                           subplot_titles=('总体通过率趋势','用例运行分析图', '校验点运行分析图','前台图','后台图'))
fig = tools.make_subplots(rows=2, cols=2, specs=[[{}, {}], [{}, {}]],
                           subplot_titles=('用例运行分析图', '校验点运行分析图','前台图','后台图'))

#fig.append_trace(line_1, 1, 1)
fig.append_trace(pie_1, 1, 1)
fig.append_trace(pie_2, 1, 2)
fig.append_trace(pie_3, 2, 1)
fig.append_trace(pie_4, 2, 2)

fig['layout'].update(height=600, width=800, title='用例运行分析图')

plotly.offline.plot(fig, filename='line_pie.html')