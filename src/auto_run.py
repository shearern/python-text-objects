'''Watch project folder and re-run generation when source files change'''

import os
import sys
import gflags
import subprocess
import winsound
from time import sleep

gflags.DEFINE_string('output',
    short_name = 'o',
    help = "Directory to write documentation to",
    default=None)

gflags.DEFINE_string('project',
    short_name = 'p',
    default = None,
    help = "Folder to extract documentation from")
gflags.MarkFlagAsRequired('project')

gflags.DEFINE_string('common',
    short_name = 'c',
    default = None,
    help = "Path to common doc blocks directory")



def list_file_mtimes():
    
    # Project Directory
    exts = ('sql', 'yml')
    for dirpath, dirnames, filenames in os.walk(gflags.FLAGS.project):
        for filename in filenames:
            for ext in exts:
                if filename.lower().endswith('.'+ext):
                    path = os.path.join(dirpath, filename)
                    yield path, os.path.getmtime(path)

    # Python FuncSpec Project Directory
    exts = ('py', 'pyc', 'html', 'css', 'sql')
    for dirpath, dirnames, filenames in os.walk(os.path.dirname(__file__)):
        for filename in filenames:
            for ext in exts:
                if filename.lower().endswith('.'+ext):
                    path = os.path.join(dirpath, filename)
                    yield path, os.path.getmtime(path)



def play_sound(filename):
    path = os.path.join(os.path.join(os.path.dirname(__file__), filename))
    winsound.PlaySound(path, 0)


if __name__ == '__main__':
    
    
    # Parse arguments
    try:
        gflags.FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print 'USAGE ERROR: %s\nUsage: %s ARGS\n%s' % (e, sys.argv[0],
                                                       gflags.FLAGS)
        sys.exit(1)
    
    flags = gflags.FLAGS
        
    os.chdir(os.path.dirname(__file__))

    mtimes = dict()
    while True:
        
        # Scan folder for changes
        do_gen = False
        for path, mtime in list_file_mtimes():
            if not mtimes.has_key(path):
                do_gen = True
            elif mtimes[path] < mtime:
                print path, "changed"
                do_gen = True
            
        if do_gen:
            print ""
            print "-"*80
            print "Re-generating"
            print "-"*80
            print ""
            play_sound('notify.wav')
                
            # Run generator
            cmd = [
                sys.executable,
                'gen_funcspec.py',
                ]
            
            if flags.output is not None:
                cmd.extend(('--output', flags.output))
            if flags.project is not None:
                cmd.extend(('--project', flags.project))
            if flags.common is not None:
                cmd.extend(('--common', flags.common))
                
            try:
                subprocess.check_call(cmd,
                    stdout = sys.stdout,
                    stderr = sys.stderr)
            except subprocess.CalledProcessError, e:
                play_sound('error.wav')
                keep_going = raw_input("Press Enter to Confirm")
                continue
            
            play_sound('finished.wav')      

            print ""
            print "Updating file mtimes..."
            for path, mtime in list_file_mtimes():
                mtimes[path] = mtime
            
            print "Waiting for changes"
        
        sleep(3)
     
    