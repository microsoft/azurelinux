# just a Makefile parallel_test.sh uses to run stuff in parallel with make
%:
	$(MAKE) -j1 -C .t/$* $*

t-exec-%:
	$(MAKE) -j1 -C ".t/t-exec-$*" \
		TEST_SSH_PORT=10$*0 \
		SKIP_LTESTS="$(shell cat .ltests/not-in/$*)" \
		BUILDDIR="$(shell pwd)/.t/t-exec-$*" \
		TEST_SHELL=sh \
		MAKE=make \
		TEST_SSH_TRACE=yes \
		TEST_SSH_FAIL_FATAL=yes \
		t-exec \
