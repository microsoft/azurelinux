%global __remake_config 0

Summary:        Open Fabric Interfaces
Name:           libfabric
Version:        1.12.0
Release:        3%{?dist}
License:        BSD OR GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ofiwg/libfabric
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  libnl3-devel
BuildRequires:  make

%if %{__remake_config}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%endif

# RDMA not available on 32-bit ARM: #1484155
%ifnarch %{arm}
BuildRequires:  libibverbs-devel
BuildRequires:  librdmacm-devel
%endif

%description
OpenFabrics Interfaces (OFI) is a framework focused on exporting fabric
communication services to applications.  OFI is best described as a collection
of libraries and applications used to export fabric services.  The key
components of OFI are: application interfaces, provider libraries, kernel
services, daemons, and test applications.

Libfabric is a core component of OFI.  It is the library that defines and
exports the user-space API of OFI, and is typically the only software that
applications deal with directly.  It works in conjunction with provider
libraries, which are often integrated directly into libfabric.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%if %{__remake_config}
./autogen.sh
%endif
%configure --disable-static --disable-silent-rules
%make_build


%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print


%ldconfig_scriptlets


%files
%license COPYING
%{_bindir}/fi_info
%{_bindir}/fi_pingpong
%{_bindir}/fi_strerror
%{_libdir}/*.so.1*
%{_mandir}/man1/*.1*

%files devel
%license COPYING
%doc AUTHORS README
# We knowingly share this with kernel-headers and librdmacm-devel
# https://github.com/ofiwg/libfabric/issues/1277
%{_includedir}/rdma/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.12.0-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Dec 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12.0-2
- Removing BR on "infinipath-psm-devel" and "libpsm2-devel".
- Using the 1.12.0 final release version of the sources instead of the release candidate.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12.0-1
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sun Jan 31 2021 Honggang Li <honli@redhat.com> - 1.12.0-0.1
- Update to upstream release v1.12.0rc1

* Wed Dec 16 2020 Honggang Li <honli@redhat.com> - 1.11.2-1
- Update to upstream release v1.11.2

* Tue Dec 08 2020 Honggang Li <honli@redhat.com> - 1.11.2-0.1
- Update to upstream release v1.11.2rc1
- Resolves: bz1905751

* Sun Oct 11 2020 Honggang Li <honli@redhat.com> - 1.11.1
- Update to upstream release v1.11.1
- Resolves: bz1887069

* Thu Oct 08 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.11.1rc1-1
- Update to 1.11.1rc1 (#1886494)

* Sat Aug 15 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.11.0-1
- Update to 1.11.0 (#1869025)

* Tue Aug 04 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.11.0rc2-1
- Update to 1.11.0rc2 (#1866049)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0rc1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.11.0rc1-1
- Update to 1.11.0rc1 (#1859427)

* Sat May 09 2020 Honggang Li <honli@redhat.com> - 1.10.1-1
- Update to upstream release v1.10.1
- Resolves: bz1833620

* Fri Apr 24 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.10.0-1
- Update to 1.10.0 (#1827815)

* Sun Apr 12 2020 Honggang Li <honli@redhat.com> - 1.10.0rc2-1
- Update to 1.10.0rc2

* Fri Apr 03 2020 Honggang Li <honli@redhat.com> - 1.10.0rc1-1
- Update to 1.10.0rc1
- Resolves: bz1820096

* Mon Mar 09 2020 Honggang Li <honli@redhat.com> - 1.9.1-1
- Update to 1.9.1
- Resolves: bz1811269

* Sun Feb 16 2020 Honggang Li <honli@redhat.com> - 1.9.1rc1-1
- Update to 1.9.1rc
- Resolves: bz1803485

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Honggang Li <honli@redhat.com> - 1.9.0
- Update to 1.9.0
- Resolves: bz1775865

* Thu Oct 24 2019 Honggang Li <honli@redhat.com> - 1.9.0rc1-1
- Update to 1.9.0rc1
- Resolves: bz1751860

* Fri Sep 06 2019 Honggang Li <honli@redhat.com> - 1.8.0-3
- Fix two segment fault issues
- Resolves: bz1749608

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 29 2019 Honggang Li <honli@redhat.com> - 1.8.0
- Update to 1.8.0

* Mon Jun 17 2019 Honggang Li <honli@redhat.com> - 1.8.0rc1
- Update to 1.8.0rc1
- Resolves: 1720773

* Mon Jun 10 2019 Honggang Li <honli@redhat.com> - 1.7.2rc2
- Update to 1.7.2rc2
- Resolves: bz1689783

* Mon Apr  8 2019 Orion Poplawski <orion@nwra.com> - 1.7.1-1
- Update to 1.7.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 31 2019 Honggang Li <honli@redhat.com> - 1.7.0-1
- Rebase libfabric to latest upstream release v1.7.0
- Resolves: bz1671189

* Mon Oct  8 2018 Honggang Li <honli@redhat.com> - 1.6.2-1
- Rebase libfabric to latest upstream release v1.6.2
- Resolves: bz1637334

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Honggang Li <honli@redhat.com> - 1.6.1-1
- Rebase to latest upstream release 1.6.1
- Resolves: bz1550404

* Thu Mar 15 2018 Orion Poplawski <orion@nwra.com> - 1.6.0-1
- Update to 1.6.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 23 2017 Adam Williamson <awilliam@redhat.com> - 1.4.2-5
- Disable RDMA support on 32-bit ARM (#1484155)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.4.2-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 11 2017 Orion Poplawski <orion@cora.nwra.com> - 1.4.2-1
- Update to 1.4.2

* Mon Apr 10 2017 Orion Poplawski <orion@cora.nwra.com> - 1.4.1-1
- Update to 1.4.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 3 2016 Orion Poplawski <orion@cora.nwra.com> - 1.4.0-1
- Update to 1.4.0

* Thu Jul 21 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.0-3
- Rebuild for aarch64 glibc update

* Tue May 31 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.0-2
- Use psm/psm2 if possible on Fedora (bug #1340988)

* Tue Apr 12 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.0-1
- Update to 1.3.0

* Wed Mar 9 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.0-1
- Update to 1.2.0
- Use psm/psm2 if possible on EL
- Add upstream patch to fix non-x86 builds

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 26 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.0-1
- Update to 1.1.0

* Mon Jul 20 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0.0-1
- Initial package
