from TextObjectProperty import TextObjectProperty

class ObjId(TextObjectProperty):
    '''A field that holds an ID that references another TextObject'''


    def __init__(self, text_name):
        super(ObjId, self).__init__(text_name)


    def handling_code(self):
        return self.SAVE_SINGLE_VALUE

