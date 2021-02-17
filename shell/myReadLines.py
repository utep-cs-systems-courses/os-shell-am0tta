#! /usr/bin/env python3

# methods to handle commands, fork
import os, sys, re
from os import read, write
        
def inputs(args):

        if len(args) == 0:
                return

        if "escape" in args:
                exit()

        elif "cd" == args[0]:
                try:
                        if len(args) == 1:
                                return

                        else:
                                os.chdir(args[1])

                except:
                        os.write(1, ("No such file or directory\n" % args[1]).encode())
        else:
                rc = os.fork()

                if rc < 0:
                        os.write(2, ("Fork failure").encode())
                        exit()
                elif rc == 0:
                        command(args)
                        exit()


def command(args):
        for dir in re.split(":", os.environ['PATH']):
                prog = "%s/%s" % (dir, args[0])
                try:
                        os.execve(prog, args, os.environ)

                except FileNotFoundError:
                        pass

        os.write(2, ("%s: command not found" % args[0]).encode())
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
