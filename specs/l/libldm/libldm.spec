# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libldm
Version:        0.2.5
Release: 3%{?dist}%{?extra_release}
Summary:        A tool to manage Windows dynamic disks

# Automatically converted from old format: LGPLv3+ and GPLv3+ - review is highly recommended.
License:        LGPL-3.0-or-later AND GPL-3.0-or-later
URL:            https://github.com/mdbooth/libldm 
Source0:        https://github.com/mdbooth/libldm/archive/%{name}-%{version}.tar.gz

# All upstream post-0.2.5
Patch:          0001-Add-example-systemd-unit-file.patch
Patch:          0002-ldmtool-fix-NULL-pointer-dereference.patch
Patch:          0003-Add-ability-to-override-device-mapper-UUID.patch
Patch:          0004-src-Fix-declaration-of-ldm_new.patch
Patch:          0005-Update-gtkdocize.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  autoconf, automake, libtool
BuildRequires:  glib2-devel >= 2.26.0
BuildRequires:  json-glib-devel >= 0.14.0
BuildRequires:  device-mapper-devel >= 1.0
BuildRequires:  zlib-devel libuuid-devel readline-devel
BuildRequires:  gtk-doc


%description
libldm is a library for managing Microsoft Windows dynamic disks, which use
Microsoft's LDM metadata. It can inspect them, and also create and remove
device-mapper block devices which can be mounted. It includes ldmtool, which
exposes this functionality as a command-line tool.

libldm is released under LGPLv3+. ldmtool is released under GPLv3+.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n %{name}-%{name}-%{version}
sed -i -e 's/-Werror //' src/Makefile.*
gtkdocize
autoreconf -i


%build
%configure --disable-static --enable-gtk-doc
%make_build


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%files
%license COPYING.lgpl COPYING.gpl
%{_libdir}/*.so.*
%{_bindir}/ldmtool
%{_mandir}/man1/ldmtool.1.gz


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/ldm-1.0.pc
%{_datadir}/gtk-doc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Feb 06 2025 Richard W.M. Jones <rjones@redhat.com> - 0.2.5-1
- New upstream version 0.2.5
- Add some post-0.2.5 patches from upstream.
- Some modernisation of the spec file.

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 0.2.4-17
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.4-4
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 0.2.4-1
- New upstream version 0.2.4.
- Remove all upstream patches.
- Build from github tarball.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.2.3-10
- Rebuild for readline 7.x

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.3-6
- Add patch to fix Werror=format-security issues

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.3-4
- Add gtk-doc to fix FTBFS
- Add patch for deprecated g_type_init

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 24 2012 Matthew Booth <mbooth@redhat.com> - 0.2.3-1
- Initial packaging
