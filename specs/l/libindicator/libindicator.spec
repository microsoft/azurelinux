# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		libindicator
Version:	12.10.1
Release: 32%{?dist}
Summary:	Shared functions for Ayatana indicators

# SPDX confirmed
License:	GPL-3.0-only
URL:		https://launchpad.net/libindicator
Source0:	https://launchpad.net/libindicator/12.10/12.10.1/+download/%{name}-%{version}.tar.gz
# From GLib 2.62
Patch1:	libindicator-12.10.1-glib262-g_define_type_with_private.patch

BuildRequires:	gtk-doc
BuildRequires:	libtool

BuildRequires:	dbus-glib-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gmodule-2.0)

BuildRequires:	gnome-common
BuildRequires:	make

%description
A set of symbols and convenience functions that all Ayatana indicators are
likely to use.


%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package	tools
Summary:	Shared functions for Ayatana indicators - Tools
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	tools
This package contains tools used by the %{name} package, the
Ayatana indicators system.


%package	gtk3
Summary:	GTK+3 build of %{name}

%description gtk3
A set of symbols and convenience functions that all Ayatana indicators
are likely to use. This is the GTK+ 3 build of %{name}, for use
by GTK+ 3 apps.


%package	gtk3-devel
Summary:	Development files for %{name}-gtk3

Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	gtk3-devel
The %{name}-gtk3-devel package contains libraries and header files for
developing applications that use %{name}-gtk3.


%package	gtk3-tools
Summary:	Shared functions for Ayatana indicators - GTK3 Tools

Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	gtk3-tools
This package contains tools used by the %{name}-gtk3 package, the
Ayatana indicators system. This package contains the builds of the
tools for the GTK+3 build of %{name}.


%prep
%setup -q
%patch -P1 -p2 -b .orig

sed -i.addvar configure.ac \
	-e '\@LIBINDICATOR_LIBS@s|\$LIBM| \$LIBM|'

# http://bazaar.launchpad.net/~indicator-applet-developers/libindicator/trunk.12.10/view/head:/autogen.sh
cat > autogen.sh <<EOF
#!/bin/sh

PKG_NAME="libindicator"

which gnome-autogen.sh || {
	echo "You need gnome-common from GNOME SVN"
	exit 1
}

USE_GNOME2_MACROS=1 \
. gnome-autogen.sh
EOF

NOCONFIGURE=1 \
	sh autogen.sh


%build
%global _configure ../configure

build() {
gtkver=$1

rm -rf build-gtk${gtkver}
mkdir build-gtk${gtkver}
pushd build-gtk${gtkver}

export CFLAGS="%{optflags} -Wno-error=deprecated-declarations"

%configure \
	--with-gtk=${gtkver} \
	--disable-static \
	--disable-silent-rules \
	%{nil}

sed -i libtool -e 's! -shared ! -Wl,--as-needed\0!g'
sed -i libtool -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g'
sed -i libtool -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g'

%make_build
popd

}

build 2
build 3


%install

install() {
gtkver=$1

pushd build-gtk${gtkver}
%make_install
popd

INDICATOR_PKGCONF_NAME=indicator-0.4
if [ $gtkver == 3 ] ; then
	INDICATOR_PKGCONF_NAME=indicator3-0.4
fi

PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
export PKG_CONFIG_PATH
for var in \
	iconsdir \
	indicatordir \
	%{nil}
do
	vardir=$(pkg-config --variable=${var} ${INDICATOR_PKGCONF_NAME})
	mkdir -p %{buildroot}${vardir}
done
}

install 2
install 3

# Ubuntu doesn't package the dummy indicator
rm -f %{buildroot}%{_libdir}/libdummy-indicator*.so

# Remove libtool files
find %{buildroot} -type f -name '*.la' -delete

%ldconfig_scriptlets
%ldconfig_scriptlets gtk3


%files
%doc	AUTHORS
%license	COPYING
%doc	NEWS
%doc	ChangeLog
%{_libdir}/libindicator.so.7{,.*}
%dir %{_datadir}/libindicator/
%dir %{_datadir}/libindicator/icons/
%{_libdir}/indicators/

%files devel
%dir %{_includedir}/libindicator-0.4/
%dir %{_includedir}/libindicator-0.4/libindicator/
%{_includedir}/libindicator-0.4/libindicator/*.h
%{_libdir}/libindicator.so
%{_libdir}/pkgconfig/indicator-0.4.pc


%files tools
%{_libexecdir}/indicator-loader
%{_datadir}/libindicator/80indicator-debugging


%files gtk3
%doc	AUTHORS
%license	COPYING
%doc	NEWS
%doc	ChangeLog

%{_libdir}/libindicator3.so.7{,.*}
%dir	%{_datadir}/libindicator/
%dir	%{_datadir}/libindicator/icons/
%{_libdir}/indicators3/


%files gtk3-devel
%dir	%{_includedir}/libindicator3-0.4/
%dir	%{_includedir}/libindicator3-0.4/libindicator/

%{_includedir}/libindicator3-0.4/libindicator/*.h
%{_libdir}/libindicator3.so
%{_libdir}/pkgconfig/indicator3-0.4.pc


%files gtk3-tools
%{_libexecdir}/indicator-loader3

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan  1 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 12.10.1-26
- SPDX migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Merlin Mathesius <mmathesi@redhat.com> - 12.10.1-18
- Minor conditional fix for ELN

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 11 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 12.10.1-16
- F-31+: Adjust GLib 2.62 change

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 15 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 12.10.1-8
- Create and own indicatordir, iconsdir (bug 1392864)

* Thu Feb  4 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 12.10.1-7
- F-24: fix FTBFS (variable expansion: perhaps due to bash behavior change)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 12.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Eduardo Echeverria  <echevemaster@gmail.com> - 12.10.1-1
- Update to 12.10.1
- Add GTK2 support

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 31 2012 Tom Callaway <spot@fedoraproject.org> - 0.4.94-2
- fix typo causing dep issues

* Sat Mar 31 2012 Tom Callaway <spot@fedoraproject.org> - 0.4.94-1
- Update to 0.4.94

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.3.22-2
- Rebuild for new libpng

* Wed Mar 23 2011 Adam Williamson <awilliam@redhat.com> - 0.3.22-1
- new release 0.3.22

* Mon Mar 07 2011 Adam Williamson <awilliam@redhat.com> - 0.3.20-1
- new release 0.3.20

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.17-4
 Rebuild against newer gtk3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.17-2
 Rebuild against newer gtk3

* Sun Jan 23 2011 Adam Williamson <awilliam@redhat.com> - 0.3.17-1
- new version 0.3.17
- drop both patches (upstream)
- no need for autoreconf any more

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.15-2
- Rebuild against newer gtk3

* Fri Dec 03 2010 Adam Williamson <awilliam@redhat.com> - 0.3.15-1
- initial package

