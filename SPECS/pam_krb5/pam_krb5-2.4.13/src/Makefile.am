AM_CFLAGS = @KRB5_CFLAGS@
LD_AS_NEEDED = @LD_AS_NEEDED@
KRB_LIBS = @KRB5_LIBS@ @KEYUTILS_LIBS@
SELINUX_LIBS = @SELINUX_LIBS@

securitydir = $(libdir)/security
security_LTLIBRARIES = pam_krb5.la
noinst_LTLIBRARIES = libpam_krb5.la
pkgsecuritydir = $(libdir)/security/$(PACKAGE)
pkgsecurity_PROGRAMS = pam_krb5_cchelper
EXTRA_DIST = afs5log.1 pam_krb5.5 pam_krb5.8 pam_krb5_cchelper.8 pam_newpag.5 pam_newpag.8
noinst_PROGRAMS = harness harness-newpag shmcat uuauth vfy
man_MANS = pam_krb5.5 pam_krb5.8 pam_krb5_cchelper.8
noinst_MANS =
if AFS
noinst_LTLIBRARIES += pam_newpag.la
noinst_MANS += pam_newpag.5 pam_newpag.8
endif
bin_PROGRAMS =

if AFS
bin_PROGRAMS += afs5log
man_MANS += afs5log.1
noinst_PROGRAMS += pagsh
endif

if WITH_DIRECT_LIBPAM
DIRECT_LIBPAM = -lpam
else
DIRECT_LIBPAM =
endif

libpam_krb5_la_SOURCES = \
	cchelper.c \
	cchelper.h \
	conv.c \
	conv.h \
	getpw.c \
	getpw.h \
	init.c \
	init.h \
	initopts.c \
	initopts.h \
	kuserok.c \
	kuserok.h \
	map.c \
	map.h \
	mkdir.c \
	mkdir.h \
	minikafs.h \
	options.c \
	options.h \
	perms.c \
	perms.h \
	prompter.c \
	prompter.h \
	shmem.c \
	shmem.h \
	sly.c \
	sly.h \
	stash.c \
	stash.h \
	userinfo.c \
	userinfo.h \
	xstr.c \
	xstr.h \
	v5.c \
	v5.h
	
pam_krb5_la_LDFLAGS = -avoid-version -export-dynamic -module -export-symbols-regex 'pam_sm.*' @SYMBOLIC_LINKER_FLAG@
pam_krb5_la_LIBADD = libpam_krb5.la $(KRB_LIBS) $(SELINUX_LIBS) $(DIRECT_LIBPAM)
pam_krb5_la_SOURCES = \
	pamitems.c \
	items.h \
	logpam.c \
	log.h \
	auth.c \
	acct.c \
	password.c \
	session.c \
	session.h

pam_newpag_la_LDFLAGS = -avoid-version -export-dynamic -module -export-symbols-regex 'pam_sm.*' @SYMBOLIC_LINKER_FLAG@
pam_newpag_la_LIBADD = libpam_krb5.la $(KRB_LIBS) $(DIRECT_LIBPAM)
pam_newpag_la_SOURCES = \
	pamitems.c \
	items.h \
	pam_newpag.c \
	logpam.c \
	log.h \
	minikafs.h

pam_krb5_cchelper_SOURCES = \
	pam_krb5_cchelper.c
pam_krb5_cchelper_LDFLAGS = @KRB5_LIBS@ @KEYUTILS_LIBS@
pam_krb5_cchelper_LDADD = xstr.lo

afs5log_SOURCES = \
	afs5log.c \
	noitems.c \
	items.h \
	logstdio.c \
	logstdio.h \
	log.h
afs5log_LDADD = libpam_krb5.la @PAM_LIBS@ @SELINUX_LIBS@ $(KRB_LIBS)

pagsh_SOURCES = \
	pagsh.c \
	logstdio.c \
	logstdio.h \
	log.h
pagsh_LDADD = libpam_krb5.la pamitems.lo @SELINUX_LIBS@ @PAM_LIBS@ $(KRB_LIBS)

harness_SOURCES = harness.c
harness_LDADD = \
	auth.lo \
	acct.lo \
	pamitems.lo \
	password.lo \
	session.lo \
	logstdio.lo \
	perms.lo \
	sly.lo \
	v5.lo
harness_LDADD += libpam_krb5.la @SELINUX_LIBS@ @PAM_LIBS@ $(KRB_LIBS)

harness_newpag_SOURCES = harness.c \
	pam_dummy_acct.c \
	pam_dummy_chauthtok.c
harness_newpag_LDADD = \
	pamitems.lo \
	pam_newpag.lo \
	logstdio.lo \
	perms.lo \
	v5.lo
harness_newpag_LDADD += libpam_krb5.la @SELINUX_LIBS@ @PAM_LIBS@ $(KRB_LIBS)

shmcat_SOURCES = shmcat.c noitems.c
shmcat_LDADD = logstdio.lo libpam_krb5.la @SELINUX_LIBS@ @PAM_LIBS@ $(KRB_LIBS)

uuauth_LDADD = logstdio.lo noitems.lo libpam_krb5.la @SELINUX_LIBS@ @PAM_LIBS@ $(KRB_LIBS)

vfy_LDADD = logstdio.lo noitems.lo libpam_krb5.la @SELINUX_LIBS@ @PAM_LIBS@ $(KRB_LIBS)

if AFS
libpam_krb5_la_SOURCES += minikafs.c minikafs.h tokens.c tokens.h
else
libpam_krb5_la_SOURCES += noafs.c tokens.h
endif
