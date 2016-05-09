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
titleFont=dict(
    family='Courier New, monospace',
    size=20,
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

    plotData = {
        "data": [

            Bar(x=depDataX, y=depDataY, name="Dependent"),
            Bar(x=indepDataX, y=indepDataY, name="Independent")

        ],
        "layout": Layout(
            title="Dependents and Independents in "+state+" by Year",
            font=titleFont,
            xaxis=dict(title="Year",
                       titlefont=tf,
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
            font=titleFont,
            xaxis=dict(title="Year",
                       titlefont=tf,
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
            font=titleFont,
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
            font=titleFont,
            xaxis=dict(title="Year",
                       titlefont=tf,
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
            font=titleFont,
            xaxis=dict(title="Year",
                       titlefont=tf,
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
            font=titleFont,
            xaxis=dict(title="Year",
                       titlefont=tf,
            ),
            yaxis=dict(title="Number of students",
                       titlefont=tf
            ),
            barmode='group'
        )}

    return plot(plotData)

def plotCompareStates(xDataA,yDataA,xDataB,yDataB,stateA,stateB):
    depDataX = []
    indepDataX = []
    depDataY = []
    indepDataY = []

    #Messy code - Check, Doesn't scale - Check
    depDataX.append((stateA + "-" + str(xDataA[0])))
    depDataX.append((stateB + "-" + str(xDataB[0])))
    depDataX.append((stateA + "-" + str(xDataA[2])))
    depDataX.append((stateB + "-" + str(xDataB[2])))
    indepDataX.append((stateA + "-" + str(xDataA[1])))
    indepDataX.append((stateB + "-" + str(xDataB[1])))
    indepDataX.append((stateA + "-" + str(xDataA[3])))
    indepDataX.append((stateB + "-" + str(xDataB[3])))

    depDataY.append(yDataA[0])
    depDataY.append(yDataB[0])
    depDataY.append(yDataA[2])
    depDataY.append(yDataB[2])
    indepDataY.append(yDataA[1])
    indepDataY.append(yDataB[1])
    indepDataY.append(yDataA[3])
    indepDataY.append(yDataB[3])

    plotData = {
        "data": [
            Bar(x=depDataX, y=depDataY, name="Dependent"),
            Bar(x=indepDataX, y=indepDataY, name="Independent")

        ],
        "layout": Layout(
            title=stateA + " vs " + stateB + " by Year",
            font=titleFont,
            xaxis=dict(title="State-Year",
                       titlefont=tf,
            ),
            yaxis=dict(title="Number of students",
                       titlefont=tf
            ),
            barmode='group'
        )}

    return plot(plotData)

def plotRegion(xData,yData,region):
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
            title="Dependents and Independents in "+region+" by Year",
            font=titleFont,
            xaxis=dict(title="Year",
                       titlefont=tf
            ),
            yaxis=dict(title="Number of students",
                       titlefont=tf
            ),
            barmode='group'
        )
    }

    return plot(plotData)


#Make a graph from the input data
#Return html string for gui
def plot(plotData):
    return plotly.offline.plot(plotData, show_link=False, output_type='div')


