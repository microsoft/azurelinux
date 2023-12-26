%global debug_package %{nil}
%define soname 1
%define _source_payload w9.gzdio
%define _binary_payload w9.gzdio
Summary:        The Apache Kafka C library
Name:           librdkafka
Version:        2.3.0
Release:        1%{?dist}
# files like src/crc32c.c are under zlib license
# files like win32/wingetopt.c are under ISC
# files like src/rdfnv1a.c are under Public Domain
# files like src/rdhdrhistogram.c are under MIT
License:        BSD AND zlib AND ISC AND Public Domain AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/C and C++
URL:            https://github.com/edenhill/librdkafka
#Source0:        https://github.com/edenhill/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cyrus-sasl-devel
BuildRequires:  gcc >= 4.1
BuildRequires:  libstdc++-devel
BuildRequires:  openssl-devel
BuildRequires:  python3
BuildRequires:  zlib-devel

%description
librdkafka is the C/C++ client library implementation of the Apache Kafka protocol, containing both Producer and Consumer support.

%package -n     %{name}%{soname}
Summary:        The Apache Kafka C library
Group:          Development/Libraries/C and C++
Requires:       cyrus-sasl
Requires:       libstdc++
Requires:       openssl
Requires:       zlib

%description -n %{name}%{soname}
librdkafka is the C/C++ client library implementation of the Apache Kafka protocol, containing both Producer and Consumer support.

%package -n     %{name}-devel
Summary:        The Apache Kafka C library (Development Environment)
Group:          Development/Libraries/C and C++
Requires:       %{name}%{soname} = %{version}

%description -n %{name}-devel
librdkafka is the C/C++ client library implementation of the Apache Kafka protocol, containing both Producer and Consumer support.
This package contains headers and libraries required to build applications
using librdkafka.

%prep
%setup -q

# --install-deps will install missing dependencies that are not available
# through BuildRequires, such as libzstd, which will be linked statically.
%configure --install-deps --disable-lz4-ext

%build
cat config.log
make
examples/rdkafka_example -X builtin.features

%check
make check

%install
DESTDIR=%{buildroot} make install

%post   -n %{name}%{soname} -p /sbin/ldconfig
%postun -n %{name}%{soname} -p /sbin/ldconfig

%files -n %{name}%{soname}
%defattr(444,root,root)
%{_libdir}/librdkafka.so.%{soname}
%{_libdir}/librdkafka++.so.%{soname}
%defattr(-,root,root)
%doc %{_docdir}/librdkafka/README.md
%doc %{_docdir}/librdkafka/CONFIGURATION.md
%doc %{_docdir}/librdkafka/INTRODUCTION.md
%doc %{_docdir}/librdkafka/STATISTICS.md
%doc %{_docdir}/librdkafka/CHANGELOG.md
%license %{_docdir}/librdkafka/LICENSE
%doc %{_docdir}/librdkafka/LICENSES.txt

%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/librdkafka
%defattr(444,root,root)
%{_libdir}/librdkafka.a
%{_libdir}/librdkafka.so
%{_libdir}/librdkafka++.a
%{_libdir}/librdkafka++.so
%{_libdir}/librdkafka-static.a
%{_libdir}/pkgconfig/rdkafka++.pc
%{_libdir}/pkgconfig/rdkafka.pc
%{_libdir}/pkgconfig/rdkafka-static.pc
%{_libdir}/pkgconfig/rdkafka++-static.pc

%changelog
* Thu Dec 21 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 2.3.0-1
- Update to v2.3.0

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.8.2-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jan 13 2022 Henry Li <lihl@microsoft.com> - 1.8.2-1
- Upgrade to version 1.8.2
- Use python3 as BR instead of python2
- Add CHANGELOG.md to librdkafka1 package

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.0-3
- Removing the explicit %%clean stage.

* Tue Sep 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.0-2
- Updating BRs to pull in "cyrus-sasl-devel".

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.2.0-1
- Initial CBL-Mariner import from Magnus Edenhill Open Source (license: BSD).
- License verified.

* Thu Apr 09 2015 Eduard Iskandarov <e.iskandarov@corp.mail.ru> 0.8.6-0
- 0.8.6 simplify build process

* Fri Oct 24 2014 Magnus Edenhill <rdkafka@edenhill.se> 0.8.5-0
- 0.8.5 release

* Mon Aug 18 2014 Magnus Edenhill <rdkafka@edenhill.se> 0.8.4-0
- 0.8.4 release

* Mon Mar 17 2014 Magnus Edenhill <vk@edenhill.se> 0.8.3-0
- Initial RPM package
