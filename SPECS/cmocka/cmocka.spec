Summary:        An elegant unit testing framework for C with support for mock objects
Name:           cmocka
Version:        1.1.5
Release:        5%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://cmocka.org
Source0:        https://cmocka.org/files/1.1/%{name}-%{version}.tar.xz
Source1:        https://cmocka.org/files/1.1/%{name}-%{version}.tar.xz.asc
Source2:        cmocka.keyring
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  gnupg2

%description
There are a variety of C unit testing frameworks available however many of them
are fairly complex and require the latest compiler technology. Some development
requires the use of old compilers which makes it difficult to use some unit
testing frameworks. In addition many unit testing frameworks assume the code
being tested is an application or module that is targeted to the same platform
that will ultimately execute the test. Because of this assumption many
frameworks require the inclusion of standard C library headers in the code
module being tested which may collide with the custom or incomplete
implementation of the C library utilized by the code under test.

Cmocka only requires a test application is linked with the standard C library
which minimizes conflicts with standard C library headers. Also, CMocka tries
to avoid the use of some of the newer features of C compilers.

This results in CMocka being a relatively small library that can be used to
test a variety of exotic code. If a developer wishes to simply test an
application with the latest compiler then other unit testing frameworks may be
preferable.

This is the successor of Google's Cmockery.

%package -n libcmocka
Summary:        Lightweight library to simplify and generalize unit tests for C
Conflicts:      cmockery2

%description -n libcmocka
There are a variety of C unit testing frameworks available however many of them
are fairly complex and require the latest compiler technology. Some development
requires the use of old compilers which makes it difficult to use some unit
testing frameworks. In addition many unit testing frameworks assume the code
being tested is an application or module that is targeted to the same platform
that will ultimately execute the test. Because of this assumption many
frameworks require the inclusion of standard C library headers in the code
module being tested which may collide with the custom or incomplete
implementation of the C library utilized by the code under test.

CMocka only requires a test application is linked with the standard C library
which minimizes conflicts with standard C library headers. Also, CMocka tries
to avoid the use of some of the newer features of C compilers.

This results in CMocka being a relatively small library that can be used to
test a variety of exotic code. If a developer wishes to simply test an
application with the latest compiler then other unit testing frameworks may be
preferable.

This is the successor of Google's Cmockery.

%package -n libcmocka-static
Summary:        Lightweight library to simplify and generalize unit tests for C

%description -n libcmocka-static
Static version of the cmocka library.

%package -n libcmocka-devel
Summary:        Development headers for the cmocka library
Requires:       libcmocka = %{version}-%{release}
Conflicts:      cmockery2-devel

%description -n libcmocka-devel
Development headers for the cmocka unit testing library.

%prep
%autosetup -p1

%build
if test ! -e "obj"; then
  mkdir obj
fi
pushd obj
%cmake \
  -DWITH_STATIC_LIB=ON \
  -DWITH_CMOCKERY_SUPPORT=ON \
  -DUNIT_TESTING=ON \
  %{_builddir}/%{name}-%{version}

make %{?_smp_mflags} VERBOSE=1
make docs
popd

%install
pushd obj
make DESTDIR=%{buildroot} install
popd
ln -s libcmocka.so %{buildroot}%{_libdir}/libcmockery.so

%ldconfig_scriptlets -n libcmocka

%check
pushd obj
ctest --output-on-failure
popd

%files -n libcmocka
%doc AUTHORS README.md ChangeLog
%license COPYING
%{_libdir}/libcmocka.so.*

%files -n libcmocka-static
%{_libdir}/libcmocka-static.a

%files -n libcmocka-devel
%doc obj/doc/html
%{_includedir}/cmocka.h
%{_includedir}/cmocka_pbc.h
%{_includedir}/cmockery/cmockery.h
%{_includedir}/cmockery/pbc.h
%{_libdir}/libcmocka.so
%{_libdir}/libcmockery.so
%{_libdir}/pkgconfig/cmocka.pc
%{_libdir}/cmake/cmocka/cmocka-config-version.cmake
%{_libdir}/cmake/cmocka/cmocka-config.cmake

%changelog
* Thu Feb 10 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.5-5
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.5-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Andreas Schneider <asn@redhat.com> - 1.1.5-1
- Update to version 1.1.5

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 27 2018 Andreas Schneider <asn@redhat.com> - 1.1.3-1
- Update to version 1.1.3

* Wed Aug 29 2018 Andreas Schneider <asn@redhat.com> - 1.1.2-1
- Update to version 1.1.2

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 28 2017 Than Ngo <than@redhat.com> - 1.1.0-5
- added workaround for gcc7 bug on ppc64le temporary 

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 21 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.1.0-1
- Update to version 1.1.0
    * Added support to catch multiple exceptions
    * Added support to verify call ordering
    * Added support to pass initial data to test cases
    * Added will_return_maybe() for ignoring mock returns
    * Added subtests for groups using TAP output
    * Added support to write multiple XML files for groups
    * Improved documentation
    * Fixed XML output generataion
    * Fixed Windows builds with VS2015

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 12 2015 Andreas Schneider <asn@redhat.com> - 1.0.1-1
- Update to version 1.0.1:
  * Added a macro for assert_ptr_equal().
  * Fixed test_realloc() if 0 size is passed.
  * Fixed objects packaging bug.
  * Fixed building with newer gcc versions.

* Mon Feb 16 2015 Andreas Schneider <asn@redhat.com> - 1.0.0-1
- Update to version 1.0.0:
  * Added new test runner with group fixtures. The old runner is deprecated
  * Added an extensible message output formatter
  * Added jUnit XML message output
  * Added subunit message output
  * Added Test Anything Protocol message output
  * Added skip() command
  * Added test_realloc()
  * Added a cmockery compat header
  * Fixed a lot of bugs on Windows

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 - Andreas Schneider <asn@redhat.com> - 0.4.1-1
- Update to version 0.4.1.

* Fri Apr 11 2014 - Andreas Schneider <asn@redhat.com> - 0.4.0-1
- Update to version 0.4.0.

* Wed Nov 06 2013 - Andreas Schneider <asn@redhat.com> - 0.3.2-1
- Update to version 0.3.2.
- Include API documentation.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 - Andreas Schneider <asn@redhat.com> - 0.3.0-2
- Update to version 0.3.1.
- Fixed cmocka issues on big endian.
- resolves: #975044

* Wed Jun 05 2013 - Andreas Schneider <asn@redhat.com> - 0.3.0-1
- Update to version 0.3.0.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 - Andreas Schneider <asn@redhat.com> - 0.2.0-3
- Fixed typo in Source URL.

* Thu Jan 17 2013 - Andreas Schneider <asn@redhat.com> - 0.2.0-2
- Fixed Source URL.
- Fixed package groups.

* Tue Jan 15 2013 - Andreas Schneider <asn@redhat.com> - 0.2.0-1
- Initial version 0.2.0
