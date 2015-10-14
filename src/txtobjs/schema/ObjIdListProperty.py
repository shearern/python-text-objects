from TextObjectProperty import TextObjectProperty

class ObjIdList(TextObjectProperty):
    '''A field that list the IDs of another text object'''


    def __init__(self, text_name, text_class):
        '''INit

        @param text_class: Class of TextObject this list refers to
        '''
        super(ObjIdList, self).__init__(text_name)


    def handling_code(self):
        return self.SAVE_LIST_ITEMS


    def valdiate(self, value):
        '''Check the validity of the value store in the field

        @return str: None if no errors, else string error description
        '''
        return None
