#! /usr/bin/python3

''' This module handles the aliases of the symptoms. '''
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

class Alias:
    ''' Provides the class to handle symptom aliases '''
    
    def __init__(self, conf=False):
        '''
        Initiates the alias object
        Accepts a Conf object as parameter
        '''
        self.data={}
        if(conf):
            self.conf=conf
        else:
            self.conf=Conf()
        self.compile()

    def compile(self):
        ''' Compile the plaintext index files to a program usable format '''
        # Loop over the alias files
        for path, subdirs, files in os.walk(self.conf.get("alias_path")):
            for name in files:
                if(fnmatch(name, "*.txt")):
                    # Open the *.txt files
                    with open(self.conf.get("alias_path")+name, "r") as f:
                        for line in f:
                            # Ignore lines starting with #
                            line=line.rstrip().split("#")[0]
                            if(len(line)==0):
                                pass
                            else:
                                terms=[]
                                # Split words separated by ; and add to the terms
                                for i in line.split(";"):
                                    if(i.strip()):
                                        terms.append(i.strip())
                                # If alias present, add terms to the data
                                if(len(terms)==2):
                                    self.data[terms[-1]]=terms[0]
                                elif(len(terms)>2):
                                    t=terms.pop(0)
                                    for i in terms:
                                        self.data[i]=t

    def get(self, term):
        '''
        Return the alias of the queried symptom

        Parameter:
        term - Queried string

        Return value:
        String containing the alias of the term
        '''
        if(term in self.data):
            return self.data[term]
        else:
            return term

def main():
    ''' Print the alias of the command line argument '''
    a=Alias()
    if(len(sys.argv)>1):
        print(a.get(sys.argv[1]))

if(__name__=="__main__"):
    main()
