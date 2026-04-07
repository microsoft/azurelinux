# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libsass
Version:        3.6.6
%global soname_version 1
Release:        5%{?dist}
Summary:        C/C++ port of the Sass CSS precompiler

# src/ast.hpp, src/utf8* is BSL-1.0
License:        MIT AND BSL-1.0
URL:            https://sass-lang.com/libsass
Source0:        https://github.com/sass/libsass/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Libsass is a C/C++ port of the Sass CSS precompiler. The original version was
written in Ruby, but this version is meant for efficiency and portability.

This library strives to be light, simple, and easy to build and integrate with
a variety of platforms and languages.

Libsass is just a library, but if you want to RUN libsass, install the sassc
package.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
export LIBSASS_VERSION=%{version}
autoreconf --force --install


%build
%configure --disable-static
%make_build


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -print -delete


%files
%license LICENSE
%doc Readme.md SECURITY.md
%{_libdir}/libsass.so.%{soname_version}{,.*}


%files devel
%{_includedir}/sass.h
%{_includedir}/sass2scss.h
%{_includedir}/sass/
%{_libdir}/libsass.so
%{_libdir}/pkgconfig/libsass.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.6.6-1
- Update to 3.6.6 (close RHBZ#1963228)

* Fri Jan 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.6.5-5
- Assorted minor packaging enhancements

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 26 2023 Aurelien Bompard <abompard@fedoraproject.org> - 3.6.5-1
- Version 3.6.5

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Marcel Plch <marcel.plch@protonmail.com> - 3.6.4-1
- Update to v3.6.4

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Nils Philippsen <nils@tiptoe.de> - 3.6.3-1
- version 3.6.3
- use source URL returning a properly named tarball

* Tue Oct 01 2019 Aurelien Bompard <abompard@fedoraproject.org> - 3.6.1-1
- Version 3.6.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Aurelien Bompard <abompard@fedoraproject.org> - 3.5.5-1
- Version 3.5.5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Aurelien Bompard <abompard@fedoraproject.org> - 3.5.4-3
- Add missing BR

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Marcel Plch <mplch@redhat.com> - 3.5.4-1
- Update to 3.5.4

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 14 2017 Miro Hrončok <mhroncok@redhat.com> - 3.4.5-4
- Export LIBSASS_VERSION, so it is possible to get it via libsass_version()

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Aurelien Bompard <abompard@fedoraproject.org> - 3.4.5-1
- version 3.4.5:  https://github.com/sass/libsass/releases/tag/3.4.5

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Aurelien Bompard <abompard@fedoraproject.org> - 3.4.1-1
- Version 3.4.1: https://github.com/sass/libsass/releases/tag/3.4.1

* Mon Dec 12 2016 Aurelien Bompard <abompard@fedoraproject.org> - 3.4.0-1
- Version 3.4.0: https://github.com/sass/libsass/releases/tag/3.4.0

* Wed Sep 30 2015 Aurelien Bompard <abompard@fedoraproject.org> - 3.3.6-1
- initial package
