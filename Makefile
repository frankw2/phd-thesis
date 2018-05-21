RUBBER=rubber -Wrefs -Wmisc
LATEXRUN:=$(shell bin/check-latexrun)

FIGS = 

CODES = code/atomic_two_write.tex \
		code/log.tex \
		code/app.tex \
		code/inode_type.tex

SRC=$(shell ( test -d ../../fscq-impl/src && echo ../../fscq-impl/src ) || \
	  echo not-found)

pdf: thesis.pdf
.PHONY: pdf

ifeq ($(V),)
quiet = @printf "  %-7s %s\n" "$1" "$@";
Q = @
else
quiet =
Q =
endif

data/app.data: bin/combine-data.py data/largefile.json data/mailbench.json
	$(call quiet,DATA)
	$(Q)python bin/combine-data.py

data/eval-app.tex: bin/combined-data.plot data/app.data
	$(call quiet,GNUPLOT)
	$(Q)gnuplot < bin/combined-data.plot

data/eval-ssd.tex: bin/combined-ssd.plot data/ssd.data
	$(call quiet,GNUPLOT)
	$(Q)gnuplot < bin/combined-ssd.plot

data/io.tex: bin/combine-data.py data/largefile.json data/mailbench.json
	$(call quiet,DATA)
	$(Q)python bin/combine-data.py

figs/%.pdf: figs/%.svg
	$(call quiet,INKSCAPE)
	$(Q)inkscape -z $(INKARGS) -f $(CURDIR)/$< -D -A $(CURDIR)/$@ 

linecount.tex: bin/linecounter.py $(wildcard $(SRC)/*.v)
	wc -l $(SRC)/*.v | python2 bin/linecounter.py > $@~
	mv $@~ $@

gitinfo.tex:
	$(call quiet,GITINFO)
	$(Q)echo "\def\gitid{$$(git describe --always --dirty=+)}" > $@.tmp
	$(Q)cmp -s $@.tmp $@ && rm $@.tmp || mv $@.tmp $@
.PHONY: gitinfo.tex
CLEAN+=gitinfo.tex gitinfo.tex.tmp

thesis.pdf: $(FIGS) $(CODES) data/eval-app.tex data/eval-ssd.tex data/io.tex \
	   gitinfo.tex FORCE
	$(call quiet,LATEX)
	$(Q)export TEXMFHOME=$$PWD/fonts/texmf TEXMFVAR=$$PWD/fonts/texmfvar; \
	if which $(LATEXRUN) >/dev/null 2>&1; then \
		$(LATEXRUN) --bibtex-args=-min-crossrefs=100 thesis.tex; \
	else \
		( echo '#!/bin/sh' ; echo 'exec '$(shell which bibtex)' -min-crossrefs=100 "$$@"' ) > bibtex; \
		chmod 755 bibtex; \
		PATH=.:$$PATH $(RUBBER) --pdf thesis.tex; \
	fi
CLEAN+=thesis.pdfsync thesis.synctex.gz

.PHONY: FORCE

clean:
	if which $(LATEXRUN) >/dev/null 2>&1; then \
		$(LATEXRUN) --clean-all; \
	else \
		$(RUBBER) --pdf --clean thesis.tex; \
	fi
.PHONY: clean

view: thesis.pdf
	evince thesis.pdf &
.PHONY: view

SPELLTEX := $(shell ./bin/get-tex-files.sh thesis.tex)
spell:
	@ for i in $(SPELLTEX) *.bbl; do aspell \
		--mode=tex \
		--add-tex-command="XXX op" \
		--add-tex-command="code p" \
		--add-tex-command="cmd p" \
		--add-tex-command="cref p" \
		--add-tex-command="Cref p" \
		--add-tex-command="thiscref p" \
		--add-tex-command="Thiscref p" \
		--add-tex-command="lcnamecref p" \
		-p ./aspell.words -c $$i; done
	@ for i in $(SPELLTEX); do perl bin/double.pl $$i; done
	@ bash bin/hyphens.sh $(SPELLTEX)
	@ ( head -1 aspell.words ; tail -n +2 aspell.words | sort ) > aspell.words~
	@ mv aspell.words~ aspell.words
.PHONY: spell

%-bw.pdf: %.pdf
	./bin/pdftobw $< $@

# The following rules must be manually invoked because they are
# expensive or require additional environment
code/fmt.tex:
	pygmentize -f latex -S default \
		| grep -vw 'PY@tok@m' \
		| grep -vw 'PY@tok@mi' \
		| grep -vw 'PY@tok@o' \
		| grep -vw 'PY@tok@mo' \
		| grep -vw 'PY@tok@kt' \
		> $@~
	mv $@~ $@

code/%.tex: code/%.py
	$(call quiet,CODE)
	$(Q)pygmentize -f latex -O envname=BVerbatim $< \
		| sed -e 's,PY{o+ow},PY{k},g' \
		> $@

code/%.tex: code/%.v
	$(call quiet,CODE)
	$(Q)pygmentize -f latex -O envname=BVerbatim $< \
		| sed -e 's,PY{o+ow},PY{k},g' \
		> $@
