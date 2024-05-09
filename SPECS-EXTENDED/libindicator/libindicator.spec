Summary:        Shared functions for Ayatana indicators
Name:           libindicator
Version:        12.10.1
Release:        24%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://launchpad.net/libindicator
Source0:        https://launchpad.net/libindicator/12.10/12.10.1/+download/%{name}-%{version}.tar.gz
BuildRequires:  chrpath
BuildRequires:  dbus-glib-devel
BuildRequires:  gnome-common
BuildRequires:  gtk-doc
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig

%description
A set of symbols and convenience functions that all Ayatana indicators are
likely to use.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package tools
Summary:        Shared functions for Ayatana indicators - Tools
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description tools
This package contains tools used by the %{name} package, the
Ayatana indicators system.

%package gtk3
Summary:        GTK+3 build of %{name}

%description gtk3
A set of symbols and convenience functions that all Ayatana indicators
are likely to use. This is the GTK+ 3 build of %{name}, for use
by GTK+ 3 apps.

%package gtk3-devel
Summary:        Development files for %{name}-gtk3
Requires:       %{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description gtk3-devel
The %{name}-gtk3-devel package contains libraries and header files for
developing applications that use %{name}-gtk3.

%package gtk3-tools
Summary:        Shared functions for Ayatana indicators - GTK3 Tools
Requires:       %{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description gtk3-tools
This package contains tools used by the %{name}-gtk3 package, the
Ayatana indicators system. This package contains the builds of the
tools for the GTK+3 build of %{name}.

%prep
%autosetup -p1

sed -i.addvar configure.ac \
	-e '\@LIBINDICATOR_LIBS@s|\$LIBM| \$LIBM|'

# https://bazaar.launchpad.net/~indicator-applet-developers/libindicator/trunk.12.10/view/head:/autogen.sh
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
rm -rf build-gtk2 build-gtk3
mkdir build-gtk2 build-gtk3

pushd build-gtk2
export CFLAGS="%{optflags} -Wno-deprecated-declarations -Wno-error"
%configure --with-gtk=2 --disable-static --disable-silent-rules
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
popd

pushd build-gtk3
export CFLAGS="%{optflags} -Wno-deprecated-declarations -Wno-error"
%configure --with-gtk=3 --disable-static --disable-silent-rules
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
popd

%install
pushd build-gtk2
make install DESTDIR=%{buildroot}
popd
(
	PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
	export PKG_CONFIG_PATH
	for var in \
		iconsdir \
		indicatordir \
		%{nil}
	do
		vardir=$(pkg-config --variable=${var} indicator-0.4)
		mkdir -p %{buildroot}${vardir}
	done
)

pushd build-gtk3
make install DESTDIR=%{buildroot}
popd
(
	PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
	export PKG_CONFIG_PATH
	for var in \
		iconsdir \
		indicatordir \
		%{nil}
	do
		vardir=$(pkg-config --variable=${var} indicator3-0.4)
		mkdir -p %{buildroot}${vardir}
	done
)

# Ubuntu doesn't package the dummy indicator
rm -f %{buildroot}%{_libdir}/libdummy-indicator*.so

# Remove libtool files
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets
%ldconfig_scriptlets gtk3

%files
%license COPYING
%doc AUTHORS NEWS ChangeLog
%{_libdir}/libindicator.so.*
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
%license COPYING
%doc AUTHORS NEWS ChangeLog
%{_libdir}/libindicator3.so.*
%dir %{_datadir}/libindicator/
%dir %{_datadir}/libindicator/icons/
%{_libdir}/indicators3/

%files gtk3-devel
%dir %{_includedir}/libindicator3-0.4/
%dir %{_includedir}/libindicator3-0.4/libindicator/
%{_includedir}/libindicator3-0.4/libindicator/*.h
%{_libdir}/libindicator3.so
%{_libdir}/pkgconfig/indicator3-0.4.pc

%files gtk3-tools
%{_libexecdir}/indicator-loader3

%changelog
* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 12.10.1-24
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- license verified

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
