%define majver %(echo %{version} | cut -d. -f 1-2)
Summary:        libxml++
Name:           libxml++
Version:        5.0.3
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://libxmlplusplus.sourceforge.net/
Source0:        https://ftp.gnome.org/pub/GNOME/sources/%{name}/%{majver}/%{name}-%{version}.tar.xz
BuildRequires:  glibmm-devel
BuildRequires:  libxml2-devel
BuildRequires:  mm-common
BuildRequires:  pkg-config
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
Requires:       glibmm
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
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/libxml++-%{majver}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files doc
%{_docdir}/*
%{_datadir}/devhelp/*

%changelog
* Wed Dec 20 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 5.0.3-1
- Update to v5.0.3

* Tue Feb 15 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.0.1-2
- Update Requires: to point at glibmm, rather than glibmm24 (removed)

* Wed Jan 26 2022 Henry Li <lihl@microsoft.com> - 5.0.1-1
- Upgrade to version 5.0.1
- Add doxygen, graphviz, libxslt and docbook-style-xsl as BR
- Use macro to represent major version

* Mon Oct 12 2020 Thomas Crain <thcrain@microsoft.com> - 3.2.0-3
- Remove .la files
- License verified

* Fri Jun 05 2020 Jonathan Chiu <jochi@microsoft.com> - 3.2.0-2
- Update dependency names

* Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> - 3.2.0-1
- Original version for CBL-Mariner
