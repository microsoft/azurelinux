# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%global commit 97d2850af13c339369093b78abe5265845d78220
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           linenoise
Version:        1.0
Release:        13.20200312git%{shortcommit}%{?dist}
Summary:        Minimal replacement for readline
License:        BSD-2-Clause
URL:            https://github.com/antirez/linenoise
Source0:        https://github.com/antirez/linenoise/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:         %{name}-build-shared-lib.patch
Patch1:         %{name}-symbol-visibility.patch
Patch2:         %{name}-add-linenoiseWasInterrupted-symbol.patch
Patch3:         %{name}-CVE-2025-9810.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires: make

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description
Linenoise is a replacement for the readline line-editing library with the goal 
of being smaller.

%description devel
This package contains files needed for developing software that uses
%{name}.

%prep
%setup -q -n %{name}-%{commit}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
LIBDIR="%{_libdir}" INCLUDEDIR="%{_includedir}" CFLAGS="%{optflags}" make %{?_smp_mflags}

%install
LIBDIR="%{_libdir}" INCLUDEDIR="%{_includedir}" CFLAGS="%{optflags}" make %{?_smp_mflags} DESTDIR="%{buildroot}" install

%files
%license LICENSE
%doc README.markdown
%{_libdir}/liblinenoise.so.*

%files devel
%doc example.c
%{_includedir}/linenoise.h
%{_libdir}/liblinenoise.so

%ldconfig_scriptlets

%changelog
* Sun Sep 07 2025 Garry T. Williams <gtwilliams@gmail.com> 1.0-13.20200312git97d2850
- Fix CVE-2025-9810

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-12.20200312git97d2850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-11.20200312git97d2850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Songsong Zhang <U2FsdGVkX1@gmail.com> - 1.0-10.20200312git97d2850
- Export linenoiseWasInterrupted symbol

* Tue Sep 17 2024 Songsong Zhang <U2FsdGVkX1@gmail.com> - 1.0-9.20200312git97d2850
- Add linenoiseWasInterrupted symbol

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-8.20200312git97d2850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-7.20200312git97d2850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6.20200312git97d2850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-5.20200312git97d2850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 05 2023 Garry T. Williams <gtwilliams@gmail.com> 1.0-5.20200312git97d2850
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4.20200312git97d2850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3.20200312git97d2850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2.20200312git97d2850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Aug 08 2021 Dan Callaghan <djc@djc.id.au> - 1.0-1.20200312git97d2850
- update to latest upstream version by original author antirez

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-19.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-18.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-17.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-16.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-15.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-14.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-13.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-12.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-11.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-10.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-9.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-8.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-7.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-6.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-5.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-4.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-3.git7946e2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Dan Callaghan <dcallagh@redhat.com> - 0-2.git7946e2c
- added licensing clarifications

* Tue Jan 08 2013 Dan Callaghan <dcallagh@redhat.com> - 0-1.git7946e2c
- initial version
