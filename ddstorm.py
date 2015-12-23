#! /usr/bin/python3

'''
DDStorm is a python application for finding differential diagnosis for
a given list of symptoms.
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

from compile import Compile
from conf import Conf
from index import Index

class DDStorm:
    ''' Provides the class for finding differential diagnosis. '''
    conf=False
    
    def __init__(self, comp=False, conf=False):
        '''
        Initiate the diagnosis finder.

        Parameters:
        comp - Recompiles the data files if set to True
        conf - Supply a Conf object
        '''
        if(conf):
            self.conf=conf
        else:
            self.conf=Conf()
        self.compiler=Compile(conf)
        if(comp):
            self.compiler.compile()
        self.index=Index(conf)

    def dd(self, symptoms):
        '''
        Find the differential diagnosis list.

        Parameter:
        symptom - list of strings containing symptoms

        Return value:
        List of strings containing the differential diagnosis
        '''

        # Return empty list if symptom list is empty
        if(not symptoms):
            return
        
        # Find DD of first symptom and discard it
        diff1=self._getDiff(symptoms.pop(0))

        # Loop through the rest of the list
        for s in symptoms:
            
            # Find DD of the current item in the list
            diff2=self._getDiff(s)

            # List for temporary holding the DDs
            temp=[]

            # Make both lists the same length by appending empty strings to the end
            if(len(diff1)>len(diff2)):
                diff2+=[""]*(len(diff1)-len(diff2))
            elif(len(diff2)>len(diff1)):
                diff1+=[""]*(len(diff2)-len(diff1))

            # Loop over both lists
            for (s1, s2) in zip(diff1, diff2):

                # Add s1 to temp if s1 or any of its upstream ancestor is common to both list
                if((s1 not in temp) and (len(s1)>0)):
                    if(s1 in diff2):
                        temp.append(s1)
                    else:
                        us=self.index.upstream(s1)
                        for i in us:
                            if(i in diff2):
                                temp.append(i)

                # Add s2 to temp if s2 or any of its upstream ancestor is common to both list
                if((s2 not in temp) and (len(s2)>0)):
                    if(s2 in diff1):
                        temp.append(s2)
                    else:
                        us=self.index.upstream(s2)
                        for i in us:
                            if(i in diff1):
                                temp.append(i)

            # Copy temp to first list
            diff1=list(temp)

        return diff1

    def _getDiff(self, symptom):
        ''' Return differential diagnosis for a single symptom '''
        diff=[]
        symptom=symptom.lower().replace("_"," ").replace("-", " ")
        if(os.path.isfile(self.conf.get("module_path")+symptom+".module")):
           with open(self.conf.get("module_path")+symptom+".module", "r") as mf:
               for line in mf:
                   diff.append(line.strip())
        return diff
        
    def symptoms(self):
        '''
        Return a full list of available symptoms

        Return value:
        List of string containing symptoms
        '''
        symp=[]
        for n in os.listdir(self.conf.get("module_path")):
            symp.append(os.path.splitext(os.path.basename(n))[0].capitalize())
        return symp

def main():
    '''
    Find differential diagnosis in command line mode.
    Accepts symptoms as command line arguments. Prints a list of
    avialable symptoms if called without any argument.

    Command line arguments:
    A list of symptoms separated by space
    '''
    s=DDStorm()
    if(len(sys.argv)>1):
        for d in s.dd(sys.argv[1:]):
            print(d)
    else:
        for s in s.symptoms():
            print(s)

if(__name__=="__main__"):
    main()
