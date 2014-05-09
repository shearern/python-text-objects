from FieldHandler import FieldHanlder

class SimpleTextField(FieldHanlder):
    '''A text field that just stores a simple string (single line?)'''


    def __init__(self, text_name):
        super(SimpleTextField, self).__init__(text_name)


    def handling_code(self):
        return self.SAVE_SINGLE_VALUE
