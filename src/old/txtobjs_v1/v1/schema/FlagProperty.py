from txtobjs.schema import SimpleTextProperty

class FlagField(SimpleTextProperty):
    '''A field value that is true if the field is defined'''

    def __init__(self, text_name):
        super(FlagField, self).__init__(text_name)


