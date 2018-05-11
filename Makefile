all: main.pdf

main.pdf: main.tex $(wildcard *.sty) $(wildcard *.tex) $(wildcard *.bib)
	pdflatex -shell-escape main
	bibtex main -min-crossrefs=1000
	pdflatex -shell-escape main
	pdflatex -shell-escape main

clean:
	rm -f main.pdf main.bbl main.blg main.log main.out main.aux
.PHONY: clean

SPELLTEX := $(shell ./bin/get-tex-files.sh main.tex) main.bbl
spell:
	@ for i in $(SPELLTEX); do aspell -l en_us --mode=tex \
					  --add-tex-command="autoref p" \
					  -p ./aspell.words -c $$i; done
	@ for i in $(SPELLTEX); do perl bin/double.pl $$i; done
	@ for i in $(SPELLTEX); do perl bin/abbrv.pl  $$i; done
	@ bash bin/hyphens.sh $(SPELLTEX)
	@ ( head -1 aspell.words ; tail -n +2 aspell.words | LC_ALL=C sort ) > aspell.words~
	@ mv aspell.words~ aspell.words
.PHONY: spell
