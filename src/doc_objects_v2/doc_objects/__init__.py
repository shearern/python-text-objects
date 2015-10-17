'''Classes for interpreting doc blocks'''

import sys
import subprocess
from textwrap import wrap

from exceptions import DocBlockStructureError


DOC_OBJECT_CLASSES = [
    # TODO
]

def encap_doc_block(raw_block):
    '''Get correct classes to interpret this raw_block'''
    global DOC_OBJECT_CLASSES
    for doc_class in DOC_OBJECT_CLASSES:
        if raw_block.doc_class == doc_class.__name__:
            return doc_class(raw_block)

    raise DocBlockStructureError(
        "No doc class found for '%s'" % (raw_block.doc_class))


from .RawDocBlock import RawDocBlock

def print_doc_classes_help():
    '''Print out doc class documentation to help developer'''
    global DOC_OBJECT_CLASSES
    for doc_class in sorted(DOC_OBJECT_CLASSES, key=lambda c: c.__name__):
        print("-"*80)
        print("")
        raw_block = RawDocBlock(doc_class.__name__,
                                name='temp',
                                attributes=dict(),
                                filename='fake')
        doc_obj = doc_class(raw_block)
        doc_obj.print_doc_class_help()
        

        
from graphviz.writer import get_graphviz_path
from graphviz.GraphNode import GraphNode
from graphviz.GraphEdge import GraphEdge
        
def write_doc_class_help_graph(output_file_path):
    '''Produce a Graphviz graph showing the structure of the doc class links'''
    global DOC_OBJECT_CLASSES
    
    src = list()

    src.append('digraph doc_classes {')
    src.append("node [shape=box];")
    src.append("rankdir=BT;")
    src.append("fontname=Helvetica;")
            
    for doc_class in DOC_OBJECT_CLASSES:
        
        # Create dummy doc_block
        raw_block = RawDocBlock(doc_class.__name__,
                                name='temp',
                                attributes=dict(),
                                filename='fake')
        doc_obj = doc_class(raw_block)
        
        # Create node for each doc class
        description = "\\n".join(wrap(doc_class.__doc__, 30))
        node = GraphNode(doc_class.__name__,
            fontsize='10',
            shape='Mrecord',
            label="{ %s | %s }" % (doc_class.__name__, description))
        src.append(str(node))
        
        # Create edges to show links
        for link_def in doc_obj._link_definitions:
            if not link_def.is_reverse:
                # Forward Links
                arrowhead = 'empty'
                if link_def.multiple:
                    arrowhead = 'crow'
                style = 'solid'
                if doc_obj.is_attr_expected(link_def.attr_name):
                    style = 'bold'
                for to_doc_class in link_def.doc_classes:
                    edge = GraphEdge(
                        from_node=doc_class.__name__,
                        to_node=to_doc_class,
                        label=link_def.name,
                        fontsize='8',
                        arrowhead=arrowhead,
                        color='purple',
                        fontcolor='purple',
                        weight='100',
                        style = style)
                    src.append(str(edge))
            else:
                # Reversed links
                for from_doc_class, link_name in link_def.linking:
                    edge = GraphEdge(
                        to_node=doc_class.__name__,
                        from_node=from_doc_class,
                        label=link_def.name + '()',
                        fontsize='8',
                        arrowtail='empty',
                        arrowhead='none',
                        dir='both',
                        style='dotted',
                        color='darkslateblue',
                        fontcolor='darkslateblue',
                        weight='1')
                    src.append(str(edge))

    src.append('}')
    
    dot_path = output_file_path + '.dot'
    print("Writing", dot_path)
    with open(dot_path, 'wt') as fh:
        fh.write("\n".join(src))
        
    img_path = output_file_path + '.png'
    print("Generating", img_path)
    subprocess.call([
        get_graphviz_path(),
        "-Tpng",
        "-o", img_path,
        dot_path],
        stdout=sys.stdout, stderr=sys.stderr)
    
    img_path = output_file_path + '.svg'
    print("Generating", img_path)
    subprocess.call([
        get_graphviz_path(),
        "-Tsvg",
        "-o", img_path,
        dot_path],
        stdout=sys.stdout, stderr=sys.stderr)
    