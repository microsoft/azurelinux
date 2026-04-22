# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 5e9be272f96e00f15a2f3c5f8ba7e124862aec38
%global date 20160216
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

Name:           aribb24
Version:        1.0.3%{!?tag:^%{date}git%{shortcommit0}}
Release: 4%{?dist}
Summary:        A library for ARIB STD-B24
License:        LGPL-3.0-only
URL:            https://github.com/nkoriyama/%{name}

%if 0%{?tag:1}
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0:        %url/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  libpng-devel

%description
A library for ARIB STD-B24, decoding JIS 8 bit characters and parsing MPEG-TS
stream.

%package devel
Summary:        Development files for the ARIB STD-B24 library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files and headers for the ARIB STD-B24 library.

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

%build
autoreconf -vif
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/lib%{name}.la

# Pick docs in the files section
rm -fr %{buildroot}%{_docdir}/%{name}

%files
%license COPYING
%doc README.md
%{_libdir}/lib%{name}.so.0
%{_libdir}/lib%{name}.so.0.0.0

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3^20160216git5e9be27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3^20160216git5e9be27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Sep 12 2024 Simone Caronni <negativo17@gmail.com> - 1.0.3^20160216git5e9be27-1
- First build.
