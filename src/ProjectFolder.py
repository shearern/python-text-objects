
import os
import gflags
import yaml

from exceptions import ArgumentException, DocBlockStructureError

from .doc_objects.RawDocBlock import RawDocBlock
from .doc_objects import encap_doc_block
from .doc_objects.DocBlockCollection import DocBlockCollection


def _list_folders(root_folder, dir_path=None):
    '''List folder recursively'''
    scan_path = root_folder
    if dir_path is not None:
        scan_path = os.path.join(scan_path, dir_path)
    for name in os.listdir(scan_path):
        path = os.path.join(scan_path, name)
        if name[0] != '.':
            if os.path.isdir(path):
                if dir_path is None:
                    rel_path = name
                else:
                    rel_path = os.path.join(dir_path, name)
                    
                yield rel_path
                
                for sub_path in _list_folders(root_folder, rel_path):
                    yield sub_path
        


def _parse_yaml_doc_blocks(src, filename, linenum=None):
    
    try:
        blocks_data = yaml.load(src)
    except yaml.YAMLError, e:
        msg = "CRITICAL ERROR: YAML block at %s could not be parsed.\n%s"
        loc = filename
        if linenum is not None:
            loc += ':' + str(linenum)
        raise DocBlockStructureError(msg % (loc, str(e)))
    
    def _encap_dock_block(block_dict, filename, line):
        # Prep error message
        error_msg = "Documentation block found at %s has error: %%s\n(%s)"
        loc = filename
        if linenum is not None:
            loc += ':' + str(linenum)
        error_msg = error_msg % (loc, str(block_dict))
        
        # Find required attributes
        if block_dict.__class__ is not dict:
            msg = "Documentation blocks must be dicts"
            raise DocBlockStructureError(error_msg % (msg))
        block_dict = block_dict.copy()
        
        if not block_dict.has_key('class'):
            msg = "Documentation blocks must have a [name] key"
            raise DocBlockStructureError(error_msg % (msg))
        block_class = block_dict['class']
        del block_dict['class']
        
        if not block_dict.has_key('name'):
            msg = "Documentation blocks must have a [name] key"
            raise DocBlockStructureError(error_msg % (msg))
        block_name = block_dict['name']
        del block_dict['name']
        
        # Encapsulate block
        return RawDocBlock(block_class,block_name,block_dict,filename,line)
        
    # Parse a list of doc blocks
    if blocks_data.__class__ is list:
        for block in blocks_data:
            yield _encap_dock_block(block, filename, linenum)

    # Parse a single block
    elif blocks_data.__class__ is dict:
        yield _encap_dock_block(blocks_data, filename, linenum)
        
    # Else, got something we didn't expect
    else:
        msg = "YAML block at %s has invalid type."
        msg += "  Use list for multiple blocks, or dict for a single block.\n%s"
        loc = filename
        if linenum is not None:
            loc += ':' + str(linenum)
        raise DocBlockStructureError(msg % (loc, str(blocks_data)))
        
    

class ProjectFolder(object):
    '''Wrap operations on the folder being documented'''
    
    def __init__(self, path):
        self.__path = path
        self.__common_folders = list()
        
    
    @property
    def path(self):
        return os.path.abspath(self.__path)
    
    
    def list_folders(self):
        '''List the folders in the project (relative to project root)'''
        for path in _list_folders(self.path):
            yield path
            
            
    def add_common_folder(self, path):
        self.__common_folders.append(path)
                
                
    def list_funcspec_folders(self):
        '''List the folders in the project that contain funcspec doc files
        
        
        Folders with the name "funspec" are treated specially:
         - All YAML files in these folders are consumed as having documenation
           blocks
           
        Returned folder paths are relative to project root
        '''
        for path in self.list_folders():
            if os.path.basename(path) == 'funcspec':
                yield path
                
    
    def list_all_files(self):
        '''List all files in the project
        
        @return: rel_folder_path, filename
        '''
        for fold_path in self.list_folders():
            for filename in os.listdir(os.path.join(self.path, fold_path)):
                path = os.path.join(self.path, fold_path, filename)
                if os.path.isfile(path):
                    yield fold_path, filename
                
    
    def list_yaml_doc_files(self):
        '''List YAML files to be inspected directly for documentation objects
        
        These YAML files include documentation blocks already in the format
        expected.
        '''
        for fold_path, filename in self.list_all_files():
            path = os.path.join(self.path, fold_path, filename)
            if filename.lower().endswith('.yml'):
                yield os.path.join(fold_path, filename)
                    
                    
    def list_plsql_doc_files(self):
        '''Find PL/SQL files to search for documentation blocks'''
        for fold_path, filename in self.list_all_files():
            path = os.path.join(self.path, fold_path, filename)
            if filename.lower().endswith('.sql'):
                yield os.path.join(fold_path, filename)
                
                
    def find_plsql_doc_block_sources(self):
        '''Find documentation block source in PL/SQL files
        
        PL/SQL can have embedded doc blocks that look like:
        
        -- FUNCSPEC:
        -- - class: TestClass
        --   name: test
        --   attr1: Attribute value 1
        --   attr2: Value 2
        
        The first line without a comment (--) designation is considered the end.
        
        The YAML can either be a list of dicts for multiple documentation blocks
        or a single dict for a single documentation block.
        
        @return rel_path, line_num, block_yaml_src
        '''
        for rel_path in self.list_plsql_doc_files():
            path = os.path.join(self.path, rel_path)
            with open(path, 'rt') as fh:
            
                cur_block = None
                start_line = None
            
                # Search PL/SQL file for blocks
                for i, line in enumerate(fh.readlines()):
                    line = line.strip()
                         
                    # Look for new blocks
                    if cur_block is None:
                        if line.startswith('--'):
                            if 'FUNCSPEC:' in line:
                                cur_block = list()
                                cur_block.append('---')
                                start_line = i+1
                         
                    # Look for end of block
                    else:
                        if line.startswith('--'):
                            cur_block.append(line[2:])
                        else:
                            yield rel_path, start_line, "\n".join(cur_block)
                            cur_block = None
                             
                # Yield last block if there is one
                if cur_block is not None:
                    yield rel_path, start_line, "\n".join(cur_block)
            
                
    
    def _find_raw_doc_blocks(self):
        '''Examine project directory to find all the doc blocks'''
        
        # Load the YAML files that are collections of doc blocks
        for rel_path in self.list_yaml_doc_files():
            path = os.path.join(self.path, rel_path)
            with open(path, 'rb') as fh:
                for raw_block in _parse_yaml_doc_blocks(fh.read(), rel_path):
                    yield raw_block
                    
        # Load YAML files in the common folders
        for path in self.__common_folders:
            for filename in os.listdir(path):
                if filename.lower().endswith('.yml'):
                    with open(os.path.join(path, filename), 'rb') as fh:
                        src = fh.read()
                    for raw_block in _parse_yaml_doc_blocks(src, path):
                        yield raw_block
                    
        # Load the YAML doc blocks in PL/SQL comments
        for rel_path, line_num, src in self.find_plsql_doc_block_sources():
            for raw_block in _parse_yaml_doc_blocks(src, rel_path, line_num):
                yield raw_block
        
                
    def find_doc_blocks(self):
        '''Examine project directory to file all the doc blocks'''
        col = DocBlockCollection()
        stack = list(self._find_raw_doc_blocks())
        while len(stack) > 0:
            raw_block = stack.pop(0)
            try:
                
                # Encapsulate into a doc block class
                if col.has_block(raw_block):
                    doc_block = col.get(raw_block.doc_class, raw_block.name)
                else:
                    doc_block = encap_doc_block(raw_block)
                    col.add(doc_block)
                    
                # Take in attributes
                doc_block._take_attributes_from(raw_block)
                
                # Allow this doc block to yield any embedded doc blocks
                embedded_blocks = list(doc_block.get_embedded_blocks())
                for embedded_raw_block in embedded_blocks:
                    stack.append(embedded_raw_block)
                                
            except DocBlockStructureError, e:
                print "ERROR: %s for block at %s" % (str(e), raw_block.loc)
                
        # Perform some validation
        has_error = True
        while has_error:
            self.__link_errors = list()
            has_error = False
            # Reset links
            for doc_block in col.get_all():
                doc_block.clear_links()
            # Do linking and validation
            for doc_block in list(col.get_all()):
                try:
                    doc_block.link_and_validate()
                except DocBlockStructureError, e:
                    print "ERROR: IGNORING BLOCK: %s" % (doc_block.full_name)
                    for line in str(e).split("\n"):
                        print ' '*3 + line
                    col.remove(doc_block.doc_class, doc_block.name)
                    has_error = True
                
        return col
    
    
    def find_attachment_file_path(self, attach_filename):
        '''Search for an attachment mentioned in a Communication .filename'''
        for rel_fold_path, filename in self.list_all_files():
            if filename == attach_filename:
                return os.path.join(self.path, rel_fold_path, filename)
                
                                