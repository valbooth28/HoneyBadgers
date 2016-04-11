"""
File: plot.py
Author: Nicholas Jenis ngj5017@rit.edu
Use Plotly graphing library to create custom graphs.
Save graphs as html string for gui
"""

import plotly
from plotly.graph_objs import Scatter, Layout, Bar


tf=dict(
    family='Courier New, monospace',
    size=28,
    color='#7f7f7f'
)


def plotByState(xData,yData,state):

    depDataX = []
    indepDataX = []
    depDataY = []
    indepDataY = []
    
    for i in range(len(xData)):
        if i % 2 == 0:
            depDataX.append(xData[i])
        else:
            indepDataX.append(xData[i])
    for i in range(len(yData)):
        if i % 2 == 0:
            depDataY.append(yData[i])
        else:
            indepDataY.append(yData[i])

            #Scatter(x=indepDataX, y=indepDataY, mode='markers',
             #       marker=dict(size=12, line=dict(width=1)), name="Independent")
            #Scatter(x=depDataX, y=depDataY, mode='markers',
            #    marker=dict(size=12, line=dict(width=1)), name="Dependent"),

    plotData = {
        "data": [

            Bar(x=depDataX, y=depDataY, name="Dependent"),
            Bar(x=indepDataX, y=indepDataY, name="Independent")

        ],
        "layout": Layout(
            title="Dependents and Independents in "+state+" by Year",
            xaxis=dict(title="Year",
                       titlefont=tf,
                       tickvals=[2012,2013,2014,2015],
                       range=[2012,2015]
            ),
            yaxis=dict(title="Number of students",
                       titlefont=tf
            ),
            barmode='group'
        )}
    return plot(plotData)


def plotByStateType(xData,yData,state):
  
    depDataPUY = []
    indepDataPUY = []
    depDataPVY = []
    indepDataPVY = []
    depDataPRY = []
    indepDataPRY = []

    ##xData is 2013
    ##yData is 2014

    yr=[]
    yr.extend([xData[0],yData[0]])

    depDataPUY.extend([xData[2][0],yData[2][0]])
    indepDataPUY.extend([xData[2][1],yData[2][1]])
    depDataPVY.extend([xData[2][2],yData[2][2]])
    indepDataPVY.extend([xData[2][3],yData[2][3]])
    depDataPRY.extend([xData[2][4],yData[2][4]])
    indepDataPRY.extend([xData[2][5],yData[2][5]])

    plotData = {
        "data": [
            Bar(x=yr, y=depDataPUY, name="Dependent Public"),
            Bar(x=yr, y=depDataPVY, name="Dependent Private"),
            Bar(x=yr, y=depDataPRY, name="Dependent Proprietary"),
            Bar(x=yr, y=indepDataPUY, name="Independent Public"),
            Bar(x=yr, y=indepDataPVY, name="Independent Private"),
            Bar(x=yr, y=indepDataPRY, name="Independent Proprietary")
        ],
        "layout": Layout(
            title="Dependents and Independents with School Type in "+state+" by Year",
            xaxis=dict(title="Year",
                       titlefont=tf,
                       tickvals=[2012,2013,2014,2015],
                       range=[2012,2015]
            ),
            yaxis=dict(title="Number of students",
                       titlefont=tf
            ),
            barmode='group'
        )
    }

    return plot(plotData)


def plotAllStates(xData,yData,year):
    depDataX = []
    depDataY = []
    indepDataX = []
    indepDataY = []

    for i in range(len(xData)):
        if i % 2 == 0:
            depDataX.append(xData[i])
            depDataY.append(yData[i])
        else:
            indepDataX.append(xData[i])
            indepDataY.append(yData[i])

    plotData = {
        "data": [
            Bar(x=depDataX, y=depDataY, name="Dependent"),
            Bar(x=indepDataX, y=indepDataY, name="Independent")
        ],
        "layout": Layout(
            title="Dependents and Independents in "+year+" by State",
            xaxis=dict(title="State",
                       titlefont=tf
            ),
            yaxis=dict(title="Number of students",
                       titlefont=tf
            ),
            barmode='group'
        )
    }

    return plot(plotData)

def plotTotal(xData,yData):

    depDataX = []
    indepDataX = []
    depDataY = []
    indepDataY = []
    
    for i in range(len(xData)):
        if i % 2 == 0:
            depDataX.append(xData[i])
        else:
            indepDataX.append(xData[i])
    for i in range(len(yData)):
        if i % 2 == 0:
            depDataY.append(yData[i])
        else:
            indepDataY.append(yData[i])

    plotData = {
        "data": [

            Bar(x=depDataX, y=depDataY, name="Dependent"),
            Bar(x=indepDataX, y=indepDataY, name="Independent")

        ],
        "layout": Layout(
            title="Total Dependents and Independents by Year",
            xaxis=dict(title="Year",
                       titlefont=tf,
                       tickvals=[2012,2013,2014,2015],
                       range=[2012,2015]
            ),
            yaxis=dict(title="Number of students",
                       titlefont=tf
            ),
            barmode='group'
        )}

    return plot(plotData)

def plotTypePerYear(xData,yData):
    depDataPUY = []
    indepDataPUY = []
    depDataPVY = []
    indepDataPVY = []
    depDataPRY = []
    indepDataPRY = []

    ##xData is 2013
    ##yData is 2014

    yr=[]
    yr.extend([xData[0],yData[0]])

    depDataPUY.extend([xData[2][0],yData[2][0]])
    indepDataPUY.extend([xData[2][1],yData[2][1]])
    depDataPVY.extend([xData[2][2],yData[2][2]])
    indepDataPVY.extend([xData[2][3],yData[2][3]])
    depDataPRY.extend([xData[2][4],yData[2][4]])
    indepDataPRY.extend([xData[2][5],yData[2][5]])

    plotData = {
        "data": [
            Bar(x=yr, y=depDataPUY, name="Dependent Public"),
            Bar(x=yr, y=depDataPVY, name="Dependent Private"),
            Bar(x=yr, y=depDataPRY, name="Dependent Proprietary"),
            Bar(x=yr, y=indepDataPUY, name="Independent Public"),
            Bar(x=yr, y=indepDataPVY, name="Independent Private"),
            Bar(x=yr, y=indepDataPRY, name="Independent Proprietary")
        ],
        "layout": Layout(
            title="Total Dependents and Independents with School Type by Year",
            xaxis=dict(title="Year",
                       titlefont=tf,
                       tickvals=[2012,2013,2014,2015],
                       range=[2012,2015]
            ),
            yaxis=dict(title="Number of students",
                       titlefont=tf
            ),
            barmode='group'
        )
    }

    return plot(plotData)

def plotQuarters(xData,yData,quarter):
    depDataX = []
    indepDataX = []
    depDataY = []
    indepDataY = []
    
    for i in range(len(xData)):
        if i % 2 == 0:
            depDataX.append(xData[i])
        else:
            indepDataX.append(xData[i])
    for i in range(len(yData)):
        if i % 2 == 0:
            depDataY.append(yData[i])
        else:
            indepDataY.append(yData[i])

    plotData = {
        "data": [

            Bar(x=depDataX, y=depDataY, name="Dependent"),
            Bar(x=indepDataX, y=indepDataY, name="Independent")

        ],
        "layout": Layout(
            title="Total Dependents and Independents in Quarter "+quarter+" by Year",
            xaxis=dict(title="Year",
                       titlefont=tf,
                       tickvals=[2012,2013,2014,2015,2016],
                       range=[2012,2016]
            ),
            yaxis=dict(title="Number of students",
                       titlefont=tf
            ),
            barmode='group'
        )}

    return plot(plotData)


def plot(plotData):
    return plotly.offline.plot(plotData, show_link=False, output_type='div')


##def plotGraphC(xData,yData):
##
## 
##    return plotly.offline.plot({
##    "data": [
##        Scatter(x=xData, y=yData,  mode = 'markers'),
##    ],
##    "layout": Layout(
##        title='Dependent Rate vs Time',
##        xaxis=dict(
##            title='2013 Quarter',
##            titlefont=tf
##        ),
##        yaxis=dict(
##            title='Dependent Rate',
##            titlefont=tf
##        )
##    )
##    }, show_link=False, output_type='div')
##
##
##
##
##def plotGraphA():
##    return plotly.offline.plot({
##    "data": [
##        Scatter(x=[1, 2, 3, 4, 5, 6], y=[0.416, 0.391, 0.373, 0.367, 0.361, 0.358],  mode = 'markers'),
##        Scatter(x=[1,6], y=[.408,.352])
##    ],
##    "layout": Layout(
##        title='Dependent Rate vs Time',
##        xaxis=dict(
##            title='2013 Quarter',
##            titlefont=dict(
##                family='Courier New, monospace',
##                size=18,
##                color='#7f7f7f'
##            )
##        ),
##        yaxis=dict(
##            title='Dependent Rate',
##            titlefont=dict(
##                family='Courier New, monospace',
##                size=18,
##                color='#7f7f7f'
##            )
##        )
##    )
##    }, show_link=False, output_type='div')


