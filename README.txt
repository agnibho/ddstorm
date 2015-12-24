                        DDStorm
                       =========

What is DDStorm?
================

DDStorm is a python application for brainstorming medical differential
diagnosis. It is designed to be modular and easily configurable. It is
meant to be used by the medical professionals.

DDStorm is still in development phase and not ready for deployment.

Usage
=====

Clone the repository to your computer. Alternatively download the
source code zip and extract it.

Run the bash script named 'start' to start the program. Alternatively
run 'python3 __main__.py' within the program directory.

The program has a graphical user interface that can be easily
used.

Add symptoms: type the symptom name in the top text entry box and
click on the <Add> button. Alternatively you can click on the
<Browse_Symptoms> button to browse through a list of available
symptoms and select from there.

The symptoms you add will appear in the left sided panel. Depending on
the symptoms you add the list of differential diagnosis will update
automatically in the right sided panel.

Configuration
=============

You can change the program configuration by editing the 'ddstorm.conf'
file in the program directory. Available options are-

library_path   - The directory where default library data is located
custom_path    - The directory where user created library data is
                 located
index_path     - The directory where the index of disease hierarchy is
                 located
module_path    - The directory where compiled module files will be
                 saved.
alias_path     - The directory where symptom aliases are located
splash_screen  - Setting this to 'yes' (without quote) will show a
                 splash screen while starting up the program
status_message - Setting this to 'on' (without quote) will show status
                 messages in the program main window
clean_log      - Setting this to 'yes' (without quote) will delete
                 previous logs every time the program starts.

Editing DDStorm data
====================

DDStorm is designed to be extremely customizable. All data files are
in plain text format and can be easily edited to suit the need of the
user.

There are three types of files-

Library files - Contains the actual differential diagnosis data
Index files   - Contains the hierarchy of diseases
Alias files   - Contains disease alias

Library files
-------------

* Naming conventions:

Library files are named after the "symptom". Names should be as
concise as possible. But care should be taken to avoid confusion.

Library files are compiled flatly and the directory hierarchy is not
preserved. So the files 'abdominal_pain/generalized.txt' and
abdominal_pain/localized.txt' will result in symptoms named
'generalized' and 'localized'. To avoid such confusion the naming
should be 'abdominal pain, generalized.txt' and
'abdominal pain, localized.txt'. The resulting symptoms would be
easily searchable in the symptom list. E.g. if you enter
'abdominal pain' in the browse box, it would show 'abdominal pain,
generalized' and 'abdominal pain, localized' as available symptoms.

The library files support setting custom priority. The priority can be
set by naming the file as <symptom.priority_number.txt>. For example
in files named 'abdominal pain.50.txt' and 'abdominal pain.120.txt'
the diagnosis mentioned in the second file will come first (120 has
higher priority than 50). If no priority number is mentioned default
priority '100' is used.

The file names may contain space, '-' or '_'. DDStorm converts '-' and
'_' to spaces during execution.

* Data structure:

Library files contain a single diagnosis per line. The diagnosis
should be as specific as possible. Preferably there should be a
corresponding entry in the index files indicating the hierarchy of the
condition.

Index files
-----------

The index files represent the hierarchy of disease conditions. For
example 'acute peritonitis' is a sub-type of 'peritonitis'. Now if
symptom 'A' has a differential diagnosis of 'peritonitis' and symptom
'B' has a differential diagnosis of 'acute peritonitis', their
combined differential diagnosis will be the more general one
i.e. 'peritonitis'.

The index files can be named anything. But for clarity it should be
named according to the disease group it represents. For example an
index files of abdominal conditions can be named 'abdomen.txt'.

* Data structure

Index files contain one disease condition per line. The sub-type of a
disease must be written below it and indented by 'spaces' (not
tabs).

For example:

peritonitis
    acute peritonitis

The disease conditions of the same level should have same number of
spaces for indentation.

Alias files
-----------

The alias files contain the alias of the disease conditions. It's
useful when a same disease may be known by multiple names.

* Data structure

The alias files should have one disease condition per line. The
aliases must be separated with ';'.

Modular structure
-----------------

As the library files are processed flatly, without considering the
directory structures, they can be freely organized in directories as
needed.

The same conditions in different medical discipline can be
kept in separate directories.

For example differential diagnosis abdominal pain in medicine and
surgery can be organized in 'medical/abdominal pain.txt' and
'surgery/abdominal pain.txt' respectively. The program will merge them
together during execution.

Licensing
=========

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

Contacts
========

Agnibho Mondal
mail@agnibho.com
www.agnibho.com
