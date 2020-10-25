Summary:        libxml++
Name:           libxml++
Version:        3.2.0
Release:        3%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://libxmlplusplus.sourceforge.net/
Source0:        https://ftp.gnome.org/pub/GNOME/sources/%{name}/3.2/%{name}-%{version}.tar.xz
BuildRequires:  glibmm24-devel
BuildRequires:  libxml2-devel
BuildRequires:  mm-common
BuildRequires:  pkg-config
Requires:       glibmm24
Requires:       libxml2

%description
This library provides a C++ interface to XML files. It uses libxml2 to access
the XML files, and in order to configure libxml++ you must have both libxml2 and
pkg-config installed.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation/Other
Requires:       %{name} = %{version}

%description doc
Documentation for %{name}

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
This library provides a C++ interface to XML files.

%prep
%setup -q

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -delete -print

%files
%license COPYING
%doc README
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/libxml++-3.0/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files doc
%{_docdir}/*
%{_datadir}/devhelp/*

%changelog
* Mon Oct 12 2020 Thomas Crain <thcrain@microsoft.com> - 3.2.0-3
- Remove .la files
- License verified

* Fri Jun 05 2020 Jonathan Chiu <jochi@microsoft.com> - 3.2.0-2
- Update dependency names

* Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> - 3.2.0-1
- Original version for CBL-Mariner
