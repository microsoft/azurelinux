Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           jose
Version:        14
Release:        3%{?dist}
Summary:        Tools for JSON Object Signing and Encryption (JOSE)

License:        Apache-2.0
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  jansson-devel >= 2.10
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  git-core
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  asciidoc
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
%autosetup -S git

%build
%meson
%meson_build

%install
rm -rf %{buildroot}
%meson_install
rm -rf %{buildroot}/%{_libdir}/lib%{name}.la

%check
%meson_test

%ldconfig_scriptlets -n lib%{name}

%files
%{_bindir}/%{name}
%{_mandir}/man1/jose*.1*
%license COPYING

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
* Mon May 12 2025 Archana Shettigar <v-shettigara@microsoft.com> - 14-3
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 23 2024 Sergio Arroutbi <sarroutb@redhat.com> - 14-1
- Update to release 14

* Wed Apr 03 2024 Sergio Correia <scorreia@redhat.com> - 13-1
- Update to release 13

* Fri Feb 02 2024 Sergio Arroutbi <sarroutb@redhat.com> - 12-1
- Update to release v12

* Tue Jan 30 2024 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 11-11
- Fix test when using zlib-ng

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 11-4
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 07 2021 Sergio Correia <scorreia@redhat.com> - 11-2
- Update sources file to v11.

* Fri May 07 2021 Sergio Correia <scorreia@redhat.com> - 11-1
- Update to new jose upstream release, v11.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Tom Stellard <tstellar@redhat.com> - 10-8
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
