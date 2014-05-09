from FieldHandler import FieldHanlder

class SimpleTextField(FieldHanlder):
    '''A text field that just stores a simple string (single line?)'''


    def __init__(self, text_name, case_sensitive=False):
        super(SimpleTextField, self).__init__(text_name, case_sensitive)


    def handling_code(self):
        return self.SAVE_SINGLE_VALUE
