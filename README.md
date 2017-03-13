# Global Pandoc configuration files

After years of trying to perfect the conversion of academic Markdown files to Word (for people who swear by it), I think I've stumbled on the holy grail, thanks to Duke's [Kieran Healy](http://kieranhealy.org/blog/archives/2014/01/23/plain-text/). This repository is a non-forked fork of [this](https://github.com/kjhealy/pandoc-templates), but with the added ability to convert Markdown files into perfeclty styled Word documents, in addition to TeX, HTML, and PDF. 

Pandoc allows you to create custom output templates for most file formats, but unfortunately not for `.docx` files. Following Kieran's lead, this repository includes `odt.template` and `reference.odt`, which places and styles custom metadata (like author information) into an `.odt` file. This can then be converted to `.docx`, either manually (by opening LibreOffice) or with the command line:

	/Applications/LibreOffice.app/Contents/MacOS/soffice.bin --invisible --convert-to docx filename.odt

HOLY GRAIL! Markdown to Word, HTML, and PDF with one command. Beautiful.


## To do

* Space after lists in Word
* Table styles in Word
* Line wrapping in memo header


## Bugs

* No captions at all in Word (because Pandoc > ODT doesn't support them)
* No caption numbers in HTML


## Binary things

Download the [latest compiled `pandoc-crossref` binary](https://github.com/lierdakil/pandoc-crossref/releases) and put it in `./bin`.
