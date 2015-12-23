#! /usr/bin/python3

'''
This module handles the upstream ancestors of symptoms.

The symptoms can be classified in different levels, with the more
generalized symtoms at upstream and the more specialized symptoms at
the downstream.

For example:
'Acute peritonitis' is a special type of 'peritonitis'
Hence 'peritionitis' will be at upstream and 'acute peritonitis' will be
at downstream.
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
import os
from fnmatch import fnmatch

from conf import Conf
from const import *

class Index:
    ''' Provides an index of the upstream ancestors of symptoms '''
    def __init__(self, conf=False):
        '''
        Initiate the index object. Accepts a Conf object as an
        optional parameter.
        '''
        if(conf):
            self.conf=conf
        else:
            self.conf=Conf()
        self.data={}
        self.compile()

    def compile(self):
        '''
        Compile the text index files to a application usable format.
        '''
        # Loop over all files under index_path
        for path, subdirs, files in os.walk(self.conf.get("index_path")):
            for name in files:
                # Only files with *.txt suffix
                if(fnmatch(name, "*.txt")):
                    with open(self.conf.get("index_path")+name, "r") as f:
                        # Two dimensional list buffer to hold the index
                        buff=[]
                        buff.append([])
                        buff.append([])
                        # Loop over all lines as separate entries
                        for line in f:
                            # Ignore commnents starting with #
                            line=line.rstrip().split("#")[0]
                            if(len(line)==0):
                                pass
                            else:
                                # Find number of leading whitespaces
                                ws=len(line)-len(line.lstrip())
                                # Format the entry
                                line=line.lstrip().capitalize()
                                
                                # No leading whitespace means a top level entry i.e. no upstream ancestor
                                if(ws==0):
                                    # Empty the buffer and add the entry
                                    del buff[0][:]
                                    buff[0].append(line.lstrip())
                                    # Reset the whitespace index
                                    del buff[1][:]
                                    buff[1].append(0)
                                # If leading whitespace > indexed whitespace, the entry is a subcategory of previous entry
                                elif(ws>buff[1][-1]):
                                    # Append entry to buffer as new item
                                    buff[0].append(line.lstrip())
                                    # Record leading whitespace to buffer
                                    buff[1].append(ws)
                                    # Copy buffer to data list
                                    self.data[buff[0][-1]]=list(reversed(buff[0]))
                                # If leading whitespace == indexed whitespace, the entry is at the same level with the previous entry
                                elif(ws==buff[1][-1]):
                                    # Append entry to last item of buffer
                                    buff[0][-1]=line.lstrip()
                                    buff[1][-1]=ws
                                    # Copy buffer to data list
                                    self.data[buff[0][-1]]=list(reversed(buff[0]))
                                # If leading whitespace < indexed whitespace, the entry is at an upper category than the previous entry
                                elif(ws<buff[1][-1]):
                                    # Loop over the buffer in reverse
                                    for i in reversed(buff[1]):
                                        # Discard all lower category items
                                        if(i>=ws):
                                            buff[0].pop()
                                            buff[1].pop()
                                        #Append the entry to buffer
                                        else:
                                            buff[0].append(line.lstrip())
                                            buff[1].append(ws)
                                            break
                                    # Copy buffer to data list
                                    self.data[buff[0][-1]]=list(reversed(buff[0]))

    def upstream(self, name):
        '''
        Return the upstream list of a symptom

        Parameter:
        name - the name of the symptom as string

        Return value:
        List of strings containing the upstream items
        '''
        if(len(name)>0):
            if name in self.data:
                return self.data[name]
            else:
                return []

    def names(self):
        ''' Return all indexed symptoms name '''
        return list(self.data.keys())

def main():
    '''
    Prints upstream items of a symptom provided as command line
    argument.
    If no argument provided, returns a list of all indexed symptoms.
    '''
    i=Index()
    if(len(sys.argv)>1):
        print(i.upstream(sys.argv[1]))
    else:
        print(i.names())

if(__name__=="__main__"):
    main()
