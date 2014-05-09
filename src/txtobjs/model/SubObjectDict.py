       
from FieldHandler import FieldHanlder

class SubObjectDict(FieldHanlder):
    '''A field that contains sub objects
    
    This is to include a listing 
    '''


    def __init__(self, text_name, text_class):
        '''INit
        
        @param text_class: Class of TextObject this list refers to
        '''
        super(SubObjectDict, self).__init__(text_name)


    def handling_code(self):
        return self.SAVE_LIST_ITEMS
        