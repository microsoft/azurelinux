# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Package auxiliary scripts which require ancient Perl 4 modules
%bcond_without cvs_enables_contrib
# Do not run lengthy tests
%bcond_with cvs_enables_extra_test
# Use kerberos
%bcond_without cvs_enables_kerberos
# Use PAM for pserver autentization
%bcond_without cvs_enables_pam
# Rebuild PDF documents from sources
# https://bugs.ghostscript.com/show_bug.cgi?id=696765#c28
%bcond_without cvs_enables_pdf
# Disable xinetd support
%bcond_with cvs_enables_xinetd

Name:       cvs
Version:    1.11.23
Release: 76%{?dist}
Summary:    Concurrent Versions System
URL:        https://cvs.nongnu.org/
# contrib/check_cvs.in:     check-cvs
# contrib/clmerge.in:       GPL-2.0-or-later
# contrib/cln_hist.in:      GPL-2.0-or-later
# contrib/commit_prep.in:   GPL-2.0-or-later
# contrib/cvs_acls.in:      GPL-2.0-or-later
# contrib/cvs2vendor.sh:    GPL-2.0-or-later
# contrib/cvscheck.sh:      GPL-2.0-or-later
# contrib/debug_check_log.sh:   GPL-2.0-or-later
# contrib/log.in:           GPL-2.0-or-later
# contrib/log_accum.in:     GPL-2.0-or-later
# contrib/mfpipe.in:        GPL-2.0-or-later
# contrib/pvcs2rcs.in:      GPL-2.0-or-later
# contrib/rcs2log.sh:       GPL-2.0-or-later
# contrib/rcs-to-cvs.sh:    GPL-2.0-or-later
# contrib/rcslock.in:       GPL-2.0-or-later
# contrib/sccs2rcs.in:      GPL-2.0-or-later
# COPYING:              GPL-1.0 text
# COPYING.LIB:          LGPL-2.0 text
# diff/analyze.c:       GPL-2.0-or-later
# diff/cmpbuf.c:        GPL-2.0-or-later
# diff/cmpbuf.h:        GPL-2.0-or-later
# diff/context.c:       GPL-2.0-or-later
# diff/diff.c:          GPL-2.0-or-later
# diff/diff.h:          GPL-2.0-or-later
# diff/diff3.c:         GPL-2.0-or-later
# diff/diffrun.h:       GPL-2.0-or-later
# diff/dir.c:           GPL-2.0-or-later
# diff/ed.c:            GPL-2.0-or-later
# diff/ifdef.c:         GPL-2.0-or-later ("Refer to the GNU DIFF License")
# diff/io.c:            GPL-2.0-or-later
# diff/normal.c:        GPL-2.0-or-later
# diff/util.c:          GPL-2.0-or-later
# diff/side.c:          GPL-2.0-or-later ("Refer to the GNU DIFF License")
# diff/system.h:        GPL-2.0-or-later
# doc/cvs.1:            GPL-2.0-or-later
# doc/cvs.man.header:   GPL-2.0-or-later (embedded into doc/cvs.1)
# doc/cvs.info-1:       Latex2e-translated-notice
# doc/cvs-paper.ms:     GPL-1.0-or-later (compiled into doc/cvs-paper.pdf)
# doc/cvs.texinfo:      Latex2e-translated-notice (WITH a Tex processing exception
#                       which is advised to be ignored)
# FAQ:                  GPL-1.0-or-later
# HACKING:              GPL-1.0-or-later
# lib/argmatch.c:       GPL-2.0-or-later
# lib/getdate.c:        LicenseRef-Fedora-Public-Domain
#                       ("in the public domain and has no copyright")
# lib/getdate.y:        LicenseRef-Fedora-Public-Domain
#                       ("in the public domain and has no copyright")
# lib/getline.c:        GPL-2.0-or-later
# lib/getopt.c:         GPL-2.0-or-later
# lib/getopt.h:         GPL-2.0-or-later
# lib/getopt1.c:        GPL-2.0-or-later
# lib/getpass.c:        GPL-2.0-or-later
# lib/getpagesize.h:    GPL-2.0-or-later
# lib/Makefile.am:      GPL-2.0-or-later
# lib/md5.c:            LicenseRef-Fedora-Public-Domain
#                       ("no copyright is claimed. This code is in the public
#                       domain;")
# lib/md5.h:            "See md5.c"
# lib/regex.c:          GPL-2.0-or-later
# lib/regex.h:          GPL-2.0-or-later
# lib/sighandle.c:      GPL-2.0-or-later
# lib/stripslash.c:     GPL-2.0-or-later
# lib/system.h:         GPL-2.0-or-later
# lib/wait.h:           GPL-2.0-or-later
# lib/xgetwd.c:         GPL-2.0-or-later
# lib/xgssapi.h:        GPL-2.0-or-later
# lib/xselect.h:        GPL-2.0-or-later
# lib/xsize.h:          GPL-2.0-or-later
# lib/xtime.h:          GPL-2.0-or-later
# lib/yesno.c:          GPL-2.0-or-later
# man/cvs.5:            Latex2e-translated-notice
# man/cvsbug.8:         GPL-2.0-or-later AND Latex2e-translated-notice
# README:               GPL-1.0-or-later
# src/admin.c:          GPL-1.0-or-later (as in the README file)
# src/annotate.c:       GPL-1.0-or-later (as in the README file)
# src/buffer.c:         GPL-2.0-or-later
# src/buffer.h:         GPL-2.0-or-later
# src/checkin.c:        GPL-1.0-or-later (as in the README file)
# src/checkout.c:       GPL-1.0-or-later (as in the README file)
# src/classify.c:       GPL-1.0-or-later (as in the README file)
# src/client.c:         GPL-2.0-or-later
# src/client.h:         GPL-2.0-or-later
# src/commit.c:         GPL-1.0-or-later (as in the README file)
# src/create_adm.c:     GPL-1.0-or-later (as in the README file)
# src/cvs.h:            GPL-1.0-or-later (as in the README file)
# src/cvsbug.in:        GPL-2.0-or-later
# src/cvsrc.c:          GPL-1.0-or-later (as in the README file)
# src/diff.c:           GPL-1.0-or-later (as in the README file)
# src/edit.c:           GPL-2.0-or-later
# src/edit.h:           GPL-2.0-or-later
# src/entries.c:        GPL-1.0-or-later (as in the README file)
# src/error.c:          GPL-2.0-or-later
# src/error.h:          GPL-2.0-or-later
# src/expand_path.c:    GPL-2.0-or-later
# src/fileattr.c:       GPL-2.0-or-later
# src/fileattr.h:       GPL-2.0-or-later
# src/filesubr.c:       GPL-2.0-or-later
# src/find_names.c:     GPL-1.0-or-later (as in the README file)
# src/hardlink.c:       GPL-2.0-or-later
# src/hardlink.h:       GPL-2.0-or-later
# src/hash.c:           GPL-1.0-or-later (as in the README file)
# src/hash.h:           GPL-1.0-or-later (as in the README file)
# src/history.c:        GPL-2.0-or-later
# src/history.h:        GPL-1.0-or-later (as in the README file)
# src/ignore.c:         GPL-2.0-or-later
# src/import.c:         GPL-1.0-or-later (as in the README file)
# src/lock.c:           GPL-1.0-or-later (as in the README file)
# src/log.c:            GPL-1.0-or-later (as in the README file)
# src/login.c:          GPL-1.0-or-later (as in the README file)
# src/logmsg.c:         GPL-1.0-or-later (as in the README file)
# src/main.c:           GPL-1.0-or-later (as in the README file)
# src/mkmodules.c:      GPL-1.0-or-later (as in the README file)
# src/modules.c:        GPL-1.0-or-later (as in the README file)
# src/myndbm.c:         GPL-1.0-or-later (as in the README file)
# src/myndbm.h:         GPL-2.0-or-later
# src/no_diff.c:        GPL-1.0-or-later (as in the README file)
# src/parseinfo.c:      GPL-1.0-or-later (as in the README file)
# src/patch.c:          GPL-1.0-or-later (as in the README file)
# src/rcs.c:            GPL-1.0-or-later (as in the README file)
# src/rcs.h:            GPL-1.0-or-later (as in the README file)
# src/rcscmds.c:        GPL-1.0-or-later (as in the README file)
# src/recurse.c:        GPL-1.0-or-later (as in the README file)
# src/release.c:        GPL-2.0-or-later
# src/remove.c:         GPL-1.0-or-later (as in the README file)
# src/repos.c:          GPL-1.0-or-later (as in the README file)
# src/root.c:           GPL-1.0-or-later (as in the README file)
# src/root.h:           GPL-1.0-or-later (as in the README file)
# src/run.c:            GPL-2.0-or-later
# src/sanity.sh:        GPL-2.0-or-later
# src/server.c:         GPL-2.0-or-later
# src/server.h:         GPL-1.0-or-later (as in the README file)
# src/stack.c:          GPL-1.0-or-later (as in the README file)
# src/stack.h:          GPL-1.0-or-later (as in the README file)
# src/status.c:         GPL-1.0-or-later (as in the README file)
# src/subr.c:           GPL-1.0-or-later (as in the README file)
# src/tag.c:            GPL-1.0-or-later (as in the README file)
# src/update.c:         GPL-1.0-or-later (as in the README file)
# src/update.h:         GPL-2.0-or-later
# src/vers_ts.c:        GPL-1.0-or-later (as in the README file)
# src/version.c:        GPL-1.0-or-later (as in the README file)
# src/watch.c:          GPL-2.0-or-later
# src/watch.h:          GPL-2.0-or-later
# src/wrapper.c:        GPL-2.0-or-later
# src/zlib.c:           GPL-2.0-or-later
## Used at build time, but not in any binary package
# acinclude.m4:         GPL-2.0-or-later AND GPL-1.0-or-later WITH Autoconf-exception-generic
# contrib/Makefile.am:  GPL-2.0-or-later
# depcomp:              GPL-2.0-or-later WITH Autoconf-exception-generic
# diff/Makefile.am:     GPL-2.0-or-later
# doc/Makefile.am:      GPL-2.0-or-later
# doc/mkman.pl:         GPL-2.0-or-later
# lib/test-getdate.sh:  GPL-2.0-or-later
# Makefile.am:          GPL-2.0-or-later
# Makefile.in:          FSFULLRWD AND GPL-2.0-or-later
# man/Makefile.am:      GPL-2.0-or-later
# mktemp.sh:            GPL-2.0-or-later
# src/Makefile.am:      GPL-2.0-or-later
# tools/Makefile.am:    GPL-2.0-or-later
# vms/Makefile.am:      GPL-2.0-or-later
# windows-NT/Makefile.am:       GPL-2.0-or-later
# windows-NT/SCC/Makefile.am:   GPL-2.0-or-later
## Never used, not packaged
# contrib/cvs_acls.html:    GPL-2.0-or-later
# contrib/descend.sh:       GPL-2.0-or-later
# contrib/rcs2sccs.sh:      GPL-2.0-or-later
# INSTALL:              GPL-1.0-or-later
## Unbundled, never used
# aclocal.m4:           FSFULLRWD AND FSFULLR
# compile:              GPL-2.0-or-later WITH Autoconf-exception-generic
# configure:            FSFUL
# contrib/Makefile.in:  FSFULLRWD AND GPL-2.0-or-later
# diff/Makefile.in:     FSFULLRWD
# doc/Makefile.in:      FSFULLRWD AND GPL-2.0-or-later
# doc/mdate-sh:         GPL-2.0-or-later WITH Autoconf-exception-generic
# doc/texinfo.tex:      GPL-2.0-or-later WITH Texinfo exception
#                       (Waiting on an identifier
#                       <https://gitlab.com/fedora/legal/fedora-license-data/-/issues/206>)
# emx/config.h:         GPL-2.0-or-later
# emx/filesubr.c:       GPL-2.0-or-later
# emx/rcmd.h:           GPL-2.0-or-later
# emx/startserver.c:    GPL-2.0-or-later
# emx/stripslash.c:     GPL-2.0-or-later
# emx/system.c:         GPL-2.0-or-later
# install-sh:           X11 AND LicenseRef-Fedora-Public-Domain
# lib/fncase.c:         GPL-2.0-or-later
# lib/fnmatch.c:        LGPL-2.0-or-later
# lib/fnmatch.h.in:     LGPL-2.0-or-later
# lib/gethostname.c:    GPL-2.0-or-later
# lib/Makefile.in:      FSFULLRWD AND GPL-2.0-or-later
# lib/memmove.c:        LGPL-2.0-or-later (copied from libiberty)
# lib/mkdir.c:          GPL-2.0-or-later
# lib/rename.c:         GPL-2.0-or-later
# lib/strerror.c:       LGPL-2.0-or-later (copied from libiberty)
# man/Makefile.in:      FSFULLRWD AND GPL-2.0-or-later
# mdate-sh:             GPL-2.0-or-later
# missing:              GPL-2.0-or-later WITH Autoconf-exception-generic
# mkinstalldirs:        LicenseRef-Fedora-Public-Domain
# os2/config.h:         GPL-2.0-or-later
# os2/dirent.c:         HPND
#                       <https://gitlab.com/fedora/legal/fedora-license-data/-/issues/204>
# os2/dirent.h:         HPND
#                       <https://gitlab.com/fedora/legal/fedora-license-data/-/issues/204>
# os2/filesubr.c:       GPL-2.0-or-later
# os2/os2inc.h:         GPL-2.0-or-later
# os2/pwd.c:            GPL-1.0-or-later
# os2/pwd.h:            GPL-1.0-or-later
# os2/rcmd.c:           GPL-2.0-or-later
# os2/rcmd.h:           GPL-2.0-or-later
# os2/run.c:            GPL-2.0-or-later
# os2/stripslash.c:     GPL-2.0-or-later
# os2/watcom.mak:       GPL-2.0-or-later
# src/Makefile.in:      FSFULLRWD AND GPL-2.0-or-later
# tools/Makefile.in:    FSFULLRWD AND GPL-2.0-or-later
# vms/dir.h:            GPL-1.0-or-later
# vms/filesubr.c:       GPL-2.0-or-later
# vms/filutils.c:       GPL-2.0-or-later
# vms/filutils.h:       GPL-2.0-or-later
# vms/getpass.c:        GPL-2.0-or-later
# vms/getwd.c:          GPL-2.0-or-later
# vms/Makefile.in:      FSFULLRWD AND GPL-2.0-or-later
# vms/misc.c:           GPL-2.0-or-later
# vms/misc.h:           GPL-2.0-or-later
# vms/ndir.c:           GPL-2.0-or-later
# vms/pathnames.h:      BSD-4-Clause
# vms/pipe.c:           GPL-2.0-or-later
# vms/pipe.h:           GPL-2.0-or-later
# vms/vmsmunch_private.h:   "not copyrighted in any way" !
# vms/waitpid.c:            GPL-2.0-or-later
# windows-NT/filesubr.c:    GPL-2.0-or-later
# windows-NT/Makefile.in:   FSFULLRWD AND GPL-2.0-or-later
# windows-NT/mkdir.c:       GPL-2.0-or-later
# windows-NT/ndir.c:        GPL-1.0-or-later
# windows-NT/ndir.h:        GPL-1.0-or-later
# windows-NT/pwd.c:         GPL-1.0-or-later
# windows-NT/pwd.h:         GPL-1.0-or-later
# windows-NT/rcmd.c:        GPL-2.0-or-later
# windows-NT/run.c:         GPL-2.0-or-later
# windows-NT/sockerror.c:   GPL-2.0-or-later
# windows-NT/SCC/Makefile.in:   FSFULLRWD AND GPL-2.0-or-later
# windows-NT/startserver.c: GPL-2.0-or-later
# windows-NT/stripslash.c:  GPL-2.0-or-later
# windows-NT/woe32.c:       GPL-2.0-or-later
# ylwrap:                   GPL-2.0-or-later WITH Autoconf-exception-generic
# zlib/*                            Zlib ("see copyright notice in zlib.h")
# zlib/contrib/asm586/match.S:      GPL-1.0-or-later
# zlib/contrib/asm686/match.S:      GPL-1.0-or-later
# zlib/contrib/iostream2/zstream.h: MIT-open-group-like
#                                   (Waiting on an identifier
#                                   <https://gitlab.com/fedora/legal/fedora-license-data/-/issues/205>)
# zlib/contrib/minizip/unzip.h:     Zlib
# zlib/contrib/minizip/zip.h:       Zlib
# zlib/Makfile.in:                  Zlib ("see copyright notice in zlib.h")
# zlib/zlib.h:                      Zlib
# zlib/zlib.html:                   Zlib
License:    GPL-2.0-or-later AND GPL-1.0-or-later AND Latex2e-translated-notice AND LicenseRef-Fedora-Public-Domain
Source0:    https://ftp.gnu.org/non-gnu/cvs/source/stable/%{version}/cvs-%{version}.tar.bz2
Source1:    https://ftp.gnu.org/non-gnu/cvs/source/stable/%{version}/cvs-%{version}.tar.bz2.sig
# Retrieved from <hkp://keyserver.ubuntu.com> key server.
Source2:    gpgkey-CB6A07CA90C54234E8A3C8D02C3D4E4C17F231A4.gpg
Source3:    cvs.xinetd
Source4:    cvs.pam
Source5:    cvs.sh
Source6:    cvs.csh
Source7:    cvs@.service
Source8:    cvs.socket
Source9:    cvs.target
Source10:   cvs.sh.5
Source11:   cvs.csh.5
# Fix up initial cvs login, bug #47457
Patch0:     cvs-1.11.23-cvspass.patch
# Build against system zlib
Patch1:     cvs-1.11.19-extzlib.patch
# Aadd 't' as a loginfo format specifier (print tag or branch name)
Patch2:     cvs-1.11.19-netbsd-tag.patch
# Deregister SIGABRT handler in clean-up to prevent loop, bug #66019
Patch3:     cvs-1.11.19-abortabort.patch
# Disable lengthy tests at build-time
Patch4:     cvs-1.11.1p1-bs.patch
# Improve proxy support, bug #144297
Patch5:     cvs-1.11.21-proxy.patch
# Do not accumulate new lines when reusing commit message, bug #64182
Patch7:     cvs-1.11.19-logmsg.patch
# Disable slashes in tag name, bug #56162
Patch8:     cvs-1.11.19-tagname.patch
# Fix NULL dereference, bug #63365
Patch9:     cvs-1.11.19-comp.patch
# Fix insecure temporary file handling in cvsbug, bug #166366
Patch11:    cvs-1.11.19-tmp.patch
# Add PAM support, bug #48937
Patch12:    cvs-1.11.21-pam.patch
# Report unknown file when calling cvs diff with two -r options, bug #18161
Patch13:    cvs-1.11.21-diff.patch
# Fix cvs diff -kk, bug #150031
Patch14:    cvs-1.11.21-diff-kk.patch
# Enable obsolete sort option called by rcs2log, bug #190009
Patch15:    cvs-1.11.21-sort.patch
# Add IPv6 support, bug #199404
Patch17:    cvs-1.11.22-ipv6-proxy.patch
# getline(3) returns ssize_t, bug #449424
Patch19:    cvs-1.11.23-getline64.patch
# Add support for passing arguments through standard input, bug #501942
Patch20:    cvs-1.11.22-stdinargs.patch
# CVE-2010-3864, bug #645386
Patch21:    cvs-1.11.23-cve-2010-3846.patch
# Remove undefinded date from cvs(1) header, bug #225672
Patch22:    cvs-1.11.23-remove_undefined_date_from_cvs_1_header.patch
# Adjust tests to accept new style getopt argument quotation and SELinux label
# notation from ls(1)
Patch23:    cvs-1.11.23-sanity.patch
# Run tests verbosely
Patch24:    cvs-1.11.23-make_make_check_sanity_testing_verbose.patch
# Set PAM_TTY and PAM_RHOST on PAM authentication
Patch25:    cvs-1.11.23-Set-PAM_TTY-and-PAM_RHOST-on-PAM-authentication.patch
# Add KeywordExpand configuration keyword
Patch26:    cvs-1.11.23-Back-port-KeywordExpand-configuration-keyword.patch
# bug #722972
Patch27:    cvs-1.11.23-Allow-CVS-server-to-use-any-Kerberos-key-with-cvs-se.patch
# CVE-2012-0804, bug #787683
Patch28:    cvs-1.11.23-Fix-proxy-response-parser.patch
# Correct texinfo syntax, bug #970716, submitted to upstream as bug #39166
Patch29:    cvs-1.11.23-doc-Add-mandatory-argument-to-sp.patch
# Excpect crypt(3) can return NULL, bug #966497, upstream bug #39040
Patch30:    cvs-1.11.23-crypt-2.diff
# Pass compilation with -Wformat-security, bug #1037029, submitted to upstream
# as bug #40787
Patch31:    cvs-1.11.23-Pass-compilation-with-Wformat-security.patch
# Fix CVE-2017-1283 (command injection via malicious SSH URL), bug #1480801
Patch32:    cvs-1.11.23-Fix-CVE-2017-12836.patch
# Close a configuration file on a syntax error, bug #815660,
# <http://savannah.nongnu.org/bugs/?36276>
Patch33:    cvs-1.11.23-Close-a-configuration-file-on-a-syntax-error.patch
# Do not use deprecated diff -L options, bug #772559,
# <https://savannah.nongnu.org/bugs/?35267>
Patch34:    cvs-1.11.23-Use-diff-label.patch
# Enable cvs to build in C99 mode, bug #2187741
Patch35:    cvs-1.11.23-c99.patch
# Adjust tests to grep-3.9, proposed to the upstream,
# <https://savannah.nongnu.org/bugs/index.php?64084>
Patch36:    cvs-1.11.23-tests-Call-nonobsolete-grep-F.patch
# Adapt to changes in GCC 15, bug #2340021, proposed to the upstream,
# <https://savannah.nongnu.org/bugs/index.php?66726>
Patch37:    cvs-1.11.23-Adapt-to-changes-in-GCC-15.patch
BuildRequires:  autoconf >= 2.58
BuildRequires:  automake >= 1.7.9
BuildRequires:  bison
BuildRequires:  coreutils
BuildRequires:  findutils
%if %{with cvs_enables_pdf}
BuildRequires:  ghostscript
BuildRequires:  groff
BuildRequires:  texinfo-tex
%endif
# glibc-common for iconv
BuildRequires:  glibc-common
BuildRequires:  gnupg2
BuildRequires:  gzip
%if %{with cvs_enables_kerberos}
BuildRequires:  krb5-devel
%endif
BuildRequires:  libtool
BuildRequires:  libxcrypt-devel
BuildRequires:  make
%if %{with cvs_enables_pam}
BuildRequires:  pam-devel
%endif
%if %{with cvs_enables_contrib}
BuildRequires:  perl-generators
%endif
BuildRequires:  systemd
# texinfo required for
# cvs-1.11.23-Back-port-KeywordExpand-configuration-keyword.patch
BuildRequires:  texinfo
BuildRequires:  vim-minimal
BuildRequires:  zlib-devel
Requires:       vim-minimal


%description
CVS (Concurrent Versions System) is a version control system that can
record the history of your files (usually, but not always, source
code). CVS only stores the differences between versions, instead of
every version of every file you have ever created. CVS also keeps a log
of who, when, and why changes occurred.

CVS is very helpful for managing releases and controlling the
concurrent editing of source files among multiple authors. Instead of
providing version control for a collection of files in a single
directory, CVS provides version control for a hierarchical collection
of directories consisting of revision controlled files. These
directories and files can then be combined together to form a software
release.


%if %{with cvs_enables_contrib}
%package contrib
Summary: Unsupported contributions collected by CVS developers
# check_cvs is a check-cvs license
License: GPL-2.0-or-later AND check-cvs
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description contrib
Scripts sent to CVS developers by contributors around the world. These
contributions are really unsupported.
%endif


%if %{with cvs_enables_xinetd}
%package inetd
Summary: CVS server configuration for xinetd
License: GPL-1.0-or-later
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: xinetd

%description inetd
A CVS server can be run locally, via a remote shell or by an inetd server.
This package provides a configuration for xinetd, an inetd implementation.
%endif


%package doc
Summary: Additional documentation for Concurrent Versions System
License: GPL-1.0-or-later AND Latex2e-translated-notice
%if !%{with cvs_enables_pdf}
# Ghostscript stores a time stamp into output files and that
# violates RPM noarch rules.
BuildArch: noarch
%endif

%description doc
FAQ, RCS format description, parallel development how-to, and Texinfo
pages in PDF.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q
%patch -p1 -P 0
%patch -p1 -P 1
%patch -p1 -P 2
%patch -p1 -P 3
%if !%{with cvs_enables_extra_test}
%patch -p1 -P 4
%endif
%patch -p1 -P 5
%patch -p1 -P 7
%patch -p1 -P 8
%patch -p1 -P 9
%patch -p1 -P 11
%if %{with cvs_enables_pam}
%patch -p1 -P 12
%endif
%patch -p1 -P 13
%patch -p1 -P 14
%patch -p1 -P 15
%patch -p1 -P 17
%patch -p1 -P 19
%patch -p1 -P 20
%patch -p1 -P 21
%patch -p1 -P 22
%patch -p1 -P 23
%patch -p1 -P 24
%patch -p1 -P 25
%patch -p1 -P 26
%patch -p1 -P 27
%patch -p1 -P 28
%patch -p1 -P 29
%patch -p1 -P 30
%patch -p1 -P 31
%patch -p1 -P 32
%patch -p1 -P 33
%patch -p1 -P 34
%patch -p1 -P 35
%patch -p1 -P 36
%patch -p1 -P 37

# Remove bundled autotools files, they will be regenerated in %%build phase.
# Keep acinclude.m4 becuse it defines ACX_WITH_GSSAPI.
rm aclocal.m4 compile configure doc/mdate-sh doc/texinfo.tex \
    install-sh mdate-sh missing mkinstalldirs ylwrap
rm {.,contrib,diff,doc,lib,man,src,tools,vms,windows-NT,windows-NT/SCC,zlib}/Makefile.in
# Remove bundled zlib
rm -r zlib
# Remove unused code
find emx -type f \! -name Makefile.in -delete
find os2 -type f \! -name Makefile.in -delete
find vms -type f \! \( -name Makefile.am -o -name config.h.in \) -delete
find windows-NT -type f \! \( -name Makefile.am -o -name config.h.in -o -name fix-msvc-mak\* \) -delete
truncate --size=0 lib/fncase.c lib/fnmatch.c lib/fnmatch.h.in lib/gethostname.c \
    lib/memmove.c lib/mkdir.c lib/rename.c lib/strerror.c
# Remove pregenerated code
rm lib/getdate.c
# Remove pregenerated documentation
%if %{with cvs_enables_pdf}
rm doc/*.pdf
%endif
# Convert files to UTF-8
for F in FAQ; do
    iconv -f ISO-8859-1 -t UTF-8 < "$F" > "${F}.UTF8"
    touch -r "$F"{,.UTF8}
    mv "$F"{.UTF8,}
done

%build
autoreconf --force --install

%if %{with cvs_enables_pam}
    PAM_CONFIG="--enable-pam"
%endif

%if %{with cvs_enables_kerberos}
    k5prefix=`krb5-config --prefix`
    CPPFLAGS=-I${k5prefix}/include/kerberosIV; export CPPFLAGS
    CFLAGS=-I${k5prefix}/include/kerberosIV; export CFLAGS
    LIBS="-lk5crypto"; export LIBS
    KRB_CONFIG="--with-gssapi --without-krb4 --enable-encryption"
%endif

%configure CFLAGS="$CFLAGS $RPM_OPT_FLAGS \
    -D_FILE_OFFSET_BITS=64 %-D_LARGEFILE64_SOURCE" \
    $PAM_CONFIG $KRB_CONFIG CSH=/bin/csh

%{make_build} all doc

%check
if [ $(id -u) -ne 0 ] ; then
    make check
fi

%install
%{make_install}
# forcefully compress the info pages so that install-info will work properly
# in the %%post
gzip $RPM_BUILD_ROOT/%{_infodir}/cvs* || true
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%if %{with cvs_enables_xinetd}
    install -D -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/xinetd.d/%{name}
%endif
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/%{name}
%if %{with cvs_enables_pam}
    install -D -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/cvs
%endif
install -D -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/cvs.sh
install -D -m 644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/cvs.csh
install -p -m 644 -D %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}/cvs\@.service
install -p -m 644 -D %{SOURCE8} $RPM_BUILD_ROOT%{_unitdir}/cvs.socket
install -p -m 644 -D %{SOURCE9} $RPM_BUILD_ROOT%{_unitdir}/cvs.target
install -D -m 644 %{SOURCE10} $RPM_BUILD_ROOT/%{_mandir}/man5/cvs.sh.5
install -D -m 644 %{SOURCE11} $RPM_BUILD_ROOT/%{_mandir}/man5/cvs.csh.5

%if !%{with cvs_enables_contrib}
rm -f $RPM_BUILD_ROOT/%{_bindir}/rcs2log
rm -fr $RPM_BUILD_ROOT/%{_datadir}/%{name}
%endif

%post
%systemd_post cvs.socket
exit 0

%preun
%systemd_preun cvs.socket
%systemd_preun cvs.target
exit 0

%postun
%systemd_postun_with_restart cvs.socket


%files
%license COPYING*
%doc AUTHORS BUGS DEVEL-CVS HACKING MINOR-BUGS NEWS PROJECTS TODO README
%{_bindir}/%{name}*
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
%{_mandir}/man8/cvsbug.*
%{_infodir}/{cvs,cvsclient}.info*
%dir %{_localstatedir}/%{name}
%if %{with cvs_enables_pam}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%endif
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*
%{_unitdir}/%{name}*

%if %{with cvs_enables_contrib}
%files contrib
%{_bindir}/rcs2log
%{_datadir}/%{name}
%endif

%if %{with cvs_enables_xinetd}
%files inetd
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%endif

%files doc
%license COPYING
%doc FAQ doc/RCSFILES doc/*.pdf


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-75
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 1.11.23-74
- Add explicit BR: libxcrypt-devel

* Thu Jan 23 2025 Petr Pisar <ppisar@redhat.com> - 1.11.23-73
- Fix building in ISO C23 with GCC 15 (bug #2340021)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-71
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-70
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 27 2023 Petr Pisar <ppisar@redhat.com> - 1.11.23-68
- Convert License tags to an SPDX format

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-67
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 19 2023 Petr Pisar <ppisar@redhat.com> - 1.11.23-66
- Modernize a spec file
- Build PDF documentation from sources
- Adjust tests to grep-3.9

* Wed Apr 19 2023 Arjun Shankar <arjun@redhat.com> - 1.11.23-65
- Adjust cvs-1.11.23-c99.patch for a cleaner fix (#2187741)

* Tue Apr 18 2023 Arjun Shankar <arjun@redhat.com> - 1.11.23-64
- Port to C99 (#2187741)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-63
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 05 2022 Kalev Lember <klember@redhat.com> - 1.11.23-62
- Avoid systemd_requires as per updated packaging guidelines

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Stewart Smith <trawets@amazon.com> - 1.11.23-60
- Add a build condition for creating contrib package

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.11.23-57
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 11 2020 Petr Pisar <ppisar@redhat.com> - 1.11.23-55
- Disable xinetd support

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.11.23-50
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Petr Pisar <ppisar@redhat.com> - 1.11.23-48
- Remove install-info from scriptlets

* Thu May 03 2018 Petr Pisar <ppisar@redhat.com> - 1.11.23-47
- Modernize spec file
- Close a configuration file on a syntax error (bug #815660)
- Do not use deprecated diff -L options (bug #772559)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.11.23-45
- Rebuilt for switch to libxcrypt

* Mon Aug 14 2017 Petr Pisar <ppisar@redhat.com> - 1.11.23-44
- Fix CVE-2017-1283 (command injection via malicious SSH URL)
  (bug #1480801)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.23-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.23-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.23-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.23-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 04 2013 Petr Pisar <ppisar@redhat.com> - 1.11.23-36
- Fix editor-log-file1 and parseroot-3r tests (bug #1037966)

* Tue Dec 03 2013 Petr Pisar <ppisar@redhat.com> - 1.11.23-35
- Fix compilation with -Wformat-security (bug #1037029)

* Wed Oct 23 2013 Petr Pisar <ppisar@redhat.com> - 1.11.23-34
- Harden build for cvs in server role (bug #983164)
- Add cvs.sh(5) manual page (bug #983164)
- Add cvs.csh(5) manual page (bug #983164)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.23-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.11.23-32
- Perl 5.18 rebuild

* Wed Jun 26 2013 Petr Pisar <ppisar@redhat.com> - 1.11.23-31
- Allow CVS server to use any Kerberos key with cvs service name. This reverts
  canonicalization on clite side introduced with 1.11.23-20 and replaces it
  with a more benevolent key selection on server side. (bug #722972)

* Wed Jun 05 2013 Petr Pisar <ppisar@redhat.com> - 1.11.23-30
- Fix texinfo documentation to work with texinfo-5.1 (bug #970716)
- Do not crash if crypt(3) returns NULL (bug #966497)

* Tue Feb 12 2013 Petr Pisar <ppisar@redhat.com> - 1.11.23-29
- Correct handling systemd service (bug #737264)
- Allow configuration with automake-1.13.1
- Allow to stop all server instances by stopping cvs.target

* Tue Aug 28 2012 Petr Pisar <ppisar@redhat.com> - 1.11.23-28
- Document patches and add Public Domain license

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 1.11.23-27
- Modernize systemd scriptlets (bug #850075)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.23-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Petr Pisar <ppisar@redhat.com> - 1.11.23-25
- Fix CVE-2012-0804 (bug #787683)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.23-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 20 2011 Petr Pisar <ppisar@redhat.com> - 1.11.23-23
- Ignore cvs exit code run as systemd socket-service to preserve memory
  (bug #739538)

* Fri Sep 16 2011 Petr Pisar <ppisar@redhat.com> - 1.11.23-22
- Add support for systemd (bug #737264)

* Mon Aug 15 2011 Kalev Lember <kalevlember@gmail.com> - 1.11.23-21
- Rebuilt for rpm bug #728707

* Thu Jul 21 2011 Petr Pisar <ppisar@redhat.com> - 1.11.23-20
- Fix GSS API authentication against multihomed server (bug #722972)

* Thu May 26 2011 Petr Pisar <ppisar@redhat.com> - 1.11.23-19
- Split contributed scripts (including rcs2log) to separate `contrib'
  sub-package due to dependencies
- Remove explicit defattr

* Thu May 26 2011 Petr Pisar <ppisar@redhat.com> - 1.11.23-18
- Filter sccs2rcs interpreter from dependencies again (bug #225672)

* Tue Apr 12 2011 Petr Pisar <ppisar@redhat.com> - 1.11.23-17
- Deliver xinetd configuration as a sub-package requiring xinetd

* Tue Mar 15 2011 Petr Pisar <ppisar@redhat.com> - 1.11.23-16
- Back-port KeywordExpand configuration keyword
- Clean spec file

* Thu Mar 10 2011 Petr Pisar <ppisar@redhat.com> - 1.11.23-15
- Set PAM_TTY and PAM_RHOST on PAM authentication

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.23-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Petr Pisar <ppisar@redhat.com> - 1.11.23-13
- Make cvs.csh valid CSH script (bug #671003)

* Mon Oct 25 2010 Petr Pisar <ppisar@redhat.com> - 1.11.23-12
- Adjust spec file to package review: remove unused patches, fix license tag,
  fix home page URL, improve summary, package additional documentation, move
  FAQ file into `doc' subpackage, remove undefined date in cvs(1), make
  contrib script executable again (bug #225672)
- Adjust sanity tests to accept new style getopt argument quotation and
  SELinux label notation from ls(1)

* Thu Oct 21 2010 Petr Pisar <ppisar@redhat.com> - 1.11.23-11
- Fix CVE-2010-3846 (bug #645386)

* Mon Mar  1 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.11.23-10
- fixed license

* Tue Jan 12 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.11.23-9
- spec file fixes based on review

* Fri Oct 16 2009 Jiri Moskovcak <jmoskovc@redhat.com> 1.11.23-8
- fixed install with --excludedocs rhbz#515981

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> 1.11.23-7
- Use password-auth common PAM configuration

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009  Jiri Moskovcak <jmoskovc@redhat.com> - 1.11.23.5
- added support for passing arguments thru stdin (patch from arozansk@redhat.com)
- Resolves: #501942

* Wed Apr 08 2009 Adam Jackson <ajax@redhat.com> 1.11.23-4
- Disable krb4 support to fix F12 buildroots.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.11.23-2
- fix license tag
- fix patches to apply with fuzz=0

* Tue Jun  3 2008 Jiri Moskovcak <jmoskovc@redhat.com> 1.11.23.1
- updated to new version 1.11.23
- fixed build on x86_64
- rewritten sanity.sh patch to match current version
- Resolves: #449424

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.11.22-13
- Autorebuild for GCC 4.3

* Mon Sep 17 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 1.11.22-12
- rewriten previous patch when trying to diff  removed files
- Resolves: #277501, #242049

* Mon Jul 30 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 1.11.22-11
- fix diff on removed file when "-r BASE" tag is used
- Resolves: #242049

* Fri Jun 15 2007 Stepan Kasal <skasal@redhat.com> - 1.11.22-10
- make sccs2rcs non-executable, so that find-requires does not add
  dependency on /bin/csh when /bin/csh is available
- add CSH=/bin/csh to configure, so that sccs2rcs #! line is not
  corrupted  when /bin/csh is not available
- replace the deprecated %%makeinstall (see Packaging Guidelines)

* Mon Feb 19 2007 Jindrich Novy <jnovy@redhat.com> - 1.11.22-9
- fix permissions of cvs.sh, add cvs.csh to /etc/profile.d (#225672)

* Fri Jan  5 2007 Jindrich Novy <jnovy@redhat.com> - 1.11.22-8
- fix post/preun scriptlets so that they won't fail with docs disabled

* Fri Dec  1 2006 Jindrich Novy <jnovy@redhat.com> - 1.11.22-7
- remove/replace obsolete rpm tags, fix rpmlint errors

* Sat Oct 28 2006 Jindrich Novy <jnovy@redhat.com> - 1.11.22-6
- respect explicit port specification in CVS_PROXY (#212418)

* Wed Oct 25 2006 Jindrich Novy <jnovy@redhat.com> - 1.11.22-5
- spec cleanup
- use dist, SOURCE0 now points to correct upstream URL

* Fri Jul 28 2006 Martin Stransky <stransky@redhat.com> - 1.11.22-4
- added ipv6 patch (#199404)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.11.22-3.1
- rebuild

* Wed Jun 28 2006 Maros Barabas <mbarabas@redhat.com> - 1.11.22-3
- fix for #196848 - double free coruption

* Thu Jun 22 2006 Martin Stransky <stransky@redhat.com> - 1.11.22-2
- added LFS support (#196259)

* Mon Jun 12 2006 Martin Stransky <stransky@redhat.com> - 1.11.22-1
- new upstream

* Tue May 9  2006 Martin Stransky <stransky@redhat.com> - 1.11.21-4
- fix for #189858 - /etc/profile.d/cvs.sh overwrite personal settings
- fix for #190009 - rcs2log uses obsolete sort option

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.11.21-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.11.21-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 21 2005 Martin Stransky <stransky@redhat.com> 1.11.21-3
- fix for #150031 - cvs diff -kk -u fails

* Wed Dec 14 2005 Martin Stransky <stransky@redhat.com> 1.11.21-2
- fix for cvs diff with two -r switches (#18161)
- pam patch (#48937)
- CVS_RSH is set to ssh (#58699)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Martin Stransky <stransky@redhat.com> 1.11.21-1
- new upstream

* Tue Aug 23 2005 Martin Stransky <stransky@redhat.com> 1.11.19-10
- fix for #166366 - CVS temporary file issue

* Thu Jul 21 2005 Martin Stransky <stransky@redhat.com> 1.11.19-9
- add vim-minimal to Requires (#163030)

* Mon Apr 18 2005 Martin Stransky <stransky@redhat.com> 1.11.19-8
- add security fix CAN-2005-0753 (Derek Price)

* Thu Mar 17 2005 Martin Stransky <stransky@redhat.com> 1.11.19-7
- fix NULL pointer comparsion (#63365)

* Mon Mar 14 2005 Martin Stransky <stransky@redhat.com> 1.11.19-6
- add '/' to invalid RCS tag characters (#56162)

* Wed Mar 9  2005 Martin Stransky <stransky@redhat.com> 1.11.19-5
- fix newline issue in log (#64182)

* Mon Mar 7  2005 Martin Stransky <stransky@redhat.com> 1.11.19-4
- remove check of HTTP_PROXY variable (#150434)

* Thu Mar 3  2005 Martin Stransky <stransky@redhat.com> 1.11.19-3
- add xinetd config file (#136929)
- add proxy-support patch (#144297)

* Mon Feb 28 2005 Martin Stransky <stransky@redhat.com> 1.11.19-2
- add opt flags

* Mon Feb 28 2005 Martin Stransky <stransky@redhat.com> 1.11.19-1
- update to 1.11.19

* Mon Feb 14 2005 Adrian Havill <havill@redhat.com>
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 10 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.17-2
- rebuild

* Thu Jun 10 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.17-1
- update to 1.11.17, which includes those last few fixes

* Fri May 28 2004 Nalin Dahyabhai <nalin@redhat.com>
- add security fix for CAN-2004-0416,CAN-2004-0417,CAN-2004-0418 (Stefan Esser)

* Fri May 28 2004 Robert Scheck 1.11.16-0
- update to 1.11.16 (#124239)

* Tue May 18 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.15-6
- rebuild

* Thu May 13 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.15-5
- use revised version of Stefan Esser's patch provided by Derek Robert Price

* Mon May  3 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.15-4
- rebuild

* Mon May  3 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.15-3
- add patch from Stefan Esser to close CAN-2004-0396

* Wed Apr 21 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.15-2
- rebuild

* Wed Apr 21 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.15-1
- update to 1.11.15, fixing CAN-2004-0180 (#120969)

* Tue Mar 23 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.14-1
- update to 1.11.14

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan  7 2004 Nalin Dahyabhai <nalin@redhat.com> 1.11.11-1
- turn kserver, which people shouldn't use any more, back on

* Tue Dec 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.11.11

* Thu Dec 18 2003 Nalin Dahyabhai <nalin@redhat.com> 1.11.10-1
- update to 1.11.10

* Mon Jul 21 2003 Nalin Dahyabhai <nalin@redhat.com> 1.11.5-3
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 30 2003 Nalin Dahyabhai <nalin@redhat.com> 1.11.5-1
- update to 1.11.5
- disable kerberos 4 support

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-9
- rebuild

* Thu Jan 16 2003 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-8
- incorporate fix for double-free in server (CAN-2003-0015)

* Tue Nov 26 2002 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-7
- don't error out in %%install if the info dir file we remove from the build
  root isn't there (depends on the version of texinfo installed, reported by
  Arnd Bergmann)

* Fri Oct  4 2002 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-6
- fixup LDFLAGS to find multilib Kerberos for linking

* Tue Sep 24 2002 Nalin Dahyabhai <nalin@redhat.com>
- incorporate patch to add 't' as a loginfo format specifier, from NetBSD

* Thu Jul 18 2002 Tim Waugh <twaugh@redhat.com 1.11.2-5
- Fix mktemp patch (bug #66669)
- Incorporate patch to fix verifymsg behaviour on empty logs (bug #66022)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.11.2-4
- automated rebuild

* Tue Jun  4 2002 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-3
- incorporate patch to fix incorrect socket descriptor usage (#65225)
- incorporate patches to not choke on empty commit messages and to always
  send them (#66017)
- incorporate patch to not infinitely recurse on assertion failures (#66019)

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May  9 2002 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-1
- update to 1.11.2

* Mon Feb 18 2002 Nalin Dahyabhai <nalin@redhat.com> 1.11.1p1-7
- build with an external zlib
- don't run automake in the %%build phase

* Tue Jan 15 2002 Nalin Dahyabhai <nalin@redhat.com> 1.11.1p1-6
- merge patch to handle timestamping of symlinks in the repository properly,
  from dwmw2 (#23333)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.11.1p1-5
- automated rebuild

* Tue Nov 13 2001 Nalin Dahyabhai <nalin@redhat.com> 1.11.1p1-4
- remove explicit dependency on krb5-libs

* Tue Jul 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.11.1p1-3
- Fix up initial cvs login (#47457)
- Bring back the leading newline at the beginning of commit messages
  "a" is one key less than "O". ;)
- Fix build in the current build system

* Mon Jun 25 2001 Bill Nottingham <notting@redhat.com>
- don't own /usr/share/info/dir

* Fri Jun 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix the files list

* Mon Jun 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.11.1p1
- drop no-longer-necessary patches
- use bundled zlib, because it's apparently not the same as the system zlib
- run the test suite in the build phase
- drop explicit Requires: on perl (RPM will catch the interpreter req)

* Mon Jan 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix cvs-1.11-security.patch, which had CR-LF line terminators (#25090)
- check for and ignore ENOENT errors when attempting to remove symlinks (#25173)

* Mon Jan 08 2001 Preston Brown <pbrown@redhat.com>
- patch from Olaf Kirch <okir@lst.de> to do tmp files safely.

* Tue Oct 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.11

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- always zero errno before calling readdir (#10374)

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new build environment (release 6)

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new build environment (release 5)
- FHS tweaks
- actually gzip the info pages

* Wed May 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- reverse sense of conditional kerberos dependency
- add kerberos IV patch from Ken Raeburn
- switch to using the system's zlib instead of built-in
- default to unstripped binaries

* Tue Apr  4 2000 Bill Nottingham <notting@redhat.com>
- eliminate explicit krb5-configs dependency

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.10.8

* Wed Mar  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- make kerberos support conditional at build-time

* Wed Mar  1 2000 Bill Nottingham <notting@redhat.com>
- integrate kerberos support into main tree

* Mon Feb 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- build with gssapi auth (--with-gssapi, --with-encryption)
- apply patch to update libs to krb5 1.1.1

* Fri Feb 04 2000 Cristian Gafton <gafton@redhat.com>
- fix the damn info pages too while we're at it.
- fix description
- man pages are compressed
- make sure %%post and %%preun work okay

* Sun Jan 9 2000  Jim Kingdon <http://bugzilla.redhat.com/bugzilla>
- update to 1.10.7.

* Wed Jul 14 1999 Jim Kingdon <http://developer.redhat.com>
- add the patch to make 1.10.6 usable
  (http://www.cyclic.com/cvs/dev-known.html).

* Tue Jun  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.6.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.5.

* Tue Feb  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.4.

* Tue Oct 20 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.3.

* Mon Sep 28 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.2.

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- remove trailing characters from rcs2log mktemp args

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.1

* Mon Aug 31 1998 Jeff Johnson <jbj@redhat.com>
- fix race conditions in cvsbug/rcs2log

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.

* Wed Aug 12 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.9.30.

* Mon Jun 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Mon Jun  8 1998 Jeff Johnson <jbj@redhat.com>
- build root
- update to 1.9.28

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 29 1997 Otto Hammersmith <otto@redhat.com>
- added install-info stuff
- added changelog section
