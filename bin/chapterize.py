#!/usr/bin/env python3

# Help convert a standalone article (i.e. with YAML front matter and headings)
# to a book chapter (i.e. with no YAML front matter, the title as a first level
# heading, and all other headings increased a level).
#
# Usage: chapterize.py [-h] input_file [output]
#
# Recommended usage: Send the Markdown output to stdout (default) and pipe
# into pandoc for instant preprocessing:
#
#   chapterize.py document.md | pandoc -o document.pdf
#

# TODO: This is super clunky and hacky and would be cool to make it an official
# paondoc filter instead, like
# https://stackoverflow.com/questions/21247978/compile-multiple-files-into-one-with-title-blocks
# or
# https://github.com/sergiocorreia/panflute/blob/master/examples/panflute/headers.py

# Load libraries
import argparse
import frontmatter  # from python-frontmatter
import sys
import re

# Get command line arguments
parser = argparse.ArgumentParser(description='Change YAML title to H1 and bump up all other headings.')
parser.add_argument('input_file', type=argparse.FileType('r'),
                    nargs='?', default=sys.stdin,
                    help='Markdown file to preprocess')
parser.add_argument('output', type=argparse.FileType('w'),
                    nargs='?', default=sys.stdout,
                    help='the name of the output file (defaults to stdout)')
args = parser.parse_args()

# Save arguments
input_file = args.input_file
output = args.output

# Bump up all headings line by line
def increase_heading_level(line):
    return(re.sub("^(#+)", "\\1#", line, flags=re.MULTILINE))


# Parse the final string for YAML frontmatter
parsed_yaml = frontmatter.loads(args.input_file.read())

# If there's a title key, extract it, bump up the headings, and add the title
# to the beginning of the file
if 'title' in parsed_yaml.keys():
    chapter_title = parsed_yaml['title']
    final_result = '# ' + chapter_title + '\n\n' + increase_heading_level(parsed_yaml.content)
else:
    final_result = parsed_yaml.content

# All done
with output as f:
    f.write(final_result)
