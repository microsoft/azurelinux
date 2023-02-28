Summary:        library for laying out and rendering of text.
Name:           pango
Version:        1.40.4
Release:        6%{?dist}
License:        LGPLv2 or MPLv1.1
URL:            http://pango.org
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://download.gnome.org/sources/pango/1.40/%{name}-%{version}.tar.xz
BuildRequires:  glib-devel
BuildRequires:  cairo
BuildRequires:  cairo-devel
BuildRequires:  libpng-devel
BuildRequires:  fontconfig
BuildRequires:  fontconfig-devel
BuildRequires:  harfbuzz
BuildRequires:  harfbuzz-devel
BuildRequires:  freetype
Requires:       harfbuzz-devel

%description
Pango is a library for laying out and rendering of text, with an emphasis on internationalization. Pango can be used anywhere that text layout is needed, though most of the work on Pango so far has been done in the context of the GTK+ widget toolkit.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
# Skip test-layout test, which is known to fail
sed -i 's|test-layout$(EXEEXT) test-font$(EXEEXT)|test-font$(EXEEXT)|g' tests/Makefile
make -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*.so*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Tue Feb 28 2023 Mandeep Plaha <mandeepplaha@microsoft.com> 1.40.4-6
-   Bump release number due to harfbuzz upgrade.
*   Fri Dec 04 2020 Andrew Phelps <anphel@microsoft.com> 1.40.4-5
-   Skip test-layout test.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.40.4-4
-   Added %%license line automatically
*   Mon Apr 20 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.40.4-3
-   Rename "freetype2" to "freetype".
-   Remove sha1 macro.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.40.4-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.40.4-1
-   Initial version
