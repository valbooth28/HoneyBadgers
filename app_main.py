"""
File: app_main.py
Author: Nicholas Jenis ngj5017@rit.edu
Driver program for the app
"""


import sys
from gui import *

if __name__ == '__main__':

    app = QApplication([])

    browser = MainWindow()
    browser.show()

    sys.exit(app.exec_())
