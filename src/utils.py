
def describe_block_loc(doc_block, container='div'):
    '''Describe where the a docblock is defined at'''
    src = list()
    
    src.append("<%s class='block_loc'>" % (container))
    src.append(doc_block.full_name)
    src.append(" defined at %s" % (doc_block.def_locs_str))
    src.append("</%s>" % (container))
    
    return "\n".join(src)
