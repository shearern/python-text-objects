'''Script to generate Functional Expert Documentation from Source''' 
import os
import sys
import gflags
import shutil
import cProfile

from fsde import ProjectFolder

from fsde.writers.DocTemplate import DocTemplate

gflags.DEFINE_string('output',
    short_name = 'o',
    help = "Directory to write documentation to",
    default=None)
gflags.MarkFlagAsRequired('output')

gflags.DEFINE_string('project',
    short_name = 'p',
    default = None,
    help = "Folder to extract documentation from")
gflags.MarkFlagAsRequired('project')

gflags.DEFINE_string('common',
    short_name = 'c',
    default = None,
    help = "Path to common doc blocks directory")

def validate_dir_path(path):
    if path is None:
        return True
    if not os.path.exists(path):
        return False
    if not os.path.isdir(path):
        return False
    return True

gflags.RegisterValidator(
    'common',
    validate_dir_path,
    "Common folder is invalid")

gflags.RegisterValidator(
    'project',
    validate_dir_path,
    "Project folder is invalid")

gflags.RegisterValidator(
    'output',
    validate_dir_path,
    "Output folder is invalid")

gflags.DEFINE_boolean('profile',
    default=False,
    help="Run gneration under profiler")


def do_generation():
    
    flags = gflags.FLAGS
    
    # Load project folder
    project = ProjectFolder(flags.project)
    if flags.common is not None:
        project.add_common_folder(flags.common)
        
    
    # Collect all blocks
    doc_blocks = project.find_doc_blocks()

    # Collect attachments
    print "Copying attachment files"
    attachments_dir = os.path.join(flags.output, 'attachments')
    if not os.path.exists(attachments_dir):
        os.mkdir(attachments_dir)
    for comm in doc_blocks.get_all('Communication'):
        if comm.filename is not None:
            path = project.find_attachment_file_path(comm.filename)
            if path is None:
                print "ERROR: Failed to find attachment:", comm.filename
            else:
                save_path = os.path.join(attachments_dir, comm.filename)
                if not os.path.exists(save_path):
                    print "%s -> %s" % (path, save_path)
                    shutil.copy(path, save_path)

    # Write out
#     for block in doc_blocks.get_all('FeedSet'):
#         write_feed_set_docs(block, flags.output)
#         print "Writing", block.html_index_path
    
    print "Writing Doc Block Debug Page"
    write_doc_block_debug_page(doc_blocks, flags.output)
    
    for block in doc_blocks.get_all('Crosswalk'):
        msg = block.reason_to_skip_writing_rules_sql
        if msg is not None:
            print "Skipping %s: %s" % (block.path_for_rules_sql, msg)
        else:
            print "Writing", block.path_for_rules_sql
            write_crosswalk_sql(block, flags.output)

    for block in doc_blocks.get_all('FeedFile'):
        print "Writing", block.html_index_path
        write_feed_file_docs(block, flags.output)
        

if __name__ == '__main__':
    
    # Parse arguments
    try:
        gflags.FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print 'USAGE ERROR: %s\nUsage: %s ARGS\n%s' % (e, sys.argv[0],
                                                       gflags.FLAGS)
        sys.exit(1)

    if gflags.FLAGS.profile:
        cProfile.run('do_generation()')
    else:
        do_generation()
        
    print "Finished"
    