# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libharu
Version:        2.4.5
# NOTE - sover is major.minor so minor updates will require rebuilds of dependent packages 
%global sover %(v=%{version}; echo ${v%.*})
Release: 2%{?dist}
Summary:        C library for generating PDF files
License:        zlib-acknowledgement
URL:            http://libharu.org
Source0:        https://github.com/libharu/libharu/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel

%description
libHaru is a library for generating PDF files. 
It is free, open source, written in ANSI C and cross platform.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%cmake -DLIBHPDF_STATIC=NO

%cmake_build

%install
%cmake_install

%ldconfig_scriptlets

%files
%license LICENSE
%doc README.md
%{_libdir}/libhpdf.so.%{sover}*
%{_datadir}/%{name}

%files devel
%{_includedir}/*
%{_libdir}/libhpdf.so

%changelog
* Sat Aug 02 2025 Orion Poplawski <orion@nwra.com> - 2.4.5-1
- Update to 2.4.5

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Orion Poplawski <orion@nwra.com> - 2.4.3-1
- Use SPDX License tag

* Mon Oct 17 2022 Dmitrij S. Kryzhevich <kryzhev@ispms.ru> - 2.4.3-1
- Update to 2.4.3
- Drop .version patch.

* Fri Oct 07 2022 Dmitrij S. Kryzhevich <kryzhev@ispms.ru> - 2.4.2-3
- Update version path (upstream PR: https://github.com/libharu/libharu/pull/241)

* Thu Oct 06 2022 Dmitrij S. Kryzhevich <kryzhev@ispms.ru> - 2.4.2-2
- Add version patch.

* Tue Oct 04 2022 Orion Poplawski <orion@nwra.com> - 2.4.2-1
- Update to 2.4.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Dmitrij S. Kryzhevich <kryzhev@ispms.ru> - 2.3.0-12
- Fix for new cmake macros.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-11
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 11 2020 Dmitrij S. Kryzhevich <kryzhev@ispms.ru> - 2.3.0-9
- Update to RC3
- Apply 157 and 187 upstream github pull requests. See rhbz #1833318

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Dmitrij S. Kryzhevich <kryzhev@ispms.ru> - 2.3.0-1
- Update to new 2.3.0.
- Drop png15 patch.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jul 30 2016 Dmitrij S. Kryzhevich <kryzhev@ispms.ru> - 2.2.1-8
- Fix BR: glibc-headers -> gcc (RHBZ #1230474).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Tom Callaway <spot@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1
- Fix compile with libpng 1.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.1.0-4
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Mar 23 2010 Alex71 <nyrk71@gmail.com> 2.1.0-2
- put libhpdf.so in the devel package and libhpdf-2.1.0.so in the main one
- removed duplicated README and CHANGES from devel package
- fixed "E: empty-debuginfo-package" with --enable-debug flag in configure
- removed INSTALL file
- added demo/ directory in doc (devel only) as doc 
* Sat Mar 20 2010 Alex71 <nyrk71@gmail.com> 2.1.0-1
- First release for Fedora
