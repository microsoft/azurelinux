Name:           duktape
Version:        2.7.0
Release:        1%{?dist}
Summary:        Embeddable Javascript engine
Vendor:         Microsoft Corporation
License:        MIT
Url:            https://duktape.org/
Source0:        https://duktape.org/%{name}-%{version}.tar.xz
Patch0:         duktape-2.7.0-link-against-libm.patch
Distribution:   Mariner 
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  make
 
%description
Duktape is an embeddable Javascript engine, with a focus on portability and
compact footprint.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description    devel
Embeddable Javascript engine.

This package contains header files and libraries needed to develop
application that use %{name}.

%prep
%autosetup -p1

%build
%make_build -f Makefile.sharedlibrary INSTALL_PREFIX=%{_prefix} LIBDIR=/%{_lib}

%install
%make_install -f Makefile.sharedlibrary INSTALL_PREFIX=%{_prefix} LIBDIR=/%{_lib}

%files
%license LICENSE.txt
%doc AUTHORS.rst
%{_libdir}/libduktape.so.*
%{_libdir}/libduktaped.so.*

%files devel
%doc examples/ README.rst
%{_includedir}/duk_config.h
%{_includedir}/duktape.h
%{_libdir}/libduktape.so
%{_libdir}/libduktaped.so
%{_libdir}/pkgconfig/duktape.pc

%changelog
* Tue Jan 02 2024 Reuben Olinsky <reubeno@microsoft.com> 2.7.0-1
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- License verified.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 2.6.0-1
- Version 2.6.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 19 2018 Gwyn Ciesla <limburgher@gmail.com> - 2.2.0-2
- Macro corrections, dist tag.

* Fri Apr 13 2018 Gwyn Ciesla <limburgher@gmail.com> - 2.2.0-1
- Adapt to modern packaging guidelines.

* Mon Mar 19 2018 jk@lutty.net
- Initial package for fedora derived from Suse
