#! /usr/bin/python3

''' This module handles the different configuration options of DDStorm. '''

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

from const import *

logging.basicConfig(filename=LOG_FILE)

class Conf:
    '''
    * This class manages DDStorm configuration options.
    * If the configuration file is found it reads the file
      and initiates the configurations.
    * If configuration couldn't be read it initiates some
      default configurations.
    * It provides the configurations to other classes through
      function calls.
    '''
    
    _conf={}
    
    def __init__(self, filename=CONF_FILE):
        '''
        The constructor accepts a configuration filename.
        If none is provided it defaults to CONF_FILE from const.
        Calls default() and read()
        '''
        self.filename=filename
        self.default()
        self.read()

    def default(self):
        ''' Set the default values '''
        self._conf["library_path"]="./library/"
        self._conf["custom_path"]="./custom/"
        self._conf["index_path"]="./index/"
        self._conf["alias_path"]="./alias/"
        self._conf["module_path"]="./modules/"
        self._conf["splash_screen"]="yes"
        self._conf["clean_log"]="no"
        self._conf["status_message"]="on"

    def read(self):
        ''' Read the configuration file and collect the values '''
        # If file is actually present
        if(os.path.isfile(self.filename)):
            try:
                with open(self.filename) as f:
                    for line in f:
                        # Removes any stray whitespaces
                        line="".join(line.split())
                        # Ignores comments starting with #
                        if(line.startswith("#")):
                            pass
                        # Library path
                        elif(line.startswith("library_path=")):
                            self._conf["library_path"]=line[13:]
                            if(os.path.isdir(self._conf["library_path"])):
                               if(not self._conf["library_path"].endswith("/")):
                                   self._conf["library_path"]+="/"
                        # Custom path
                        elif(line.startswith("custom_path=")):
                            self._conf["custom_path"]=line[12:]
                            if(os.path.isdir(self._conf["custom_path"])):
                               if(not self._conf["custom_path"].endswith("/")):
                                   self._conf["custom_path"]+="/"
                        # Index path
                        elif(line.startswith("index_path=")):
                            self._conf["index_path"]=line[11:]
                            if(os.path.isdir(self._conf["index_path"])):
                               if(not self._conf["index_path"].endswith("/")):
                                   self._conf["index_path"]+="/"
                        # Alias path
                        elif(line.startswith("alias_path=")):
                            self._conf["alias_path"]=line[11:]
                            if(os.path.isdir(self._conf["alias_path"])):
                               if(not self._conf["alias_path"].endswith("/")):
                                   self._conf["alias_path"]+="/"
                        # Module path
                        elif(line.startswith("module_path=")):
                            self._conf["module_path"]=line[12:]
                            if(os.path.isdir(self._conf["module_path"])):
                               if(not self._conf["module_path"].endswith("/")):
                                   self._conf["module_path"]+="/"
                        # Splash screen
                        elif(line.startswith("splash_screen=")):
                            self._conf["splash_screen"]=line[14:]
                        # Clean log
                        elif(line.startswith("clean_log=")):
                            self._conf["clean_log"]=line[10:]
                        # Status message
                        elif(line.startswith("status_message=")):
                            self._conf["status_message"]=line[15:]
                        # Unknown option
                        else:
                            logging.warning("Unrecognized configuration: "+line)
            except:
                logging.error("Configuration file "+self.filename+" could not be read. Using default configurations.")

    def get(self, key=False):
        '''
        Return the requested configuration item.
        Return all if none specified.

        Parameters:
        key - string specifying the configuration item name
        
        Return value:
        String value if key is specified
        Dictionary containing all options if key not specified
        '''
        if(key):
            return self._conf[key]
        else:
            return self._conf

    def set(self, key, value):
        '''
        Allow modification of a configuration to a new value

        Parameters:
        key - configuration item name
        value - the value to set the configuration item to
        '''
        self._conf[key]=value

    def write(self):
        ''' Write configurations to file '''
        with open(CONF_FILE, "w") as f:
            for k in self._conf:
                print(k+"="+self._conf[k], file=f)

#If invoked directly, prints a list of available configurations
if(__name__=="__main__"):
    c=Conf(CONF_FILE)
    print(c.get())
