XMLFILES=$(addprefix ../, $(shell cat POTFILES.in))
POFILES=$(wildcard *.po)

# intltool hack
top_srcdir=..

all:

comps.pot: $(XMLFILES)
	intltool-update --pot --gettext-package=comps
	

report:
	for cat in *.po; do \
		echo -n "$$cat: "; \
		msgfmt -v --statistics -o /dev/null $$cat; \
	done
