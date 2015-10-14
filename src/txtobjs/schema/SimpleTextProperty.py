from TextObjectProperty import TextObjectProperty

class SimpleTextField(TextObjectProperty):
    '''A text field that just stores a simple string (single line?)'''


    def __init__(self, text_name):
        super(SimpleTextField, self).__init__(text_name)


    def handling_code(self):
        return self.SAVE_SINGLE_VALUE


    def valdiate(self, value):
        '''Check the validity of the value store in the field

        @return str: None if no errors, else string error description
        '''
        if value is None or len(value) == 0:
            return "Field value is required"
        if value is not None and value.__class__ is not str:
            return "Value must be a string"
        return None
