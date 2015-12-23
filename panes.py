'''
This module provides the application panes containing essential
functionalities.
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

from PyQt4 import QtGui, QtCore

class Symptoms(QtGui.QFrame):
    ''' Provides the widget for symptoms input '''

    # List to hold the symptoms
    sympList=[]

    # Signal to notify any change in input
    changed=QtCore.pyqtSignal(list)
    
    def __init__(self, auto):
        '''
        Initiate the symptom input pane. Takes a list of string as
        argument. The list is used as the auto-complete list during
        user input.

        Parameter:
        auto - A list of string containing all available symptoms for
               autocomplete.
        '''
        super(Symptoms, self).__init__()
        self.auto=auto
        self.initUI()

    def initUI(self):
        ''' Initiate the user interface '''
        self.label=QtGui.QLabel("Symptoms")
        self.label.setStyleSheet("font-size:18px")

        self.listWidget=QtGui.QListWidget(self)
        self.listWidget.setStyleSheet("font-size:14px")
        self.listWidget.setSelectionMode(4)

        self.rm=QtGui.QPushButton("Remove")
        self.rm.clicked.connect(self.remove)

        self.cl=QtGui.QPushButton("Clear All")
        self.cl.clicked.connect(self.removeAll)

        self.browse=QtGui.QPushButton("Browse Symptoms")
        self.browse.clicked.connect(self.browseSymptoms)

        self.add=QtGui.QPushButton("Add")
        self.add.clicked.connect(self.addItem)

        self.new=QtGui.QLineEdit(self)
        self.new.returnPressed.connect(self.addItem)
        self.completer=QtGui.QCompleter(self.auto)
        self.completer.setCaseSensitivity(0)
        self.completer.setCompletionMode(2)
        self.new.setCompleter(self.completer)

        self.browser=SymptomBrowser(self.auto)
        self.browser.added.connect(self.addItem)

        hboxt=QtGui.QHBoxLayout()
        hboxt.addWidget(self.new)
        hboxt.addWidget(self.add)
        hboxb=QtGui.QHBoxLayout()
        hboxb.addWidget(self.rm)
        hboxb.addWidget(self.cl)
        hboxb.addWidget(self.browse)
        vbox=QtGui.QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hboxt)
        vbox.addWidget(self.listWidget)
        vbox.addLayout(hboxb)
        self.setLayout(vbox)

    def addItem(self, text=""):
        ''' Add a new symptom '''
        if(not text):
            text=self.new.text()
        if(len(text)>0):
            if(text in self.sympList):
                QtGui.QMessageBox.information(self, "Duplicate Symptom", "'"+text+"' has already been added to the symptom list.")
            elif(text in self.auto):
                QtGui.QListWidgetItem(text, self.listWidget)
                self.sympList.append(text)
                self.new.clear()
                self.changed.emit(list(self.sympList))
            else:
                QtGui.QMessageBox.warning(self, "Symptom Unvailable", "'"+text+"' is not available in the current Library.")

    def remove(self, all=False):
        ''' Remove selected symptoms '''
        if(len(self.listWidget.selectedItems())>0):
            for item in self.listWidget.selectedItems():
                self.sympList.remove(item.text())
                self.listWidget.takeItem(self.listWidget.row(item))
            self.changed.emit(list(self.sympList))

    def removeAll(self):
        ''' Clear all symptoms '''
        self.listWidget.clear()
        del self.sympList[:]
        self.changed.emit(list(self.sympList))

    def browseSymptoms(self):
        ''' Open the symptom browser '''
        self.browser.exec_()

    def getList(self):
        ''' Return a list of all symptoms '''
        return self.sympList


class SymptomBrowser(QtGui.QDialog):
    '''
    Provides a dialog with a list of symptoms for alternative user
    input.
    '''
    added=QtCore.pyqtSignal(str)
    
    def __init__(self, items):
        ''' Initiate the input dialog '''
        super(SymptomBrowser, self).__init__()
        self.setWindowTitle("Choose Symptom")
        self.items=items
        self.initUI()

    def initUI(self):
        ''' Initiate the dialog interface '''
        self.search=QtGui.QLineEdit()
        self.search.textChanged.connect(self.refresh)
        self.listItems=QtGui.QListWidget()
        self.listItems.activated.connect(self.sendUp)

        layout=QtGui.QVBoxLayout(self)
        layout.addWidget(self.search)
        layout.addWidget(self.listItems)

        self.listItems.addItems(self.items)
        self.search.setFocus()

    def refresh(self):
        ''' Refresh the symptom list based on search term '''
        term=self.search.text()
        buff=[]
        for i in self.items:
            if(term.lower() in i.lower()):
                buff.append(i)
        self.listItems.clear()
        self.listItems.addItems(buff)
    
    def sendUp(self):
        ''' Emit signal and close when a symptom is selected '''
        self.added.emit(self.listItems.currentItem().text())
        self.close()


class Differentials(QtGui.QFrame):
    ''' Provides the widget for differential diagnosis output '''
    data=[]
    
    def __init__(self):
        ''' Initiate the diagnosis output pane '''
        super(Differentials, self).__init__()
        self.initUI()
        
    def initUI(self):
        ''' Initiate the user interface '''
        self.label=QtGui.QLabel("Differential Diagnosis")
        self.label.setStyleSheet("font-size:18px")
        self.listWidget=QtGui.QListWidget(self)
        self.listWidget.setStyleSheet("font-size:14px")
        self.listWidget.setSelectionMode(0)
        box=QtGui.QVBoxLayout()
        box.addWidget(self.label)
        box.addWidget(self.listWidget)
        self.setLayout(box)

    def update(self, data):
        '''
        Update the outut pane with updated diagnosis list.
        
        Parameter:
        data - List of strings containing new list of differential
               diagnosis
        '''
        self.data=data
        self.listWidget.clear()
        if(self.data):
            for d in self.data:
                QtGui.QListWidgetItem(d, self.listWidget)

    def getList(self):
        ''' Return a list of current differential diagnosis '''
        return self.data
