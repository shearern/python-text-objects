'''
Created on May 8, 2014

@author: nshearer
'''

class FieldInfo(object):
    '''Hold info about a field'''
    def __init__(self):
        self.name = None
        self.value = None
        self.handler = None
        self.value_source_loc = None


class TextObject(object):
    '''Base class for objects generated from text source files



    The primary data contained in a TextObject is in fields.  The term "fields"
    here is used to not conflict with Python object properties, but there
    is a close mapping between them.  The fields that belong to a specific
    TextObject are defined by the TextObjectFactory producing the TextObject
    from the text source.

    Field values are made available like Python properties.
    (e.g.: self.first_name = self.get_field_value('first_name') )

    '''

    def __init__(self, text_obj_class):
        self.__text_class = text_obj_class

        self.__field_names = list()
        self.__fields = dict()


    @property
    def text_class(self):
        '''Type of data stored in this TextObject

        Text Objects have a "text_class" which is a string that defines what
        type of data the TextObject is holding.  This is basically a poor-man's
        class implementation, and only used to inform application specific code
        which fields to expect.
        '''
        return self.__text_class


    def define_field(self, name, init_value=None):
        '''Define a new field for this object'''
        pass





