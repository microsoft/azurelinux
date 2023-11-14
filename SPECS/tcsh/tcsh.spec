# Got the intial spec from Fedora and modified it
Summary:        An enhanced version of csh, the C shell
Name:           tcsh
Version:        6.22.03
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Shells
URL:            https://www.tcsh.org/
Source0:        https://astron.com/pub/%{name}/old/%{name}-%{version}.tar.gz
BuildRequires:  ncurses-devel
BuildRequires:  libxcrypt-devel
%if %{with_check}
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif
Requires:       ncurses
Requires(post): /bin/grep
Requires(postun): /bin/grep
Requires(postun): coreutils

Provides:       csh = %{version}
Provides:       /bin/csh
Provides:       /bin/tcsh

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell.  Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.

%prep
%autosetup

%build
sed -i -e 's|\$\*|#&|' -e 's|fR/g|&m|' tcsh.man2html &&

%configure --prefix=%{_prefix}
make %{?_smp_mflags} all

%install
mkdir -p %{buildroot}%{_mandir}/man1 %{buildroot}%{_bindir}
install -p -m 755 tcsh %{buildroot}%{_bindir}/tcsh
install -p -m 644 tcsh.man %{buildroot}%{_mandir}/man1/tcsh.1
ln -sf tcsh %{buildroot}%{_bindir}/csh
ln -sf tcsh.1 %{buildroot}%{_mandir}/man1/csh.1

while read lang language ; do
  dest=%{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  if test -f nls/$language.cat ; then
    mkdir -p $dest
    install -p -m 644 nls/$language.cat $dest/tcsh
    echo "%lang($lang) %{_datadir}/locale/$lang/LC_MESSAGES/tcsh"
  fi
done > tcsh.lang << _EOF
de german
el greek
en C
es spanish
et et
fi finnish
fr french
it italian
ja ja
pl pl
ru russian
uk ukrainian
_EOF

%check
# tcsh expect nonroot user to run a tests
chmod g+w . -R
useradd test -G root -m
sudo -u test make check && userdel test -r -f

%post
if [ $1 -eq 1 ] ; then
  if [ ! -f %{_sysconfdir}/shells ]; then
   echo "%{_bindir}/tcsh" >> %{_sysconfdir}/shells
   echo "%{_bindir}/csh"  >> %{_sysconfdir}/shells
   echo "/bin/tcsh" >> %{_sysconfdir}/shells
   echo "/bin/csh"  >> %{_sysconfdir}/shells
  else
   grep -q '^%{_bindir}/tcsh$' %{_sysconfdir}/shells || \
   echo "%{_bindir}/tcsh" >> %{_sysconfdir}/shells
   grep -q '^%{_bindir}/csh$'  %{_sysconfdir}/shells || \
   echo "%{_bindir}/csh"  >> %{_sysconfdir}/shells
   grep -q '^/bin/tcsh$' %{_sysconfdir}/shells || \
   echo "/bin/tcsh" >> %{_sysconfdir}/shells
   grep -q '^/bin/csh$'  %{_sysconfdir}/shells || \
   echo "/bin/csh"  >> %{_sysconfdir}/shells
  fi
fi

%postun
if [ $1 -eq 0 ] ; then
  if [ ! -x %{_bindir}/tcsh ]; then
   grep -v '^%{_bindir}/tcsh$'  %{_sysconfdir}/shells | \
   grep -v '^%{_bindir}/csh$' > %{_sysconfdir}/shells.rpm && \
   mv %{_sysconfdir}/shells.rpm %{_sysconfdir}/shells
  fi
  if [ ! -x /bin/tcsh ]; then
   grep -v '^/bin/tcsh$'  %{_sysconfdir}/shells | \
   grep -v '^/bin/csh$' > %{_sysconfdir}/shells.rpm && \
   mv %{_sysconfdir}/shells.rpm %{_sysconfdir}/shells
  fi
fi

%files -f tcsh.lang
%defattr(-,root,root,-)
%license Copyright
%{_bindir}/tcsh
%{_bindir}/csh
%{_mandir}/man1/*.1*

%changelog
* Fri Nov 10 2023 Andrew Phelps <anphel@microsoft.com> - 6.22.03-2
- Link with libxcrypt

* Tue Feb 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 6.22.03-1
- Update version to 6.22.03.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.20.00-10
- Removing the explicit %%clean stage.

* Mon Nov 16 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.20.00-9
- Adding 'BuildRequires' on 'shadow-utils' and 'sudo' to fix the package tests.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 6.20.00-8
- Added %%license line automatically

* Mon Apr 13 2020 Eric Li <eli@microsoft.com> - 6.20.00-7
- Verified license.

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 6.20.00-6
- Remove toybox and only use coreutils for requires.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 6.20.00-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.20.00-4
- Requires coreutils or toybox and /bin/grep

* Tue Jun 6 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.20.00-3
- Fix make check issues.

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 6.20.00-2
- Ensure non empty debuginfo

* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> - 6.20.00-1
- Updated to version 6.20.00

* Tue Feb 07 2017 Divya Thaluru <dthaluru@vmware.com> - 6.19.00-6
- Added /bin/csh and /bin/tsch entries in /etc/shells

* Wed Dec 14 2016 Alexey Makhalov <amakhalov@vmware.com> - 6.19.00-5
- tcsh.glibc-2.24.patch

* Wed May 25 2016 Anish Swaminathan <anishs@vmware.com> - 6.19.00-4
- Fix calloc for gcc 5 optimization

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 6.19.00-3
- GA - Bump release of all rpms

* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 6.19.00-2
- Fix for upgrade issues

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> - 6.19.00-1
- Upgrade version

* Wed Apr 1 2015 Divya Thaluru <dthaluru@vmware.com> - 6.18.01-1
- Initial build. First version
