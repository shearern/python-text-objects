from GraphNode import GraphNode

class RecordNodeRow(object):
    def __init__(self, label):
        self.label = label
        self.port_name = None
    def __str__(self):
        if self.port_name is None:
            return str(self.label)
        else:
            return "<%s> %s" % (self.port_name, self.label)
        

class RecordNode(GraphNode):
    '''Encapsulates the source for a node'''
    
    def __init__(self, name, **kwargs):
        super(RecordNode, self).__init__(name, shape='record')
        self._rows = list()
        for k, v in kwargs.items():
            self.attrs[k] = v
        
        
    def add_row(self, label, port_name=None):
        row = RecordNodeRow(label)
        self._rows.append(row)
        if port_name is not None:
            row.port_name = port_name
            
                
    def __str__(self):        
        self.attrs['label'] = ' | '.join([str(row) for row in self._rows])
        return super(RecordNode, self).__str__()

