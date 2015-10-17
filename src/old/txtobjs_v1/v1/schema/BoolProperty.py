from txtobjs.schema import SimpleTextProperty

class BoolProperty(SimpleTextProperty):

    def __init__(self, text_name):
        super(BoolProperty, self).__init__(text_name)


