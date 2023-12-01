Summary:        library for laying out and rendering of text.
Name:           pango
Version:        1.45.5
Release:        1%{?dist}
License:        LGPLv2 OR MPLv1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://pango.org
Source0:        https://download.gnome.org/sources/pango/1.45/%{name}-%{version}.tar.xz
Patch0:         0001-skip-tests-which-are-known-to-fail.patch
BuildRequires:  cairo-devel
BuildRequires:  fontconfig
BuildRequires:  fontconfig-devel
BuildRequires:  freetype
BuildRequires:  glib-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  harfbuzz
BuildRequires:  harfbuzz-devel
BuildRequires:  libpng-devel
BuildRequires:  meson
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(fribidi)
Requires:       harfbuzz-devel

%description
Pango is a library for laying out and rendering of text, with an emphasis on internationalization. Pango can be used anywhere that text layout is needed, though most of the work on Pango so far has been done in the context of the GTK+ widget toolkit.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%meson

%meson_build

%install
%meson_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
%meson_test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*.so*
%{_datadir}/*
%{_libdir}/girepository-1.0/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun Apr 17 2022 Muhammad Falak <mwani@microsoft.com> - 1.45.5-1
- Bump version to 1.45.5 to address CVE-2019-1010238

* Thu Feb 03 2022 Muhammad Falak <mwani@microsoft.com> - 1.44.7-3
- Use 'meson test' instead of 'make check'
- Introduce patch to skip tests that are known to fail
- License verified

* Tue Apr 27 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.44.7-2
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 1.40.4-5: Skip test-layout test.

* Fri Apr 16 2021 Henry Li <lihl@microsoft.com> - 1.44.7-1
- Upgrade to version 1.44.7
- Switch to meson build and install
- Add meson and pkgconfig(fribidi) as build requirement
- Fix file section for pango
- Remove cairo from build requirement

* Sat May 09 00:21:07 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.40.4-4
- Added %%license line automatically

* Mon Apr 20 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.40.4-3
- Rename "freetype2" to "freetype".
- Remove sha1 macro.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.40.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.40.4-1
- Initial version
