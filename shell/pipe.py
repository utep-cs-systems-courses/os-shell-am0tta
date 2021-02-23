#! /usr/bin/env python3

# Method that handles piping to allow communication between processes

import os, sys, time, re
from redirection import outRedir, inRedir


def piping(args):

    # '|' for split command
    args = args.split('|')
    
    # left and right arguments
    lArg = args[0].split(), rArg = args[1].split()
    pipeRead, pipeWrite = os.pipe()

    rc = os.fork()

    if rc < 0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        exit()

    # The left argument will be executed
    elif rc == 0:
        if '<' in lArg:
            inRedir("in")

        if '>' in lArg:
            inRedir("out")

    # The right argument will be executed
    else:
            if '<' in rArg:
                outRedir("in")

            if '>' in rArg:
                outRedir("out")
    


'''''

From p5-pipe-fork.py within the demos directory


pid = os.getpid()               # get and remember pid

pr,pw = os.pipe()
for f in (pr, pw):
    os.set_inheritable(f, True)
    print("pipe fds: pr=%d, pw=%d" % (pr, pw))

    import fileinput
    
    print("About to fork (pid=%d)" % pid)

    rc = os.fork()

    if rc < 0:
        print("fork failed, returning %d\n" % rc, file=sys.stderr)
        sys.exit(1)

    elif rc == 0:                   #  child - will write to pipe
        print("Child: My pid==%d.  Parent's pid=%d" % (os.getpid(), pid), file=sys.stderr)
        args = ["wc", "p3-exec.py"]

        os.close(1)                 # redirect child's stdout
        os.dup(pw)

        for fd in (pr, pw):
            os.close(fd)
        print("hello from child")

    else:                           # parent (forked ok)
        print("Parent: My pid==%d.  Child's pid=%d" % (os.getpid(), rc), file=sys.stderr)
        os.close(0)
        os.dup(pr)
        for fd in (pw, pr):
            os.close(fd)
        for line in fileinput.input():
            print("From child: <%s>" % line)
                                                                
'''''
