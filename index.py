#! /usr/bin/python3

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

import sys, os
from fnmatch import fnmatch
from conf import Conf
from const import *

class Index:
    def __init__(self, conf=False):
        if(conf):
            self.conf=conf
        else:
            self.conf=Conf()
        self.data={}
        self.compile()

    def compile(self):
        for path, subdirs, files in os.walk(self.conf.get("index_path")):
            for name in files:
                if(fnmatch(name, "*.txt")):
                    with open(self.conf.get("index_path")+name, "r") as f:
                        buff=[]
                        buff.append([])
                        buff.append([])
                        for line in f:
                            line=line.rstrip().split("#")[0]
                            if(len(line)==0):
                                pass
                            else:
                                ws=len(line)-len(line.lstrip())
                                line=line.lstrip().capitalize()
                                if(ws==0):
                                    del buff[0][:]
                                    buff[0].append(line.lstrip())
                                    del buff[1][:]
                                    buff[1].append(0)
                                elif(ws>buff[1][-1]):
                                    buff[0].append(line.lstrip())
                                    buff[1].append(ws)
                                    self.data[buff[0][-1]]=list(reversed(buff[0]))
                                elif(ws==buff[1][-1]):
                                    buff[0][-1]=line.lstrip()
                                    buff[1][-1]=ws
                                    self.data[buff[0][-1]]=list(reversed(buff[0]))
                                elif(ws<buff[1][-1]):
                                    for i in reversed(buff[1]):
                                        if(i>=ws):
                                            buff[0].pop()
                                            buff[1].pop()
                                        else:
                                            buff[0].append(line.lstrip())
                                            buff[1].append(ws)
                                            break
                                    self.data[buff[0][-1]]=list(reversed(buff[0]))

    def upstream(self, name):
        if(len(name)>0):
            if name in self.data:
                return self.data[name]
            else:
                return []

def main():
    i=Index()
    if(len(sys.argv)>1):
        print(i.upstream(sys.argv[1]))

if(__name__=="__main__"):
    main()
