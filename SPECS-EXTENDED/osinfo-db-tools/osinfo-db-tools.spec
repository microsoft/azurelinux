
%define with_mingw 0
%if 0%{?fedora}
    %define with_mingw 0%{!?_without_mingw:1}
%endif

Summary: 	Tools for managing the osinfo database
Name: 		osinfo-db-tools
Version:	1.12.0
Release: 	1%{?dist}	
License: 	GPL-2.0-or-later
Vendor:         Microsoft Corporation                                                         
Distribution:   Azure Linux
URL:		 https://libosinfo.org
Source: 	https://releases.pagure.org/libosinfo/%{name}-%{version}.tar.xz

BuildRequires: meson
BuildRequires: gcc
BuildRequires: gettext-devel
BuildRequires: git
BuildRequires: glib2-devel
BuildRequires: libxml2-devel >= 2.6.0
BuildRequires: libxslt-devel >= 1.0.0
%if 0%{?fedora} > 36 || 0%{?rhel} > 9
BuildRequires: libsoup3-devel
%else
BuildRequires: libsoup-devel
%endif
BuildRequires: libarchive-devel
BuildRequires: json-glib-devel
BuildRequires: perl-podlators

#Required for testing purposes
BuildRequires: python3
BuildRequires: python3-pytest
BuildRequires: python3-requests

%if %{with_mingw}
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc
BuildRequires: mingw32-binutils
BuildRequires: mingw32-glib2
BuildRequires: mingw32-json-glib
BuildRequires: mingw32-libxml2
BuildRequires: mingw32-libxslt
BuildRequires: mingw32-libarchive
BuildRequires: mingw32-libsoup

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc
BuildRequires: mingw64-binutils
BuildRequires: mingw64-glib2
BuildRequires: mingw64-json-glib
BuildRequires: mingw64-libxml2
BuildRequires: mingw64-libxslt
BuildRequires: mingw64-libarchive
BuildRequires: mingw64-libsoup
%endif

%description
This package provides tools for managing the osinfo database of
information about operating systems for use with virtualization

%if %{with_mingw}
%package -n mingw32-osinfo-db-tools
Summary: %{summary}
BuildArch: noarch
Requires: pkgconfig

%description -n mingw32-osinfo-db-tools
This package provides tools for managing the osinfo database of
information about operating systems for use with virtualization

%package -n mingw64-osinfo-db-tools
Summary: %{summary}
BuildArch: noarch
Requires: pkgconfig

%description -n mingw64-osinfo-db-tools
This package provides tools for managing the osinfo database of
information about operating systems for use with virtualization

%{?mingw_debug_package}
%endif

%prep
%autosetup -S git

%build
%meson
%meson_build

%if %{with_mingw}
%mingw_meson
%mingw_ninja
%endif

%check
%meson_test

%install
%meson_install

%find_lang %{name}

%if %{with_mingw}
%mingw_ninja_install

# Manpages don't need to be bundled
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/man
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/man

%mingw_debug_install_post

%mingw_find_lang osinfo-db-tools
%endif

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

%if %{with_mingw}
%files -n mingw32-osinfo-db-tools -f mingw32-osinfo-db-tools.lang
%doc NEWS README
%license COPYING
%{mingw32_bindir}/osinfo-db-export.exe
%{mingw32_bindir}/osinfo-db-import.exe
%{mingw32_bindir}/osinfo-db-path.exe
%{mingw32_bindir}/osinfo-db-validate.exe

%files -n mingw64-osinfo-db-tools -f mingw64-osinfo-db-tools.lang
%doc NEWS README
%license COPYING
%{mingw64_bindir}/osinfo-db-export.exe
%{mingw64_bindir}/osinfo-db-import.exe
%{mingw64_bindir}/osinfo-db-path.exe
%{mingw64_bindir}/osinfo-db-validate.exe
%endif

%changelog
* Tue Dec 17 2024 Jyoti kanase <v-jykanase@microsoft.com> -  1.12.0 -1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.
