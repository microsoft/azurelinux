Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           jose
Version:        10
Release:        7%{?dist}
Summary:        Tools for JSON Object Signing and Encryption (JOSE)

License:        ASL 2.0
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  jansson-devel >= 2.10
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
Requires: lib%{name}%{?_isa} = %{version}-%{release}

%description
José is a command line utility for performing various tasks on JSON
Object Signing and Encryption (JOSE) objects. José provides a full
crypto stack including key generation, signing and encryption.

%package -n lib%{name}
Summary:        Library implementing JSON Object Signing and Encryption
Conflicts:      jansson < 2.10
Provides:       lib%{name}-openssl = %{version}-%{release}
Obsoletes:      lib%{name}-openssl < %{version}-%{release}
Provides:       lib%{name}-zlib = %{version}-%{release}
Obsoletes:      lib%{name}-zlib < %{version}-%{release}

%description -n lib%{name}
This package contains a C library for performing JOSE operations.

%package -n lib%{name}-devel
Summary:        Development files for lib%{name}
Requires:       lib%{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       jansson-devel
Provides:       lib%{name}-openssl-devel = %{version}-%{release}
Obsoletes:      lib%{name}-openssl-devel < %{version}-%{release}
Provides:       lib%{name}-zlib-devel = %{version}-%{release}
Obsoletes:      lib%{name}-zlib-devel < %{version}-%{release}

%description -n lib%{name}-devel
This package contains development files for lib%{name}.

%prep
%setup -q

%build
%if 0%{?rhel}
%__sed -i 's|libcrypto >= 1\.0\.2|libcrypto >= 1\.0\.1|' configure
%endif
%configure --disable-openmp
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
rm -rf %{buildroot}/%{_libdir}/lib%{name}.la

%check
make %{?_smp_mflags} check

%ldconfig_scriptlets -n lib%{name}

%files
%{_bindir}/%{name}
%{_mandir}/man1/jose*.1*

%files -n lib%{name}
%license COPYING
%{_libdir}/lib%{name}.so.*

%files -n lib%{name}-devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/jose*.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Nathaniel McCallum <npmccallum@redhat.com> - 10-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 16 2017 Nathaniel McCallum <npmccallum@redhat.com> - 9-1
- New upstream release

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 8-1
- New upstream release

* Fri Mar 17 2017 Nathaniel McCallum <npmccallum@redhat.com> - 7-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Nathaniel McCallum <npmccallum@redhat.com> - 6-4
- Add a conflicts on old versions of jansson

* Fri Nov 11 2016 Nathaniel McCallum <npmccallum@redhat.com> - 6-3
- Fix build on big-endian platforms (fix already upstream)

* Thu Nov 10 2016 Nathaniel McCallum <npmccallum@redhat.com> - 6-2
- Rebuild to pick up new architectures

* Tue Oct 25 2016 Nathaniel McCallum <npmccallum@redhat.com> - 6-1
- New upstream release

* Fri Oct 14 2016 Nathaniel McCallum <npmccallum@redhat.com> - 5-1
- New upstream release

* Fri Sep 23 2016 Nathaniel McCallum <npmccallum@redhat.com> - 4-1
- New upstream release

* Wed Sep 21 2016 Nathaniel McCallum <npmccallum@redhat.com> - 3-1
- Initial package
