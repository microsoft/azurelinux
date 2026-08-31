# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libnftnl
Version:        1.2.9
Release:        2%{?dist}
Summary:        Library for low-level interaction with nftables Netlink's API over libmnl

License:        GPL-2.0-or-later
URL:            https://netfilter.org/projects/libnftnl/
Source0:        %{url}/files/%{name}-%{version}.tar.xz
Source1:        %{url}/files/%{name}-%{version}.tar.xz.sig
Source2:        coreteam-gpg-key-0xD70D1A666ACF2B21.txt

BuildRequires:  libmnl-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gnupg2

%description
A library for low-level interaction with nftables Netlink's API over libmnl.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%configure --disable-static --disable-silent-rules
%make_build

%check
%make_build check

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%files
%doc COPYING
%{_libdir}/*.so.*

%files devel
%{_libdir}/libnft*.so
%{_libdir}/pkgconfig/libnftnl.pc
%{_includedir}/libnftnl

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 15 2025 Phil Sutter <psutter@redhat.com> - 1.2.9-1
- New version 1.2.9

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 1.2.8-2
- Rebuild for Jansson 2.14
  (https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/3PYINSQGKQ4BB25NQUI2A2UCGGLAG5ND/)

* Fri Oct 04 2024 Phil Sutter <psutter@redhat.com> - 1.2.8-1
- new version

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Phil Sutter <psutter@redhat.com> - 1.2.7-1
- new version 1.2.7

* Fri Jul 05 2024 Phil Sutter <psutter@redhat.com> - 1.2.6-8
- Add missing build dependency

* Fri Jul 05 2024 Phil Sutter <psutter@redhat.com> - 1.2.6-7
- Verify tarball GPG signature

* Tue Jul 02 2024 Phil Sutter <psutter@redhat.com> - 1.2.6-6
- Upstream dropped JSON parsing support in version 1.1.2, drop remains
- Update upstream tarball source URL
- Drop references to libnftables-devel package which retired in 2014
- Add upstream-identified fixes

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 11 2023 Phil Sutter <psutter@redhat.com> - 1.2.6-3
- Convert license to SPDX format

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Phil Sutter <psutter@redhat.com> - 1.2.6-1
- Drop outdated libnftables provides, it might clash with the new
  nftables-provided libnftables at some point in future
- Backport one late fix from upstream
- new version 1.2.6

* Fri Mar 10 2023 Phil Sutter <psutter@redhat.com> - 1.2.5-1
- new version 1.2.5

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Phil Sutter <psutter@redhat.com> - 1.2.4-1
- new version 1.2.4

* Wed Aug 10 2022 Phil Sutter <psutter@redhat.com> - 1.2.3-1
- New version 1.2.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 07 2022 Phil Sutter <psutter@redhat.com> - 1.2.2-1
- Update to 1.2.2. Fixes rhbz#2094429

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 27 2021 Kevin Fenzi <kevin@scrye.com> - 1.2.1-1
- Update to 1.2.1. Fixes rhbz#2024580

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 01 2021 Phil Sutter <psutter@redhat.com> - 1.2.0-1
- Update to 1.2.0. Fixes rhbz#1964391

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 1.1.9-1
- Update to 1.1.9. Fixes rhbz#1916855

* Sat Oct 31 2020 Kevin Fenzi <kevin@scrye.com> - 1.1.8-1
- Update to 1.1.8. Fixes bug #1891597

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.1.7-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jun 05 2020 Phil Sutter <psutter@redhat.com> - 1.1.7-1
- Rebase onto upstream version 1.1.7

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 04 2019 Phil Sutter <psutter@redhat.com> - 1.1.5-1
- Update to 1.1.5. Fixes bug #1778850

* Fri Aug 23 2019 Kevin Fenzi <kevin@scrye.com> - 1.1.4-1
- Update to 1.1.4. Fixes bug #1743175

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 16 2019 Kevin Fenzi <kevin@scrye.com> - 1.1.3-1
- Update to 1.1.3. Fixes bug #1714231

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Kevin Fenzi <kevin@scrye.com> - 1.1.1-5
- Fix FTBFS bug #1604620

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Phil Sutter <psutter@redhat.com> - 1.1.1-3
- Disable running tests/test-script.sh again, it breaks builds on big endian.

* Thu Jun 14 2018 Phil Sutter <psutter@redhat.com> - 1.1.1-2
- Drop leftover mxml dependency. Fixes bug #1594107
- Enable running tests/test-scrip.sh again when checking.

* Sat Jun 09 2018 Kevin Fenzi <kevin@scrye.com> - 1.1.1-1
- Update to 1.1.1. Fixes bug #1589403

* Fri May 04 2018 Kevin Fenzi <kevin@scrye.com> - 1.1.0-1
- Update to 1.1.0. Fixes bug #1574094

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Kevin Fenzi <kevin@scrye.com> - 1.0.9-1
- Update to 1.0.9. Fixes bug #1531004

* Sat Oct 21 2017 Kevin Fenzi <kevin@scrye.com> - 1.0.8-4
- Update to 1.0.8. Fixes bug #1504350

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Kevin Fenzi <kevin@scrye.com> - 1.0.7-1
- Update to 1.0.7. Fixes bug #1406201

* Wed Jun 01 2016 Kevin Fenzi <kevin@scrye.com> - 1.0.6-1
- Update to 1.0.6. Fixes bug #1341384

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 17 2015 Kevin Fenzi <kevin@scrye.com> 1.0.5-1
- Update to 1.0.5. Fixes bug #1263684

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 26 2014 Kevin Fenzi <kevin@scrye.com> 1.0.3-1
- Update to final 1.0.3

* Wed Sep 03 2014 Kevin Fenzi <kevin@scrye.com> 1.0.3-0.1.20140903git
- Update to 20140903 git snapshot

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 25 2014 Kevin Fenzi <kevin@scrye.com> 1.0.2-1
- Update to 1.0.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Kevin Fenzi <kevin@scrye.com> 1.0.1-1.
- Update to 1.0.1

* Sun Mar 30 2014 Kevin Fenzi <kevin@scrye.com> 1.0.0-1.20140330git
- Update to 20140330 snapshot
- Sync version to be a post 1.0.0 snapshot

* Wed Mar 26 2014 Kevin Fenzi <kevin@scrye.com> 0-0.10.20140326git
- Update to 20140326 snapshot

* Fri Mar 07 2014 Kevin Fenzi <kevin@scrye.com> 0-0.9.20140307git
- Update to 20140307 snapshot

* Sat Jan 25 2014 Kevin Fenzi <kevin@scrye.com> 0-0.8.20140125git
- Update to 20140125

* Thu Jan 23 2014 Kevin Fenzi <kevin@scrye.com> 0-0.7.20140122git
- Add obsoletes/provides to devel subpackage as well. 

* Wed Jan 22 2014 Kevin Fenzi <kevin@scrye.com> 0-0.6.20140122git
- Renamed libnftnl
- Update to 20140122 snapshot.

* Sat Jan 18 2014 Kevin Fenzi <kevin@scrye.com> 0-0.5.20140118git
- Update to 20140118 snapshot.

* Sat Jan 11 2014 Kevin Fenzi <kevin@scrye.com> 0-0.4.20140111git
- Update to 20140111 snapshot. 
- Enable xml (some tests stll fail, but it otherwise builds ok)

* Mon Dec 02 2013 Kevin Fenzi <kevin@scrye.com> 0-0.3.20131202git
- Update to 20131202 snapshot, switch to upstream snapshot repo instead of git checkouts. 

* Mon Dec 02 2013 Kevin Fenzi <kevin@scrye.com> 0-0.2
- Fixes from review. 

* Sat Nov 30 2013 Kevin Fenzi <kevin@scrye.com> 0-0.1
- initial version for Fedora review
