all: fillup.info.gz  fillup.txt

fillup.info.gz: fillup.sgml
	sgml2info fillup.sgml
	gzip -9 fillup.info

fillup.txt: fillup.sgml
	sgml2txt fillup.sgml

clean:
	rm -fr fillup.info fillup.info.gz fillup.txt *~ \#*