Summary:        A tool to manage Windows dynamic disks
Name:           libldm
Version:        0.2.5
Release:        1%{?dist}
License:        LGPLv3+ AND GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/mdbooth/libldm
Source0:        https://github.com/mdbooth/libldm/archive/%{name}-%{version}.tar.gz

BuildRequires:  %{_bindir}/xsltproc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  device-mapper-devel >= 1.0
BuildRequires:  glib2-devel >= 2.26.0
BuildRequires:  json-glib-devel >= 0.14.0
BuildRequires:  libtool
BuildRequires:  libuuid-devel
BuildRequires:  readline-devel
BuildRequires:  zlib-devel

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
%setup -q -n %{name}-%{name}-%{version}
sed -i -e 's/-Werror //' src/Makefile.*

# Disable doc generation.
sed -i -E 's@ docs/reference/\S+@@g' Makefile.am

autoreconf -i

%build
%configure --disable-static --disable-gtk-doc
make %{?_smp_mflags} V=1

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets

%files
%license COPYING.lgpl COPYING.gpl
%{_libdir}/*.so.*
%{_bindir}/ldmtool

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/ldm-1.0.pc

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.2.5-1
- Auto-upgrade to 0.2.5 - Azure Linux 3.0 - package upgrades

* Fri Apr 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.4-9
- Cleaning-up spec. License verified.

* Mon Mar 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.4-8
- Adding BR on '%%{_bindir}/xsltproc'.
- Disabled gtk doc generation to remove network dependency during build-time.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.4-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
