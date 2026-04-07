# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Automated Testing Framework
Name:    atf
Version: 0.23
Release: 2%{?dist}
# Automatically converted from old format: BSD - review is highly recommended.
License: LicenseRef-Callaway-BSD
URL:     https://github.com/freebsd/atf
Source0: %{url}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1: README.Fedora

%global _testsdir %{_libexecdir}/atf/tests

%global common_description The Automated Testing Framework (ATF) is a collection of libraries to \
implement test programs in a variety of languages.  At the moment, ATF \
offers C, C++ and POSIX shell bindings with which to implement tests. \
These bindings all offer a similar set of functionality and any test \
program written with them exposes a consistent user interface. \
\
ATF-based test programs rely on a separate runtime engine to execute them. \
The runtime engine is in charge of isolating the test programs from the \
rest of the system to ensure that their results are deterministic and that \
they cannot affect the running system.  The runtime engine is also \
responsible for gathering the results of all tests and composing reports. \
The current runtime of choice is Kyua.

BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
There is no main package being built here.  This is unused.

# Ideally, we would ship one tests package for every component, namely
# libatf-c-tests, libatf-c++-tests and libatf-sh-tests.  However, the test
# suite of ATF has not been written with this in mind, and the tests of one
# component often have dependencies on the rest of the components.  It is
# much easier to ship a single package with the whole test suite rather
# than attempting to fight this fact.
%package tests
Summary: Automated Testing Framework - Test suite
Requires: libatf-c = %{version}-%{release}
Requires: libatf-c++ = %{version}-%{release}
Requires: libatf-sh = %{version}-%{release}
Requires: libatf-c-devel = %{version}-%{release}
Requires: libatf-c++-devel = %{version}-%{release}
Requires: libatf-sh-devel = %{version}-%{release}

%description tests
%{common_description}

This package installs the run-time tests for all the components of ATF, which
include tests for the C, C++ and POSIX shell libraries and the run-time tools.
Please see the README.Fedora file in the documentation directory for further
details on how to run the installed tests.

%package -n libatf-c
Summary: Automated Testing Framework - C bindings

%description -n libatf-c
%{common_description}

This package provides the run-time libraries to run tests that use the
ATF C bindings.

%package -n libatf-c-devel
Summary: Automated Testing Framework - C bindings (headers)
Requires: libatf-c = %{version}-%{release}

%description -n libatf-c-devel
%{common_description}

This package provides the libraries, header files and documentation to
develop tests that use the ATF C bindings.


%package -n libatf-c++
Summary: Automated Testing Framework - C++ bindings

%description -n libatf-c++
%{common_description}

This package provides the run-time libraries to run tests that use the
ATF C++ bindings.


%package -n libatf-c++-devel
Summary: Automated Testing Framework - C++ bindings (headers)
Requires: libatf-c = %{version}-%{release}
Requires: libatf-c-devel = %{version}-%{release}
Requires: libatf-c++ = %{version}-%{release}

%description -n libatf-c++-devel
%{common_description}

This package provides the libraries, header files and documentation to
develop applications that use the ATF C++ bindings.


%package -n libatf-sh
Summary: Automated Testing Framework - POSIX shell bindings
Requires: libatf-c++ = %{version}-%{release}

%description -n libatf-sh
%{common_description}

This package provides the run-time libraries to run tests that use the
ATF POSIX shell bindings.


%package -n libatf-sh-devel
Summary: Automated Testing Framework - POSIX shell bindings (headers)
Requires: libatf-sh = %{version}-%{release}

%description -n libatf-sh-devel
%{common_description}

This package provides the supporting files and documentation to develop
applications that use the ATF POSIX shell bindings.

%prep
%autosetup -n %{name}-%{name}-%{version}

# Put the README.Fedora file in the top-level directory of the source tree so
# that the %doc call below can pick it up.
cp -p %{SOURCE1} README.Fedora

%build
autoreconf -is
%configure INSTALL="/usr/bin/install -p" --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build pkgtestsdir=%{_testsdir} testsdir=%{_testsdir}

%check
make check

%install
%make_install doc_DATA= \
             pkgtestsdir=%{_testsdir} testsdir=%{_pkgtestsdir}
rm %{buildroot}%{_libdir}/libatf*.la


%files tests
%doc README.Fedora
%{_testsdir}
%{_mandir}/man7/atf.7.gz

%files -n libatf-c
%{_libdir}/libatf-c.so.1
%{_libdir}/libatf-c.so.1.0.0
%{_datadir}/man/man1/atf-test-program.1.gz
%{_datadir}/man/man4/atf-test-case.4.gz
%{_mandir}/man3/atf-c.3.gz

%files -n libatf-c-devel
%{_datadir}/aclocal/atf-c.m4
%{_datadir}/aclocal/atf-common.m4
%{_includedir}/atf-c.h
%{_includedir}/atf-c
%{_libdir}/libatf-c.so
%{_libdir}/pkgconfig/atf-c.pc

%files -n libatf-c++
%{_libdir}/libatf-c++.so.2
%{_libdir}/libatf-c++.so.2.0.0
%{_mandir}/man3/atf-c++.3.gz

%files -n libatf-c++-devel
%{_datadir}/aclocal/atf-c++.m4
%{_includedir}/atf-c++.hpp
%{_includedir}/atf-c++
%{_libdir}/libatf-c++.so
%{_libdir}/pkgconfig/atf-c++.pc

%files -n libatf-sh
%{_bindir}/atf-sh
# Cheat a bit: While this directory should be supposedly owned by the main
# 'atf' package, 'atf' depends on libatf-sh.  Therefore, it's easier to handle
# ownership here.
%{_datadir}/atf
%{_libexecdir}/atf-check
%{_mandir}/man1/atf-sh.1.gz
%{_mandir}/man3/atf-sh.3.gz

%files -n libatf-sh-devel
%{_datadir}/aclocal/atf-sh.m4
%{_libdir}/pkgconfig/atf-sh.pc
%{_mandir}/man1/atf-check.1.gz


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 08 2025 Sérgio Basto <sergio@serjux.com> - 0.23-1
- Update atf to 0.23
- Resolves: rhbz#2355972

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Jonathan Wright <jonathan@almalinux.org> - 0.22-1
- Update to 0.22

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 0.21-6
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 15 2023 Sérgio Basto <sergio@serjux.com> - 0.21-1
- Update atf to 0.21
- Use make macros ( https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro )
- The %ldconfig_scriptlets macro can be removed on all Fedoras. Possibly also on
  EPEL 8. But it is required on EPEL 7.

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.20-10
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.20-4
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Julio Merino <julio@meroh.net> 0.20-1
- Update to new upstream version 0.20.
- The atf binary package, which used to provide the deprecated binary
  tools (atf-config, atf-report, atf-run and atf-version), is now gone.
- The libatf-c package now installs the atf-test-program(1) and
  atf-test-case(4) manual pages and the package documentation files.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Julio Merino <julio@meroh.net> 0.17-1
- Update to new upstream version 0.17.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Julio Merino <julio@meroh.net> 0.16-1
- Updated to new upstream version 0.16.

* Mon Jun 18 2012 Julio Merino <jmmv@julipedia.org> 0.15-2
- Added the atf-tests package, which provides the run-time tests of ATF
  readily runnable by the end users.
- Made the installation of the package preserve the build times of the files.
- Fixed URL to the project's page.

* Thu May 3 2012 Julio Merino <jmmv@julipedia.org> 0.15-1
- Initial release for Fedora.


