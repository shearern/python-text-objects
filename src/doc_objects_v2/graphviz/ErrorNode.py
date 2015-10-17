from GraphNode import GraphNode


class ErrorNode(GraphNode):
    '''Display an error on the graph'''
    
    NEXT_ERROR_ID=0
    
    def __init__(self, error):
        self._error_id = ErrorNode.NEXT_ERROR_ID
        ErrorNode.NEXT_ERROR_ID += 1
        
        super(ErrorNode, self).__init__(
            name = 'error_%d' % (self._error_id),
            shape = 'none',
            label = 'ERROR: ' + error.replace('"', ''),
            fontcolor = 'red')
        
