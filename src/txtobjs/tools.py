from textwrap import wrap

def wrap_with_indent(line, wrap_at, indent_len):
    '''Print a line with wordwrap, indenting lines under the first'''
    rtn = list()
    
    # Wrap first line at wrap_at
    lines = wrap(line, wrap_at)
    rtn.append(lines[0])
    
    # Re-wrap remaining lines at wrap_at - indent_len
    lines = wrap("\n".join(lines[1:]), wrap_at - indent_len)
    for line in lines:
        rtn.append(" "*indent_len + ' ' + line)
        
    return "\n".join(rtn)