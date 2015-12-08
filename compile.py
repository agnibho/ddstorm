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

import os, logging, re
from operator import itemgetter
from fnmatch import fnmatch
from conf import Conf
from const import *
from alias import Alias
logging.basicConfig(filename=LOG_FILE)

class Compile:
    def __init__(self, conf=False):
        self.source=set()
        self.custom=set()
        if(conf):
            self.conf=conf
        else:
            self.conf=Conf()
        self.alias=Alias(conf)
        self.clean=True
        for path, subdirs, files in os.walk(self.conf.get("library_path")):
            for name in files:
                if(fnmatch(name, "*.txt")):
                    self.source.add(os.path.join(path, name))
        for path, subdirs, files in os.walk(self.conf.get("custom_path")):
            for name in files:
                if(fnmatch(name, "*.txt")):
                    self.custom.add(os.path.join(path, name))
        if(not os.path.isdir(self.conf.get("module_path"))):
            os.makedirs(self.conf.get("module_path"))
        for f in os.listdir(self.conf.get("module_path")):
            if(fnmatch(f, "*.module")):
                os.unlink(self.conf.get("module_path")+f)
        self.priorityRegex=re.compile("(?<=\.)\d+$")
        for src in self._sortPriority(self.source):
            self._makeModule(src)
        for src in self._sortPriority(self.custom):
            self._makeModule(src)

    def _sortPriority(self, files):
        ls=[]
        for addr in files:
            name=os.path.splitext(os.path.basename(addr))[0].lower().replace("_"," ").replace("-", " ")
            m=re.search(self.priorityRegex, name)
            if(m):
                ls.append((name.replace("."+m.group(), ""), int(m.group()), addr))
            else:
                ls.append((name, 100, addr))
        ls.sort(reverse=True)
        if(ls):
            return(list(zip(*ls))[2])
        else:
            return ls
        
    def _makeModule(self, src):
        module=os.path.splitext(os.path.basename(src))[0].lower().replace("_"," ").replace("-", " ")
        m=re.search(self.priorityRegex, module)
        if(m):
            module=module.replace("."+m.group(), "")
        modFile=self.conf.get("module_path")+module+".module"
        modFlag=False
        with open(src, "r") as sf, open(modFile, "a") as tf:
            for line in sf:
                line=line.strip().split("#")[0]
                if(len(line)==0):
                    pass
                elif(line.startswith("!")):
                    pass
                elif(line.startswith("#")):
                    pass
                elif(line.startswith("+")):
                    modFlag=True
                elif(line.startswith("-")):
                    modFlag=True
                elif(line.replace(" ","").replace("-","").replace("_","").replace("'","").isalnum()):
                    print(self.alias.get(line).capitalize(), file=tf)
                else:
                    self.clean=False
                    logging.warning("Syntax error in file '"+src+"': "+line)
        if(modFlag):
            modFlag=False
            with open(src, "r") as f:
                for line in f:
                    line=line.strip().split("#")[0]
                    if(line[1:].replace(" ","").replace("-","").replace("_","").replace("'","").isalnum()):
                        if(line.startswith("+")):
                            with open(modFile, "r") as fn:
                                text=fn.read()
                            with open(modFile, "w") as fn:
                                print(self.alias.get(line[1:]).capitalize()+"\n"+text, file=fn)
                        elif(line.startswith("-")):
                            with open(modFile, "r") as fn:
                                text=fn.read()
                            text=text.replace(self.alias.get(line[1:]).capitalize()+"\n", "")
                            with open(modFile, "w") as fn:
                                print(text, file=fn)

def main():
    c=Compile()

if(__name__=="__main__"):
    main()