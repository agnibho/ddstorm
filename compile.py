#! /usr/bin/python3

'''
This module converts text differetial diagnosis files
to a simplified modular file format that can be used
by the program.
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

import os
import logging
import re
from operator import itemgetter
from fnmatch import fnmatch

from conf import Conf
from const import *
from alias import Alias

logging.basicConfig(filename=LOG_FILE)

class Compile:
    '''
    This class creates a compiler for the DDStorm
    that compiles the text files containing list of
    differential diagnosis to simplified modular
    data files usable by the program.
    '''
    
    def __init__(self, conf=False):
        '''
        The constructor optionally accepts a configuration.
        If none is provided it creates a default configuration.

        Parameters:
        conf - A dictionary containing configuration options
        '''
        if(conf):
            self._conf=conf
        else:
            self._conf=Conf()
        self.clean=True

    def compile(self):
        ''' Compile the text files to DDStorm modules. '''
        self.source=set()
        self.custom=set()
        self.alias=Alias(self._conf)
        
        # Loop over library files and add *.txt files to source
        for path, subdirs, files in os.walk(self._conf.get("library_path")):
            for name in files:
                if(fnmatch(name, "*.txt")):
                    self.source.add(os.path.join(path, name))

        # Loop over custom files and add *.txt files to custom
        for path, subdirs, files in os.walk(self._conf.get("custom_path")):
            for name in files:
                if(fnmatch(name, "*.txt")):
                    self.custom.add(os.path.join(path, name))

        # Create module directory if not already present and delete all module files
        if(not os.path.isdir(self._conf.get("module_path"))):
            os.makedirs(self._conf.get("module_path"))
        for f in os.listdir(self._conf.get("module_path")):
            if(fnmatch(f, "*.module")):
                os.unlink(self._conf.get("module_path")+f)

        # Create a regex for calculating priority from filename
        self.priorityRegex=re.compile("(?<=\.)\d+$")

        # First sort files by priority then compile them to module
        for src in self._sortPriority(self.source):
            self._makeModule(src)
        for src in self._sortPriority(self.custom):
            self._makeModule(src)

    def _sortPriority(self, files):
        ''' Sort data files based on their priority settings. '''
        ls=[]
        # Loop over the files
        for addr in files:
            # Format the file name
            name=os.path.splitext(os.path.basename(addr))[0].lower().replace("_"," ").replace("-", " ")
            # Search for priority tag on file name
            m=re.search(self.priorityRegex, name)
            # Add to ls as (symptom name, priority number, file name) with default priority of 100
            if(m):
                ls.append((name.replace("."+m.group(), ""), int(m.group()), addr))
            else:
                ls.append((name, 100, addr))
        # Sort the file list, first by the symptom name, then by the priority number
        ls.sort(reverse=True)
        if(ls):
            return(list(zip(*ls))[2])
        else:
            return ls
        
    def _makeModule(self, src):
        ''' Create application usable modules from data files. '''
        # Format the file name
        module=os.path.splitext(os.path.basename(src))[0].lower().replace("_"," ").replace("-", " ")
        # Remove the priority tag from file name
        m=re.search(self.priorityRegex, module)
        if(m):
            module=module.replace("."+m.group(), "")
        # Create the module file name
        modFile=self._conf.get("module_path")+module+".module"
        modFlag=False
        # Loop over both files, the source data file and the target module file
        with open(src, "r") as sf, open(modFile, "a") as tf:
            # Ignore lines starting with ! or #, + and - has special meaning, write other lines to module. Log the errors.
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
        # Deal with special lines
        if(modFlag):
            modFlag=False
            with open(src, "r") as f:
                for line in f:
                    line=line.strip().split("#")[0]
                    if(line[1:].replace(" ","").replace("-","").replace("_","").replace("'","").isalnum()):
                        # If line starts with + add it to the module file
                        if(line.startswith("+")):
                            with open(modFile, "r") as fn:
                                text=fn.read()
                            with open(modFile, "w") as fn:
                                print(self.alias.get(line[1:]).capitalize()+"\n"+text, file=fn)
                        # If line starts with - remove corresponding item from the module file
                        elif(line.startswith("-")):
                            with open(modFile, "r") as fn:
                                text=fn.read()
                            text=text.replace(self.alias.get(line[1:]).capitalize()+"\n", "")
                            with open(modFile, "w") as fn:
                                print(text, file=fn)

    def is_clean(self):
            '''Report if compilation ended successfully'''
            return self.clean

def main():
    ''' Compile the data files into formatted module files '''
    c=Compile().compile()

if(__name__=="__main__"):
    main()
