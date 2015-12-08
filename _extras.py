# DDStorm
# -------
# Copyright (c) 2015 Agnibho Mondal
# All rights reserved

# This file is part of DDStorm.

# DDStorm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# DDStorm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DDStorm.  If not, see <http://www.gnu.org/licenses/>.

import subprocess, os
from PyQt4 import QtGui, QtCore
from const import *

def x_settings():
    subprocess.Popen(["xdg-open", CONF_FILE])

def x_lib():
    if(os.path.isfile(CONF_FILE)):
            with open(CONF_FILE) as conf:
                for line in conf:
                    if(line.startswith("library_path=")):
                       library_path=line[13:-1]
                       if(os.path.isdir(library_path)):
                           subprocess.Popen(["xdg-open", library_path])

def x_save(w, symp, diff):
    fname=QtGui.QFileDialog.getSaveFileName(w, "Save File", "~", "HTML files('*.html')")
    if(not fname.endswith(".html")):
        fname=fname+".html"
    with open(fname, "w") as f:
        print("<!DOCTYPE html><html><head><title>Differential Diagnosis</title></head>", file=f)
        print("<body><h1>Differential Diagnosis</h1>", file=f)
        print("<table style='width:100%'>", file=f)
        print("<tr><th>Symptoms</th><th>Diffrential Diagnosis</th></tr>", file=f)
        print("<tr><td style='vertical-align:text-top'><ol>", file=f)
        for s in symp:
            print("<li>"+s+"</li>", file=f)
        print("</ol></td><td style='vertical-align:text-top'><ol>", file=f)
        for d in diff:
            print("<li>"+d+"</li>", file=f)
        print("</ol></td></tr></table></body></html>", file=f)

def x_help():
    if(os.path.isfile(HELP_FILE)):
        subprocess.Popen(["xdg-open", HELP_FILE])
    else:
        subprocess.Popen(["xdg-open", "http://www.agnibho.com"])

def x_logfile():
    subprocess.Popen(["xdg-open", LOG_FILE])

class SettingsDialog(QtGui.QDialog):
    def __init__(self, conf):
        super(SettingsDialog, self).__init__()
        self.setWindowTitle("Settings")
        self.conf=conf
        self.initUI()
    def initUI(self):
        self.lpLabel=QtGui.QLabel("Libary Path:")
        self.lpEdit=QtGui.QLineEdit(self.conf.get("library_path"))
        self.lpBrowse=QtGui.QPushButton("Browse")
        self.lpBrowse.clicked.connect(self.lpUpdate)
        self.mpLabel=QtGui.QLabel("Module Path:")
        self.mpEdit=QtGui.QLineEdit(self.conf.get("module_path"))
        self.mpBrowse=QtGui.QPushButton("Browse")
        self.mpBrowse.clicked.connect(self.mpUpdate)
        self.splash=QtGui.QCheckBox("Show Splash Screen")
        if(self.conf.get("splash_screen")=="yes"):
            self.splash.setChecked(True)
        self.clean=QtGui.QCheckBox("Clean Log on Exit")
        if(self.conf.get("clean_log")=="yes"):
            self.clean.setChecked(True)
        self.status=QtGui.QCheckBox("Show Status Message")
        if(self.conf.get("status_message")=="on"):
            self.status.setChecked(True)
        self.ok=QtGui.QPushButton("Ok")
        self.ok.clicked.connect(self.save)
        self.cancel=QtGui.QPushButton("Cancel")
        self.cancel.clicked.connect(self.close)
        self.default=QtGui.QPushButton("Default")
        self.default.clicked.connect(self.reset)

        ctrl=QtGui.QHBoxLayout()
        ctrl.addWidget(self.ok)
        ctrl.addWidget(self.cancel)
        ctrl.addWidget(self.default)
        layout=QtGui.QGridLayout(self)
        layout.addWidget(self.lpLabel, 0, 0)
        layout.addWidget(self.lpEdit, 0, 1)
        layout.addWidget(self.lpBrowse, 0, 2)
        layout.addWidget(self.mpLabel, 1, 0)
        layout.addWidget(self.mpEdit, 1, 1)
        layout.addWidget(self.mpBrowse, 1, 2)
        layout.addWidget(self.splash, 2, 0)
        layout.addWidget(self.clean, 3, 0)
        layout.addWidget(self.status, 4, 0)
        layout.addLayout(ctrl, 5, 1)

        self.cancel.setFocus()

    def lpUpdate(self):
        self.lpEdit.setText(self.getFolder())
    def cpUpdate(self):
        self.cpEdit.setText(self.getFolder())
    def mpUpdate(self):
        self.mpEdit.setText(self.getFolder())

    def getFolder(self):
        dn=QtGui.QFileDialog.getExistingDirectory()
        if(dn.startswith(QtCore.QDir.currentPath())):
           dn="."+dn[len(QtCore.QDir.currentPath()):]+"/"
        else:
            dn=dn+"/"
        return dn

    def save(self):
        self.conf.set("library_path", self.lpEdit.text())
        self.conf.set("class_path", self.cpEdit.text())
        self.conf.set("module_path", self.mpEdit.text())
        if(self.splash.isChecked()):
            self.conf.set("splash_screen", "yes")
        else:
            self.conf.set("splash_screen", "no")
        if(self.clean.isChecked()):
            self.conf.set("clean_log", "yes")
        else:
            self.conf.set("clean_log", "no")
        if(self.status.isChecked()):
            self.conf.set("status_message", "on")
        else:
            self.conf.set("status_message", "off")
        QtGui.QMessageBox.information(self, "Restart required", "Some settings takes effect only after restarting DDStorm")
        self.close()
        self.conf.write()

    def reset(self):
        self.conf.default()
        self.lpEdit.setText(self.conf.get("library_path"))
        self.cpEdit.setText(self.conf.get("class_path"))
        self.mpEdit.setText(self.conf.get("module_path"))
        if(self.conf.get("splash_screen")=="yes"):
            self.splash.setChecked(True)
        else:
            self.splash.setChecked(False)
        if(self.conf.get("clean_log")=="yes"):
            self.clean.setChecked(True)
        else:
            self.clean.setChecked(False)
        if(self.conf.get("status_message")=="on"):
            self.status.setChecked(True)
        else:
            self.status.setChecked(False)
