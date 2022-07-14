SUBDIRS = config tools kdc

EXTRA_DIST = run-tests.sh testenv.sh.in pwhelp.txt \
	001-pambasic/run.sh \
	001-pambasic/stderr.expected \
	001-pambasic/stdout.expected \
	002-pamchpw-wrongpw/run.sh \
	002-pamchpw-wrongpw/stderr.expected \
	002-pamchpw-wrongpw/stdout.expected \
	003-pamchpw-warn/run.sh \
	003-pamchpw-warn/stderr.expected \
	003-pamchpw-warn/stdout.expected \
	004-pamchpw-nowarn/run.sh \
	004-pamchpw-nowarn/stderr.expected \
	004-pamchpw-nowarn/stdout.expected \
	005-pamchpw-success/run.sh \
	005-pamchpw-success/stderr.expected \
	005-pamchpw-success/stdout.expected \
	011-pkinit/run.sh \
	011-pkinit/stderr.expected \
	011-pkinit/stdout.expected \
	012-armor/run.sh \
	012-armor/stderr.expected \
	012-armor/stdout.expected \
	014-options-defccdir/run.sh \
	014-options-defccdir/stderr.expected \
	014-options-defccdir/stdout.expected \
	015-options-ccdir/run.sh \
	015-options-ccdir/stderr.expected \
	015-options-ccdir/stdout.expected \
	016-options-banner/run.sh \
	016-options-banner/stderr.expected \
	016-options-banner/stdout.expected \
	017-options-help/run.sh \
	017-options-help/stderr.expected \
	017-options-help/stdout.expected \
	018-options-ccpattern/run.sh \
	018-options-ccpattern/stderr.expected \
	018-options-ccpattern/stdout.expected \
	019-pamchpw-prompt-wrongpw/run.sh \
	019-pamchpw-prompt-wrongpw/stderr.expected \
	019-pamchpw-prompt-wrongpw/stdout.expected \
	020-pamchpw-prompt-success/run.sh \
	020-pamchpw-prompt-success/stderr.expected \
	020-pamchpw-prompt-success/stdout.expected \
	021-options-ccpattern-keyring/run.sh \
	021-options-ccpattern-keyring/stderr.expected \
	021-options-ccpattern-keyring/stdout.expected \
	022-shmem/run.sh \
	022-shmem/stderr.expected \
	022-shmem/stdout.expected \
	023-update/run.sh \
	023-update/stderr.expected \
	023-update/stdout.expected \
	024-shmem-external/run.sh \
	024-shmem-external/stderr.expected \
	024-shmem-external/stdout.expected \
	025-external/run.sh \
	025-external/stderr.expected \
	025-external/stdout.expected \
	026-options-ccpattern-global/run.sh \
	026-options-ccpattern-global/stderr.expected \
	026-options-ccpattern-global/stdout.expected

check: all testenv.sh
	test -x ./tools/kd_tests && ./tools/kd_tests
	$(srcdir)/run-tests.sh
