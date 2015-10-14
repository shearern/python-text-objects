import weakref

class DocBlockCollection(object):
    '''Collection of documentation blocks'''
    
    def __init__(self):
        self.__blocks = dict()      # [class][name] = DocBlock
        self.__block_order = dict() # [class] = list(names)
        self.cache = dict()         # Cleared every time collection is changed
        
    
    def add(self, doc_block):
        
        if doc_block.doc_class == 'FeedRecordType':
            if doc_block.name in ['earnings', 'deductions', 'workstudy_earnings', 'unemployment_earnings']:
                pass
        
        if not self.__blocks.has_key(doc_block.doc_class):
            self.__blocks[doc_block.doc_class] = dict()
        if self.__blocks[doc_block.doc_class].has_key(doc_block.name):
            raise IndexError("Duplicate index: " + doc_block.full_name)
        self.__blocks[doc_block.doc_class][doc_block.name] = doc_block
        
        if not self.__block_order.has_key(doc_block.doc_class):
            self.__block_order[doc_block.doc_class] = list()
        self.__block_order[doc_block.doc_class].append(doc_block.name)
        
        doc_block._col = weakref.ref(self)
        
        self.cache = dict()
        
        
    def has(self, doc_class, doc_name):
        return self.get(doc_class, doc_name, required=False) is not None
    

    def has_block(self, doc_block):
        return self.has(doc_block.doc_class, doc_block.name)
    
    
    def get(self, doc_class, doc_name, required=True):
        if self.__blocks.has_key(doc_class):
            if self.__blocks[doc_class].has_key(doc_name):
                return self.__blocks[doc_class][doc_name]
            
        if required:
            msg = "No existing doc block for %s.%s"
            raise IndexError(msg % (doc_class, doc_name))
        else:
            return None
        
    
    def remove(self, doc_class, doc_name):
        '''Remove a doc block from the collection'''
        if self.__blocks.has_key(doc_class):
            if self.__blocks[doc_class].has_key(doc_name):
                del self.__blocks[doc_class][doc_name]
        
        if self.__block_order.has_key(doc_class):
            if doc_name in self.__block_order[doc_class]:
                self.__block_order[doc_class].remove(doc_name)
                
        self.cache = dict() 
        
    
    def get_all(self, doc_class=None):
        # Yield all blocks
        if doc_class is None:
            for doc_class in self.__blocks.keys():
                for block in self.get_all(doc_class):
                    yield block
                    
        # Yield all block in a doc class
        else:
            if self.__blocks.has_key(doc_class):
                for doc_name in self.__block_order[doc_class]:
                    yield self.__blocks[doc_class][doc_name]
                    
                    
    def list_all_doc_classes(self):
        return self.__blocks.keys()
    
    
    def count_blocks_with_class(self, doc_class):
        if self.__blocks.has_key(doc_class):
            return len(self.__block_order[doc_class])
        return 0
    
    