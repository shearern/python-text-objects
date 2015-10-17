from abc import ABCMeta, abstractmethod

class DocBlockFactoryBase(object):
    '''Class to instantiate project specific doc classes
    
    Each text object / documentation block has a defined class string
    This class string dictates which Python object is used to represent the
    documentation block.
    
    This class is derived to convert doc class strings into actual class
    instances
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def create_doc_block(self, doc_class_name):
        pass