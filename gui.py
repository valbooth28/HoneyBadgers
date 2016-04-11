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
    4 : "Total"
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
        else:               
            return

        self.view.setHtml(newGraph)

    #Switch graphing mode. Show/Hide options
    def switchMode(self, mode):
        #Individual State
        if mode == 0:
            self.yearComboAction.setVisible(False)
            self.quartersComboAction.setVisible(False)
            self.stateLabelAction.setVisible(True)
            self.stateComboAction.setVisible(True)
            self.stateLabelSpacerAction.setVisible(True)
            self.typesCheckBoxAction.setVisible(True)

            self.typesCheckBox.setChecked(False)
            self.stateCombo.setCurrentIndex(0)
        #All States
        elif mode == 1:
            self.stateComboAction.setVisible(False)
            self.stateLabelAction.setVisible(False)
            self.typesCheckBoxAction.setVisible(False)
            self.stateLabelSpacerAction.setVisible(False)
            self.quartersComboAction.setVisible(False)
            self.yearComboAction.setVisible(True)

        #Type Years or Total
        elif mode == 2 or mode == 4:
            self.stateComboAction.setVisible(False)
            self.typesCheckBoxAction.setVisible(False)
            self.stateLabelAction.setVisible(False)
            self.yearComboAction.setVisible(False)
            self.stateLabelSpacerAction.setVisible(False)
            self.quartersComboAction.setVisible(False)
            self.quartersComboAction.setVisible(False)

        #Quarters
        elif mode == 3:
            self.stateComboAction.setVisible(False)
            self.typesCheckBoxAction.setVisible(False)
            self.stateLabelAction.setVisible(False)
            self.yearComboAction.setVisible(False)
            self.stateLabelSpacerAction.setVisible(False)
            self.quartersComboAction.setVisible(False)
            self.quartersComboAction.setVisible(True)

            self.quartersCombo.setCurrentIndex(0)

    #Set up the graph mode combo box
    def setupGraphCombo(self):
        ret = []
        for mode in Mode:
            ret.append(Mode[mode])
        return ret


