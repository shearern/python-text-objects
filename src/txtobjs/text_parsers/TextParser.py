from abc import ABCMeta, abstractmethod

class TextParser(object):
    '''Base class for Readers which convert text source to normalized objects'''
    __metaclass__ = ABCMeta


    def __init__(self):
        pass


    @abstractmethod
    def parse(self, src, schema, multiple=False):
        '''Parse an input file and return the associated TextObjects

        @param src: Contents of text file to be parsed
        @param schema: TextObject schema to use to interpret source
        @param multiple: If true, root level of text file is a list of multiple
            objects, each with the Text Class specified by schema

        @return generator: Generated objects
        '''


