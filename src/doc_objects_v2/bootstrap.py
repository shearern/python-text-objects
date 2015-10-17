'''Import into your own script to make generating documentation faster

call bootstrap()
''' 
import os
import sys
import gflags

from doc_objects.DocBlockCollection import DocBlockCollection

gflags.DEFINE_string('output',
    short_name = 'o',
    help = "Directory to write documentation to",
    default=None)
gflags.MarkFlagAsRequired('output')

gflags.DEFINE_string('project',
    short_name = 'p',
    default = None,
    help = "Folder to extract documentation from (separate multiple with comma)")
gflags.MarkFlagAsRequired('project')

gflags.DEFINE_boolean('watch',
    short_name = 'w',
    help = "Watch input directories and regen on change",
    default=False)


def _validate_output_path(path):
    if path is None:
        return True
    if not os.path.exists(path):
        return False
    if not os.path.isdir(path):
        return False
    return True

gflags.RegisterValidator(
    'output',
    _validate_output_path,
    "Output folder is invalid")

def _validate_project_paths(value):
    for path in value.split(","):
        if not _validate_output_path(path.strip()):
            return False
    return True
        
        
def _prc_raw_block(col, raw_block, factory):
    
    # Convert to real doc block (DocBlockBase)
    doc_class = raw_block.doc_class
    name = raw_block.name
    if col.has_block(raw_block):
        doc_block = col.get(doc_class, name)
    else:
        doc_block = factory.create_doc_block(doc_class)
        col.add(doc_block)
         
    # Take in attributes
    doc_block._take_attributes_from(raw_block)
    
    # Allow this doc block to yield any embedded doc blocks
    embedded_blocks = list(doc_block.get_embedded_blocks())
    for embedded_raw_block in embedded_blocks:
        _prc_raw_block(col, embedded_raw_block, factory)
        

def bootstrap(doc_block_factory, file_processor, return_doc_class=None):
    '''Do work of:
    
    1) Looking for files in project folders
       file_processor() is called for each file, and is expected to yeild
       RawDocBlocks
    2) Collect all doc blocks into a collection
    3) Return the requested doc block classes
    
    @param doc_block_factory: An instance of DocBlockFactoryBase for your
        project that can instantiate DocBlockBase objects for the raw blocks
        as determined by the .class
    @param file_processor: A function that takes the two parameters
        path and filename, and yields back RawDocBlocks
    @param return_doc_class: The name of the doc_class to return.
        If specified, then the resulting collection must contain exactly one
        doc block with that doc_class.  If not, and error will be created.
         
        Use this to return the "root" doc_block expected in your project.
        The collection containing all the doc block will be accessible through:
            root_block.col
            
        If not specified (None), then will return collection of all blocks
        instead
    '''

    # Parse command line arguments
    try:
        gflags.FLAGS(sys.argv)
    except gflags.FlagsError as e:
        print('USAGE ERROR: %s\nUsage: %s ARGS\n%s' % (
                e, sys.argv[0], gflags.FLAGS))
        sys.exit(1)
    flags = gflags.FLAGS

    # Create collection
    col = DocBlockCollection()
    factory = doc_block_factory

    # Search for files to consider
    for proj_path in [p.strip() for p in flags.project.split(",")]:
        for dirpath, dirnames, filenames in os.walk(proj_path):
            for filename in filenames:
                path = os.path.abspath(os.path.join(dirpath, filename))
                
                # Collect raw doc blocks found in file
                for raw_block in file_processor(path, filename):
                    _prc_raw_block(raw_block)
                    
                    
        