#!/usr/bin/env python3

# Replace all references to external files in this format:
#
#   !INCLUDE "path/to/file.md"
#
# with the actual file contents.
# Loosely adapted from https://github.com/jreese/markdown-pp
#
# Usage: process_include.py [-h] input_file [output]
#
# Recommended usage: Send the Markdown output to stdout (default) and pipe
# into pandoc for instant preprocessing:
#
#   replace_includes.py document.md | pandoc -f markdown -t html -o document.html
#
# TODO: Check if !INCLUDE command is indented. If so, indent the whole inserted thing.

# Load libraries
import re
import argparse
import sys
from os import path

# Get command line arguments
parser = argparse.ArgumentParser(description='Replace !INCLUDE commands with external Markdown files.')
parser.add_argument('input_file', type=argparse.FileType('r'),
                    nargs='?', default=sys.stdin,
                    help='Markdown file to preprocess')
parser.add_argument('output', type=argparse.FileType('w'),
                    nargs='?', default=sys.stdout,
                    help='the name of the output file (defaults to stdout)')
args = parser.parse_args()

# Save arguments
input_text = args.input_file.read()
input_name = args.input_file.name
directory_name = path.dirname(input_name)
output = args.output


# ---------------------------------------------------
# Replace the matched object with its file contents
# ---------------------------------------------------
def include(match):
    # print(match)
    # The filename match should generally be group 2
    if match.group(1) is None:
        filename = match.group(2)
    else:
        filename = match.group(1)

    if directory_name:
        filename = path.join(directory_name, filename)

    # Open the file
    if path.isfile(filename):
        with open(filename, 'r') as f:
            data = f.read()
        return(data)

    # If there's not an actual file there, return the !INCLUDE string
    return(match.group(0))

# Match all instances of !INCLUDE "asdf" and replace with file contents
result = re.sub("!INCLUDE\s+(?:\"([^\"]+)\"|'([^']+)')", include, input_text)
with output as f:
    f.write(result)
