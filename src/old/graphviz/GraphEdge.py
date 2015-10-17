from GraphNode import sanitize_name

class GraphEdge(object):
    '''Encapsulates the source for an edge'''
    
    def __init__(self, from_node, to_node, label=None, **kwargs):
        self.from_node = sanitize_name(from_node)
        self.to_node = sanitize_name(to_node)
        
        self.attrs = dict()
        if label is not None:
            self.attrs['label'] = label
        for k, v in kwargs.items():
            self.attrs[k] = v
            
            
    def __str__(self):        
        if len(self.attrs) > 0:
            attrs = ', '.join(['%s="%s"' % (k, v) for k, v in self.attrs.items()])
            return '%s -> %s [%s];' % (
                sanitize_name(self.from_node),
                sanitize_name(self.to_node),
                attrs);
        else:
            return '%s -> %s;' % (
                sanitize_name(self.from_node),
                sanitize_name(self.to_node))
            
    @property
    def elm_type(self):
        return 'edge'            
        