# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Major version
%define major 1

Name:           libserf
Version:        1.3.10
Release:        12%{?dist}
Summary:        High-Performance Asynchronous HTTP Client Library
License:        Apache-2.0
URL:            https://serf.apache.org/
Source0:        https://archive.apache.org/dist/serf/serf-%{version}.tar.bz2
BuildRequires:  gcc, pkgconfig
BuildRequires:  apr-devel, apr-util-devel, krb5-devel, openssl-devel
BuildRequires:  zlib-devel, cmake
%ifnarch %ix86
BuildRequires: openssl, libfaketime
%endif
Patch0:         %{name}-norpath.patch
Patch1:         %{name}-1.3.9-errgetfunc.patch
Patch2:		%{name}-1.3.9-multihome.patch
Patch3:		%{name}-1.3.9-cmake.patch
Patch4:		%{name}-1.3.10-gssapi.patch

%description
The serf library is a C-based HTTP client library built upon the Apache 
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       apr-devel%{?_isa}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n serf-%{version} -p1
%ifnarch %ix86
pushd test/server
openssl req -x509 -newkey rsa:2048 -keyout serfrootcacert.pem -out serfrootcacert.pem -sha256 -days 3650 -nodes -subj "/C=BE/ST=Antwerp/L=Mechelen/O=In Serf we trust, Inc./OU=Test Suite Root CA/CN=Serf Root CA/emailAddress=serfrootca@example.com"
openssl req -x509 -newkey rsa:2048 -keyout serfcacert.pem -out serfcacert.pem -sha256 -days 3650 -nodes -subj "/C=BE/ST=Antwerp/L=Mechelen/O=In Serf we trust, Inc./OU=Test Suite CA/CN=Serf CA/emailAddress=serfca@example.com" -CA serfrootcacert.pem -CAkey serfrootcacert.pem
openssl req -x509 -newkey rsa:2048 -keyout serfserverkey.pem -out serfservercert.pem -sha256 -days 3650 -subj "/C=BE/ST=Antwerp/L=Mechelen/O=In Serf we trust, Inc./OU=Test Suite Server/CN=localhost/emailAddress=serfserver@example.com" -CA serfcacert.pem -CAkey serfcacert.pem -passout pass:serftest
faketime '2050-12-24 08:15:42' openssl req -x509 -out serfserver_future_cert.pem -subj "/C=BE/ST=Antwerp/L=Mechelen/O=In Serf we trust, Inc./OU=Test Suite Server/CN=localhost/emailAddress=serfserver@example.com" -CA serfcacert.pem -CAkey serfcacert.pem -key serfserverkey.pem -days 30 -passout pass:serftest -passin pass:serftest
faketime '1990-12-24 08:15:42' openssl req -x509 -out serfserver_expired_cert.pem -subj "/C=BE/ST=Antwerp/L=Mechelen/O=In Serf we trust, Inc./OU=Test Suite Server/CN=localhost/emailAddress=serfserver@example.com" -CA serfcacert.pem -CAkey serfcacert.pem -key serfserverkey.pem -days 30 -passout pass:serftest -passin pass:serftest
openssl req -x509 -newkey rsa:2048 -keyout serfclientkey.pem -out serfclientcert.pem -sha256 -days 3650 --CA serfcacert.pem --CAkey serfcacert.pem -subj "/C=BE/ST=Antwerp/L=Mechelen/O=In Serf we trust, Inc./OU=Test Suite Client/CN=Serf Client/emailAddress=serfclient@example.com" --nodes
openssl pkcs12 -export -in serfclientcert.pem -inkey serfclientkey.pem -out serfclientcert.p12 -passout pass:serftest
popd
%endif

%build
%cmake -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DGSSAPI=ON -DSKIP_STATIC=ON
%cmake_build

%install
%cmake_install

%if %{major} == 1
# Create compat stub library for cross-distro compatibility, since
# upstream unintentionally bumped the soname from libserf-1.so.0 to
# libserf-1.so.1 in 1.3.0. This can be deleted once major is 2.
# See: https://lists.apache.org/thread/o1vvpbv6pvw0bh8x5zqwyzbsqk4ntj7c
%define compatso libserf-1.so.1
%{__cc} %{optflags} -shared -o %{buildroot}%{_libdir}/%{compatso} \
       -Wl,-soname,%{compatso} -L%{buildroot}%{_libdir} -lserf-1
%endif

%check
%ifnarch %ix86
%ctest 
%else
true
%endif
grep '^Version: %{version}' %{buildroot}%{_libdir}/pkgconfig/serf-%{major}.pc

%ldconfig_scriptlets

%files
%license LICENSE NOTICE
%{_libdir}/*.so.*

%files devel
%doc CHANGES README design-guide.txt
%{_includedir}/serf-%{major}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/serf*.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 23 2025 Joe Orton  <jorton@redhat.com> - 1.3.10-11
- create compat libserf-1.so.1 for compatibility with upstream 1.x soname
- only ship serf-1.pc not serf.pc

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 13 2024 Joe Orton <jorton@redhat.com> - 1.3.10-7
- fix version in libserf.pc
- provide both libserf-1.pc and libserf.pc pkg-config files

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 07 2023 Tomas Korbar <tkorbar@redhat.com> - 1.3.10-3
- Add linking of gssapi to support Kerberos authentication
- Resolves: rhbz#2245095

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 06 2023 Tomas Korbar <tkorbar@redhat.com> - 1.3.10-1
- Update to 1.3.10
- Resolves: rhbz#2211498

* Sun Mar 12 2023 Tomas Korbar <tkorbar@redhat.com> - 1.3.9-28
- Change the License tag to the SPDX format

* Mon Feb 06 2023 Tomas Korbar <tkorbar@redhat.com> - 1.3.9-27
- Fix testsuite
- Resolves: rhbz#2166252

* Tue Jan 31 2023 Tomas Korbar <tkorbar@redhat.com> - 1.3.9-26
- Fix multihome server handling and backport cmake support
- Related: rhbz#1130328

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct  4 2021 Joe Orton <jorton@redhat.com> - 1.3.9-22
- fix build with OpenSSL 3.0

* Mon Sep 20 2021 Tomas Korbar <tkorbar@redhat.com> - 1.3.9-21
- Fix internal BIO control function

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.3.9-20
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-17
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Joe Orton <jorton@redhat.com> - 1.3.9-14
- revert broken IPv6 workaround

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Joe Orton <jorton@redhat.com> - 1.3.9-12
- fix IPv6 fallback behaviour (#1130328)
- use Python3 in tests

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.9-9
- Switch to %%ldconfig_scriptlets

* Mon Jul 02 2018 Nils Philippsen <nils@redhat.com> - 1.3.9-8
- use the Python 3 version of scons from Fedora 29 on

* Wed Mar  7 2018 Joe Orton <jorton@redhat.com> - 1.3.9-7
- add gcc to BR

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Joe Orton <jorton@redhat.com> - 1.3.9-2
- rebuild for OpenSSL 1.1.0

* Fri Sep 02 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.3.9-1
- Update to 1.3.9 (RHBZ #1372506)

* Sat Apr 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.3.8-3
- Add LDFLAGS provided by RPM

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 23 2015 Joe Orton <jorton@redhat.com> - 1.3.8-1
- update to 1.3.8 (#1155115, #1155392)
- remove RPATHs (#1154690)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Christopher Meng <rpm@cicku.me> - 1.3.7-1
- Update to 1.3.7

* Tue Jun 17 2014 Christopher Meng <rpm@cicku.me> - 1.3.6-1
- Update to 1.3.6

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Christopher Meng <rpm@cicku.me> - 1.3.5-1
- Update to 1.3.5

* Mon Feb 17 2014 Joe Orton <jorton@redhat.com> - 1.3.4-1
- Update to 1.3.4

* Tue Dec 10 2013 Joe Orton <jorton@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Wed Nov  6 2013 Joe Orton <jorton@redhat.com> - 1.3.2-1
- Update to 1.3.2
- Require krb5-devel for libgssapi (#1027011)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Christopher Meng <rpm@cicku.me> - 1.2.1-3
- SPEC cleanup.

* Thu Jun 13 2013 Christopher Meng <rpm@cicku.me> - 1.2.1-2
- Fix the permission of the library.

* Sun Jun 09 2013 Christopher Meng <rpm@cicku.me> - 1.2.1-1
- Initial Package.
