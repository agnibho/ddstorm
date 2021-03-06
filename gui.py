#! /usr/bin/python3

'''
This module provides the main graphical user interface for DDStorm
'''
'''
Copyright (c) 2015 Agnibho Mondal
All rights reserved

This file is part of DDStorm.

DDStorm is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DDStorm is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DDStorm.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import time
import subprocess

from PyQt5 import QtWidgets, QtGui, QtCore

from panes import Symptoms, Differentials
from ddstorm import DDStorm
from conf import Conf
from extras import *
from const import *

conf=False

class Content(QtWidgets.QWidget):
    '''
    Provides the main content widget. Contains the sysmptoms and
    the diagnosis panes. Also creates the DDStorm object and performs
    the main operation.
    '''

    # Signal to detect when 
    change=QtCore.pyqtSignal()
    
    def __init__(self):
        ''' Initiate the content widget '''
        super(Content, self).__init__()
        
        # Create DDStorm object with the global configuration
        self.dd=DDStorm(True, conf)

        # Show warning if any error happened during data compilation 
        if(not self.dd.compiler.is_clean()):
            ret=QtWidgets.QMessageBox.warning(self, "Compilation Error", "Error was encountered while compiling the Knowledgebase.", "Ignore", "View Log")
            if(ret==1):
                x_logfile()
        
        self.initUI()
        
    def initUI(self):
        ''' Create the user interface of the widget '''
        
        global conf

        grid=QtWidgets.QGridLayout()
        self.setLayout(grid)

        self.symp=Symptoms(self.dd.symptoms())
        self.symp.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.symp.changed.connect(self.update)

        self.diff=Differentials()
        self.diff.setFrameShape(QtWidgets.QFrame.StyledPanel)

        grid.addWidget(self.symp, 0, 0)
        grid.addWidget(self.diff, 0, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create("Cleanlooks"))
        
    def update(self, data):
        ''' Update the inteface with refreshed information '''
        self.diff.update(self.dd.dd(data))
        self.change.emit()


class Window(QtWidgets.QMainWindow):
    '''
    Provides main application window. Acts as a container for the
    content widget. Also contains the menubar and the status bar.
    '''
    
    def __init__(self):
        ''' Initiate the main window '''
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        ''' Create the user interface '''
        global conf
        self.con=Content()
        self.sett=SettingsDialog(conf)
        if(conf.get("status_message")=="on"):
            self.con.change.connect(self.showStatus)

        menu=self.menuBar()
        menuFile=menu.addMenu("&File")
        menuFile.addAction("&Save").triggered.connect(self.savefile)
        menuFile.addAction("E&xit").triggered.connect(self.close)
        menuEdit=menu.addMenu("&Edit")
        menuEdit.addAction("&Add").triggered.connect(self.con.symp.addItem)
        menuEdit.addAction("&Browse Symptoms").triggered.connect(self.con.symp.browseSymptoms)
        rmAction=QtWidgets.QAction("&Remove", self)
        rmAction.setShortcut("Delete")
        rmAction.triggered.connect(self.con.symp.remove)
        menuEdit.addAction(rmAction)
        menuEdit.addAction("&Clear All").triggered.connect(self.con.symp.removeAll)
        menuTool=menu.addMenu("&Tools")
        menuTool.addAction("&Library").triggered.connect(x_lib)
        menuTool.addAction("&Settings").triggered.connect(self.settings)
        menuTool.addAction("&View Log").triggered.connect(x_logfile)
        menuHelp=menu.addMenu("&Help")
        menuHelp.addAction("&Help").triggered.connect(x_help)
        menuHelp.addAction("&About").triggered.connect(self.about)

        self.setCentralWidget(self.con)
        self.status=self.statusBar()
        self.setGeometry(200, 200, 600, 400)
        self.setWindowTitle("D/D Storm")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))
        self.showMaximized()
        self.con.symp.new.setFocus()

    def showStatus(self):
        ''' Show status message '''
        if(self.con.symp.getList() and self.con.diff.getList()):
            self.status.showMessage(str(len(self.con.diff.getList()))+" differential diagnosis for "+str(len(self.con.symp.getList()))+" symptom(s).")
        else:
            self.status.showMessage("")

    def savefile(self):
        ''' Save data to a file '''
        x_save(self, self.con.symp.getList(), self.con.diff.getList())

    def settings(self):
        ''' Open the settings dialog '''
        self.sett.exec_()

    def about(self):
        ''' Show information about this application '''
        QtWidgets.QMessageBox.about(self, "About", "<h1>DDStorm</h1>\nBrainstorm Medicine")


def main():
    ''' Start the main application interface '''
    app=QtWidgets.QApplication(sys.argv)

    # Initiate the global configuration
    global conf
    conf=Conf()
    
    # Clean the log file
    if(conf.get("clean_log")=="yes"):
        open(LOG_FILE, "w").close()

    # Show splash-screen
    if(conf.get("splash_screen")=="yes"):
        ss=True
    else:
        ss=False
    if(ss):
        splash=QtWidgets.QSplashScreen(QtWidgets.QPixmap("icons/splash.png"))
        splash.show()
        time.sleep(0.1)
        app.processEvents()
        splash.showMessage("Loading...")

    # Create main window
    w=Window()
    if(ss):
        splash.finish(w)

    # Start application
    sys.exit(app.exec_())

if(__name__=="__main__"):
    main()
