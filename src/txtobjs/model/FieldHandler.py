from abc import ABCMeta, abstractmethod

class FieldHanlder(object):
    '''Defines how to treat a field within the text source'''
    __metaclass__ = ABCMeta


    def __init__(self, text_name, case_sensitive=False):
        '''Init

        @param text_property_name: Name of the field in the text file
        @param case_sensitive: Is text_name case sensitive
        '''
        self.__match_text_name = text_name
        self.__text_name_case_sensitive = case_sensitive
        self.__identifies_obj = False
        self.__required = False


    @property
    def is_unique_id(self):
        '''Does this this field value unqiuely identify the object'''
        return self.__identifies_obj


    @property
    def is_required(self):
        '''Is this field required to have a value on every text object?'''
        return self.__required


    def matches_text_name(self, text_name):
        '''Check to see if the give text name matches this field handler

        @param text_name: Name of the field from the text source
        '''
        if self.__text_name_case_sensitive:
            return text_name == self.__match_text_name

        text_name = text_name.lower()
        my_name = self.__match_text_name.lower()
        return text_name == my_name


    # -- Fluid Interface ------------------------------------------------------

    def identifies_obj(self):
        '''Note that this field can be used to unqiuely identify the object'''
        self.__identifies_obj = True
        self.required()
        return self


    def required(self):
        self.__required = True
        return self


    # -- Value Handling -------------------------------------------------------

    # Single values are the basic fields where the value is a single value
    # that needs to be stored.
    # Parser should:
    #  1) Call convert_parsed_value()
    #  2) Save the parsed value to the field value
    SAVE_SINGLE_VALUE = 'SAVE_SINGLE_VALUE'

    @abstractmethod
    def handling_code(self):
        '''Tell parser what to do with this field when it is being parsed

        This method must return one of the class constants which instructs
        the parser how to handle the value.  This is used primarily to help
        the parser know if it's parsing a field value, a sub object, or a
        collection value.

        @return str: Class constant
        '''


    def convert_parsed_value(self, parsed_value):
        '''Take the value parsed from the text file and encode value for field

        @param parsed_value: Value parsed from text source.  Typically str.
        @return: Value to save as field value
        '''
        return parsed_value