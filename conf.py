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

from const import *                     # Import constants

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
    
    conf={} #Initiates configuration dictionary
    
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
        self.conf["library_path"]="./library/"
        self.conf["custom_path"]="./custom/"
        self.conf["index_path"]="./index/"
        self.conf["alias_path"]="./alias/"
        self.conf["module_path"]="./modules/"
        self.conf["splash_screen"]="yes"
        self.conf["clean_log"]="no"
        self.conf["status_message"]="on"

    def read(self):
        ''' Read the configuration file and collect the values '''
        if(os.path.isfile(self.filename)):         # If file is actually present
            try:
                with open(self.filename) as f:     # Open file
                    for line in f:
                        line="".join(line.split()) # Removes any stray whitespaces
                        if(line.startswith("#")):  # Ignores comments
                            pass
                        elif(line.startswith("library_path=")):                 # Library files path
                            self.conf["library_path"]=line[13:]
                            if(os.path.isdir(self.conf["library_path"])):
                               if(not self.conf["library_path"].endswith("/")):
                                   self.conf["library_path"]+="/"
                        elif(line.startswith("custom_path=")):                  # Custom files path
                            self.conf["custom_path"]=line[12:]
                            if(os.path.isdir(self.conf["custom_path"])):
                               if(not self.conf["custom_path"].endswith("/")):
                                   self.conf["custom_path"]+="/"
                        elif(line.startswith("index_path=")):                   # Index files path
                            self.conf["index_path"]=line[11:]
                            if(os.path.isdir(self.conf["index_path"])):
                               if(not self.conf["index_path"].endswith("/")):
                                   self.conf["index_path"]+="/"
                        elif(line.startswith("alias_path=")):                   # Alias files path
                            self.conf["alias_path"]=line[11:]
                            if(os.path.isdir(self.conf["alias_path"])):
                               if(not self.conf["alias_path"].endswith("/")):
                                   self.conf["alias_path"]+="/"
                        elif(line.startswith("module_path=")):                  # Path to save compiled modules
                            self.conf["module_path"]=line[12:]
                            if(os.path.isdir(self.conf["module_path"])):
                               if(not self.conf["module_path"].endswith("/")):
                                   self.conf["module_path"]+="/"
                        elif(line.startswith("splash_screen=")):                # Whether to show a splash screen
                            self.conf["splash_screen"]=line[14:]
                        elif(line.startswith("clean_log=")):                    # Whether to clean logs before exit
                            self.conf["clean_log"]=line[10:]
                        elif(line.startswith("status_message=")):               # Whether to show status messages
                            self.conf["status_message"]=line[15:]
                        else:
                            logging.warning("Unrecognized configuration: "+line) # Log a warning if unrecognized option found
            except:     # Go with default if file could not be read and log an error
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
            return self.conf[key]
        else:
            return self.conf

    def set(self, key, value):
        '''
        Allow modification of a configuration to a new value

        Parameters:
        key - configuration item name
        value - the value to set the configuration item to
        '''
        self.conf[key]=value

    def write(self):
        ''' Write configurations to file '''
        with open(CONF_FILE, "w") as f:
            for k in self.conf:
                print(k+"="+self.conf[k], file=f)

#If invoked directly, prints a list of available configurations
if(__name__=="__main__"):
    c=Conf(CONF_FILE)
    print(c.get())
