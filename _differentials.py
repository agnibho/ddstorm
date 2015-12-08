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

from PyQt4 import QtGui

class Differentials(QtGui.QFrame):
    data=[]
    def __init__(self):
        super(Differentials, self).__init__()
        self.initUI()
    def initUI(self):
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
        self.data=data
        self.listWidget.clear()
        if(self.data):
            for d in self.data:
                QtGui.QListWidgetItem(d, self.listWidget)

    def getList(self):
        return self.data
