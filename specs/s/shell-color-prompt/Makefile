bash-color-prompt.sh: bash-color-prompt.sh.in gen.m4
	m4 gen.m4 $< > $@

timestamp:
	cp -p bash-color-prompt.sh bash-color-prompt.sh.$(shell date "+%FT%T")

check:
	cd tests/bats && make check
