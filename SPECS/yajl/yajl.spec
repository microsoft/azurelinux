Summary:        Yet Another JSON Library (YAJL)
Name:           yajl
Version:        2.1.0
Release:        19%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://lloyd.github.com/yajl/
#
# NB, upstream does not provide pre-built tar.gz downloads. Instead
# they make you use the 'on the fly' generated tar.gz from GITHub's
# web interface
Source0:        https://github.com/lloyd/%{name}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch1:         %{name}-%{version}-pkgconfig-location.patch
Patch2:         %{name}-%{version}-pkgconfig-includedir.patch
Patch3:         %{name}-%{version}-test-location.patch
Patch4:         %{name}-%{version}-dynlink-binaries.patch
Patch5:         CVE-2023-33460.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  which

%package devel
Summary:        Libraries, includes, etc to develop with YAJL
Requires:       %{name} = %{version}-%{release}

%description
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.

%description devel
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.

This sub-package provides the libraries and includes
necessary for developing against the YAJL library

%prep
%autosetup -p1

%build
# NB, we are not using upstream's 'configure'/'make'
# wrapper, instead we use cmake directly to better
# align with Fedora standards
mkdir build
cd build
%cmake ..
%make_build VERBOSE=1 %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

# No static libraries
rm -f %{buildroot}%{_libdir}/libyajl_s.a

%check
cd test
(cd parsing && ./run_tests.sh)
(cd api && ./run_tests.sh)

%ldconfig_scriptlets

%files
%license COPYING
%doc ChangeLog README TODO
%{_bindir}/json_reformat
%{_bindir}/json_verify
%{_libdir}/libyajl.so.2
%{_libdir}/libyajl.so.2.*

%files devel
%dir %{_includedir}/yajl
%{_includedir}/yajl/yajl_common.h
%{_includedir}/yajl/yajl_gen.h
%{_includedir}/yajl/yajl_parse.h
%{_includedir}/yajl/yajl_tree.h
%{_includedir}/yajl/yajl_version.h
%{_libdir}/libyajl.so
%{_libdir}/pkgconfig/yajl.pc

%changelog
* Fri Jun 16 2023 Suresh Thelkar <sthelkar@microsoft.com> - 2.1.0-19
- Patch CVE-2023-33460

* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.0-18
- Fixing source URL.

* Thu Jun 03 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.1.0-17
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.0-9
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Daniel P. Berrange <berrange@redhat.com> - 2.1.0-1
- Update to 2.1.0 release (rhbz #1080935)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug  6 2012 Daniel P. Berrange <berrange@redhat.com> - 2.0.4-1
- Update to 2.0.4 release (rhbz #845777)
- Fix License tag to reflect change in 2.0.0 series from BSD to ISC

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Daniel P. Berrange <berrange@redhat.com> - 2.0.1-1
- Update to 2.0.1 release

* Tue May  3 2011 Daniel P. Berrange <berrange@redhat.com> - 1.0.12-1
- Update to 1.0.12 release

* Fri Dec 17 2010 Daniel P. Berrange <berrange@redhat.com> - 1.0.11-1
- Update to 1.0.11 release

* Mon Jan 11 2010 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-3
- Fix ignoring of cflags (rhbz #547500)

* Tue Dec  8 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-2
- Change use of 'define' to 'global'

* Mon Dec  7 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-1
- Initial Fedora package
