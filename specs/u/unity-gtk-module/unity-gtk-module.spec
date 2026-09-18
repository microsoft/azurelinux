# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# old code base is not fully compatible with GCC 14
%global build_type_safety_c 2

Name:		unity-gtk-module
Version:	0.0.0+17.04.20170403
Release:	23%{?dist}
Summary:	GTK+ module for exporting old-style menus as GMenuModels

# Automatically converted from old format: LGPLv3 - review is highly recommended.
License:	LGPL-3.0-only
URL:		https://launchpad.net/%{name}
Source0:	http://archive.ubuntu.com/ubuntu/pool/main/u/%{name}/%{name}_%{version}.orig.tar.gz

BuildRequires: make
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libX11-devel
BuildRequires:	libtool
BuildRequires:	python3-devel

%description
GTK+ module for exporting old-style menus as GMenuModels.
Many applications implement menus as GtkMenuShells and GtkMenuItems
and aren't looking to migrate to the newer GMenuModel API.
This GTK+ module watches for these types of menus and exports the
appropriate GMenuModel implementation.


%package -n libunity-gtk-parser-devel
Summary:	Common development-files for libunity-gtk{2,3}-parser

BuildArch:	noarch

BuildRequires:	gtk-doc

%description -n libunity-gtk-parser-devel
This package contains common headers and documentation for
libunity-gtk{2,3}-parser.


%package -n libunity-gtk2-parser
Summary:	Gtk2MenuShell to GMenuModel parser

BuildRequires:	gtk2-devel

%description -n libunity-gtk2-parser
This library converts Gtk2MenuShells into GMenuModels.


%package -n libunity-gtk2-parser-devel
Summary:	Development-files for libunity-gtk2-parser

Requires:	gtk2-devel%{?_isa}
Requires:	libunity-gtk-parser-devel	== %{version}-%{release}
Requires:	libunity-gtk2-parser%{?_isa}	== %{version}-%{release}

%description -n libunity-gtk2-parser-devel
This package contains development-files for libunity-gtk2-parser.


%package -n libunity-gtk3-parser
Summary:	Gtk3MenuShell to GMenuModel parser

BuildRequires:	gtk3-devel

%description -n libunity-gtk3-parser
This library converts Gtk3MenuShells into GMenuModels.


%package -n libunity-gtk3-parser-devel
Summary:	Development-files for libunity-gtk3-parser

Requires:	gtk3-devel%{?_isa}
Requires:	libunity-gtk-parser-devel	== %{version}-%{release}
Requires:	libunity-gtk3-parser%{?_isa}	== %{version}-%{release}

%description -n libunity-gtk3-parser-devel
This package contains development-files for libunity-gtk3-parser.


%package -n unity-gtk-module-common
Summary:	Common files for unity-gtk{2,3}-module

BuildArch:	noarch

BuildRequires:	systemd

Requires:	/bin/sh
Requires:	dbus
Requires:	gawk
Requires:	sed
Requires:	systemd

%description -n unity-gtk-module-common
This package contains common data-files for unity-gtk{2,3}-module.


%package -n unity-gtk2-module
Summary:	Gtk2MenuShell D-Bus exporter

Requires:	libunity-gtk2-parser%{?_isa}	== %{version}-%{release}
Requires:	unity-gtk-module-common		== %{version}-%{release}

Provides:	appmenu-gtk			== %{version}-%{release}
Provides:	appmenu-gtk%{?_isa}		== %{version}-%{release}

%description -n unity-gtk2-module
This GTK+ 2 module exports Gtk2MenuShells over D-Bus.


%package -n unity-gtk3-module
Summary:	Gtk3MenuShell D-Bus exporter

Requires:	libunity-gtk3-parser%{?_isa}	== %{version}-%{release}
Requires:	unity-gtk-module-common		== %{version}-%{release}

Provides:	appmenu-gtk3			== %{version}-%{release}
Provides:	appmenu-gtk3%{?_isa}		== %{version}-%{release}

%description -n unity-gtk3-module
This GTK+ 3 module exports Gtk3MenuShells over D-Bus.


%prep
%autosetup -c
%{__mkdir} -p build/gtk2 build/gtk3 m4

# Initialize build-environment.
%{_bindir}/gtkdocize --copy
%{_bindir}/autoreconf -fiv

# Setup systemd-unit for Fedora.
f="data/%{name}.service"
%{__sed} -i.orig -e's!^Before=!After=dbus.service\n&!'		\
	-e's!ubuntu-session.target$!default.target!g'		\
	-e's!graphical-session.target$!default.target!g'	\
	-e's!dbus-update-activation-environment!%{_bindir}/&!g'	\
	-e's!awk!%{_bindir}/&!g' -e's!sed!%{_bindir}/&!' ${f}
%{_bindir}/touch -r ${f}.orig ${f} && %{__rm} ${f}.orig


%build
export PYTHON="%{__python3}"
export SRC_DIR="$(%{_bindir}/pwd)"
for i in 2 3 ; do
	pushd build/gtk${i}
	%{_bindir}/ln ../../configure configure
	%configure	\
		--disable-silent-rules				\
		--disable-static				\
		--enable-gtk-doc				\
		--with-gtk=${i}					\
		--srcdir="${SRC_DIR}"
	%make_build
	popd
done


%install
for i in 2 3 ; do
	%make_install -C build/gtk${i}
done

# Setup systemd.
%{__mkdir} -p %{buildroot}%{_userunitdir}/default.target.wants
%{_bindir}/ln -s						\
	%{_userunitdir}/%{name}.service				\
	%{buildroot}%{_userunitdir}/default.target.wants/%{name}.service

# We don't ship libtool-dumplings.
%{_bindir}/find %{buildroot}%{_libdir} -name '*.la' -delete

# Those files are not needed during runtime.
%{__rm} -rf %{buildroot}%{_datadir}/upstart/			\
	%{buildroot}%{python3_sitelib}

# Prepare demos for inclusion in %%doc.
%{__rm} -f demos/Makefile*


%ldconfig_scriptlets -n libunity-gtk2-parser


%ldconfig_scriptlets -n libunity-gtk3-parser


%files -n libunity-gtk-parser-devel
%doc demos
%doc %{_datadir}/gtk-doc
%{_includedir}/unity-gtk-parser

%files -n libunity-gtk2-parser
%license AUTHORS COPYING*
%{_libdir}/libunity-gtk2-parser.so.0*

%files -n libunity-gtk2-parser-devel
%{_libdir}/libunity-gtk2-parser.so
%{_libdir}/pkgconfig/unity-gtk2-parser.pc

%files -n libunity-gtk3-parser
%license AUTHORS COPYING*
%{_libdir}/libunity-gtk3-parser.so.0*

%files -n libunity-gtk3-parser-devel
%{_libdir}/libunity-gtk3-parser.so
%{_libdir}/pkgconfig/unity-gtk3-parser.pc

%files -n unity-gtk-module-common
%license AUTHORS COPYING*
%{_datadir}/glib-2.0
%{_userunitdir}/default.target.wants
%{_userunitdir}/%{name}.service

%files -n unity-gtk2-module
%{_libdir}/gtk-2.0/modules/lib%{name}.so

%files -n unity-gtk3-module
%{_libdir}/gtk-3.0/modules/lib%{name}.so


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 0.0.0+17.04.20170403-21
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 09 2020 Petr Viktorin <pviktori@redhat.com> - 0.0.0+17.04.20170403-12
- Switch BuildRequires to python3

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-11
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.0.0+17.04.20170403-4
- Remove obsolete scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+17.04.20170403-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 05 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.0+17.04.20170403-1
- New upstream release (rhbz#1438992)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0+16.10.20160913-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 14 2016 Björn Esser <fedora@besser82.io> - 0.0.0+16.10.20160913-3
- Updated Url-tag

* Fri Oct 14 2016 Björn Esser <fedora@besser82.io> - 0.0.0+16.10.20160913-2
- Drop dependency on glib2 and gtk-doc, own the dir in the package instead

* Fri Oct 07 2016 Björn Esser <fedora@besser82.io> - 0.0.0+16.10.20160913-1
- Initial import (rhbz 1382813)

* Fri Oct 07 2016 Björn Esser <fedora@besser82.io> - 0.0.0+16.10.20160913-0.2
- Add Requires for directory-ownership

* Thu Oct 06 2016 Björn Esser <fedora@besser82.io> - 0.0.0+16.10.20160913-0.1
- Initial package (rhbz 1382813)
