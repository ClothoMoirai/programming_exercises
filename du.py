#!/usr/bin/python3
# Every wake up with an idea to do something for the hack value despite it being a Bad Idea?
# That's how this came to be: let's implement du(1) in Python.
# Most likely this won't be exact for a few reasons, e.g. I have to figure out how to find the allocation cluster size.
import os
from typing import List
from collections import defaultdict
mydir = "/home/danielle/foo"


def islink(filename: str) -> bool:
    return os.path.islink(filename)


def isdir(filename: str) -> bool:
    # for this purpose we want to exclude links.
    return os.path.isdir(filename) and not islink(filename)


def process_this_dir_contents(filename: str) -> int:
    # prints the size of contents of a directory
    this_dir_total_size = 0
    if isdir(filename):
        this_dir_contents = os.listdir(filename)
        for this_file in this_dir_contents:
            my_file = os.path.join(filename, this_file)
            if isdir(my_file):
                this_dir_size = process_this_dir_contents(my_file)
                my_file_size = os.stat(my_file).st_size + this_dir_size
                this_dir_total_size += my_file_size
                print(my_file_size, my_file)
            else:
                my_file_size = os.stat(my_file).st_size
                this_dir_total_size += my_file_size
                print(my_file_size, my_file)
    return this_dir_total_size


def main(thisdir: str) -> None:
    thisdir = os.path.expanduser(thisdir)  # gets the absolute path if given in a form like ~/mydir
    if isdir(thisdir):
        print((process_this_dir_contents(thisdir) + os.stat(thisdir).st_size), thisdir)
    else:
        print(os.stat(thisdir).st_size, thisdir)


main(mydir)