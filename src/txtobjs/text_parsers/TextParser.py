from abc import ABCMeta, abstractmethod

class TextParser(object):
    '''Base class for Readers which convert text source to normalized objects'''
    __metaclass__ = ABCMeta


    def __init__(self):
        pass


    @abstractmethod
    def parse(self, path):
        '''Parse an input file and return the associated TextObjects'''