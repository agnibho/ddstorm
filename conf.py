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

import os, logging
from const import *
logging.basicConfig(filename=LOG_FILE)

class Conf:
    conf={}
    def __init__(self, filename=CONF_FILE):
        self.filename=filename
        self.default()
        self.read()

    def default(self):
        self.conf["library_path"]="./library/"
        self.conf["custom_path"]="./custom/"
        self.conf["index_path"]="./index/"
        self.conf["alias_path"]="./alias/"
        self.conf["module_path"]="./modules/"
        self.conf["splash_screen"]="yes"
        self.conf["clean_log"]="no"
        self.conf["status_message"]="on"

    def read(self):
        if(os.path.isfile(self.filename)):
            with open(self.filename) as f:
                for line in f:
                    line="".join(line.split())
                    if(line.startswith("#")):
                        pass
                    elif(line.startswith("library_path=")):
                       self.conf["library_path"]=line[13:]
                       if(os.path.isdir(self.conf["library_path"])):
                           if(not self.conf["library_path"].endswith("/")):
                               self.conf["library_path"]+="/"
                    elif(line.startswith("custom_path=")):
                       self.conf["custom_path"]=line[12:]
                       if(os.path.isdir(self.conf["custom_path"])):
                           if(not self.conf["custom_path"].endswith("/")):
                               self.conf["custom_path"]+="/"
                    elif(line.startswith("index_path=")):
                       self.conf["index_path"]=line[11:]
                       if(os.path.isdir(self.conf["index_path"])):
                           if(not self.conf["index_path"].endswith("/")):
                               self.conf["index_path"]+="/"
                    elif(line.startswith("alias_path=")):
                       self.conf["alias_path"]=line[11:]
                       if(os.path.isdir(self.conf["alias_path"])):
                           if(not self.conf["alias_path"].endswith("/")):
                               self.conf["alias_path"]+="/"
                    elif(line.startswith("module_path=")):
                       self.conf["module_path"]=line[12:]
                       if(os.path.isdir(self.conf["module_path"])):
                           if(not self.conf["module_path"].endswith("/")):
                               self.conf["module_path"]+="/"
                    elif(line.startswith("splash_screen=")):
                       self.conf["splash_screen"]=line[14:]
                    elif(line.startswith("clean_log=")):
                       self.conf["clean_log"]=line[10:]
                    elif(line.startswith("status_message=")):
                       self.conf["status_message"]=line[15:]
                    else:
                        logging.warning("Unrecognized configuration: "+line)

    def get(self, key=False):
        if(key):
            return self.conf[key]
        else:
            return self.conf
    def set(self, key, value):
        self.conf[key]=value

    def write(self):
        with open(CONF_FILE, "w") as f:
            for k in self.conf:
                print(k+"="+self.conf[k], file=f)

if(__name__=="__main__"):
    c=Conf(CONF_FILE)
    print(c.get())
