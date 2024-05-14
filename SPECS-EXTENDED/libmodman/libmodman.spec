Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libmodman
Version:        2.0.1
Release:        23%{?dist}
Summary:        A simple library for managing C++ modules (plug-ins)

License:        LGPLv2+
URL:            https://code.google.com/p/libmodman/
Source0:        https://libmodman.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  zlib-devel

%description
libmodman is a simple library for managing C++ modules (plug-ins).

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup

%build
%cmake
%make_build

%check
make test

%install
%make_install

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS
%{_libdir}/libmodman.so.*

%files devel
%{_includedir}/libmodman/
%{_libdir}/libmodman.so
%{_libdir}/pkgconfig/libmodman-2.0.pc
%dir %{_datadir}/cmake
%dir %{_datadir}/cmake/Modules
%{_datadir}/cmake/Modules/Findlibmodman.cmake

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.0.1-23
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.1-14
- Drop useless dependency on cmake
- Trivial fixes in packaging

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.0.1-10
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 07 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.0.1-1
- Update to 2.0.1

* Tue Aug 31 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-1
- Update to 2.0.0

* Sat Jul 03 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.0.1-5
- Remove conflict with libproxy, its not really necessary since
  we already have the latest libproxy in rawhide.

* Sun Jun 20 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.0.1-4
- Remove docs from -devel package
- Upgrade cmake requirement to 2.8.0
- Add cmake to -devel requires

* Fri Jun 18 2010 Nathaniel McCallum - 1.0.1-3
- Add docs to -devel package
- Fix include directory ownership

* Fri Jun 18 2010 Nathaniel McCallum - 1.0.1-2
- Added BuildRequires on zlib-devel (used for tests)

* Sun Jun 13 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.0.1-1
- First release
