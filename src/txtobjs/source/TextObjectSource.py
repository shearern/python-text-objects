from tosAttribute import tosAttribute
from ..tools import wrap_with_indent

class TextObjectSource(object):
    '''Encapsulates a block of text
    
    Typically these are represented by YAML in the format of a dictionary, or
    some other equivalent:
    
        ---
        - class: FileField
          name:  eid
          label: Employee ID
          *:     *
          
    Each block must be parseble down to attributes.
          
    Each document block must have at least these attributes:
        class:  Determines which class is used to interpret the document block
        name:   Identifies the document object.  Multiple document blocks
                with the same class and name will be combined
                
    ''' 
    
    def __init__(self, text_class, name, attributes, filename, line=None):
        '''Init
        
        @param text_class: The class of the documentation block
        @param name:
            Name to identify the documentation block (within text_class)
        @param attributes: Dictionary of attributes
        @param filename: Path to the file block was pulled from
        @param line: Line number block was found at within filename (if known)
        '''
        self.__text_class = text_class
        self.__name = name
        self.__attributes = dict()
        self.__filename = filename
        self.__line_num = int(line)
        
        # Interpret attributes
        if attributes.__class__ is tuple or attributes.__class__ is list:
            for name, value in attributes:
                self.__attributes[name] = tosAttribute(
                     name = name,
                     value = value,
                     filename = filename,
                     line = line)
        else:
            for name in attributes.values():
                self.__attributes[name] = tosAttribute(
                     name = name,
                     value = attributes[name],
                     filename = filename,
                     line = line)

        
        
    @property
    def text_class(self):
        return self.__text_class
    
    @property
    def name(self):
        return self.__name

    @property
    def attr_names(self):
        return list(self.__attributes.keys())

    
    @property
    def attributes(self):
        for attr_name in self.attr_names:
            yield self.__attributes[attr_name]
            
    
    @property
    def filename(self):
        return self.__filename
    
    @property
    def line_num(self):
        return self.__line_num
    
    @property
    def loc(self):
        loc = self.filename
        if self.__line_num is not None:
            loc += ':' + str(self.__line_num)
        return loc
    
    
    def __str__(self):
        src = list()
        
        src.append("%s @ %s:" % (repr(self), self.loc))
        for attr in self.attributes:
            src.append("  %-20s %s" % (
                attr.name+':',
                wrap_with_indent(str(attr.value), 80, 22)))
        
        return "\n".join(src)
        
        
    def __repr__(self):
        return "TextObjectSource('%s', '%s')" % (self.text_class, self.name)
    
    

    
    
        
        