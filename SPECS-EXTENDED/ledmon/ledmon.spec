Summary: Enclosure LED Utilities
Name: ledmon
Version: 1.1.0
Release: 2%{?dist}
License: GPL-2.0-only AND LGPL-2.1-or-later AND GPL-3.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://github.com/intel/ledmon
Source0: https://github.com/intel/ledmon/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: autoconf automake
BuildRequires: autoconf-archive
BuildRequires: gcc make
BuildRequires: libconfig-devel
BuildRequires: libtool
BuildRequires: pciutils-devel
BuildRequires: sg3_utils-devel
# Needed for pkgconfig usage.
BuildRequires: pkgconfig
BuildRequires: systemd
# Needed for the udev dependency.
BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros

Obsoletes: ledctl = 0.1-1
Provides: ledctl = %{version}-%{release}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

%description
The ledmon and ledctl are user space applications design to control LED
associated with each slot in an enclosure or a drive bay. There are two
types of system: 2-LED system (Activity LED, Status LED) and 3-LED system
(Activity LED, Locate LED, Fail LED). User must have root privileges to
use this application.

%package        libs
Summary:        Runtime library files for %{name}
Requires:       pciutils-libs
Requires:       sg3_utils-libs

%description    libs
The %{name}-libs package contains runtime libraries for applications
that use %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pciutils-devel
Requires:       sg3_utils-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1
autoreconf -fiv

%build
%configure --enable-systemd=yes --enable-library --disable-static
%make_build

%install
%make_install

%post
%systemd_post ledmon.service

%preun
%systemd_preun ledmon.service

%postun
%systemd_postun_with_restart ledmon.service

%files
%license COPYING
%doc README.md
%{_sbindir}/ledctl
%{_sbindir}/ledmon
%{_mandir}/*/*
%{_unitdir}/ledmon.service

%files libs
%{_libdir}/*.so.*
%{_libdir}/libled.la

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Mar 11 2025 Aninda Pradhan <v-anipradhn@microsoft.com> - 1.1.0-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Mon Nov 11 2024 Jan Macku <jamacku@redhat.com> - 1.1.0-1
- update to 1.1.0
- drop Packit config

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 27 2024 Jan Macku <jamacku@redhat.com> - 1.0.0-1
- update to 1.0.0
- package shared ledmon library by Tony Asleson

* Wed Feb 14 2024 Lukáš Zaoral <lzaoral@redhat.com> - 0.97-6
- fix incorrect License field syntax

* Fri Feb 09 2024 Dan Horák <dan@danny.cz> - 0.97-5
- rebuilt for sg3_utils 1.48

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 16 2023 Jan Macku <jamacku@redhat.com> - 0.97-2
- use correct SPDX license

* Tue May 16 2023 Jan Macku <jamacku@redhat.com> - 0.97-1
- update to 0.97

* Tue Apr 11 2023 Lukáš Zaoral <lzaoral@redhat.com> - 0.96-7
- migrate to SPDX license format

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.96-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Lukáš Zaoral <lzaoral@redhat.com> - 0.96-5
- Fix build on Rawhide
- Remove explicit library runtime dependency as suggested by rpmlint
- Modernise used macros

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.96-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 27 2022 Jan Macku <jamacku@redhat.com> - 0.96-3
- Rebuild

* Mon Jun 27 2022 Jan Macku <jamacku@redhat.com> - 0.96-2
- Use systemd-rpm-macros to handle ledmon.service (#2101300)

* Wed Jun 01 2022 Jan Macku <jamacku@redhat.com> - 0.96-1
- update to 0.96 (#2092134)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.95-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.95-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 06 2021 Tomas Bzatek <tbzatek@redhat.com> - 0.95-4
- rebuilt for sg3_utils 1.46

* Mon Feb 22 2021 Jan Macku <jamacku@redhat.com> - 0.95-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Feb 02 2021 Jan Macku <jamacku@redhat.com> - 0.95-2
- drop perl dependency

* Tue Feb 02 2021 Jan Macku <jamacku@redhat.com> - 0.95-1
- clean up spec based on RHEL 8.4.0 spec
- remove -Werror=format-truncation=1 from configure
- update to 0.95 (#1880599)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.92-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.92-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Dan Horák <dan@danny.cz> - 0.92-4
- rebuilt for sg3_utils 1.45 (#1809392)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 15 2019 Jan Synáček <jsynacek@redhat.com> - 0.92-1
- update to 0.92 (#1699783)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug  7 2018 Jan Synáček <jsynacek@redhat.com> - 0.90-3
- fix manpage generation (#1611428)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 14 2018 Jan Synáček <jsynacek@redhat.com> - 0.90-1
- update to 0.90 (#1555099)

* Mon Feb 26 2018 Jan Synáček <jsynacek@redhat.com> - 0.80-6
- use distribution LDFLAGS during build (#1548551)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec  6 2016 Jan Synáček <jsynacek@redhat.com> - 0.80-1
- Update to 0.80 (#1401924)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.79-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 28 2013 Michal Sekletar <msekleta@redhat.com> - 0.79-1
- update to 0.79

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 Michal Sekletar <msekleta@redhat.com> - 0.78-1
- Update to 0.78

* Fri Apr 19 2013 Jan Synáček <jsynacek@redhat.com> - 0.77-1
- Update to 0.77
- Documentation enhancements

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 07 2013 Jan Synáček <jsynacek@redhat.com> - 0.75-1
- Update to 0.75 and drop upstreamed patch

* Thu Nov 15 2012 Jan Synáček <jsynacek@redhat.com> - 0.74-3
- Some coverity fixes

* Fri Oct 19 2012 Jan Synáček <jsynacek@redhat.com> - 0.74-2
- Require sg3_utils-libs

* Mon Aug 13 2012 Jan Synáček <jsynacek@redhat.com> - 0.74-1
- Update to 0.74
- Resolves: #847072

* Tue Aug 07 2012 Jan Synáček <jsynacek@redhat.com> - 0.72-1
- Update to 0.72 and update patch
- Resolves: #846018

* Wed Jul 25 2012 Jan Synáček <jsynacek@redhat.com> - 0.40-1
- Update to 0.40
- Resolves: #838086
- Make spec fedora-review friendly

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 05 2012 Jan Synáček <jsynacek@redhat.com> - 0.32-1
- Update to 0.32

* Fri Feb 10 2012 Jan Synáček <jsynacek@redhat.com> - 0.31-1
- Update to 0.31

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Jiri Moskovcak <jmoskovc@redhat.com> 0.1-2
- renamed to ledmon, because ledctl is taken

* Fri Jan 07 2011 Jiri Moskovcak <jmoskovc@redhat.com> 0.1-1
- initial release
