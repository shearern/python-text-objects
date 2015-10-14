from txtobjs.schema import SimpleTextProperty

class DateProperty(SimpleTextProperty):
    '''A field value that represents a date'''

    def __init__(self, text_name):
        super(DateProperty, self).__init__(text_name)


