# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond optional_tests %{undefined rhel}

Name:		librdkafka
Version:	2.4.0
Release: 6%{?dist}
Summary:	The Apache Kafka C library

License:	Apache-2.0
URL:		https://github.com/edenhill/librdkafka
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	make
BuildRequires:	python3
BuildRequires:	libzstd-devel
BuildRequires:	lz4-devel
BuildRequires:	openssl-devel
BuildRequires:	cyrus-sasl-devel
BuildRequires:	zlib-devel
%if %{with optional_tests}
BuildRequires:	rapidjson-devel
%endif

Patch1: disable-ssl-engine.patch
Patch2: include-ossl-rand.patch

%description
Librdkafka is a C/C++ library implementation of the Apache Kafka protocol,
containing both Producer and Consumer support.
It was designed with message delivery reliability and high performance in mind,
current figures exceed 800000 messages/second for the producer and 3 million
messages/second for the consumer.

%package	devel
Summary:	The Apache Kafka C library (Development Environment)
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
librdkafka is a C/C++ library implementation of the Apache Kafka protocol,
containing both Producer and Consumer support.
This package contains headers and libraries required to build applications
using librdkafka.

%prep
%autosetup -p1

%build
# This package has a configure test which uses ASMs, but does not link the
# resultant .o files.  As such the ASM test is always successful, even on
# architectures were the ASM is not valid when compiling with LTO.
#
# -ffat-lto-objects is sufficient to address this issue.  It is the default
# for F33, but is expected to only be enabled for packages that need it in
# F34, so we use it here explicitly
%define _lto_cflags -flto=auto -ffat-lto-objects

%configure \
    --enable-zlib \
    --enable-zstd \
    --enable-lz4 \
    --enable-lz4-ext \
    --enable-ssl \
    --enable-gssapi \
    --enable-sasl \
    --disable-ssl-engine

%make_build

%check
make check

%install
%make_install
find %{buildroot} -name '*.a' -delete -print
find %{buildroot} -name '*-static.pc' -delete -print

%ldconfig_scriptlets

%files
%{_libdir}/librdkafka.so.*
%{_libdir}/librdkafka++.so.*
%doc README.md CONFIGURATION.md INTRODUCTION.md LICENSE LICENSES.txt STATISTICS.md CHANGELOG.md
%license LICENSE LICENSE.pycrc LICENSE.snappy

%files devel
%dir %{_includedir}/librdkafka
%{_includedir}/librdkafka/*
%{_libdir}/librdkafka.so
%{_libdir}/librdkafka++.so
%{_libdir}/pkgconfig/rdkafka.pc
%{_libdir}/pkgconfig/rdkafka++.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 19 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.0-4
- Avoid rapidjson dependency on RHEL

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 27 2024 Attila Lakatos <alakatos@redhat.com> - 2.4.0-1
- Rebase to 2.4.0
  resolves: rhbz#2222220
- Disable building with SSL engine support

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Attila Lakatos <alakatos@redhat.com> - 2.1.1-1
- Rebase to latest upstream version
  resolves: rhbz#1947184

* Wed May 31 2023 Attila Lakatos <alakatos@redhat.com> - 1.9.2-3
- Update License tag for SPDX
- Upstream sources claim that the Apache 2.0 is used

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 12 2022 Steve Traylen <steve.traylen@cern.ch> - 1.9.2-1
- Update to 1.9.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.6.1-3
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 08 2021 Attila Lakatos <alakatos@redhat.com> - 1.6.1-1
- Update to upstream 1.6.1
  resolves: rhbz#1932286

* Wed Feb 03 2021 Neal Gompa <ngompa@datto.com> - 1.6.0-1
- Update to upstream 1.6.0
  resolves: rhbz#1883910
- Enable all missing features
- Fix linking to external lz4 library
- Minor spec cleanups

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 09 2020 Zoltan Fridrich <zfridric@redhat.com> - 1.5.0-1
- Update to upstream 1.5.0
  resolves: rhbz#1818082

* Wed Sep 09 2020 Zoltan Fridrich <zfridric@redhat.com> - 1.3.0-6
- Switch BuildRequires from python2 to python3
  resolves: rhbz#1808329

* Fri Aug 21 2020 Jeff Law <law@redhat.com> - 1.3.0-5
- Re-enable LTO

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 1.3.0-3
- Disable LTO

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Michal Luscon <mluscon@gmail.com> - 1.3.0-1
- Update to upstream 1.3.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Javier Peña <jpena@redhat.com> - 0.11.6-1
- Update to upstream 0.11.6

* Mon Sep 17 2018 Michal Luscon <mluscon@gmail.com> - 0.11.5-1
- Update to upstream 0.11.5

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 20 2018 Michal Luscon <mluscon@gmail.com> - 0.11.4-1
- Update to upstream 0.11.4

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.11.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Michal Luscon <mluscon@gmail.com> - 0.11.3-1
- Update to upstream 0.11.3

* Thu Nov 02 2017 Michal Luscon <mluscon@gmail.com> - 0.11.1-1
- Update to upstream 0.11.1

* Thu Aug 31 2017 Michal Luscon <mluscon@gmail.com> - 0.11.0-1
- Update to 0.11.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 Radovan Sroka <rsroka@redhat.com> - 0.9.5-1
- Update to 0.9.4

* Sat Mar 11 2017 Michal Luscon <mluscon@gmail.com> - 0.9.4-1
- Update to 0.9.4
- enable lz4, ssl, sasl

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild


* Fri Nov 11 2016 Radovan Sroka <rsroka@redhat.com> 0.9.2-1
- 0.9.2 release
- package created
