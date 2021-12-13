Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           cjose
Version:        0.6.1
Release:        6%{?dist}
Summary:        C library implementing the Javascript Object Signing and Encryption (JOSE)

License:        MIT
URL:            https://github.com/cisco/cjose
Source0:  	https://github.com/cisco/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

Patch1: concatkdf.patch

BuildRequires:  gcc
BuildRequires:  doxygen
BuildRequires:  openssl-devel
BuildRequires:  jansson-devel
BuildRequires:  check-devel

%description
Implementation of JOSE for C/C++


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure
%make_build


%install
%make_install
find %{buildroot} -name '*.a' -exec rm -f {} ';'
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%check
make check || (cat test/test-suite.log; exit 1)

%files
%license LICENSE
%doc CHANGELOG.md README.md
%doc /usr/share/doc/cjose
%{_libdir}/*.so.*


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/cjose.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug  2 2018  <jdennis@redhat.com> - 0.6.1-2
- fix concatkdf big endian architecture problem.
  Upstream issue #77.

* Wed Aug  1 2018  <jdennis@redhat.com> - 0.6.1-1
- upgrade to latest upstream 0.6.1

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 0.5.1-1
- Initial packaging
