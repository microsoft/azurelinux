Summary:        mm-common module
Name:           mm-common
Version:        1.0.5
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/C and C++
URL:            https://gtkmm.org
Source0:        https://ftp.gnome.org/pub/GNOME/sources/%{name}/1.0/%{name}-%{version}.tar.xz
%define debug_package %{nil}
BuildRequires:  pkg-config
BuildArch:      noarch

%description
The mm-common module provides the build infrastructure and utilities
shared among the GNOME C++ binding libraries.  It is only a required
dependency for building the C++ bindings from the gnome.org version
control repository.

%prep
%setup -q

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%license COPYING
%doc README.md OVERVIEW.md
%{_bindir}/*
%{_datadir}/%{name}/*
%{_datadir}/pkgconfig/*
%{_datadir}/aclocal/*
%{_docdir}/%{name}/*
%{_mandir}/*

%changelog
* Mon Jan 22 2024 Sindhu Karri <lakarri@microsoft.com> - 1.0.5-1
- Upgrade to 1.0.5

* Thu Feb 17 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.0.4-1
- Upgrading to v1.0.4

* Mon Oct 12 2020 Thomas Crain <thcrain@microsoft.com> - 1.0.0-3
- Update Source0 (removes need for libstdc++.tag file)
- Lint for Mariner style
- License verified

* Tue Jun 09 2020 Jonathan Chiu <jochi@microsoft.com> - 1.0.0-2
- Include libstdc++.tag in source files so package can be built offline

* Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner
