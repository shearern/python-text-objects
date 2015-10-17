import yaml
from StringIO import StringIO

from TextParser import TextParser

class YamlTextParser(TextParser):
    '''Parse YAML formatted files into NormTextObjects'''


    def __init__(self):
        super(YamlTextParser, self).__init__()


    def parse(self, src, schema, multiple=False):
        '''Parse an input file and return the associated TextObjects

        @param src: Contents of text file to be parsed
        @param schema: TextObject schema to use to interpret source
        @param multiple: If true, root level of text file is a list of multiple
            objects, each with the Text Class specified by schema

        @return generator: Generated objects
        '''

        # Parse YAML source
        fh = StringIO(src)
        data = yaml.load(fh)

        
