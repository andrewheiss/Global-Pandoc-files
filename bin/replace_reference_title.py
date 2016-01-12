#!/usr/bin/env python3

# Append LaTeX and Markdown to create a hanging indented references section at
# the end of a pandoc-generated PDF. The section will use the YAML entry
# `reference-section-title` (and defaults to "References").
#
# This is necessary because pandoc-generated PDFs *can* use pandoc-citeproc's
# new reference-section-title, but it inserts it into the intermediate TeX file
# as a \chapter{}, which goes against the standard H1/-> \section{} mapping.
# Additionally, the custom hanging indent LaTeX commands aren't used properly
# when reference-section-title is used.
#
# Usage: replace_reference_title.py [-h] input_file [output]
#
# Recommended usage: Send the Markdown output to stdout (default) and pipe
# into pandoc for instant preprocessing:
#
#   replace_reference_title.py document.md | pandoc -o document.pdf
#

# Load libraries
import argparse
import sys

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
input_text = args.input_file.readlines()
output = args.output


# -------------------------------------------------------
# Generate code for final hanging indented bibliography
# -------------------------------------------------------
clean_text = []
reference_title = 'References'
for line in input_text:
    if line.startswith('reference-section-title:'):
        reference_title = line.replace('reference-section-title:', '').strip()
    else:
        clean_text.append(line)

reference_template = """
# {0}

\\setlength{{\\parindent}}{{-0.2in}}
\\setlength{{\\leftskip}}{{0.2in}}
\\setlength{{\\parskip}}{{0pt}}
\\vspace*{{0in}}
\\noindent
"""

result = ''.join(clean_text) + reference_template.format(reference_title)

with output as f:
    f.write(result)
