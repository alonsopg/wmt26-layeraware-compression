LATEXMK ?= latexmk

.PHONY: all clean

all: main.pdf

main.pdf: main.tex references.bib acl-style-files/acl.sty acl-style-files/acl_natbib.bst
	TEXINPUTS=.:acl-style-files//: BSTINPUTS=.:acl-style-files//: $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	$(LATEXMK) -C main.tex
