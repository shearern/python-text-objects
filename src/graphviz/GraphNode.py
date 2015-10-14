
def sanitize_name(name):
    return name.replace(' ', '_')


class GraphNode(object):
    '''Encapsulates the source for a node'''
    
    def __init__(self, name, label=None, **kwargs):
        self.name = sanitize_name(name)
        self.attrs = dict()
        if label is not None:
            self.attrs['label'] = label
        for k, v in kwargs.items():
            self.attrs[k] = v
        self.group = None
            
    def __str__(self):        
        if len(self.attrs) > 0:
            attrs = ', '.join(['%s="%s"' % (k, v) for k, v in self.attrs.items()])
            return '%s [%s];' % (
                sanitize_name(self.name),
                attrs);
        else:
            return '%s;' % (sanitize_name(self.name))

    @property
    def elm_type(self):
        return 'node'
