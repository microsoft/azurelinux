# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sepol_ver 3.9
%global selinux_ver 3.9

Name:           setools
Version:        4.6.0
Release: 5%{?dist}
Summary:        Policy analysis tools for SELinux

License:        GPL-2.0-only AND LGPL-2.1-only
URL:            https://github.com/SELinuxProject/setools/wiki
Source0:        https://github.com/SELinuxProject/setools/archive/%{version}.tar.gz
Source1:        setools.pam
Source2:        apol.desktop

# Remove redundant runtime requirement on setuptools
Patch:          https://github.com/SELinuxProject/setools/pull/156.patch
# Fix seinfo argument parsing when policy path follows query
Patch:          https://github.com/SELinuxProject/setools/pull/157.patch

Obsoletes:      setools < 4.0.0, setools-devel < 4.0.0
BuildRequires:  flex,  bison
BuildRequires:  glibc-devel, gcc, git-core
BuildRequires:  libsepol-devel >= %{sepol_ver}, libsepol-static >= %{sepol_ver}
BuildRequires:  swig
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  libselinux-devel

Requires:       %{name}-console = %{version}-%{release}
Requires:       %{name}-console-analyses = %{version}-%{release}
Requires:       %{name}-gui = %{version}-%{release}

%description
SETools is a collection of graphical tools, command-line tools, and
Python modules designed to facilitate SELinux policy analysis.

%package     console
Summary:     Policy analysis command-line tools for SELinux
License:     GPL-2.0-only
Requires:    python3-setools = %{version}-%{release}
Requires:    libselinux >= %{selinux_ver}

%description console
SETools is a collection of graphical tools, command-line tools, and
libraries designed to facilitate SELinux policy analysis.

This package includes the following console tools:

  sediff       Compare two policies to find differences.
  seinfo       List policy components.
  sesearch     Search rules (allow, type_transition, etc.)


%package     console-analyses
Summary:     Policy analysis command-line tools for SELinux
License:     GPL-2.0-only
Requires:    python3-setools = %{version}-%{release}
Requires:    libselinux >= %{selinux_ver}
Requires:    python3-networkx

%description console-analyses
SETools is a collection of graphical tools, command-line tools, and
libraries designed to facilitate SELinux policy analysis.

This package includes the following console tools:

  sedta        Perform domain transition analyses.
  seinfoflow   Perform information flow analyses.


%package     -n python3-setools
Summary:     Policy analysis tools for SELinux
License:     LGPL-2.1-only
Obsoletes:   setools-libs < 4.0.0

%description -n python3-setools
SETools is a collection of graphical tools, command-line tools, and
Python 3 modules designed to facilitate SELinux policy analysis.


%package     gui
Summary:     Policy analysis graphical tools for SELinux
License:     GPL-2.0-only
Requires:    python3-setools = %{version}-%{release}
Requires:    python3-pyqt6 python3-pyqt6-sip
Requires:    python3-networkx

%description gui
SETools is a collection of graphical tools, command-line tools, and
Python modules designed to facilitate SELinux policy analysis.


%prep
%autosetup -p 1 -S git -n setools-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install

%check
%if %{?_with_check:1}%{!?_with_check:0}
# dnf install python3-pytest python3-pytest-qt
%pytest
%endif


%files

%files console
%license COPYING.GPL
%{_bindir}/sechecker
%{_bindir}/sediff
%{_bindir}/seinfo
%{_bindir}/sesearch
%{_mandir}/man1/sechecker*
%{_mandir}/man1/sediff*
%{_mandir}/man1/seinfo*
%{_mandir}/man1/sesearch*
%{_mandir}/ru/man1/sediff*
%{_mandir}/ru/man1/seinfo*
%{_mandir}/ru/man1/sesearch*

%files console-analyses
%license COPYING.GPL
%{_bindir}/sedta
%{_bindir}/seinfoflow
%{_mandir}/man1/sedta*
%{_mandir}/man1/seinfoflow*
%{_mandir}/ru/man1/sedta*
%{_mandir}/ru/man1/seinfoflow*

%files -n python3-setools
%license COPYING COPYING.LGPL
%{python3_sitearch}/setools
%{python3_sitearch}/setools-*

%files gui
%license COPYING.GPL
%{_bindir}/apol
%{python3_sitearch}/setoolsgui
%{_mandir}/man1/apol*
%{_mandir}/ru/man1/apol*

%changelog
* Mon Dec 01 2025 Veronika Syncakova <vsyncako@redhat.com> - 4.6.0-4
- Fix seinfo argument parsing when policy path follows query options

* Thu Oct 02 2025 Miro Hrončok <mhroncok@redhat.com> - 4.6.0-3
- Drop redundant runtime requirement on python3-setuptools (redux)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.6.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Sep 09 2025 Petr Lautrbach <lautrbach@redhat.com> - 4.6.0-1
- SETools 4.6.0

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.5.1-11
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 04 2025 Miro Hrončok <mhroncok@redhat.com> - 4.5.1-10
- Drop redundant runtime requirement on python3-setuptools (correction)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 05 2025 Petr Lautrbach <lautrbach@redhat.com> - 4.5.1-8
- Rebuilt with SELinux userspace 3.9-rc2 release

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 4.5.1-7
- Rebuilt for Python 3.14

* Tue Apr 01 2025 Miro Hrončok <mhroncok@redhat.com> - 4.5.1-6
- Drop redundant runtime requirement on python3-setuptools, dropped in setools 4.5.1

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.5.1-3
- Rebuilt for Python 3.13

* Thu May 02 2024 Petr Lautrbach <lautrbach@redhat.com> - 4.5.1-2
- Fix License tag

* Thu May 02 2024 Petr Lautrbach <lautrbach@redhat.com> - 4.5.1-1
- SETools 4.5.1

* Thu Apr 18 2024 Petr Lautrbach <lautrbach@redhat.com> - 4.5.0-1
- SETools 4.5.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Petr Lautrbach <lautrbach@redhat.com> - 4.4.4-1
- SETools 4.4.4 release

* Mon Aug 28 2023 Petr Lautrbach <lautrbach@redhat.com> - 4.4.3-2
- Use Qt 6

* Wed Aug  9 2023 Petr Lautrbach <lautrbach@redhat.com> - 4.4.3-1
- SETools 4.4.3 release

* Wed Jul 26 2023 Petr Lautrbach <lautrbach@redhat.com> - 4.4.2-4
- Disable/remove neverallow options in sediff.
- Improve man pages
- seinfoflow: Add -r option to get flows into the source type.
- seinfoflow.1: Remove references to sepolgen permission map.
- AVRule/AVRuleXperm: Treat rules with no permissions as invalid policy.
- SELinuxPolicy: Add explicit cast for libspol message

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.4.2-2
- Rebuilt for Python 3.12

* Thu Apr 20 2023 Petr Lautrbach <lautrbach@redhat.com> - 4.4.2-1
- SETools 4.4.2 release

* Mon Feb  6 2023 Petr Lautrbach <lautrbach@redhat.com> - 4.4.1-1
- SETools 4.4.1 release

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 4.4.0-8
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Petr Lautrbach <plautrba@redhat.com> - 4.4.0-7
- Update required userspace versions to 3.4
- Drop unnecessary Recommends

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.4.0-6
- Rebuilt for Python 3.11

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 19 2021 Petr Lautrbach <plautrba@redhat.com> - 4.4.0-4
- Make seinfo output predictable
  https://github.com/SELinuxProject/setools/issues/65

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.4.0-2
- Rebuilt for Python 3.10

* Mon Mar  8 2021 Petr Lautrbach <plautrba@redhat.com> - 4.4.0-1
- SETools 4.4.0 release

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-0.3.20210121git16c0696
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Petr Lautrbach <plautrba@redhat.com> - 4.4.0-0.2.20210121git16c0696
- Rebuild with SELinux userspace 3.2-rc1
- Update to 16c0696

* Thu Dec 10 2020 Petr Lautrbach <plautrba@redhat.com> - 4.4.0-0.2.20201102git05e90ee
- Fix imports in /usr/bin/sedta

* Tue Nov  3 2020 Petr Lautrbach <plautrba@redhat.com> - 4.4.0-0.1.20201102git05e90ee
- Update to 05e90ee
- Add /usr/bin/sechecker
- Adapt to new libsepol filename transition structures
- Rebuild with libsepol.so.2

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Petr Lautrbach <plautrba@redhat.com> - 4.3.0-3
- rebuild with SELinux userspace 3.1 release

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.3.0-2
- Rebuilt for Python 3.9

* Thu Apr  2 2020 Petr Lautrbach <plautrba@redhat.com> - 4.3.0-1
- SETools 4.3.0 release
- Revised sediff method for TE rules. This drastically reduced memory and run time.
- Added infiniband context support to seinfo, sediff, and apol.
- Added apol configuration for location of Qt assistant.
- Fixed sediff issue where properties header would display when not requested.
- Fixed sediff issue with type_transition file name comparison.
- Fixed permission map socket sendto information flow direction.
- Added methods to TypeAttribute class to make it a complete Python collection.
- Genfscon now will look up classes rather than using fixed values which
    were dropped from libsepol.

* Mon Mar 23 2020 Petr Lautrbach <plautrba@redhat.com> - 4.2.2-5
- setools requires -console, -console-analyses and -gui packages (#1794314)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.2-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.2-2
- Rebuilt for Python 3.8

* Mon Jul 08 2019 Vit Mojzis <vmojzis@redhat.com> - 4.2.2-1}
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
