Python Text Objects
===================

Create Python objects from text files.

This project is designed to assist with quickly creating Python objects
from text files.  There are a few situations where a developer may wish
to create Python objects directly from text files such as XML, YAML, or INI.
This library simply tries to make that process as quick as possible.

Project Goals
-------------

 - Take one or more text files with an optionally hierarchical plain text format,
   and generate object instances that can be used in Python projects.
 - Secondary Goals
    - Allow object base class to be configured to allow generated classes to be
      modified
    - Allow easy cross-referencing between generated objects
      (e.g.: person.fater -> another_person)
    - Allow unique naming of objects and collecting into dictionaries (or not
      nameing, and collecting into lists)
    - Validate text file properties w/rules
    - Specifying property value interpretations such as dates

