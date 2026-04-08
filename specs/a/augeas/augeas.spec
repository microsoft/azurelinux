# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           augeas
Version:        1.14.2
Summary:        A library for changing configuration files
License:        LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND (GPL-3.0-or-later WITH Bison-exception-2.2) AND Kazlib AND GPL-2.0-or-later AND BSD-2-Clause AND LicenseRef-Fedora-Public-Domain

%global forgeurl https://github.com/hercules-team/%%{name}
%global commit af2aa88ab37fc48167d8c5e43b1770a4ba2ff403
%forgemeta

Release:        0.6%{?dist}
URL:            %{forgeurl}
Source0:        %{forgesource}

# The problem with packaging from the upstream git repo is that we
# need to provide our own gnulib submodule.  I created this by doing:
# git archive --format=tar --prefix=.gnulib/ HEAD | gzip -9 > gnulib-2f7479a16a.tar.gz
Source1:        gnulib-2f7479a16a.tar.gz

# Upstream Augeas is missing several important fixes which affect
# Fedora.  For this reason I have taken the regrettable but hopefully
# temporary step of forking upstream with some extra patches, here:
# https://github.com/rwmjones/augeas/tree/fedora-43
Patch:          0001-lenses-fstab.aug-Tighten-parsing-of-the-vfstype-fiel.patch
Patch:          0002-lenses-fstab.aug-Allow-individual-mount-options-to-b.patch

Provides:       bundled(gnulib)

BuildRequires:  autoconf, automake, libtool
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  readline-devel
BuildRequires:  libselinux-devel
BuildRequires:  libxml2-devel
BuildRequires:  bash-completion
%if 0%{?fedora} > 40 || 0%{?rhel} > 10
BuildRequires:  bash-completion-devel
%endif

Requires:       %{name}-libs = %{version}-%{release}

%description
A library for programmatically editing configuration files. Augeas parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.

The transformation works very hard to preserve comments and formatting
details. It is controlled by ``lens'' definitions that describe the file
format and the transformation into a tree.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        libs
Summary:        Libraries for %{name}

%description    libs
The libraries for %{name}.

Augeas is a library for programmatically editing configuration files. It parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.

%package        static
Summary:        Static libraries for %{name}
Requires:       %{name}-devel = %{version}-%{release}

%description    static
The %{name}-static package contains static libraries needed to produce
static builds using %{name}.


%package bash-completion
Summary:       Bash tab-completion for %{name}
BuildArch:     noarch
Requires:      bash-completion >= 2.0
# Don't use _isa here because it's a noarch package.  This dependency
# is just to ensure that the subpackage is updated along with augeas.
Requires:      %{name} = %{version}-%{release}


%description bash-completion
Install this package if you want intelligent bash tab-completion
for %{name}.


%prep
%forgeautosetup -p1
zcat %{SOURCE1} | tar xf -

# Copied from upstream ./bootstrap:
modules='argz fnmatch getline getopt-gnu gitlog-to-changelog
canonicalize-lgpl isblank locale mkstemp regex safe-alloc selinux-h
stpcpy stpncpy strchrnul strndup sys_wait vasprintf'
.gnulib/gnulib-tool             \
  --lgpl=2                      \
  --with-tests                  \
  --m4-base=gnulib/m4           \
  --source-base=gnulib/lib      \
  --tests-base=gnulib/tests     \
  --aux-dir=build/ac-aux        \
  --libtool                     \
  --quiet                       \
  --import $modules

autoreconf -fiv


%build
%configure \
%ifarch riscv64
    --disable-gnulib-tests \
%endif
    --enable-static
# Disable _smp_mflags because parallel tests fail with the git version
# because it tries to run lex and yacc in parallel even though lex
# depends on parser.h from yacc.
# https://github.com/hercules-team/augeas/issues/572
#make %%{?_smp_mflags}
make


%check
# Disable test-preserve.sh SELinux testing. This fails when run under mock due
# to differing SELinux labelling.
export SKIP_TEST_PRESERVE_SELINUX=1

# Tests disabled because gnulib tests fail see:
# https://bugzilla.redhat.com/show_bug.cgi?id=1674672
make %{?_smp_mflags} check || {
  echo '===== tests/test-suite.log ====='
  cat tests/test-suite.log
  exit 1
}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# The tests/ subdirectory contains lenses used only for testing, and
# so it shouldn't be packaged.
rm -r $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/dist/tests

# In 1.9.0, the example /usr/bin/dump gets installed inadvertently
rm -f $RPM_BUILD_ROOT/usr/bin/dump

%ldconfig_scriptlets libs

%files
%{_bindir}/augmatch
%{_bindir}/augparse
%{_bindir}/augprint
%{_bindir}/augtool
%{_bindir}/fadot
%doc %{_mandir}/man1/*
%{_datadir}/vim/vimfiles/syntax/augeas.vim
%{_datadir}/vim/vimfiles/ftdetect/augeas.vim

%files libs
# _datadir/augeas and _datadir/augeas/lenses are owned
# by filesystem.
%{_datadir}/augeas/lenses/dist
%{_libdir}/*.so.*
%doc AUTHORS COPYING NEWS

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/augeas.pc

%files static
%{_libdir}/libaugeas.a
%{_libdir}/libfa.a

%files bash-completion
%if 0%{?fedora} > 40 || 0%{?rhel} > 10
%dir %{bash_completions_dir}
%{bash_completions_dir}/augmatch
%{bash_completions_dir}/augprint
%{bash_completions_dir}/augtool
%else
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/augmatch
%{_datadir}/bash-completion/completions/augprint
%{_datadir}/bash-completion/completions/augtool
%endif

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 15 2025 Richard W.M. Jones <rjones@redhat.com> - 1.14.2-0.5
- Rebase our branch on top of Augeas
- Use patches to make it clearer what we are adding on top of upstream.

* Mon Mar 24 2025 Alexander Bokovoy <abokovoy@redhat.com> - 1.14.2-0.4
- rhbz#235444: CVE-2025-2588

* Mon Feb 24 2025 Richard W.M. Jones <rjones@redhat.com> - 1.14.2-0.3
- Move to fork of Augeas which contains a small number of PRs:
- lenses/tmpfiles.aug: Permit '$' character in /usr/lib/tmpfiles.d/*.conf
- lenses/multipath.aug: Support all possible values for find_multipaths
- lenses/systemd.aug: Allow "+"(fullprivileges) command flag

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 03 2024 Richard W.M. Jones <rjones@redhat.com> - 1.14.2-0
- Move to latest upstream
- Use forge macros
- Run autoreconf unconditionally
- Fix bash-completion-devel test
- Fix chrony.conf option leapseclist unsupported (RHBZ#2309439)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Richard W.M. Jones <rjones@redhat.com> - 1.14.1-1
- New upstream version 1.14.1
- Use github tarballs again.
- New binary augprint.
- New bash-completions subpackage.

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Richard W.M. Jones <rjones@redhat.com> - 1.13.0-1
- New upstream version 1.13.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-0.2.git18558bb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 06 2021 Richard W.M. Jones <rjones@redhat.com> - 1.12.1-0.1
- Package up a git pre-release of 1.12.1 or 1.13.0.

* Thu Apr 15 2021 Richard W.M. Jones <rjones@redhat.com> - 1.12.0-6
- Add upstream patch to parse chrony configuration.
- Use %%autosetup.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 15 2019 Richard W.M. Jones <rjones@redhat.com> - 1.12.0-1
- New upstream release 1.12.0.

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.11.0-4
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 26 2018 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-2
- Augeas uses gnulib, add the correct 'Provides' line.

* Tue Aug 28 2018 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-1
- New upstream version 1.11.0.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 David Lutterkort <lutter@watzmann.net> - 1.10.1-1
- New upstream version 1.10.1

* Fri Jan 26 2018 Richard W.M. Jones <rjones@redhat.com> - 1.10.0-1
- New upstream version 1.10.0 (RHBZ#1538846).
- Remove upstream patch.
- New tool ‘augmatch’.

* Tue Nov 21 2017 David Lutterkort <lutter@watzmann.net> - 1.9.0
- New upstream version 1.9.0 (RHBZ#1482713)
- Add -static subpackage (RHBZ#1405600)

* Thu Aug 24 2017 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-1
- New upstream version 1.8.1.
- Fixes CVE-2017-7555 (RHBZ#1482340).

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Dominic Cleal <dominic@cleal.org> - 1.8.0-1
- Update to 1.8.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.7.0-3
- Rebuild for readline 7.x

* Sat Nov 12 2016 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-2
- riscv64: Disable gnulib tests on riscv64 architecture.

* Wed Nov 09 2016 Dominic Cleal <dominic@cleal.org> - 1.7.0-1
- Update to 1.7.0

* Mon Aug 08 2016 Dominic Cleal <dominic@cleal.org> - 1.6.0-1
- Update to 1.6.0

* Thu May 12 2016 Dominic Cleal <dominic@cleal.org> - 1.5.0-1
- Update to 1.5.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Dominic Cleal <dcleal@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Sat Nov 08 2014 Dominic Cleal <dcleal@redhat.com> - 1.3.0-1
- Update to 1.3.0; remove all patches

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Dominic Cleal <dcleal@redhat.com> - 1.2.0-2
- Add patch for Krb5, parse braces in values (RHBZ#1079444)

* Wed Feb 12 2014 Dominic Cleal <dcleal@redhat.com> - 1.2.0-1
- Update to 1.2.0, add check section
- Update source URL to download.augeas.net (RHBZ#996032)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 David Lutterkort <lutter@redhat.com> - 1.1.0-1
- Update to 1.1.0; remove all patches

* Tue Jun 18 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-4
- Fix /etc/sysconfig/network (RHBZ#904222).

* Wed Jun  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-3
- Don't package lenses in tests/ subdirectory.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 David Lutterkort <lutter@redhat.com> - 1.0.0-1
- New version; remove all patches

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 David Lutterkort <lutter@redhat.com> - 0.10.0-3
- Add patches for bugs 247 and 248 (JSON lens)

* Sat Dec  3 2011 Richard W.M. Jones <rjones@redhat.com> - 0.10.0-2
- Add patch to resolve missing libxml2 requirement in augeas.pc.

* Fri Dec  2 2011 David Lutterkort <lutter@redhat.com> - 0.10.0-1
- New version

* Mon Jul 25 2011 David Lutterkort <lutter@redhat.com> - 0.9.0-1
- New version; removed patch pathx-whitespace-ea010d8

* Tue May  3 2011 David Lutterkort <lutter@redhat.com> - 0.8.1-2
- Add patch pathx-whitespace-ea010d8.patch to fix BZ 700608

* Fri Apr 15 2011 David Lutterkort <lutter@redhat.com> - 0.8.1-1
- New version

* Wed Feb 23 2011 David Lutterkort <lutter@redhat.com> - 0.8.0-1
- New version

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Matthew Booth <mbooth@redhat.com> - 0.7.4-1
- Update to version 0.7.4

* Thu Nov 18 2010 Richard W.M. Jones <rjones@redhat.com> - 0.7.3-2
- Upstream patch proposed to fix GCC optimization bug (RHBZ#651992).

* Fri Aug  6 2010 David Lutterkort <lutter@redhat.com> - 0.7.3-1
- Remove upstream patches

* Tue Jun 29 2010 David Lutterkort <lutter@redhat.com> - 0.7.2-2
- Patches based on upstream fix for BZ 600141

* Tue Jun 22 2010 David Lutterkort <lutter@redhat.com> - 0.7.2-1
- Fix ownership of /usr/share/augeas. BZ 569393

* Wed Apr 21 2010 David Lutterkort <lutter@redhat.com> - 0.7.1-1
- New version

* Thu Jan 14 2010 David Lutterkort <lutter@redhat.com> - 0.7.0-1
- Remove patch vim-ftdetect-syntax.patch. It's upstream

* Tue Dec 15 2009 David Lutterkort <lutter@redhat.com> - 0.6.0-2
- Fix ftdetect file for vim

* Mon Nov 30 2009 David Lutterkort <lutter@redhat.com> - 0.6.0-1
- Install vim syntax files

* Mon Sep 14 2009 David Lutterkort <lutter@redhat.com> - 0.5.3-1
- Remove separate xorg.aug, included in upstream source

* Tue Aug 25 2009 Matthew Booth <mbooth@redhat.com> - 0.5.2-3
- Include new xorg lens from upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 David Lutterkort <lutter@redhat.com> - 0.5.2-1
- New version

* Fri Jun  5 2009 David Lutterkort <lutter@redhat.com> - 0.5.1-1
- Install fadot

* Fri Mar 27 2009 David Lutterkort <lutter@redhat.com> - 0.5.0-2
- fadot isn't being installed just yet

* Tue Mar 24 2009 David Lutterkort <lutter@redhat.com> - 0.5.0-1
- New program /usr/bin/fadot

* Mon Mar  9 2009 David Lutterkort <lutter@redhat.com> - 0.4.2-1
- New version

* Fri Feb 27 2009 David Lutterkort <lutter@redhat.com> - 0.4.1-1
- New version

* Fri Feb  6 2009 David Lutterkort <lutter@redhat.com> - 0.4.0-1
- New version

* Mon Jan 26 2009 David Lutterkort <lutter@redhat.com> - 0.3.6-1
- New version

* Tue Dec 23 2008 David Lutterkort <lutter@redhat.com> - 0.3.5-1
- New version

* Mon Feb 25 2008 David Lutterkort <dlutter@redhat.com> - 0.0.4-1
- Initial specfile
