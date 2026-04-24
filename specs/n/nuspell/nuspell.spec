# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           nuspell
Version:        5.1.6
Release: 9%{?dist}
Summary:        Fast and safe spellchecking C++ library and command-line tool
License:        LGPL-3.0-or-later
URL:            https://nuspell.github.io
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

# Add DLL version suffix
Patch0:         nuspell-dllver.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libicu-devel
BuildRequires:  pandoc
BuildRequires:  catch-devel

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-icu

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-dlfcn
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-icu

Requires:       hunspell-en-US

%description
Nuspell is a fast and safe spelling checker software program. It is designed \
for languages with rich morphology and complex word compounding. Nuspell is \
written in modern C++ and it supports Hunspell dictionaries.


%package devel
Summary:        Development tools for %{name}
Requires:       libicu-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and developer docs for \
%{name}.


%package -n mingw32-%{name}
Summary:       MinGW Windows %{name} library
BuildArch:     noarch

%description -n mingw32-%{name}
MinGW Windows %{name} library.


%package -n mingw64-%{name}
Summary:       MinGW Windows %{name} library
BuildArch:     noarch

%description -n mingw64-%{name}
MinGW Windows %{name} library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{name}-%{version}


%build
%cmake
%cmake_build

%mingw_cmake -DBUILD_TESTING=OFF
%mingw_make_build


%install
%cmake_install
%mingw_make_install

# Drop docs from mingw packages
rm -rf %{buildroot}%{mingw32_docdir}/%{name}
rm -rf %{buildroot}%{mingw64_docdir}/%{name}
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}

%mingw_debug_install_post


%check
%ctest


%files
%doc AUTHORS CHANGELOG.md README.md
%license COPYING COPYING.LESSER
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.5*
%{_mandir}/man1/nuspell.1*

%files devel
%doc %{_docdir}/nuspell/
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so

%files -n mingw32-%{name}
%license COPYING COPYING.LESSER
%{mingw32_bindir}/%{name}.exe
%{mingw32_bindir}/lib%{name}-5.dll
%{mingw32_includedir}/%{name}/
%{mingw32_libdir}/cmake/%{name}/
%{mingw32_libdir}/pkgconfig/%{name}.pc
%{mingw32_libdir}/lib%{name}.dll.a


%files -n mingw64-%{name}
%license COPYING COPYING.LESSER
%{mingw64_bindir}/%{name}.exe
%{mingw64_bindir}/lib%{name}-5.dll
%{mingw64_includedir}/%{name}/
%{mingw64_libdir}/cmake/%{name}/
%{mingw64_libdir}/pkgconfig/%{name}.pc
%{mingw64_libdir}/lib%{name}.dll.a


%changelog
* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 5.1.6-8
- Rebuilt for icu 77.1

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 26 2025 Tim Landscheidt <tim@tim-landscheidt.de> - 5.1.6-6
- Fix description for mingw32-nuspell

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 5.1.6-4
- Rebuild (mingw-icu)

* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 5.1.6-3
- Rebuild (mingw-icu)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Sandro Mani <manisandro@gmail.com> - 5.1.6-1
- Update to 5.1.6

* Wed Jul 03 2024 Sandro Mani <manisandro@gmail.com> - 5.1.5-1
- Update to 5.1.5

* Mon Feb 05 2024 Sandro Mani <manisandro@gmail.com> - 5.1.4-5
- Rebuild (icu)

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 5.1.4-4
- Rebuild for ICU 74

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 09 2023 Sandro Mani <manisandro@gmail.com> - 5.1.4-1
- Update to 5.1.4

* Tue Aug 29 2023 Sandro Mani <manisandro@gmail.com> - 5.1.3-1
- Update to 5.1.3

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Sandro Mani <manisandro@gmail.com> - 5.1.2-6
- Rebuild (mingw-icu)

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 5.1.2-5
- Rebuilt for ICU 73.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Sandro Mani <manisandro@gmail.com> - 5.1.2-3
- Rebuild (mingw-icu)

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 5.1.2-2
- Rebuild for ICU 72

* Sat Oct 01 2022 Sandro Mani <manisandro@gmail.com> - 5.1.2-1
- Update to 5.1.2

* Tue Sep 13 2022 Sandro Mani <manisandro@gmail.com> - 5.1.1-1
- Update to 5.1.1

* Sat Aug 06 2022 Sandro Mani <manisandro@gmail.com> - 5.1.0-4
- Rebuild (mingw-icu)

* Thu Aug 04 2022 Sandro Mani <manisandro@gmail.com> - 5.1.0-3
- Add mingw subpackages

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.1.0-2
- Rebuilt for ICU 71.1

* Sun Jul 31 2022 Sandro Mani <manisandro@gmail.com> - 5.1.0-1
- Update to 5.1.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 16 2021 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 5.0.1-1
- Resolves: rhbz#2022753 nuspell-5.0.1 is available

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 14 2021 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 5.0.0-1 
- New release 5.0.0

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 4.2.0-5
- Rebuild for ICU 69

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 4.2.0-4
- Rebuild for ICU 69

* Wed Feb 03 2021 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 4.2.0-3 
- SPEC file cleanup

* Tue Feb 02 2021 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 4.2.0-2 
- Update the package summary 

* Tue Feb 02 2021 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 4.2.0-1 
- New release 4.2.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 3.1.2-5
- Rebuilt for Boost 1.75

* Fri Oct 09 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.1.2-4
- Resolves: rhbz#1865076: FTBFS in Fedora rawhide/f33
- updated make_build and make_install to cmake_build and cmake_install macro
  
* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.1.2-1 
- New release 3.1.2

* Sat May 30 2020 Jonathan Wakely <jwakely@redhat.com> - 3.1.1-3
- Rebuilt for Boost 1.73

* Wed May 20 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.1.1-2
- added tests

* Fri May 15 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.1.1-1
- Updated description and summary
- New release 3.1.1

* Mon Apr 27 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.1.0-1
- New release

* Fri Apr 3 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.0.0-5
- Added license files and doc files 

* Thu Mar 26 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.0.0-4
- renamed archive name 
- replaced cmake with %%cmake and make with %%make_build macro

* Mon Mar 02 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.0.0-3
- Update URL link
- Updated description
- Modified man page files macro

* Thu Feb 27 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.0.0-2
- Updated files to _libdir/cmake/nuspell/ instead of *.cmake files

* Tue Feb 25 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 3.0.0-1
- First release
