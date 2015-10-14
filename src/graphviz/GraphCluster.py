from GraphNode import sanitize_name

class GraphCluster(object):
    '''Groups nodes into a cluster'''
    
    def __init__(self, name, label=None, **kwargs):
        self.name = sanitize_name(name)
        self.attrs = dict()
        if label is not None:
            self.attrs['label'] = label
        for k, v in kwargs.items():
            self.attrs[k] = v
        self.members = list() # Populated externally
            
    def __str__(self):
        src = list()
        src.append('subgraph cluster_%s {' % (sanitize_name(self.name)))
        for k, v in self.attrs.items():
            src.append('  %s = "%s";' % (k, v))
        for member in self.members:
            src.append('  '+str(member))
        src.append("}")
        return "\n".join(src)

    @property
    def elm_type(self):
        return 'cluster'