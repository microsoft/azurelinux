# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global libpqos_ver 6.0.1
%global desc %{expand: \
This package provides basic support for Intel Resource Director Technology
including, Cache Monitoring Technology (CMT), Memory Bandwidth Monitoring
(MBM), Cache Allocation Technology (CAT), Code and Data Prioritization 
(CDP) and Memory Bandwidth Allocation (MBA).}

Name:		intel-cmt-cat
Version:	25.04
Release: 4%{?dist}
Summary:	Intel cache monitoring and allocation technology config tool

License:	BSD-3-Clause
URL: 		https://github.com/intel/intel-cmt-cat
Source: 	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:		0001-alter-install-paths.patch
Patch1:		0002-remove-build-and-install-of-examples.patch
Patch2:		0003-allow-debian-flags-to-be-added.patch

ExclusiveArch:	x86_64

BuildRequires:	gcc
BuildRequires:	make

%description
%{desc}

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel %{desc}

Development files.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%make_build

%install
%make_install BIN_DIR="%{buildroot}%{_bindir}" SBIN_DIR="%{buildroot}%{_sbindir}"

%ldconfig_scriptlets

%files
%license LICENSE
%doc ChangeLog README.md
%{_bindir}/membw
%{_sbindir}/pqos
%{_sbindir}/pqos-msr
%{_sbindir}/pqos-os
%{_sbindir}/rdtset
%{_libdir}/libpqos.so.6
%{_libdir}/libpqos.so.%{libpqos_ver}
%{_mandir}/man8/membw.8*
%{_mandir}/man8/pqos.8*
%{_mandir}/man8/pqos-msr.8*
%{_mandir}/man8/pqos-os.8*
%{_mandir}/man8/rdtset.8*

%files -n %{name}-devel
%{_includedir}/pqos.h
%{_libdir}/libpqos.so

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 29 2025 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 25.04-1
- Update to 25.04

* Wed Feb 12 2025 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 24.05-4
- Merging upstream patches and Rawhide FTBFS fix

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 26 2024 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 24.05-1
- Update to 24.05

* Wed Mar 13 2024 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 23.11.1-1
- Update to 23.11.1

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 23.11-1
- Update to 23.11

* Thu Aug 31 2023 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 23.08-1
- Update to 23.08

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 06 2023 Raghavan Kanagaraj <raghavan.kanagaraj@intel.com> - 4.5.0-1
- New release 4.5.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 12 2022 Marcel cornu <marcel.d.cornu@intel.com> - 4.4.1-1
- New release 4.4.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 1 2022 Khawar Abbasi <khawar.abbasi@intel.com> - 4.3.0-1
- New release 4.3.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 2020 Khawar Abbasi <khawar.abbasi@intel.com> - 4.1.0-1
- New release 4.1.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Khawar Abbasi <khawar.abbasi@intel.com> - 4.0.0-1
- New release 4.0.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 30 2019 Marcel cornu <marcel.d.cornu@intel.com> - 3.1.1-1
- New release 3.1.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Marcel cornu <marcel.d.cornu@intel.com> - 3.0.1-1
- New release 3.0.1

* Mon Feb 18 2019 Marcel cornu <marcel.d.cornu@intel.com> - 3.0.0-1
- New release 3.0.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Marcel cornu <marcel.d.cornu@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> 2.1.0-1
- New release 2.1.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Marcel cornu <marcel.d.cornu@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> - 2.0.0-1
- New release 2.0.0

* Thu Mar 08 2018 Marcel cornu <marcel.d.cornu@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> - 1.2.0-3
- Updated spec file with BuildRequires tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 29 2017 Marcel Cornu <marcel.d.cornu@intel.com>, Wojciech Andralojc <wojciechx.andralojc@intel.com> 1.2.0-1
- New release 1.2.0

* Thu Aug 3 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Marcel Cornu <marcel.d.cornu@intel.com> 1.1.0-1
- New release 1.1.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Marcel Cornu <marcel.d.cornu@intel.com> 1.0.1-1
- Spec file bug fixes

* Wed Jun 07 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Marcel Cornu <marcel.d.cornu@intel.com> 1.0.1-1
- new release
- bug fixes

* Fri May 19 2017 Aaron Hetherington <aaron.hetherington@intel.com>, Michal Aleksinski <michalx.aleksinski@intel.com> 1.0.0-1
- new release

* Tue Feb 14 2017 Aaron Hetherington <aaron.hetherington@intel.com> 0.1.5-1
- new release

* Mon Oct 17 2016 Aaron Hetherington <aaron.hetherington@intel.com> 0.1.5
- new release

* Tue Apr 19 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-3
- global typo fix
- small edits in the description

* Mon Apr 18 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-2
- LICENSE file added to the package

* Thu Apr 7 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-1
- initial version of the package
