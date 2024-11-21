# NOTE: python2 support is no longer available.  Do not build for EPEL versions
# that do not support python3.
#
# NOTE: perl support was dropped in version 1.4.3.  It is available here:
# https://github.com/jelmer/subunit-perl

# Disable the tests in a bootstrap situation
%global majver  %(cut -d. -f-2 <<< %{version})
%global giturl  https://github.com/testing-cabal/subunit
Summary:        C bindings for subunit
Name:           subunit
Version:        1.4.4
Release:        5%{?dist}
License:        Apache-2.0 OR BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://launchpad.net/subunit
Source:         %{giturl}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pkgconfig(cppunit)
# This can be removed when F43 reaches EOL
Obsoletes:      %{name}-perl < 1.4.3
%bcond bootstrap 0
VCS:            git:%{giturl}.git
%if %{without bootstrap}
BuildRequires:  pkgconfig(check)
%endif

%description
Subunit C bindings.  See the python-subunit package for test processing
functionality.

%package devel
Summary:        Header files for developing C applications that use subunit
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for developing C applications that use subunit.

%package cppunit
Summary:        Subunit integration into cppunit
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description cppunit
Subunit integration into cppunit.

%package cppunit-devel
Summary:        Header files for applications that use cppunit and subunit
Requires:       %{name}-cppunit%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       cppunit-devel%{?_isa}

%description cppunit-devel
Header files and libraries for developing applications that use cppunit
and subunit.

%package shell
Summary:        Shell bindings for subunit
BuildArch:      noarch

%description shell
Subunit shell bindings.  See the python-subunit package for test
processing functionality.

%package -n python3-%{name}
Summary:        Streaming protocol for test results
# This can be removed when Fedora 41 reaches EOL
Obsoletes:      python2-%{name} < 1.4.1
BuildArch:      noarch

%description -n python3-%{name}
Subunit is a streaming protocol for test results.  The protocol is a
binary encoding that is easily generated and parsed.  By design all the
components of the protocol conceptually fit into the xUnit TestCase ->
TestResult interaction.

Subunit comes with command line filters to process a subunit stream and
language bindings for python, C, C++ and shell.  Bindings are easy to
write for other languages.

A number of useful things can be done easily with subunit:
- Test aggregation: Tests run separately can be combined and then
  reported/displayed together.  For instance, tests from different
  languages can be shown as a seamless whole.
- Test archiving: A test run may be recorded and replayed later.
- Test isolation: Tests that may crash or otherwise interact badly with
  each other can be run separately and then aggregated, rather than
  interfering with each other.
- Grid testing: subunit can act as the necessary serialization and
  deserialization to get test runs on distributed machines to be
  reported in real time.

%package -n python3-%{name}-test
Summary:        Test code for the python 3 subunit bindings
Requires:       %{name}-filters = %{version}-%{release}
Requires:       python3-%{name} = %{version}-%{release}
BuildArch:      noarch

%description -n python3-%{name}-test
%{summary}.

%package filters
Summary:        Command line filters for processing subunit streams
Requires:       %{py3_dist junitxml}
Requires:       gtk3 >= 3.20
Requires:       libnotify >= 0.7.7
Requires:       python3-%{name} = %{version}-%{release}
Requires:       python3-gobject
BuildArch:      noarch

%description filters
Command line filters for processing subunit streams.

%package static
Summary:        Static C library for subunit
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Subunit C bindings in a static library, for building statically linked
test cases.

%prep
%autosetup -p1

fixtimestamp() {
  touch -r $1.orig $1
  rm $1.orig
}

# Fix underlinked library
sed "/^tests_LDADD/ilibcppunit_subunit_la_LIBADD = -lcppunit libsubunit.la\n" \
    -i Makefile.am

# Do not use env
for fil in $(grep -Frl "%{_bindir}/env python"); do
  sed -ri.orig 's,%{_bindir}/env python3?,%{python3},' $fil
  fixtimestamp $fil
done

# Update an obsolete autoconf macro
sed -i 's/AC_PROG_LIBTOOL/LT_INIT/' configure.ac

%generate_buildrequires
%pyproject_buildrequires -x docs,test

%build
# Generate the configure script
autoreconf -fi

# Build for python3
export PYTHON=%{_bindir}/python3
%configure --enable-shared --enable-static

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC=.g..|& -Wl,--as-needed|' \
    -i libtool

%make_build
%pyproject_wheel

%install
%pyproject_install
chmod 0755 %{buildroot}%{python3_sitelib}/%{name}/run.py
chmod 0755 %{buildroot}%{python3_sitelib}/%{name}/tests/sample-script.py
chmod 0755 %{buildroot}%{python3_sitelib}/%{name}/tests/sample-two-script.py

# We set pkgpython_PYTHON for efficiency to disable automake python compilation
%make_install pkgpython_PYTHON='' INSTALL="%{_bindir}/install -p"

# Install the shell interface
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cp -p shell/share/%{name}.sh %{buildroot}%{_sysconfdir}/profile.d

# Remove unwanted libtool files
find %{buildroot} -type f -name "*.la" -delete -print

# Fix permissions
chmod 0755 %{buildroot}%{python3_sitelib}/%{name}/filter_scripts/*.py
chmod 0644 %{buildroot}%{python3_sitelib}/%{name}/filter_scripts/__init__.py
chmod 0755 %{buildroot}%{python3_sitelib}/%{name}/tests/sample-script.py
chmod 0755 %{buildroot}%{python3_sitelib}/%{name}/tests/sample-two-script.py

# Fix timestamps
touch -r c/include/%{name}/child.h %{buildroot}%{_includedir}/%{name}/child.h
touch -r c++/SubunitTestProgressListener.h \
      %{buildroot}%{_includedir}/%{name}/SubunitTestProgressListener.h

%check
%if %{without bootstrap}
# Run the tests for python3
export LD_LIBRARY_PATH=$PWD/.libs
export PYTHON=%{python3}
make check
%endif

%files
%doc NEWS README.rst
%license Apache-2.0 BSD COPYING
%{_libdir}/lib%{name}.so.0*

%files devel
%doc c/README
%dir %{_includedir}/%{name}/
%{_includedir}/%{name}/child.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc

%files cppunit
%{_libdir}/libcppunit_%{name}.so.0*

%files cppunit-devel
%doc c++/README
%{_includedir}/%{name}/SubunitTestProgressListener.h
%{_libdir}/libcppunit_%{name}.so
%{_libdir}/pkgconfig/libcppunit_%{name}.pc

%files shell
%doc shell/README
%license Apache-2.0 BSD COPYING
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.sh

%files -n python3-%{name}
%license Apache-2.0 BSD COPYING
%{python3_sitelib}/%{name}/
%{python3_sitelib}/python_%{name}-%{version}.dist-info/
%exclude %{python3_sitelib}/%{name}/tests/

%files -n python3-%{name}-test
%{python3_sitelib}/%{name}/tests/

%files static
%{_libdir}/*.a

%files filters
%{_bindir}/subunit*
%{_bindir}/tap2subunit

%changelog
* Thu Sep 12 2024 Zhichun Wan <zhichunwan@microsoft.com> - 1.4.4-5
- Initial Azure Linux import from Fedora 42 (license: MIT)
- License Verified

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.4.4-3
- Rebuilt for Python 3.13

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 17 2023 Jerry James <loganjerry@gmail.com> - 1.4.4-1
- Version 1.4.4

* Wed Nov  8 2023 Jerry James <loganjerry@gmail.com> - 1.4.3-1
- Version 1.4.3
- python-iso8601 is no longer bundled in python3-subunit
- perl support has moved to https://github.com/jelmer/subunit-perl

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.4.2-3
- Rebuilt for Python 3.12

* Fri Feb 24 2023 Jerry James <loganjerry@gmail.com> - 1.4.2-2
- Dynamically generate python BuildRequires

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Jerry James <loganjerry@gmail.com> - 1.4.2-1
- Version 1.4.2

* Sat Nov  5 2022 Jerry James <loganjerry@gmail.com> - 1.4.1-1
- Version 1.4.1
- Upstream no longer provides GPG signatures
- Convert License tag to SPDX
- Python 2 is no longer supported

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.4.0-12
- Rebuilt for Python 3.11

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0-11
- Perl 5.36 rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Jerry James <loganjerry@gmail.com> - 1.4.0-9
- Update python macros for the python3 cases
- Simplify python2 conditional

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.4.0-8
- Rebuilt for Python 3.10

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0-7
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0-3
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-2
- Rebuilt for Python 3.9

* Wed Mar 18 2020 Jerry James <loganjerry@gmail.com> - 1.4.0-1
- Version 1.4.0
- Drop all patches; all have been upstreamed
- Verify the source tarball

* Wed Mar 11 2020 Jerry James <loganjerry@gmail.com> - 1.3.0-19
- Drop the -decode-binary-to-unicode patch; it doesn't work with the bundled
  version of iso8601.
- Add 0003 and 0004 patches to fix bugs reported to upstream.

* Tue Mar 10 2020 Jerry James <loganjerry@gmail.com> - 1.3.0-18
- The python iso8601 module in Fedora has diverged too much from the bundled
  version.  Allow this package to bundle it (bz 1811697).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 25 2019 David Tardon <dtardon@redhat.com> - 1.3.0-16
- rebuild for cppunit 1.15.1

* Sat Dec 21 2019 David Tardon <dtardon@redhat.com> - 1.3.0-15
- rebuild for cppunit 1.15.0

* Wed Oct 16 2019 Jerry James <loganjerry@gmail.com> - 1.3.0-14
- Fix symlinks for python 3.8

* Fri Sep 20 2019 Jerry James <loganjerry@gmail.com> - 1.3.0-13
- Drop python2 support in Fedora 32+ and EPEL 9+ (bz 1753957)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-12
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.0-10
- Perl 5.30 rebuild

* Thu Mar 28 2019 Jerry James <loganjerry@gmail.com> - 1.3.0-9
- Do not ship the python 2 tests for F30+
- Run tests on aarch64 again

* Wed Mar 20 2019 Andreas Schneider <asn@redhat.com> - 1.3.0-8
- Ship the python tests, needed by Samba

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan  9 2019 Haïkel Guémar <hguemar@fedoraproject.org> - 1.3.0-6
- Ensure patches get applied

* Wed Jan  2 2019 Haïkel Guémar <hguemar@fedoraproject.org> - 1.3.0-5
- Fix python3 compatibility

* Fri Nov 30 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.3.0-4
- Migrate GUI filters to Gtk3/GObject introspection
- Migrate filters to python3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul  3 2018 Jerry James <loganjerry@gmail.com> - 1.3.0-2
- One more perl 5.28 rebuild

* Tue Jul  3 2018 Jerry James <loganjerry@gmail.com> - 1.3.0-1
- New upstream release
- Add -static subpackage (bz 1575054)

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 1.2.0-21
- Perl 5.28 rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.0-20
- Perl 5.28 rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-19
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.0-18
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Jerry James <loganjerry@gmail.com> - 1.2.0-14
- Rebuild to fix broken perl dependencies

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.0-13
- Perl 5.26 rebuild

* Fri May  5 2017 Jerry James <loganjerry@gmail.com> - 1.2.0-12
- Rebuild for cppunit 1.14.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Jerry James <loganjerry@gmail.com> - 1.2.0-10
- Add Requires on python-junitxml to -filter subpackage (bz 1417291)

* Tue Dec 20 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-9
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun  3 2016 Jerry James <loganjerry@gmail.com> - 1.2.0-7
- Fix -python3 dependency on /usr/bin/python (bz 1342508)
- Comply with latest python packaging guidelines
- Drop workaround for bz 1251568, now fixed

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.0-6
- Perl 5.24 rebuild

* Mon Apr 18 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.2.0-5
- Added missing check for %%with_py3 to make it buildable under RHEL/CentOS

* Sun Feb 14 2016 David Tardon <dtardon@redhat.com> - 1.2.0-4
- rebuild for cppunit 1.13.2

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 23 2015 Jerry James <loganjerry@gmail.com> - 1.2.0-1
- New upstream release

* Wed Sep  2 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 1.1.0-5
- Backport upstream patches (RHBZ#1259286)

* Fri Aug  7 2015 Jerry James <loganjerry@gmail.com> - 1.1.0-4
- Fix FTBFS due to older python-testtools (bz 1249714)

* Tue Jul 14 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.1.0-3
- Symlink iso8601 file into subunit Python dirs to preserve compatibility while unbundling
Resolves: rhbz#1233581

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Jerry James <loganjerry@gmail.com> - 1.1.0-1
- New upstream release
- Enable python3 tests

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.0-3
- Perl 5.22 rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Tue Dec  9 2014 Jerry James <loganjerry@gmail.com> - 1.0.0-1
- New upstream release (bz 1171483 and 1172204)
- Add python3 subpackage (bz 1172195)

* Wed Nov 19 2014 Pádraig Brady <pbrady@redhat.com> - 0.0.21-2
- Make python-subunit egginfo available for pip etc.

* Fri Sep 19 2014 Jerry James <loganjerry@gmail.com> - 0.0.21-1
- New upstream release
- Fix license handling

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.0.18-5
- Perl 5.20 rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Jerry James <loganjerry@gmail.com> - 0.0.18-2
- Add license text to all independent packages
- Add perl module Requires to the -perl subpackage
- Fix timestamps after install

* Fri Feb 14 2014 Jerry James <loganjerry@gmail.com> - 0.0.18-1
- Initial RPM
