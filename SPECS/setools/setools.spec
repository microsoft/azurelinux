%global libselinux_ver 3.2-1
%global libsepol_ver 3.2-1
Summary:        Policy analysis tools for SELinux
Name:           setools
Version:        4.4.0
Release:        2%{?dist}
# binaries are GPL and libraries are LGPL.  See COPYING.
License:        GPLv2 AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/SELinuxProject/setools
Source0:        https://github.com/SELinuxProject/setools/releases/download/%{version}/%{name}-%{version}.tar.bz2
Patch0:         0001-Make-NetworkX-optional.patch
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  libselinux-devel >= %{libselinux_ver}
BuildRequires:  libsepol-devel >= %{libsepol_ver}
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  qt5-qtbase-devel
BuildRequires:  swig

%description
SETools is a collection of graphical tools, command-line tools, and
Python modules designed to facilitate SELinux policy analysis.

%package        console
Summary:        Policy analysis command-line tools for SELinux
License:        GPLv2
Requires:       %{name}-python3 = %{version}-%{release}
Requires:       libselinux >= %{libselinux_ver}

%description    console
SETools is a collection of graphical tools, command-line tools, and
libraries designed to facilitate SELinux policy analysis.

This package includes the following console tools:

  sediff       Compare two policies to find differences.
  seinfo       List policy components.
  sesearch     Search rules (allow, type_transition, etc.)

%package        python3
Summary:        Policy analysis tools for SELinux
License:        GPLv2 AND LGPLv2+
Requires:       python3-setuptools
Recommends:     libselinux-python3
Provides:       python3-%{name} = %{version}-%{release}
Obsoletes:      %{name}-libs < 4.0.0

%description python3
SETools is a collection of graphical tools, command-line tools, and
Python 3 modules designed to facilitate SELinux policy analysis.

%prep
%autosetup -p1 -n %{name}

%build
%{python3} setup.py build_ext
%{python3} setup.py build

%install
%py3_install

# Remove unpackaged files.  These are tools for which the dependencies
# are not yet available on mariner (python3-networkx)
# Once networkx is added, the first 4 lines below should be
# added to setools-console-analyses and the last 3 should
# go in setools-gui.
rm -rf %{buildroot}%{_bindir}/sedta
rm -rf %{buildroot}%{_bindir}/seinfoflow
rm -rf %{buildroot}%{_mandir}/{,ru/}man1/sedta*
rm -rf %{buildroot}%{_mandir}/{,ru/}man1/seinfoflow*
rm -rf %{buildroot}%{_bindir}/apol
rm -rf %{buildroot}%{python3_sitearch}/setoolsgui
rm -rf %{buildroot}%{_mandir}/{,ru/}man1/apol*

%files console
%license COPYING COPYING.GPL COPYING.LGPL
%{_bindir}/sechecker
%{_bindir}/sediff
%{_bindir}/seinfo
%{_bindir}/sesearch
%{_mandir}/man1/sechecker*
%{_mandir}/man1/sediff*
%{_mandir}/ru/man1/sediff*
%{_mandir}/man1/seinfo*
%{_mandir}/ru/man1/seinfo*
%{_mandir}/man1/sesearch*
%{_mandir}/ru/man1/sesearch*

%files python3
%license COPYING COPYING.GPL COPYING.LGPL
%{python3_sitearch}/setools
%{python3_sitearch}/setools-*

%changelog
* Tue Dec 14 2021 Chris PeBenito <chpebeni@microsoft.com> - 4.4.0-2
- Make NetworkX optional for setools-console tools.  It is not used
  by them.
- Fix lint issues.

* Fri Aug 13 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.4.0-1
- Upgrade to latest upstream
- Update version of libselinux/libsepol dependencies
- Add python3-setools provides to python3 subpackage
- Lint spec
- License verified

* Tue Sep 01 2020 Daniel Burgener <daburgen@microsoft.com> - 4.2.2-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT)
- License verified

* Mon Jul 08 2019 Vit Mojzis <vmojzis@redhat.com> - 4.2.2-1
- SETools 4.2.2 release

* Mon May 13 2019 Vit Mojzis <vmojzis@redhat.com> - 4.2.1-3
- Use %set_build_flags instead of %optflags

* Mon May 06 2019 Vit Mojzis <vmojzis@redhat.com> - 4.2.1-2
- SELinuxPolicy: Create a map of aliases on policy load (#1672631)

* Tue Mar 26 2019 Petr Lautrbach <plautrba@redhat.com> - 4.2.1-1
- SETools 4.2.1 release (#1581761, #1595582)

* Wed Nov 14 2018 Vit Mojzis <vmojzis@redhat.com> - 4.2.0-1
- Update source to SETools 4.2.0 release

* Mon Oct 01 2018 Vit Mojzis <vmojzis@redhat.com> - 4.2.0-0.3.rc
- Update upstream source to 4.2.0-rc

* Wed Sep 19 2018 Vit Mojzis <vmojzis@redhat.com> - 4.2.0-0.2.beta
- Require userspace release 2.8
- setools-gui requires python3-setools
- Add Requires for python[23]-setuptools - no longer required (just recommended) by python[23] (#1623371)
- Drop python2 subpackage (4.2.0 no longer supports python2)

* Wed Aug 29 2018 Vit Mojzis <vmojzis@redhat.com> - 4.1.1-13
- Add Requires for python[23]-setuptools - no longer required (just recommended)
  by python[23] (#1623371)

* Wed Aug 22 2018 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-12.1
- Fix SCTP patch - https://github.com/SELinuxProject/setools/issues/9

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.1.1-10
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-9
- Move gui python files to -gui subpackage

* Thu Apr 26 2018 Vit Mojzis <vmojzis@redhat.com> - 4.1.1-8
- Add support for SCTP protocol (#1568333)

* Thu Apr 19 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 4.1.1-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 04 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-5
- setools-python2 requires python2-enum34

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.1.1-4
- Add Provides for the old name without %%_isa

* Thu Aug 10 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.1.1-3
- Python 2 binary package renamed to python2-setools
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
- Python 3 binary package renamed to python3-setools

* Thu Aug 10 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-2
- bswap_* macros are defined in byteswap.h

* Mon Aug 07 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.0-3
- setools-python{,3} packages should have a weak dependency on libselinux-python{,3}
  (#1447747)

* Thu Feb 23 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.0-2
- Move python networkx dependency to -gui and -console-analyses
- Ship sedta and seinfoflow in setools-console-analyses

* Wed Feb 15 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.0-1
- New upstream release.
