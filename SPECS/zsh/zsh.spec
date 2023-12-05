# this file is encoded in UTF-8  -*- coding: utf-8 -*-

Summary:        Z shell
Name:           zsh
Version:        5.9
Release:        3%{?dist}
License:        MIT AND GPLv2.0 AND GPLv3.0 AND GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Shells
URL:            http://zsh.sourceforge.net/
Source0:        https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.xz
Source1:        zprofile.rhs
Source2:        zshrc
Patch0:         0001-Skipping-test-if-ran-as-superuser.patch
Patch1:         fix-script-shebangs.patch
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  elfutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  libcap-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  sed
BuildRequires:  tar
BuildRequires:  texinfo
Requires(post): /bin/grep
Requires(postun): /bin/grep
Requires(postun): coreutils
Provides:       /bin/zsh

%description
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

%package html
Summary:        Zsh shell manual in html format
Group:          System Environment/Shells

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

%build
# make loading of module's dependencies work again (#1277996)
export LIBLDFLAGS='-z lazy'

%configure --enable-etcdir=%{_sysconfdir} --with-tcsetpgrp --enable-maildir-support

make all html

%check
rm -f Test/C02cond.ztst
make check

%install

%makeinstall install.info \
  fndir=%{buildroot}%{_datadir}/%{name}/%{version}/functions \
  sitefndir=%{buildroot}%{_datadir}/%{name}/site-functions \
  scriptdir=%{buildroot}%{_datadir}/%{name}/%{version}/scripts \
  sitescriptdir=%{buildroot}%{_datadir}/%{name}/scripts \
  runhelpdir=%{buildroot}%{_datadir}/%{name}/%{version}/help

rm -f %{buildroot}%{_bindir}/zsh-%{version}
rm -f %{buildroot}%{_infodir}/dir

mkdir -p %{buildroot}%{_sysconfdir}
for i in %{SOURCE1}; do
    install -m 644 $i %{buildroot}%{_sysconfdir}/"$(basename $i .rhs)"
done

mkdir -p %{buildroot}%{_sysconfdir}/skel
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/skel/.zshrc

sed -i "s!%{buildroot}%{_datadir}/%{name}/%{version}/help!%{_datadir}/%{name}/%{version}/help!" \
    %{buildroot}%{_datadir}/zsh/%{version}/functions/{run-help,_run-help}


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

%preun
%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -i '\!^%{_bindir}/%{name}$!d' %{_sysconfdir}/shells
  sed -i '\!^/bin/%{name}$!d' %{_sysconfdir}/shells
fi

%files
%defattr(-,root,root)
%license LICENCE
%doc README Etc/BUGS Etc/CONTRIBUTORS Etc/FAQ FEATURES MACHINES
%doc NEWS Etc/zsh-development-guide Etc/completion-style-guide
%attr(755,root,root) %{_bindir}/zsh
%{_mandir}/*/*
%{_infodir}/*
%{_datadir}/zsh
%{_libdir}/zsh
%config(noreplace) %{_sysconfdir}/skel/.z*
%config(noreplace) %{_sysconfdir}/z*

%files html
%defattr(-,root,root)
%doc Doc/*.html

%changelog
* Thu Nov 30 2023 Dan Streetman <ddstreet@ieee.org> - 5.9-3
- Remove umask 027

* Thu Jun 16 2022 Olivia Crain <oliviacrain@microsoft.com> - 5.9-2
- Fix package install by patching out bad shebangs in included scripts

* Tue May 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.9-1
- Update to v5.9 to address CVE-2021-45444

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.8-5
- Removing the explicit %%clean stage.

* Tue Nov 10 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.8-4
- Adding a patch to skip globbing test if ran as root.
- Removing redundant 'sed' and 'chmod' commands in %%install.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 5.8-3
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 5.8-2
- Renaming linux-api-headers to kernel-headers

* Fri Apr 10 2020 Jon Slobodzian <joslobo@microsoft.com> - 5.8-1
- Updated to latest version to fix CVE CVE-2019-20044.
- Fixed Source0 download link
- Verified license.

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 5.6.1-3
- Remove coreutils and only use toybox in requires.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 5.6.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> - 5.6.1-1
- Upgrading to latest

* Mon Mar 19 2018 Xiaolin Li <xiaolinl@vmware.com> - 5.3.1-5
- Fix CVE-2018-7548

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 5.3.1-4
- Requires coreutils or toybox and /bin/grep

* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> - 5.3.1-3
- Clean up check

* Wed Aug 02 2017 Chang Lee <changlee@vmware.com> - 5.3.1-2
- Skip a test case that is not supported from photon OS chroot

* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.3.1-1
- Updated to version 5.3.1.

* Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> - 5.2-1
- Initial zsh for photon os
