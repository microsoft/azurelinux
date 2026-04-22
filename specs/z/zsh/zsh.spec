# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Powerful interactive shell
Name: zsh
Version: 5.9
Release: 19%{?dist}
License: MIT-Modern-Variant AND ISC AND GPL-2.0-only
URL: http://zsh.sourceforge.net/
Source0: https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
Source1: zlogin.rhs
Source2: zlogout.rhs
Source3: zprofile.rhs
Source4: zshrc.rhs
Source5: zshenv.rhs
Source6: dotzshrc
Source7: dotzprofile

# do not use egrep in tests to make them pass again
Patch1: 0001-zsh-5.9-do-not-use-egrep-in-tests.patch
# Upstream commit ab4d62eb975a4c4c51dd35822665050e2ddc6918
Patch2: 0002-zsh-Use-int-main-in-test-c-codes.patch
# upstream commit a84fdd7c8f77935ecce99ff2b0bdba738821ed79
Patch3: 0003-zsh-fix-module-loading-problem-with-full-RELRO.patch
# upstream commit 1b421e4978440234fb73117c8505dad1ccc68d46
Patch4: 0004-zsh-enable-PCRE-locale-switching.patch
# upstream commit b62e911341c8ec7446378b477c47da4256053dc0 and 10bdbd8b5b0b43445aff23dcd412f25cf6aa328a
Patch5: 0005-zsh-port-to-pcre2.patch
# upstream commit ecd3f9c9506c7720dc6c0833dc5d5eb00e4459c4
Patch6: 0006-zsh-support-texinfo-7.0.patch
# upstream commit 4c89849c98172c951a9def3690e8647dae76308f
Patch7: 0007-zsh-configure-c99.patch
# upstream commit d3edf318306e37d2d96c4e4ea442d10207722e94
Patch8: 0008-zsh-deletefilelist-segfault.patch
# upstream commit b70b241cc5ca88cc129ff9ba14f8af2e889b90e6
Patch9: 0009-zsh-support-dnf5.patch
# upstream commit 071e325c826a89b792056c3faf0c400b8c0c5738
Patch10: 0010-zsh-fix-dnf5-completion-with-rpm-files.patch

BuildRequires: autoconf
BuildRequires: coreutils
BuildRequires: gawk
BuildRequires: gcc
BuildRequires: gdbm-devel
BuildRequires: glibc-langpack-ja
BuildRequires: libcap-devel
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: pcre2-devel
BuildRequires: sed
BuildRequires: texi2html
BuildRequires: texinfo
Requires(post): grep
Requires(postun): coreutils grep

# the hostname package is not available on RHEL-6
%if 12 < 0%{?fedora} || 6 < 0%{?rhel}
BuildRequires: hostname
%else
# /bin and /usr/bin are separate directories on RHEL-6
%define _bindir /bin
%endif

Provides: /bin/zsh

%description
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

%package html
Summary: Zsh shell manual in html format
BuildArch:	noarch

%description html
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

This package contains the Zsh manual in html format.

%prep
%autosetup -p1
autoreconf -fiv

# enable parallel build
sed -e 's|^\.NOTPARALLEL|#.NOTPARALLEL|' -i 'Config/defs.mk.in'

%build
# make build of run-time loadable modules work again (#1535422)
%undefine _strict_symbol_defs_build

# avoid build failure in case we have working ypcat (#1687574)
export zsh_cv_sys_nis='no'

%configure \
    --enable-etcdir=%{_sysconfdir} \
    --with-tcsetpgrp \
    --enable-maildir-support \
    --enable-pcre

# prevent the build from failing while running in parallel
make -C Src headers
make -C Src -f Makemod zsh{path,xmod}s.h version.h

%make_build all html

%check
# avoid unnecessary failure of the test-suite in case ${RPS1} is set
unset RPS1

# run the test-suite
make check

%install
%make_install install.info \
  fndir=%{_datadir}/%{name}/%{version}/functions \
  sitefndir=%{_datadir}/%{name}/site-functions \
  scriptdir=%{_datadir}/%{name}/%{version}/scripts \
  sitescriptdir=%{_datadir}/%{name}/scripts \
  runhelpdir=%{_datadir}/%{name}/%{version}/help

rm -f $RPM_BUILD_ROOT%{_bindir}/zsh-%{version}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
for i in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5}; do
    install -m 644 $i $RPM_BUILD_ROOT%{_sysconfdir}/"$(basename $i .rhs)"
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/skel
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.zshrc
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.zprofile

# This is just here to shut up rpmlint, and is very annoying.
# Note that we can't chmod everything as then rpmlint will complain about
# those without a she-bang line.
for i in checkmail harden run-help test-repo-git-rebase-{apply,merge} zcalc zkbd; do
    sed -i -e 's!/usr/local/bin/zsh!%{_bindir}/zsh!' \
    $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/$i
    chmod +x $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/$i
done


%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/%{name}" > %{_sysconfdir}/shells
    echo "/bin/%{name}" >> %{_sysconfdir}/shells
  else
    grep -q "^%{_bindir}/%{name}$" %{_sysconfdir}/shells || echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
    grep -q "^/bin/%{name}$" %{_sysconfdir}/shells || echo "/bin/%{name}" >> %{_sysconfdir}/shells
  fi
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -i '\!^%{_bindir}/%{name}$!d' %{_sysconfdir}/shells
  sed -i '\!^/bin/%{name}$!d' %{_sysconfdir}/shells
fi


%files
%doc README LICENCE Etc/BUGS Etc/CONTRIBUTORS Etc/FAQ FEATURES MACHINES
%doc NEWS Etc/zsh-development-guide Etc/completion-style-guide
%attr(755,root,root) %{_bindir}/zsh
%{_mandir}/*/*
%{_infodir}/*
%{_datadir}/zsh
%{_libdir}/zsh
%config(noreplace) %{_sysconfdir}/skel/.z*
%config(noreplace) %{_sysconfdir}/z*

%files html
%doc Doc/*.html

%changelog
* Mon Sep 29 2025 Christoph Erhardt <fedora@sicherha.de> - 5.9-18
- Add completion support for dnf5

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 13 2024 Lukáš Zaoral <lzaoral@redhat.com> - 5.9-14
- fix zlogout when ncurses is not installed (rhbz#2279741)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Lukáš Zaoral <lzaoral@redhat.com> - 5.9-12
- fix segfault in delerefilelist (rhbz#2245462)

* Fri Dec  8 2023 Florian Weimer <fweimer@redhat.com> - 5.9-11
- Fix C compatibility issue in the configure script

* Tue Nov 21 2023 Lukáš Zaoral <lzaoral@redhat.com> - 5.9-10
- fix FTBFS caused by texinfo 7.1
- fix build of the PCRE module

* Mon Aug 21 2023 Lukáš Zaoral <lzaoral@redhat.com> - 5.9-9
- port to PCRE 2 (rhbz#1938979)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Lukáš Zaoral <lzaoral@redhat.com> - 5.9-7
- Make zsh/{tcp,zftp} compatible with full RELRO (rhbz#2212160)

* Wed May 17 2023 David Cantrell <dcantrell@redhat.com> - 5.9-6
- Update the License tag to use SPDX identifiers

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Timm Bäder <tbaeder@redhat.com> - 5.9-4
- use 'int main()' in test C-codes in configure

* Mon Jan 09 2023 Kamil Dudka <kdudka@redhat.com> - 5.9-3
- do not use egrep in tests to make them pass again

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun May 15 2022 Kamil Dudka <kdudka@redhat.com> - 5.9-1
- update to latest upstream release

* Sun Feb 13 2022 Kamil Dudka <kdudka@redhat.com> - 5.8.1-1
- update to latest upstream release (fixes CVE-2021-45444)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Kamil Dudka <kdudka@redhat.com> - 5.8-8
- prepend ~/.local/bin and ~/bin to $PATH for newly created users (#1900809)

* Thu Nov 25 2021 Debarshi Ray <rishi@fedoraproject.org> - 5.8-7
- Overwrite PROMPT only if it's set to the built-in default (#2026749)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 25 2021 Kamil Dudka <kdudka@redhat.com> - 5.8-5
- complete file arguments after rpmbuild -r/-b/-t

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 5.8-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Feb 24 2020 Kamil Dudka <kdudka@redhat.com> - 5.8-1
- update to latest upstream release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Kamil Dudka <kdudka@redhat.com> - 5.7.1-4
- make failed searches of history in Zle robust (#1722703)

* Tue Mar 12 2019 Kamil Dudka <kdudka@redhat.com> - 5.7.1-3
- avoid build failure in case we have working ypcat (#1687574)

* Fri Mar  8 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 5.7.1-2
- Remove obsolete requirements for %%post/%%preun scriptlets

* Mon Feb 04 2019 Kamil Dudka <kdudka@redhat.com> - 5.7.1-1
- update to latest upstream release

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Jason L Tibbitts III <tibbs@math.uh.edu> - 5.7-1
- Update to latest upstream release.

* Fri Nov 30 2018 Kamil Dudka <kdudka@redhat.com> - 5.6.2-3
- return non-zero exit status on nested parse error (#1654989)

* Mon Nov 12 2018 Kamil Dudka <kdudka@redhat.com> - 5.6.2-2
- fix programming mistakes detected by static analysis

* Fri Sep 14 2018 Kamil Dudka <kdudka@redhat.com> - 5.6.2-1
- update to latest upstream release

* Mon Sep 10 2018 Kamil Dudka <kdudka@redhat.com> - 5.6.1-1
- update to latest upstream release

* Tue Sep 04 2018 Kamil Dudka <kdudka@redhat.com> - 5.6-1
- update to latest upstream release (fixes CVE-2018-0502 and CVE-2018-13259)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 17 2018 Kamil Dudka <kdudka@redhat.com> - 5.5.1-1
- update to latest upstream release

* Mon Apr 09 2018 Kamil Dudka <kdudka@redhat.com> - 5.5-1
- update to latest upstream release, which fixes the following vulnerabilities:
    CVE-2018-1100 - stack-based buffer overflow in utils.c:checkmailpath()
    CVE-2018-1083 - stack-based buffer overflow in compctl.c:gen_matches_files()
    CVE-2018-1071 - stack-based buffer overflow in exec.c:hashcmd()

* Tue Mar 06 2018 Kamil Dudka <kdudka@redhat.com> - 5.4.2-7
- avoid crash when copying empty hash table (CVE-2018-7549)
- avoid NULL dereference when using ${(PA)...} on an empty array (CVE-2018-7548)

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 5.4.2-6
- add explicit BR for the gcc compiler

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Kamil Dudka <kdudka@redhat.com> - 5.4.2-4
- make build of run-time loadable modules work again (#1535422)

* Tue Jan 16 2018 Kamil Dudka <kdudka@redhat.com> - 5.4.2-3
- rebuild against latest gdbm-devel (#1533176)

* Wed Oct 04 2017 Kamil Dudka <kdudka@redhat.com> - 5.4.2-2
- make the call depth limit configurable by $FUNCNEST (#1441092)

* Mon Aug 28 2017 Kamil Dudka <kdudka@redhat.com> - 5.4.2-1
- update to latest upstream release

* Wed Aug 09 2017 Kamil Dudka <kdudka@redhat.com> - 5.4.1-1
- update to latest upstream release

* Tue Aug 01 2017 Kamil Dudka <kdudka@redhat.com> - 5.3.1-12
- use %%make_install instead of %%makeinstall, which is deprecated
- modernize spec file (Group tag, %%clean, %%defattr)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Kamil Dudka <kdudka@redhat.com> - 5.3.1-10
- enable parallel build

* Wed Jun 14 2017 Kamil Dudka <kdudka@redhat.com> - 5.3.1-9
- fix unsafe use of a static buffer in history isearch (#1461483)

* Thu Jun 08 2017 Kamil Dudka <kdudka@redhat.com> - 5.3.1-8
- make the zsh-html subpackage noarch (#1459657)

* Thu May 25 2017 Kamil Dudka <kdudka@redhat.com> - 5.3.1-7
- drop unmaintained and undocumented zshprompt.pl script

* Wed May 17 2017 Kamil Dudka <kdudka@redhat.com> - 5.3.1-6
- drop workaround for broken terminals over serial port (#56353)

* Thu May 11 2017 Kamil Dudka <kdudka@redhat.com> - 5.3.1-5
- compile with -fconserve-stack to prevent stack overflow (#1441092)

* Fri Mar 31 2017 Jason L Tibbitts III <tibbs@math.uh.edu> - 5.3.1-4
- Add build deps on gdbm-devel and pcre-devel.  Pass --enable-pcre to
  configure.  These should ensure that the pcre and gdbm modules are built.
  (#1438009)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Kamil Dudka <kdudka@redhat.com> - 5.3.1-2
- do not require the hostname package when being built on RHEL-6

* Wed Dec 21 2016 Kamil Dudka <kdudka@redhat.com> - 5.3.1-1
- Update to latest upstream release: Zsh 5.3.1

* Wed Dec 14 2016 Kamil Dudka <kdudka@redhat.com> - 5.3-2
- drop zsh-4.3.6-8bit-prompts.patch which was superseeded by an upstream patch
  (see http://www.zsh.org/mla/users/2007/msg00468.html for details)
- drop undocumented zsh-test-C02-dev_fd-mock.patch

* Tue Dec 13 2016 Kamil Dudka <kdudka@redhat.com> - 5.3-1
- apply patches automatically to ease maintenance
- Update to latest upstream release: Zsh 5.3

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Kamil Dudka <kdudka@redhat.com> - 5.2-4
- prevent zsh from crashing when printing the "out of memory" message (#1300958)

* Thu Jan 07 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 5.2-3
- Add patch to fix VCS_INFO_nbvsformats bug.

* Fri Dec 25 2015 Adrien Vergé <adrienverge@gmail.com> - 5.2-2
- update zsh completion script for dnf to the latest upstream version

* Thu Dec 03 2015 Kamil Dudka <kdudka@redhat.com> - 5.2-1
- Update to latest upstream release: Zsh 5.2

* Thu Nov 05 2015 Kamil Dudka <kdudka@redhat.com> - 5.1.1-3
- make loading of module's dependencies work again (#1277996)

* Thu Oct 08 2015 Kamil Dudka <kdudka@redhat.com> - 5.1.1-2
- fix crash in ksh mode with -n and $HOME (#1269883)

* Mon Sep 14 2015 Kamil Dudka <kdudka@redhat.com> - 5.1.1-1
- Update to latest upstream release: Zsh 5.1.1

* Mon Aug 31 2015 Kamil Dudka <kdudka@redhat.com> - 5.1-1
- Update to latest upstream release: Zsh 5.1
- remove outdated workarounds in %%check

* Thu Jul 30 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.8-6
- fix handling of command substitution in math context

* Wed Jul 22 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.8-5
- prevent infinite recursion in ihungetc() (#1245712)

* Tue Jul 07 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.8-4
- backport completion for dnf (#1239337)

* Thu Jul 02 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.8-3
- backport completion-related upstream fixes (#1238544)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.8-1
- Update to latest upstream release: Zsh 5.0.8

* Fri May 22 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.7-8
- fix SIGSEGV of the syntax check in ksh emulation mode (#1222867)

* Mon Apr 20 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.7-7
- fix SIGSEGV when handling heredocs and keyboard interrupt (#972624)
- queue signals when manipulating global state to avoid deadlock

* Sun Jan 25 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.7-6
- use correct allocation function in the new 'cd' code (#1183238)

* Fri Jan 23 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.7-5
- suppress a warning about closing an already closed file descriptor (#1184002)
- improve handling of NULL in the 'cd' built-in (#1183238)

* Wed Nov 19 2014 Kamil Dudka <kdudka@redhat.com> - 5.0.7-4
- update documentation of POSIX_JOBS in the zshoptions.1 man page (#1162198)

* Tue Nov 18 2014 Kamil Dudka <kdudka@redhat.com> - 5.0.7-3
- replace an incorrect comment in /etc/zshenv (#1164313)

* Mon Nov 10 2014 Kamil Dudka <kdudka@redhat.com> - 5.0.7-2
- make the wait built-in work for already exited processes (#1162198)

* Wed Oct 08 2014 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.7-1
- Update to latest upstream release: Zsh 5.0.7

* Thu Aug 28 2014 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.6-1
- Update to latest upstream release: Zsh 5.0.6

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.5-7
- apply upstream patch which fixes CPU load issue (RHBZ#1120424)

* Wed Jul 09 2014 Adam Jackson <ajax@redhat.com> 5.0.5-6
- Fix missing 'fi' in %%post

* Thu Jul 03 2014 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.5-5
- improve handling of /etc/shells

* Wed Jul 02 2014 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.5-4
- fix FTBFS issue (RHBZ#1106713)
- remove individual _bindir setting; install to /usr/bin/ (RHBZ#1034060)
- require info package instead of /sbin/install-info binary

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.5-1
- Update to latest upstream release: Zsh 5.0.5

* Thu Jan 16 2014 James Antill <james@fedoraproject.org> - 5.0.2-8
- Remove unneeded build require on tetex.

* Sat Oct 26 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.2-7
- Require hostname package instead of /bin/hostname

* Tue Oct 22 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.2-6
- remove systemd completion, it delivers it's own now (RHBZ#1022039)

* Thu Aug 01 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.2-5
- update systemd completion (adds machinectl command)

* Tue Jun 25 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.2-4
- up-to-date systemd completion (#949003)
- apply patch for building for aarch64 (#926864)

* Mon Apr 15 2013 James Antill <james@fedoraproject.org> - 5.0.2-3
- Fix the changelog dates.
- Fix the texi itemx bug.
- Resolves: bug#927863

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 08 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.2-1
- Update to new upstream version: Zsh 5.0.2

* Wed Nov 21 2012 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.0-1
- Update to new upstream version: Zsh 5.0.0

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 04 2012 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.17-1
- Update to new upstream version: Zsh 4.3.17

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.15-1
- Update to new upstream version: Zsh 4.3.15

* Sat Dec 17 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.14-2
- change the License field to MIT (RHBZ#768548)

* Sat Dec 10 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.14-1
- Update to new upstream version: Zsh 4.3.14

* Sat Dec 03 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.13-1
- Update to new upstream version: Zsh 4.3.13

* Sat Aug 13 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.12-1
- Update to new upstream version: Zsh 4.3.12

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Christopher Ailon <caillon@redhat.com> - 4.3.11-1
- Rebase to upstream version 4.3.11

* Tue Dec 7 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 4.3.10-6
- Rebuild for FTBFS https://bugzilla.redhat.com/show_bug.cgi?id=631197
- Remove deprecated PreReq, the packages aren't needed at runtime and they're
  already in Requires(post,preun,etc): lines.

* Mon Mar 22 2010 James Antill <james@fedoraproject.org> - 4.3.10-5
- Add pathmunge to our /etc/zshrc, for profile.d compat.
- Resolves: bug#548960

* Fri Aug  7 2009 James Antill <james@fedoraproject.org> - 4.3.10-4
- Allow --excludedocs command to work!
- Resolves: bug#515986

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 James Antill <james@fedoraproject.org> - 4.3.10-1
- Import new upstream 4.3.10

* Wed Jun 10 2009 Karsten Hopp <karsten@redhat.com> 4.3.9-4.1
- skip D02glob test on s390, too

* Mon Mar  2 2009 James Antill <james@fedoraproject.org> - 4.3.9-4
- Remove D02glob testcase on ppc/ppc64, and hope noone cares

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
