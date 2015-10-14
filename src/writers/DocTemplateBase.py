from abc import ABCMeta, abstractproperty

import os
import zipfile
import cStringIO
import base64

from mako.template import Template as MakoTemplate

class DocTemplateBase(object):
    '''Base for reading template files'''
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self._load_template_zip()
        
    
    @abstractproperty
    def template_zip_base64(self):
        '''Base 64 encoding of zipfile of templates'''
        
    ZIP_SRC = None
    ZIP = None

    @property
    def __zip(self):
        return DocTemplateBase.ZIP
    
    
    TEMPLATES = [
        'feed_set.html',
        'feed_file.html',
        'doc_block_debug.html',
        'crosswalk.sql',
        ]
    
    def _load_template_zip(self):
        '''Load the template zip file'''
        if DocTemplateBase.ZIP_SRC is None:
            DocTemplateBase.ZIP_SRC = cStringIO.StringIO()
            tpl = self.template_zip_base64
            DocTemplateBase.ZIP_SRC.write(base64.b64decode(tpl))
            
            DocTemplateBase.ZIP = zipfile.ZipFile(DocTemplateBase.ZIP_SRC, 'r')
        

    def list_asset_files(self):
        '''List asset files to be written to the documentation folder'''
        for entry in self.__zip.namelist():
            if os.path.basename(entry) not in self.TEMPLATES:
                yield entry
                
                
    def write_asset_files_to(self, path):
        for rel_path in self.list_asset_files():
            
            # Create Directory
            dir_path = os.path.dirname(rel_path)
            if dir_path is not None and dir_path not in ('', '.'):
                full_dir_path = os.path.join(path, dir_path)
                if not os.path.exists(full_dir_path):
                    os.makedirs(full_dir_path)
                    
            # Write file
            full_path = os.path.join(path, rel_path)
            with open(full_path, 'wb') as ofh:
                ifh = self.__zip.open(rel_path, 'r')
                ofh.write(ifh.read())
                ifh.close()
        
        
    def get_template(self, name):
        
        # Extract template source
        try:
            fh = self.__zip.open(name, 'r')
            src = fh.read()
            fh.close()
        except KeyError:
            raise Exception("Invalid template name: " + name)
        
        # Return template
        return MakoTemplate(src)
    
