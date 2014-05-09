from FieldHandler import FieldHanlder

class RemoteObjList(FieldHanlder):
    '''A field that list the IDs of another text object'''


    def __init__(self, text_name, text_class):
        '''INit
        
        @param text_class: Class of TextObject this list refers to
        '''
        super(RemoteObjList, self).__init__(text_name)


    def handling_code(self):
        return self.SAVE_LIST_ITEMS
