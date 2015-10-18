
class tosAttribute(object):
    '''A single attribute value interpreted from the source text
    
    These store attribute values for TextObjectSource objects.
    '''
    
    def __init__(self, name, value, filename, line=None):
        '''
        @param name: Name of the attribute
        @param value: Value of the attribute as extracted from text source
        @param filename: Name of the file that this attribute value came from
        @param line: Line number in the file this 
        '''
        
        self.name = str(name)
        self.__value = value
        
        # Source info
        self.filename = filename
        self.line = line

    
    @property
    def value(self):
        value = self.__value
        if value is None:
            return None
        if value.__class__ is str:
            value = value.strip()
            if len(value) == 0:
                return None
        return value


    @property
    def value_as_list(self):
        value = self.value
        if value.__class__ is list:
            return value
        elif value.__class__ is str:
            return [v.strip() for v in value.split(",")]
        else:
            msg = "Don't know how to interpret %s as a list"
            raise ValueError(msg % (value.__class__.__name__))        
    
    @property
    def loc(self):
        loc = self.filename
        if self.line is not None:
            loc += ':' + str(self.line)
        return loc
    
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return "tosAttribute('%s')" % (self.name)
    
    
