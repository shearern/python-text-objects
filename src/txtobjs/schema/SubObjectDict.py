
from FieldHandler import FieldHanlder

class SubObjectDict(FieldHanlder):
    '''A field that contains sub objects

    This is to include a listing
    '''


    def __init__(self, text_name, schema):
        '''INit

        @param schema: Schema to apply to objects in collection
        '''
        super(SubObjectDict, self).__init__(text_name)


    def handling_code(self):
        return self.SAVE_LIST_ITEMS


    def valdiate(self, value):
        '''Check the validity of the value store in the field

        @return str: None if no errors, else string error description
        '''
        return None
