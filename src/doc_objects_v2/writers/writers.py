import os
import gflags
import shutil
from time import sleep
from textwrap import wrap

from DocTemplate import DocTemplate 
from ..doc_objects.DocBlockBase import DocBlockBase
from ..utils import describe_block_loc

def _prep_doc_dir(path):
    
    # Sanity check: Are we in the output dir
    path = os.path.abspath(path)
    output_path = os.path.abspath(gflags.FLAGS.output)
    if not path.startswith(output_path):
        raise Exception("%s not under %s" % (path, output_path))
    
    # Delete existing files
    if os.path.exists(path):
        shutil.rmtree(path)
        sleep(3)
        
    # Create directory
    os.makedirs(path)
    
    
def implode(list_val, glue=', '):
    '''Implode a list of values'''
    if list_val.__class__ is list:
        return glue.join(list_val)
    return list_val
    

def yes_no(val, yes_val='yes', no_val='no'):
    if val:
        return yes_val
    else:
        return no_val


def anchor_name(doc_block):
    return '%s__%s' % (doc_block.doc_class, doc_block.safe_name)

def create_anchor(name):
    return "<a name='%s'></a>" % (name)

def create_db_anchor(doc_block):
    name = anchor_name(doc_block)
    return create_anchor(name)
    
def link_to_db_anchor(doc_block, text=None):
    if text is None:
        try:
            text = doc_block.title
        except AttributeError:
            text = doc_block.name
    return "<a href='#%s'>%s</a>" % (anchor_name(doc_block), text)


def make_list(value):
    if value.__class__ is list:
        return value 
    else:
        return [value, ]


def count_todo_items_in_block(doc, lvl=None):
    cnt = 0
    # Use Field todo method if available
    try:
        for todo_item in doc.get_todo_items_for_field():
            if lvl is None or todo_item.level == lvl:
                cnt += 1
    except AttributeError:
        for todo_item in doc.get_todo_item_objs():
            if lvl is None or todo_item.level == lvl:
                cnt += 1
    return cnt
    
        
def count_todo_items(col, doc_class=None, lvl=None):
    cnt = 0
    for doc in col.get_all(doc_class):
        cnt += count_todo_items_in_block(doc, lvl)
    return cnt

    

# Adding new writers:
#  - Add new template names to DocTemplateBase.TEMPLATES
#  - Add html_index_path attribute to block class
#  - Change block name parameter


def write_feed_set_docs(feed_set_block, output_root_dir):
    '''Generate a document describing a FeedSet'''
    
    feed_set = feed_set_block
    tpls = DocTemplate()
    
    # Create directory to write to
    index_path = os.path.join(output_root_dir, feed_set.html_index_path)
    output_dir_path = os.path.dirname(index_path)
    _prep_doc_dir(output_dir_path)
    
    # Write out assets
    tpls.write_asset_files_to(output_dir_path)
        
    # Write Template
    tpl = tpls.get_template('feed_set.html')
    with open(index_path, 'wb') as fh:
        fh.write(tpl.render(
            feed_set = feed_set))
            
            
def write_feed_file_docs(feed_file_block, output_root_dir):
    '''Generate a document describing a FeedFile'''
    
    feed_file = feed_file_block
    tpls = DocTemplate()
    
    # Create directory to write to
    index_path = os.path.join(output_root_dir, feed_file.html_index_path)
    output_dir_path = os.path.dirname(index_path)
    _prep_doc_dir(output_dir_path)
    
    # Write out assets
    tpls.write_asset_files_to(output_dir_path)
        
    # Write Template
    tpl = tpls.get_template('feed_file.html')
    with open(index_path, 'wb') as fh:
        fh.write(tpl.render(
            feed_file = feed_file,
            
            # Utils:
            implode = implode,
            yes_no = yes_no,
            anchor_name = anchor_name,
            create_anchor = create_anchor,
            create_db_anchor = create_db_anchor,
            link_to_db_anchor = link_to_db_anchor,
            describe_block_loc = describe_block_loc,

            count_todo_items_in_block = count_todo_items_in_block,  
            count_todo_items = count_todo_items,
            ))
                        
                        
def write_doc_block_debug_page(doc_block_col, output_root_dir):
    '''List all doc blocks in a collection'''
    
    tpls = DocTemplate()
    
    # Create directory to write to
    index_path = os.path.join(output_root_dir, 'debug/all_doc_blocks.html')
    output_dir_path = os.path.dirname(index_path)
    _prep_doc_dir(output_dir_path)
    
    # Write out assets
    tpls.write_asset_files_to(output_dir_path)
    
    # Collect link errors
    link_errors = list()
    for doc_block in doc_block_col.get_all():
        link_errors.extend(doc_block._link_errors)
        
    # Write Template
    tpl = tpls.get_template('doc_block_debug.html')
    with open(index_path, 'wb') as fh:
        fh.write(tpl.render(
            col = doc_block_col,
            link_errors = link_errors,
            
            # Utils:
            implode = implode,
            yes_no = yes_no,
            anchor_name = anchor_name,
            create_anchor = create_anchor,
            create_db_anchor = create_db_anchor,
            link_to_db_anchor = link_to_db_anchor,
            describe_block_loc = describe_block_loc,
            make_list = make_list,
            
            count_todo_items_in_block = count_todo_items_in_block,
            count_todo_items = count_todo_items,
            
            # Classes:
            DocBlockBase = DocBlockBase,
            ))
    
    
def write_crosswalk_sql(crosswalk_block, output_root_dir):
    '''Generate a document describing a FeedFile'''
    
    tpls = DocTemplate()
    
    values = list(crosswalk_block.value_docs)
    
    crosswalk_filename = crosswalk_block.path_for_rules_sql
    crosswalk_path = os.path.join(output_root_dir, crosswalk_filename)
    
    description = wrap(crosswalk_block.rule_desc, 60)
    
    # Write Template
    tpl = tpls.get_template('crosswalk.sql')
    with open(crosswalk_path, 'wb') as fh:
        fh.write(tpl.render(
            crosswalk = crosswalk_block,
            description = description,
            values = values,
            ))
                        
                        
