# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libfido2

Version:        1.16.0
Release:        3%{?dist}
Summary:        FIDO2 library

License:        BSD-2-Clause
URL:            https://github.com/Yubico/%{name}
Source0:        https://developers.yubico.com/%{name}/Releases/%{name}-%{version}.tar.gz
Source1:        https://developers.yubico.com/%{name}/Releases/%{name}-%{version}.tar.gz.sig
#
# Yubico does not provide a central gpg keyring download file. Instead, they
# provide a list of individuals that release code and their fingerprints at
#   https://developers.yubico.com/Software_Projects/Software_Signing.html
# One must import all the keys and then export into the keyfile.
#   gpg2 --homedir /tmp/ --receive-keys "keyid0"
#   gpg2 --homedir /tmp/ --receive-keys "keyid1"
#   gpg2 --homedir /tmp/ --export --armor --output yubico-release-gpgkeys.asc
#
Source2:        yubico-release-gpgkeys.asc

BuildRequires:  gnupg2
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig(libcbor)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)

%description
%{name} is an open source library to support the FIDO2 protocol.  FIDO2 is
an open authentication standard that consists of the W3C Web Authentication
specification (WebAuthn API), and the Client to Authentication Protocol
(CTAP).  CTAP is an application layer protocol used for communication
between a client (browser) or a platform (operating system) with an external
authentication device (for example the Yubico Security Key).

################################################################################

%package devel

Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{name}-devel contains development libraries and header files for %{name}.

################################################################################

%package -n fido2-tools

Summary:        FIDO2 tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n fido2-tools
FIDO2 command line tools to access and configure a FIDO2 compliant
authentication device.

################################################################################


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n %{name}-%{version}


%build
%cmake
%cmake_build


%install
%cmake_install
# Remove static files per packaging guidelines
find %{buildroot} -type f -name "*.a" -delete -print


%check
%ctest \-E regress_cred


%files
%doc NEWS README.adoc
%license LICENSE
%{_libdir}/libfido2.so.1{,.*}

%files devel
%{_libdir}/pkgconfig/libfido2.pc
%{_libdir}/libfido2.so
%{_includedir}/fido.h
%{_includedir}/fido
%{_mandir}/man3/fido_*.3{,.*}
%{_mandir}/man3/eddsa_pk_*.3{,.*}
%{_mandir}/man3/es256_pk_*.3{,.*}
%{_mandir}/man3/es384_pk_*.3{,.*}
%{_mandir}/man3/rs256_pk_*.3{,.*}

%files -n fido2-tools
%{_bindir}/fido2-assert
%{_bindir}/fido2-cred
%{_bindir}/fido2-token
%{_mandir}/man1/fido2-assert.1{,.*}
%{_mandir}/man1/fido2-cred.1{,.*}
%{_mandir}/man1/fido2-token.1{,.*}


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.16.0-2
- Rebuild for libcbor 0.12.0

* Fri Jul 04 2025 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.16.0-1
- Update to 1.16.0 release ( resolves: rhbz#2364444 )
- Document how to create the gpg releases keyfile for verification 

* Fri May 09 2025 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.15.0-8
- Rebuilt for libcbor 0.12.0

* Fri May 09 2025 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.15.0-7
- Rebuild for libcbor 0.12.0

* Fri Mar 21 2025 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.15.0-6
- Rebuilt for libcbor 0.12.0

* Wed Mar 19 2025 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.15.0-5
- Rebuilt for libcbor 0.12.0

* Mon Mar 17 2025 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.15.0-4
- Rebuilt for libcbor 0.12.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 14 2024 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.15.0-1
- Update to 1.15.0 release ( resolves: rhbz#2292292 )

* Mon Feb 05 2024 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.14.0-4
- Rebuilt for libcbor 0.11.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.14.0-1
- Update to 1.14.0 release ( resolves: rhbz#2249531 )

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 07 2023 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.13.0-2
- Rebuilt for libcbor 0.10.2

* Tue Feb 21 2023 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.13.0-1
- Update to 1.13.0 release ( resolves: rhbz#2172297 )
- Perform some deglobing of files per packaging guidelines

* Tue Feb 21 2023 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.12.0-5
- Fix sources file for keyring move

* Fri Feb 10 2023 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.12.0-4
- Move keyring to SCM per packaging guidelines

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 12 2022 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.12.0-2
- exclude (future invalid crypto policy) test (resolves: rhbz#2141852)

* Fri Sep 23 2022 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.12.0-1
- 1.12.0 release (resolves: rhbz#2129268)
- remove unneeded BR for hidapi-hidraw
- change to SPDX license (BSD -> BSD-2-Clause)
- add check section

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.11.0-2
- Rebuilt for epel8 (resolves: rhbz#2059387)

* Wed May 04 2022 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.11.0-1
- 1.11.0 release (resolves: rhbz#2081706)

* Wed Feb 16 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.10.0-3
- Drop dependency on systemd-udev (#2018913)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.10.0-1
- 1.10.0 release (#2041621)

* Thu Oct 28 2021 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.9.0-1
- 1.9.0 release (#2018007)

* Fri Sep 17 2021 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.8.0-4
- migrate from BR: foo-devel to BR: pkgconfig(foo)

* Wed Sep 15 2021 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.8.0-3
- Apply upstream patches for OpenSSL 3.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.8.0-2
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.8.0-1
- 1.8.0 release (#1985131)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 01 2021 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.7.0-1
- 1.7.0 release (#1944499)
- Remove workaround for gcc-11 (fixed upstream)
- add new BR zlib-devel

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.6.0-1
- 1.6.0 release (#1910101)

* Thu Dec 17 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.5.0-4
- Use gpgverify macro and ascii armored yubico release keys

* Wed Nov 04 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.5.0-3
- add BR make
- fix typo in changelog day (Tuu -> Thu) to make rpmlint happy

* Thu Oct 29 2020 Jeff Law <law@redhat.com> 1.5.0-2
- Work around false positive diagnostic in gcc-11

* Fri Sep 11 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.5.0-1
- 1.5.0 release (#1824326)
- include upstream patch to fix 32-bit platform compile, reported at
  https://github.com/Yubico/libfido2/issues/210

* Tue Sep 08 2020 Kalev Lember <klember@redhat.com> - 1.4.0-4
- Rebuilt for libcbor soname bump

* Wed Jul 29 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.4.0-3
- adapt to new Fedora cmake rpm macros

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 15 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.4.0-1
- 1.4.0 release (#1824326)

* Sat Apr 11 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.1-2
- change to require u2f-hidraw-policy only if systemd-udev (#1823002)

* Thu Feb 20 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.1-1
- 1.3.1 release

* Mon Dec 16 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.0-3
- use yubico corp release site for sources and gpg signature

* Sat Dec 14 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.0-2
- packaging cleanups

* Sat Nov 30 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.0-1
- 1.3.0 release

* Mon Jul 29 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.2.0-1
- 1.2.0 release

* Sat May 11 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.1.0-1
- 1.1.0 release

* Fri Apr 05 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.0.0-2
- include backported upstream patches for compiler dependencies and soname version
- modify libdir glob to meet newer packaging recommendations

* Thu Mar 21 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.0.0-1
- 1.0.0 release

* Mon Jan 07 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.4.0-1
- 0.4.0 release

* Wed Sep 12 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-1
- 0.3.0 release

* Fri Sep 07 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.8.20180907git878fcd8
- update to upstream master

* Thu Sep 06 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.7.20180906gitff7ece8
- update to upstream master

* Wed Sep 05 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.6.20180905gitcb4951c
- update to upstream master

* Tue Sep 04 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.5.20180904git2b5f0d0
- update to upstream master

* Mon Aug 27 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.4.20180827git9d178b2
- Update to upstream master

* Thu Aug 23 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.3.20180823git0f40181
- Update to upstream master

* Tue Aug 21 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.2.20180821gitfff65a4
- Update to upstream master

* Wed Aug 08 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.1.20180808git5be8903
- Update to new spec

