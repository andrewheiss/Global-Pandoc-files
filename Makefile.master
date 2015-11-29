# Put this Makefile in your project directory---i.e., the directory containing
# the paper you are writing. You can use it to create .html, .docx, and .pdf
# output files (complete with bibliography, if present) from your Markdown
# file.
#
# Additional notes:
# *	Change the paths at the top of the file as needed.
#
# *	Using `make` without arguments will generate html, tex, pdf, docx,
# 	and odt output files from all of the files with the designated
#	markdown extension. The default is `.md` but you can change this.
#
# *	You can specify an output format with `make tex`, `make pdf`,
#  	`make html`, `make odt`, or `make docx`
#
# *	Running `make clean` will only remove all, .html, .pdf, .odt,
#	and .docx files in your working directory **that have the same name
#	as your Markdown files**. Other files with these extensions will be safe.
#
# *	If wanted, remove the automatic call to `clean` to rely on make's
#   timestamp checking. However, if you do this, you'll need to add all the
#   document's images, etc. as dependencies, which means it might be easier
#   to just clean and delete everything every time you rebuild.


# ----------------------
# Modifiable variables
# ----------------------
# Markdown extension (e.g. md, markdown, mdown).
MEXT = md

# Location of Pandoc support files.
PREFIX = /Users/andrew/.pandoc

# Location of your working bibliography file
BIB_FILE = /Users/andrew/Dropbox/Readings/Papers.bib

# CSL stylesheet (located in the csl folder of the PREFIX directory).
# Common CSLs:
#	* american-political-science-association
#   * chicago-fullnote-bibliography
#	* chicago-fullnote-no-bib
#   * chicago-syllabus-no-bib
#   * apa
#   * apsa-no-bib
CSL = american-political-science-association

# Cross reference options
CROSSREF = --filter pandoc-crossref -M figPrefix:"Figure" -M eqnPrefix:"Equation" -M tblPrefix:"Table"

# To add version control footer support in PDFs:
#   1. Run vcinit in the directory
#   2. Place `./vc` at the front of the formula
#   3. Add `-V vc` to the pandoc command
#   4. Change pagestyle to athgit instead of ath


#--------------------
# Color definitions
#--------------------
NO_COLOR    = \x1b[0m
BOLD_COLOR	= \x1b[37;01m
OK_COLOR    = \x1b[32;01m
WARN_COLOR  = \x1b[33;01m
ERROR_COLOR = \x1b[31;01m


# --------------------
# Target definitions
# --------------------
# All markdown files in the working directory
SRC = $(wildcard *.$(MEXT))
BASE = $(basename $(SRC))

# Targets
PDF=$(SRC:.md=.pdf)
HTML=$(SRC:.md=.html)
TEX=$(SRC:.md=.tex)
ODT=$(SRC:.md=.odt)
DOCX=$(SRC:.md=.docx)
MS_ODT=$(SRC:.md=-manuscript.odt)
MS_DOCX=$(SRC:.md=-manuscript.docx)
BIB=$(SRC:.md=.bib)

all:	clean $(PDF) $(HTML) $(ODT) $(DOCX) $(MS_ODT) $(MS_DOCX) $(BIB)

pdf:	clean $(PDF)
html:	clean $(HTML)
odt:	clean $(ODT)
docx:	clean $(DOCX)
ms: 	clean $(MS_ODT)
msdocx:	clean $(MS_DOCX)
bib:	$(BIB)

%.html:	%.md
	@echo "$(WARN_COLOR)Converting Markdown to HTML using standard template...$(NO_COLOR)"
	replace_includes $< | replace_pdfs | \
	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block -w html -S \
		$(CROSSREF) \
		--default-image-extension=png \
		--template=$(PREFIX)/templates/html.template \
		--css=$(PREFIX)/styles/marked/kultiad-serif.css \
		--filter pandoc-citeproc \
		--csl=$(PREFIX)/csl/$(CSL).csl \
		--bibliography=$(BIB_FILE) \
	-o $@
	@echo "$(OK_COLOR)All done!$(NO_COLOR)"

%.pdf:	%.md
	@echo "$(WARN_COLOR)Converting Markdown to PDF using hikma-article template...$(NO_COLOR)"
	replace_includes $< | \
	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block -w latex -s -S \
		$(CROSSREF) \
		--default-image-extension=pdf \
		--latex-engine=xelatex \
		--template=$(PREFIX)/templates/xelatex.template \
		--filter pandoc-citeproc \
		--csl=$(PREFIX)/csl/$(CSL).csl \
		--bibliography=$(BIB_FILE) \
		-V chapterstyle=hikma-article \
		-V pagestyle=ath \
	-o $@
	@echo "$(OK_COLOR)All done!$(NO_COLOR)"

%.odt:	%.md
	@echo "$(WARN_COLOR)Converting Markdown to .odt using standard template...$(NO_COLOR)"
	replace_includes $< | replace_pdfs | \
	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block -w odt -S \
		$(CROSSREF) \
		--default-image-extension=png \
		--template=$(PREFIX)/templates/odt.template \
		--reference-odt=$(PREFIX)/styles/reference.odt \
		--filter pandoc-citeproc \
		--csl=$(PREFIX)/csl/$(CSL).csl \
		--bibliography=$(BIB_FILE) \
	-o $@;
	@echo "$(OK_COLOR)All done!$(NO_COLOR)"

%.docx:	%.odt
	@echo "$(WARN_COLOR)Converting .odt to .docx...$(NO_COLOR)"
	/Applications/LibreOffice.app/Contents/MacOS/soffice --invisible --convert-to docx $<
	@echo "$(WARN_COLOR)Removing .odt file...$(NO_COLOR)"
	rm $<
	@echo "$(OK_COLOR)All done!$(NO_COLOR)"

%-manuscript.odt: %.md
	@echo "$(WARN_COLOR)Converting Markdown to .odt using manuscript template...$(NO_COLOR)"
	replace_includes $< | replace_pdfs | \
	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block -w odt -S \
		$(CROSSREF) \
		--default-image-extension=png \
		--template=$(PREFIX)/templates/odt-manuscript.template \
		--reference-odt=$(PREFIX)/styles/reference-manuscript.odt \
		--filter pandoc-citeproc \
		--csl=$(PREFIX)/csl/$(CSL).csl \
		--bibliography=$(BIB_FILE) \
	-o $@

%-manuscript.docx:	%-manuscript.odt
	@echo "$(WARN_COLOR)Converting .odt manuscript to .docx...$(NO_COLOR)"
	/Applications/LibreOffice.app/Contents/MacOS/soffice --invisible --convert-to docx $<
	@echo "$(WARN_COLOR)Removing .odt file...$(NO_COLOR)"
	rm $<
	@echo "$(OK_COLOR)All done!$(NO_COLOR)"

%.bib: %.md
	@echo "$(WARN_COLOR)Extracing all citations into a standalone .bib file...$(NO_COLOR)"
	bib_extract --bibtex_file $(BIB_FILE) $< $@

clean:
	@echo "$(WARN_COLOR)Deleting all existing targets...$(NO_COLOR)"
	rm -f $(addsuffix .html, $(BASE)) $(addsuffix .pdf, $(BASE)) \
		$(addsuffix .odt, $(BASE)) $(addsuffix .docx, $(BASE)) \
		$(addsuffix -manuscript.odt, $(BASE)) $(addsuffix -manuscript.docx, $(BASE)) \
		$(addsuffix .bib, $(BASE))
