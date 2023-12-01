Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:       opencc
Version:    1.1.1
Release:    3%{?dist}
Summary:    Libraries for Simplified-Traditional Chinese Conversion
License:    ASL 2.0
URL:        https://github.com/BYVoid/OpenCC
Source0:    https://github.com/BYVoid/OpenCC/archive/ver.%{version}.tar.gz#/OpenCC-ver.%{version}.tar.gz
Patch0:     parallel-build-fix.patch

BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  python3

%description
OpenCC is a library for converting characters and phrases between
Traditional Chinese and Simplified Chinese.

%package doc
Summary:    Documentation for OpenCC
Requires:   %{name} = %{version}-%{release}

%description doc
Doxygen generated documentation for OpenCC.


%package tools
Summary:    Command line tools for OpenCC
Requires:   %{name} = %{version}-%{release}

%description tools
Command line tools for OpenCC, including tools for conversion via CLI and
for building dictionaries.


%package devel
Summary:    Development files for OpenCC
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n OpenCC-ver.%{version}

%build
%cmake -DENABLE_GETTEXT:BOOL=ON -DBUILD_DOCUMENTATION:BOOL=ON
%cmake_build

%install
%cmake_install

%check
%ctest

#%find_lang %{name}

%ldconfig_scriptlets

%files
%doc AUTHORS LICENSE README.md
%{_libdir}/lib*.so.*
%{_datadir}/opencc/
%exclude %{_datadir}/opencc/doc

%files doc
%{_datadir}/opencc/doc

%files tools
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.1.1-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Add patch to fix parallel build issue

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug  4 2020 Peng Wu <pwu@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Peng Wu <pwu@redhat.com> - 1.0.5-3
- Security fix for CVE-2018-16982

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Peng Wu <pwu@redhat.com> - 1.0.5-1
- Update to 1.0.5

* Mon Mar 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0.3-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 16 2016 Peng Wu <pwu@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.2-3
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 19 2015 Peng Wu <pwu@redhat.com> - 1.0.2-2
- Fixes postun script

* Tue Jan  6 2015 Peng Wu <pwu@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Peng Wu <pwu@redhat.com> - 0.4.3-1
- Update to 0.4.3

* Mon Mar  4 2013 Peng Wu <pwu@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012  Peng Wu <pwu@redhat.com> - 0.3.0-4
- Fixes Download URL

* Mon Jul 23 2012  Peng Wu <pwu@redhat.com> - 0.3.0-3
- Fixes cmake

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012  Peng Wu <pwu@redhat.com> - 0.3.0-1
- Update to 0.3.0, and fixes ctest

* Wed Feb  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.2.0-6
- Drop unnessary ExclusiveArch directive

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011  Peng Wu <pwu@redhat.com> - 0.2.0-4
- Change i386 to i686

* Wed Nov 30 2011  Peng Wu <pwu@redhat.com> - 0.2.0-3
- Only build for i386 and x86_64

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 25 2010 BYVoid <byvoid.kcp@gmail.com> - 0.2.0-1
- Upstream release.
- Use CMake instead of autotools.

* Wed Sep 29 2010 jkeating - 0.1.2-2
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.2-1
- Upstream release.

* Thu Aug 12 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.1-1
- Upstream release.

* Thu Jul 29 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.0-1
- Upstream release.

* Fri Jul 16 2010 BYVoid <byvoid.kcp@gmail.com> - 0.0.4-1
- Initial release of RPM.

