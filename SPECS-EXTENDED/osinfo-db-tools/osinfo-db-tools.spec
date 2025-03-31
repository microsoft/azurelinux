Summary: 	Tools for managing the osinfo database
Name: 		osinfo-db-tools
Version:	1.12.0
Release: 	2%{?dist}	
License: 	GPL-2.0-or-later
Vendor:         Microsoft Corporation                                                         
Distribution:   Azure Linux
URL:		https://libosinfo.org
Source: 	https://releases.pagure.org/libosinfo/%{name}-%{version}.tar.xz

BuildRequires: meson
BuildRequires: gcc
BuildRequires: gettext-devel
BuildRequires: git
BuildRequires: glib2-devel
BuildRequires: libxml2-devel >= 2.6.0
BuildRequires: libxslt-devel >= 1.0.0
BuildRequires: libsoup-devel
BuildRequires: libarchive-devel
BuildRequires: json-glib-devel
BuildRequires: perl-podlators

#Required for testing purposes
BuildRequires: python3
BuildRequires: python3-pytest
BuildRequires: python3-requests

%description
This package provides tools for managing the osinfo database of
information about operating systems for use with virtualization.


%prep
%autosetup -S git

%build
%meson
%meson_build

%check
%meson_test

%install
%meson_install

%find_lang %{name}

%files -f %{name}.lang
%doc NEWS README
%license COPYING
%{_bindir}/osinfo-db-export
%{_bindir}/osinfo-db-import
%{_bindir}/osinfo-db-path
%{_bindir}/osinfo-db-validate
%{_mandir}/man1/osinfo-db-export.1*
%{_mandir}/man1/osinfo-db-import.1*
%{_mandir}/man1/osinfo-db-path.1*
%{_mandir}/man1/osinfo-db-validate.1*

%changelog
* Tue Dec 17 2024 Jyoti kanase <v-jykanase@microsoft.com> -  1.12.0 -2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.
