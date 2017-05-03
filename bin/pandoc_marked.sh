#!/usr/bin/env bash
[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"

/Users/andrew/bin/replace_includes $input | \
pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block \
    -t html5 --smart --normalize -s \
    --filter pandoc-crossref -M figPrefix:"Figure" -M eqnPrefix:"Equation" -M tblPrefix:"Table" \
    --default-image-extension=png \
    --template=/Users/andrew/.pandoc/templates/html.template \
    --filter pandoc-citeproc \
    --csl=/Users/andrew/.pandoc/csl/american-political-science-association.csl \
    --bibliography=/Users/andrew/Dropbox/Readings/Papers.bib \
    -M reference-section-title=References
