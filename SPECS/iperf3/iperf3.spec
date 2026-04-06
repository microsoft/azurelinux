# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           iperf3
Version:        3.19.1
Release:        1%{?dist}
Summary:        Measurement tool for TCP/UDP bandwidth performance

# src/cjson.{c,h} and src/net.{c,h} are MIT
# part of the code is dtoa
# part of src/net.c is BSD-3-Clause-HP
# src/queue.h is BSD-3-Clause
# src/units.{c.h} is NCSA
# src/portable_endian.h is LicenseRef-Fedora-Public-Domain
License:        BSD-3-Clause-LBNL AND MIT AND dtoa AND BSD-3-Clause AND NCSA AND LicenseRef-Fedora-Public-Domain
URL:            https://github.com/esnet/iperf
Source0:        %{url}/archive/%{version}/iperf-%{version}.tar.gz
# Add some reporting: https://github.com/esnet/iperf/pull/1278
Patch0:         1278-rebase.patch
BuildRequires:  libuuid-devel
BuildRequires:  gcc
BuildRequires:  lksctp-tools-devel
BuildRequires:  openssl-devel
BuildRequires:  make

%description
Iperf is a tool to measure maximum TCP bandwidth, allowing the tuning of
various parameters and UDP characteristics. Iperf reports bandwidth, delay
jitter, data-gram loss.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n iperf-%{version} -p1

%build
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall -C src INSTALL_DIR="%{buildroot}%{_bindir}"
mkdir -p %{buildroot}%{_mandir}/man1
rm -f %{buildroot}%{_libdir}/libiperf.la

%files
%doc README.md LICENSE RELNOTES.md
%{_mandir}/man1/iperf3.1.gz
%{_mandir}/man3/libiperf.3.gz
%{_bindir}/iperf3
%{_libdir}/*.so.*

%files          devel
%{_includedir}/iperf_api.h
%{_libdir}/*.so

%changelog
* Sat Jul 26 2025 Kevin Fenzi <kevin@scrye.com> - 3.19.1-1
- Update to 3.19.1. Fixes rhbz#2383609

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Kevin Fenzi <kevin@scrye.com> - 3.19-1
- Update to 3.19. Fixes rhbz#2366951

* Sat Jan 18 2025 Kevin Fenzi <kevin@scrye.com> - 3.18-3
- Rebase upstream patch from https://github.com/esnet/iperf/pull/1278

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Dec 21 2024 Kevin Fenzi <kevin@scrye.com> - 3.18-1
- Update to 3.18. Fixes rhbz#2332370

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 27 2024 Kevin Fenzi <kevin@scrye.com> - 3.17.1-1
- Update to 3.17.1
- Fixes CVE-2024-26306

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 06 2023 Jonathan Wright <jonathan@almalinux.org> - 3.16-1
- Update to 3.16 rhbz#2252641

* Tue Oct 17 2023 Jonathan Wright <jonathan@almalinux.org> - 3.15-1
- Update to 3.15 rhbz#2239199 rhbz#2244708

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Jonathan Wright <jonathan@almalinux.org> - 3.14-2
- update spec file syntax

* Tue Jul 18 2023 Jonathan Wright <jonathan@almalinux.org> - 3.14-1
- update to 3.14 rhbz#2183634
- Security fix for CVE-2023-38403 rhbz#2222204 rhbz#2223495

* Mon Feb 20 2023 Jonathan Wright <jonathan@almalinux.org> - 3.13-1
- update to 3.13 rhbz#2170949

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Jonathan Wright <jonathan@almalinux.org> - 3.12-1
- Update to 3.12 rhbz#2131418

* Tue Sep 27 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 3.11-3
- Backport PR#1278: Report number of reorder_seen. Fixes: rhbz#2063959

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Feb 20 2022 Kevin Fenzi <kevin@scrye.com> - 3.11-1
- Update to 3.11. Fixes rhbz#2050303

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.10.1-3
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Kevin Fenzi <kevin@scrye.com> - 3.10.1-1
- Update to 3.10.1. Fixes rhbz#1965275

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Oct 31 2020 Kevin Fenzi <kevin@scrye.com> - 3.9-5
- Update to 3.9. Fixes bug #1846161

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 19 2020 Michal Ruprich <mruprich@redhat.com> - 3.7-4
- Add openssl-devel to BuildRequires to enable authentization of client

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 22 2019 Kevin Fenzi <kevin@scrye.com> - 3.7-1
- Update to 3.7. Fixes bug #1723020

* Tue Feb 26 2019 Tomas Korbar <tkorbar@redhat.com> - 3.6-5
- Add lksctp-tools-devel to BuildRequires
- Fix bug #1647385

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Kevin Fenzi <kevin@scrye.com> - 3.6-3
- Fix FTBFS bug #1604377 by adding BuildRequires: gcc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Kevin Fenzi <kevin@scrye.com> - 3.6-1
- Update to 3.6. Fixes bug #1594995

* Sat Mar 03 2018 Kevin Fenzi <kevin@scrye.com> - 3.5-1
- Update to 3.5. Fixes bug #1551166

* Fri Feb 16 2018 Kevin Fenzi <kevin@scrye.com> - 3.4-1
- Upgrade to 3.4. Fixes bug #1545468

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 04 2017 Kevin Fenzi <kevin@scrye.com> - 3.3-1
- Update to 3.3. Fixes bug #1508669

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Kevin Fenzi <kevin@scrye.com> - 3.2-1
- Update to 3.2. Fixes bug #1465195

* Wed Mar 08 2017 Kevin Fenzi <kevin@scrye.com> - 3.1.7-1
- Update to 3.1.7. Fixes bug #1429901

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Kevin Fenzi <kevin@scrye.com> - 3.1.6-1
- Update to 3.1.6. Fixes bug #1418879

* Fri Jan 13 2017 Kevin Fenzi <kevin@scrye.com> - 3.1.5-1
- Update to 3.1.5. Fixes bug #1412848

* Sat Nov 05 2016 Kevin Fenzi <kevin@scrye.com> - 3.1.4-1
- Update to 3.1.4. Fixes bug #1390396

* Wed Jun 08 2016 Kevin Fenzi <kevin@scrye.com> - 3.1.3-1
- Update to 3.1.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1b3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 08 2015 Susant Sahani <ssahani@gmail.com> 3.1b3
- Update to 3.1b3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Susant Sahani <ssahani@gmail.com> 3.0.11-1
- Update to 3.0.11

* Sat Dec 20 2014 Susant Sahani <ssahani@redhat.com> 3.0.10-1
- Update to 3.0.10

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Susant Sahani <ssahani@redhat.com> 3.0.6-1
- Update to 3.0.6

* Thu Jun 19 2014 Susant Sahani <ssahani@redhat.com> 3.0.5-1
- Update to 3.0.5

* Tue Jun 10 2014 Susant Sahani <ssahani@redhat.com> - 3.0.3-5
- fix compilation BZ #1106803

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 2 2014 François Cami <fcami@fedoraproject.org> - 3.0.3-3
- Drop static library support (#1081486).
- iperf3-devel subpackage must require iperf3.
- iperf3-devel should only contain the unversioned shared library.
- Call ldconfig since we are installing a shared library now.
- Removed INSTALL file.

* Wed Apr 2 2014 Susant Sahani <ssahani@redhat.com> 3.0.3-2
- Moved static library to devel section only .

* Sun Mar 30 2014 Susant Sahani <ssahani@redhat.com> 3.0.3-1
- Update to 3.0.3 and added devel rpm support

* Tue Mar 11 2014 Susant Sahani <ssahani@redhat.com> 3.0.2-1
- Update to 3.0.2

* Tue Jan 14 2014 Susant Sahani <ssahani@redhat.com> 3.0.1-1
- Update to 3.0.1

* Fri Oct 25 2013 Steven Roberts <strobert@strobe.net> 3.0-1
- Update to 3.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.5.b5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 04 2013 Kevin Fenzi <kevin@scrye.com> 3.0-0.4.b5
- Update to 3.0b5

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.3.b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.2.b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.1.b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 06 2011 G.Balaji <balajig81@gmail.com> 3.0b4-2
- Changed the Spec name, removed static libs generation and devel
- package.

* Sat Mar 26 2011 G.Balaji <balajig81@gmail.com> 3.0b4-1
- Initial Version
