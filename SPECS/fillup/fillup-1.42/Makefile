#
#
#
# Copyright (c) 1996 S.u.S.E. GmbH Fuerth, Germany.   
#
# please send bugfixes or comments to feedback@suse.de.
#
#


compile: 
	make -C SRC all

install:
	make -C SRC install

test:
	make -C TEST

clean:
	make -C SRC clean
	make -C TEST clean
	rm -f BIN/fillup
