
#! /usr/bin/env python3

# Lab 1: Build a user shell that mimics some of the behaviors of a bash shell

import os, sys, re
from myReadLines import inputs, command 

def main():
    
    while 1:

        # print prompt $
        if 'PS1' in os.environ:
            os.write(1,(os.environ['PS1']).encode())
        else:
            os.write(1, ("$ ").encode())
            
        userInput = os.read(0, 1024)
        
        if len(userInput) == 0:
            break

        userInput = userInput.decode().split("\n")

        # If no command is given (user just presses enter), we go
        # back to the beginning of the while loop
        if not userInput:
            continue

        for arg in userInput:
            inputs(arg.split())
        # if userInput[0] == "end":
        #    exit()

#print("Hello")
if __name__ == '__main__':
    main()
