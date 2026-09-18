# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       twolame
Version:    0.4.0
Release:    8%{?dist}
Summary:    Optimized MPEG Audio Layer 2 encoding library based on tooLAME
# build-scripts/install-sh is MIT/X11, build-scripts/{libtool.m4, ltmain.sh} are GPLv2+
License:    LGPL-2.1-or-later
URL:        http://www.twolame.org/

Source:     http://downloads.sourceforge.net/twolame/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  pkgconfig(sndfile) >= 1.0.0

Requires:   %{name}-libs%{?_isa} = %{version}-%{release}

%description
TwoLAME is an optimized MPEG Audio Layer 2 (MP2) encoder. It should be able to
be used as a drop-in replacement for LAME (a MPEG Layer 3 encoder). The frontend
takes very similar command line options to LAME, and the backend library has a
very similar API to LAME.

This package contains the command line frontend.

%package libs
Summary:    TwoLAME is an optimized MPEG Audio Layer 2 encoding library based on tooLAME
%description libs
TwoLAME is an optimized MPEG Audio Layer 2 (MP2) encoder. It should be able to
be used as a drop-in replacement for LAME (a MPEG Layer 3 encoder). The frontend
takes very similar command line options to LAME, and the backend library has a
very similar API to LAME.

This package contains the shared library.

%package devel
Summary:    Development tools for TwoLAME applications
Requires:   %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and documentation needed to develop
applications with TwoLAME.

%prep
%autosetup

%build
autoreconf -vif
%configure \
    --disable-static \
    --enable-sndfile
%make_build

%install
%make_install
rm %{buildroot}%{_libdir}/*.la

# Let RPM pick up the docs in the files section
rm -rf %{buildroot}%{_docdir}

%if 0%{?rhel} == 7
%ldconfig_scriptlets libs
%endif

%files
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files libs
%license COPYING
%{_libdir}/lib%{name}.so.*

%files devel
%doc doc/api.txt doc/html doc/psycho.txt doc/vbr.txt
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h

%changelog
* Tue Jul 29 2025 Wim Taymans <wtaymans@redhat.com> - 0.4.0-8
- Add Requires: to main package

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 19 2022 Simone Caronni <negativo17@gmail.com> - 0.4.0-1
- Update to 0.4.0.

* Fri Aug 19 2022 Simone Caronni <negativo17@gmail.com> - 0.3.13-21
- Clean up SPEC file.
- Trim changelog.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
