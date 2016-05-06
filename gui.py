"""
File: gui.py
Author: Nicholas Jenis ngj5017@rit.edu
Generate a Python gui built from PyQt to render the html Plotly graph.
Allows the user to generate a custom graph based on the data.

"""


from PyQt5.QtWidgets import QAction, QApplication, QMainWindow,\
            QRadioButton, QPushButton, QComboBox, QCheckBox, QLabel
from PyQt5.QtWebKitWidgets import QWebView

import plot
from filter import *

#Graph Modes
Mode = {
    0 : "Individual State",
    1 : "All States",
    2 : "Type Years",
    3 : "Quarter Years",
    4 : "Total",
    5 : "Compare States"
}

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
       
        self.view = QWebView(self)
        self.setWindowTitle("Plot")

        #Graph Type
        self.graphLabel = QLabel("Mode: ", self)
        self.graphCombo = QComboBox(self)
        self.graphCombo.addItems(self.setupGraphCombo())
        self.graphCombo.activated[int].connect(self.switchMode)
        
       
        #Individual States
        self.stateLabel = QLabel("State: ", self)
        self.stateCombo = QComboBox(self)
        self.stateCombo.addItems(allStateNames())
        self.stateLabelSpacer = QLabel(" ", self)
        self.typesCheckBox = QCheckBox("School Types", self)

        #All States
        self.yearCombo = QComboBox(self)
        self.yearCombo.addItems(allYears())

        #Qtr Years
        self.quartersCombo = QComboBox(self)
        self.quartersCombo.addItems(['1','2','3','4','5','6'])

        #Compare States
        self.stateALabel = QLabel("State A: ", self)
        self.stateACombo = QComboBox(self)
        self.stateACombo.addItems(allStateNames())
        self.stateALabelSpacer = QLabel(" ", self)
        self.stateBLabel = QLabel("State B: ", self)
        self.stateBCombo = QComboBox(self)
        self.stateBCombo.addItems(allStateNames())
        
        
        
        self.graphBtn = QPushButton("Graph", self)
        self.graphBtn.clicked.connect(self.graph)

        #Add Widgets to the toolbar
        self.toolbar = self.addToolBar("Hide")
        self.toolbar.addWidget(self.graphLabel)
        self.toolbar.addWidget(self.graphCombo)
        self.toolbar.addSeparator()
        self.stateLabelAction = self.toolbar.addWidget(self.stateLabel)
        self.stateComboAction = self.toolbar.addWidget(self.stateCombo)
        self.stateLabelSpacerAction = self.toolbar.addWidget(self.stateLabelSpacer)
        self.typesCheckBoxAction = self.toolbar.addWidget(self.typesCheckBox)
        self.yearComboAction = self.toolbar.addWidget(self.yearCombo)
        self.quartersComboAction = self.toolbar.addWidget(self.quartersCombo)
        self.stateALabelAction = self.toolbar.addWidget(self.stateALabel)
        self.stateAComboAction = self.toolbar.addWidget(self.stateACombo)
        self.stateALabelSpacerAction = self.toolbar.addWidget(self.stateALabelSpacer)
        self.stateBLabelAction =  self.toolbar.addWidget(self.stateBLabel)
        self.stateBComboAction = self.toolbar.addWidget(self.stateBCombo)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.graphBtn)
        self.setCentralWidget(self.view)

        self.switchMode(0)

    #Generate a graph based on the users current selection
    def graph(self):
        newGraph = ""
        mode = self.graphCombo.currentIndex()

        #Individual State
        if mode == 0:
            state = self.stateCombo.currentText()
            if self.typesCheckBox.isChecked():
                #TODO: bug here with AS
                xData,yData = typesInState(state)
                newGraph = plot.plotByStateType(xData,yData,state)                    
            else:
                xData,yData = stateOnly(state)
                newGraph = plot.plotByState(xData,yData,state)
        #All States    
        elif mode == 1:
            year = self.yearCombo.currentText()
            xData,yData = allStatesYear(year)
            newGraph = plot.plotAllStates(xData,yData,year)
            
        #Type Years
        elif mode == 2:
            xData,yData = typePerYear()
            newGraph = plot.plotTypePerYear(xData,yData)

        #Qtr Years
        elif mode == 3:
            quarter = self.quartersCombo.currentText()
            xData,yData = qtrYears(quarter)
            newGraph = plot.plotQuarters(xData,yData,quarter)

        #Total
        elif mode == 4:
            xData,yData = total()
            newGraph = plot.plotTotal(xData,yData)
            
        #Compare States
        elif mode == 5:
            stateA = self.stateACombo.currentText()
            stateB = self.stateBCombo.currentText()
            xDataA,yDataA = stateOnly(stateA)
            xDataB,yDataB = stateOnly(stateB)
            newGraph = plot.plotCompareStates(xDataA,yDataA,xDataB,yDataB,stateA,stateB)
            
        else:               
            return

        self.view.setHtml(newGraph)

    #Switch graphing mode. Show/Hide options
    def switchMode(self, mode):
        #Individual State
        if mode == 0:
            self.setStateMode(True)
            self.setAllStatesMode(False)
            self.setQuarterYearsMode(False)
            self.setCompareStatesMode(False)
            
        #All States
        elif mode == 1:      
            self.setStateMode(False)
            self.setAllStatesMode(True)
            self.setQuarterYearsMode(False)
            self.setCompareStatesMode(False)

        #Type Years or Total
        elif mode == 2 or mode == 4:
            self.setStateMode(False)
            self.setAllStatesMode(False)
            self.setQuarterYearsMode(False)
            self.setCompareStatesMode(False)

        #Quarters
        elif mode == 3:
            self.setStateMode(False)
            self.setAllStatesMode(False)
            self.setQuarterYearsMode(True)
            self.setCompareStatesMode(False)

        #Comparse States
        elif mode == 5:
            self.setStateMode(False)
            self.setAllStatesMode(False)
            self.setQuarterYearsMode(False)
            self.setCompareStatesMode(True)


    #Setup the toolbar for each mode
    def setQuarterYearsMode(self, b):
        self.quartersComboAction.setVisible(b)
        self.quartersCombo.setCurrentIndex(0)

    def setAllStatesMode(self, b):
        self.yearComboAction.setVisible(b)
        self.stateCombo.setCurrentIndex(0)

    def setStateMode(self, b):
        self.stateLabelAction.setVisible(b)
        self.stateComboAction.setVisible(b)
        self.stateLabelSpacerAction.setVisible(b)
        self.typesCheckBoxAction.setVisible(b)
        self.typesCheckBox.setChecked(False)

    def setCompareStatesMode(self, b):
        self.stateALabelAction.setVisible(b)
        self.stateAComboAction.setVisible(b)
        self.stateALabelSpacerAction.setVisible(b)
        self.stateBLabelAction.setVisible(b)
        self.stateBComboAction.setVisible(b)
        self.stateACombo.setCurrentIndex(0)
        self.stateBCombo.setCurrentIndex(0)

    #Set up the graph mode combo box
    def setupGraphCombo(self):
        ret = []
        for mode in Mode:
            ret.append(Mode[mode])
        return ret


