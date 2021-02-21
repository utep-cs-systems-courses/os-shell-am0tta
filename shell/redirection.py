#! /usr/bin/env python3

import os, sys, time, re

# Output redirection
def outRedir(args):

    # Close fd1 to disconnect it
    os.close(1)
    # Open filename for reading. Creates a file if it's non-existent
    os.open("filename.txt", os.O_CREAT | os.O_WRONLY)
    # Make fd1 inheritable
    os.set_inheritable(1, True)

# Input redirection
def inRedir(args):

    # Close fd0 to disconnect it
    os.close(0)
    os.open("filename.txt", os.O_CREAT | os.O_WRONLY)
    # Make fd0 inheritable
    os.set_inheritable(0, True)

'''''
pid = os.getpid()               # get and remember pid

os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

rc = os.fork()

if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)


elif rc == 0:                   # child
    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                 (os.getpid(), pid)).encode())

    args = ["wc", "p3-exec.py"]


    os.close(1)                 # redirect child's stdout
    os.open("p4-output.txt", os.O_CREAT | os.O_WRONLY);
    os.set_inheritable(1, True)

    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly

        
        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error

        else:                           # parent (forked ok)

                os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                             (pid, rc)).encode())

                childPidCode = os.wait()
                os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                             childPidCode).encode())
'''''
