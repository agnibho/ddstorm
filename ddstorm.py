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
from compile import Compile
from conf import Conf
from index import Index

class DDStorm:
    conf=False
    def __init__(self, comp=False, conf=False):
        if(conf):
            self.conf=conf
        else:
            self.conf=Conf()
        if(comp):
            self.compiler=Compile(conf).compile()
        self.index=Index(conf)

    def dd(self, symptoms):
        if(not symptoms):
            return
        diff1=self._getDiff(symptoms.pop(0))
        for s in symptoms:
            diff2=self._getDiff(s)
            temp=[]
            if(len(diff1)>len(diff2)):
                diff2+=[""]*(len(diff1)-len(diff2))
            elif(len(diff2)>len(diff1)):
                diff1+=[""]*(len(diff2)-len(diff1))
            for (s1, s2) in zip(diff1, diff2):
                if((s1 not in temp) and (len(s1)>0)):
                    if(s1 in diff2):
                        temp.append(s1)
                    else:
                        us=self.index.upstream(s1)
                        for i in us:
                            if(i in diff2):
                                temp.append(i)
                if((s2 not in temp) and (len(s2)>0)):
                    if(s2 in diff1):
                        temp.append(s2)
                    else:
                        us=self.index.upstream(s2)
                        for i in us:
                            if(i in diff1):
                                temp.append(i)
            diff1=list(temp)
        return diff1

    def _getDiff(self, symptom):
        diff=[]
        symptom=symptom.lower().replace("_"," ").replace("-", " ")
        if(os.path.isfile(self.conf.get("module_path")+symptom+".module")):
           with open(self.conf.get("module_path")+symptom+".module", "r") as mf:
               for line in mf:
                   diff.append(line.strip())
        return diff
        
    def symptoms(self):
        symp=[]
        for n in os.listdir(self.conf.get("module_path")):
            symp.append(os.path.splitext(os.path.basename(n))[0].capitalize())
        return symp

def main():
    s=DDStorm()
    if(len(sys.argv)>1):
        for d in s.dd(sys.argv[1:]):
            print(d)
    else:
        for s in s.symptoms():
            print(s)

if(__name__=="__main__"):
    main()
