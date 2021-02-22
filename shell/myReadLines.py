#! /usr/bin/env python3

# methods to handle commands, fork
import os, sys, re
from os import read, write
from redirection import outRedir, inRedir

def inputs(args):

        if len(args) == 0:
                return

        # Causes shell to terminate
        if "exit" in args:
                exit()
                

        # Change directory command
        elif "cd" == args[0]:
                try:
                        if len(args) == 1:
                                return

                        else:
                                os.chdir(args[1])
                # Print error message when specified file/directory does not exist
                except:
                        os.write(1, ("No such file or directory\n" % args[1]).encode())
        else:
                rc = os.fork()

                if rc < 0:
                        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
                        exit()

                elif rc == 0:
                        if ">" in args:
                                outRedir(args)
                        if "<" in args:
                                inRedir(args)

                        command(args)
                        exit()


def command(args):

        # Try each directory in the path
        for dir in re.split(":", os.environ['PATH']):  
                prog = "%s/%s" % (dir, args[0])
                try:

                        # Try to exec program
                        os.execve(prog, args, os.environ)

                # ...expected
                except FileNotFoundError:

                        # ...failed quietly
                        pass

        # Prints an error message when a command is not found
        os.write(2, ("%s: command not found...\n" % args[0]).encode())
        
        # Terminate with error
        exit()


'''''  numLines = 0


inLine = stdin.readline()

print(f"Stdin uses file descriptor {stdin.fileno()}\n")
print(f"Stdout uses file descriptor {stdout.fileno()}\n")

while len(inLine):

        numLines += 1
        stdout.write(f"### Line {numLines}: <{str(inLine)}> ###\n")
        inLine = stdin.readline()

stdout.write(f"EOF after {numLines} lines\n")
'''''
