from textwrap import wrap

class DocBlockAttribute(object):
    '''A single attribute set for a doc block'''
    
    def __init__(self, name, value, block_class, block_name, filename, line=None):
        self.name = str(name)
        self.value = self._translate_raw_value(value)
        self.block_class = block_class
        self.block_name = block_name
        self.filename = filename
        self.line = line

    @property
    def full_name(self):
        return "%s('%s').%s" % (self.block_class, self.block_name, self.name)
    

    @property
    def value_as_list(self):
        if self.value.__class__ is list:
            return self.value
        elif self.value.__class__ is str:
            return [v.strip() for v in self.value.split(",")]        
    
    @property
    def loc(self):
        loc = self.filename
        if self.line is not None:
            loc += ':' + str(self.line)
        return loc
    
    
    def _translate_raw_value(self, value):
        if value is None:
            return None
        if value.__class__ is str:
            if len(value.strip()) == 0:
                return None
            return value.strip()
        return value

    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return "DocBlockAttribute('%s')" % (self.name)
    
    


class RawDocBlock(object):
    '''Encapsulates a block of documentation
    
    The base item of documentation for this engine are Documentation Blocks.
    Typically these are represented by YAML in the format of a dictionary:
        ---
        - class: FileField
          name:  eid
          label: Employee ID
          *:     *
          
    Each document block must have at least these attributes:
        class:  Determines which class is used to interpret the document block
        name:   Identifies the document object.  Multiple document blocks
                with the same class and name will be combined
                
    ''' 
    
    def __init__(self, doc_class, name, attributes, filename, line=None):
        '''Init
        
        @param doc_class: The class of the documentation block
        @param name: Name to identify the documentation block (within class)
        @param attributes: Dictionary of attributes
        @param filename: Path to the file docblock was pulled from
        @param line: Lin number docblock was found at
        '''
        self.__doc_class = doc_class
        self.__name = name
        self.__attributes = dict(attributes)
        self.__filename = filename
        self.__line_num = line
        
        
    @property
    def doc_class(self):
        return self.__doc_class
    
    @property
    def name(self):
        return self.__name

    @property
    def attr_names(self):
        return self.__attributes.keys()

    @property
    def attributes(self):
        for attr_name in self.attr_names:
            yield DocBlockAttribute(
                name = attr_name,
                value = self.__attributes[attr_name],
                block_class = self.__doc_class,
                block_name = self.name,
                filename = self.__filename,
                line = self.__line_num)
    
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
        
        def wrap_with_indent(line, wrap_at, indent_len):
            '''Print a line with wordwrap, indenting lines under the first'''
            rtn = list()
            
            # Wrap first line at wrap_at
            lines = wrap(line, wrap_at)
            rtn.append(lines[0])
            
            # Re-wrap remaining lines at wrap_at - indent_len
            lines = wrap("\n".join(lines[1:]), wrap_at - indent_len)
            for line in lines:
                rtn.append(" "*indent_len + ' ' + line)
                
            return "\n".join(rtn)
        
        
        src.append("%s @ %s:" % (repr(self), self.loc))
        for attr in self.attributes:
            src.append("  %-20s %s" % (
                attr.name+':',
                wrap_with_indent(str(attr.value), 80, 22)))
        
        return "\n".join(src)
        
        
    def __repr__(self):
        return "RawDocBlock('%s', '%s')" % (self.doc_class, self.name)
    
    

    
    
        
        