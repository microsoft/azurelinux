Name:           libsass
Version:        3.6.3
Release:        3%{?dist}
Summary:        C/C++ port of the Sass CSS precompiler

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://sass-lang.com/libsass
Source0:        https://github.com/sass/libsass/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  gcc-c++

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
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%license LICENSE
%doc Readme.md SECURITY.md
%{_libdir}/*.so.*

%files devel
%license LICENSE
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6.3-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
