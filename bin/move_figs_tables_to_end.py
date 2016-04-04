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

# TODO: Also do listings, since Healy-esque pandoc uses those too

# Get command line arguments
parser = argparse.ArgumentParser(description='Move all figures and tables to the end.')
parser.add_argument('input_file', type=argparse.FileType('r'),
                    nargs='?', default=sys.stdin,
                    help='Markdown file to preprocess')
parser.add_argument('output', type=argparse.FileType('w'),
                    nargs='?', default=sys.stdout,
                    help='the name of the output file (defaults to stdout)')
args = parser.parse_args()

# Save arguments
input_text = args.input_file.readlines()
input_name = args.input_file.name
directory_name = path.dirname(input_name)
output = args.output

actual_text = []
figures = []

marker_template = '\[@{0} here\]'

def move_to_end(text):
    for line in text:
        if re.search('{#fig:', line):
            figures.append(line)

            fig_label = re.search('{#(fig:.*)}', line)
            marker = marker_template.format(fig_label.group(1))
            actual_text.append(marker)
        elif re.search('{#tbl:', line):
            tbl_label = re.search('{#(tbl:.*)}', line)
            marker = marker_template.format(tbl_label.group(1))

            actual_text.append(line)
            actual_text.append('')
            actual_text.append(marker)
        else:
            actual_text.append(line)

    joined_text = '\n'.join([x.replace('\n', '') for x in actual_text])
    joined_figures = '\n\n'.join([x.strip() for x in figures])
    return(joined_text + '\n\n# Tables\n\n Manually add tables here' +
           '\n\n# Figures\n\n' + joined_figures + '\n')

with output as f:
    f.write(move_to_end(input_text))
