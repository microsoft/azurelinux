BINDIR = /usr/bin
DESTDIR = ..overridden in spec file..

all: install

install: install-xsl install-img install-extensions install-misc install-epub

install-xsl:
	mkdir -p $(DESTDIR)/{common,eclipse,fo,html,htmlhelp/doc,javahelp,lib,template,xhtml,xhtml-1_1,manpages,profiling,highlighting,roundtrip,website}
	cp common/*.dtd $(DESTDIR)/common
	cp common/*.ent $(DESTDIR)/common
	cp common/*.xml $(DESTDIR)/common
	cp common/*.xsl $(DESTDIR)/common
	cp eclipse/*.xsl $(DESTDIR)/eclipse
	cp fo/*.xml $(DESTDIR)/fo
	cp fo/*.xsl $(DESTDIR)/fo
	cp html/*.xml $(DESTDIR)/html
	cp html/*.xsl $(DESTDIR)/html
	cp htmlhelp/*.xsl $(DESTDIR)/htmlhelp
	cp javahelp/*.xsl $(DESTDIR)/javahelp
	cp lib/*.xsl $(DESTDIR)/lib
	cp template/*.xsl $(DESTDIR)/template
	cp xhtml/*.xsl $(DESTDIR)/xhtml
	cp xhtml-1_1/*.xsl $(DESTDIR)/xhtml-1_1
	cp manpages/*.xsl $(DESTDIR)/manpages
	cp profiling/*.xsl $(DESTDIR)/profiling
	cp highlighting/*.xml $(DESTDIR)/highlighting
	cp highlighting/*.xsl $(DESTDIR)/highlighting
	cp roundtrip/*.xml $(DESTDIR)/roundtrip
	cp roundtrip/*.xsl $(DESTDIR)/roundtrip
	cp roundtrip/*.dtd $(DESTDIR)/roundtrip
	cp website/*.xsl $(DESTDIR)/website

install-img:
	mkdir -p $(DESTDIR)/images/callouts
	cp images/*.gif $(DESTDIR)/images
	cp images/*.png $(DESTDIR)/images
	cp images/*.svg $(DESTDIR)/images
	cp images/callouts/*.png $(DESTDIR)/images/callouts
	cp images/callouts/*.gif $(DESTDIR)/images/callouts
	cp images/callouts/*.svg $(DESTDIR)/images/callouts

install-extensions:
	mkdir -p $(DESTDIR)/extensions
	cp -r extensions/* $(DESTDIR)/extensions

install-epub:
	mkdir -p $(DESTDIR)/epub
	cp -r epub/* ${DESTDIR}/epub

install-misc:
	cp VERSION $(DESTDIR)
