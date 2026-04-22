# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define majorver 8.6
%define	vers %{majorver}.16
%{!?sdt:%define sdt 1}

Summary: Tool Command Language, pronounced tickle, version 8
Name: tcl8
Version: %{vers}
Release: 3%{?dist}
Epoch: 1
License: TCL AND GPL-3.0-or-later WITH Bison-exception-2.2 AND BSD-3-Clause
URL: http://tcl.sourceforge.net/
Source: http://downloads.sourceforge.net/sourceforge/tcl/tcl-core%{version}-src.tar.gz
BuildRequires: make
Buildrequires: autoconf
BuildRequires: gcc
BuildRequires: zlib-devel
Provides: tcl(abi) = %{majorver}
Provides: tcl-tcldict = %{vers}
Patch: tcl-8.6.15-autopath.patch
Patch: tcl-8.6.15-conf.patch
Patch: tcl-8.6.13-tcltests-path-fix.patch
Patch: tcl-8.6.13-configure-c99.patch

%if %sdt
BuildRequires: systemtap-sdt-dtrace
BuildRequires: systemtap-sdt-devel
%endif

%description
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

%package devel
Summary: Tcl scripting language development environment
Requires: %{name} = %{epoch}:%{version}-%{release}
Provides: tcl-devel = %{epoch}:%{version}-%{release}
Conflicts: tcl-devel >= 1:9.0.0-1

%description devel
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The package contains the development files and man pages for tcl.

%prep
%autosetup -p1 -n tcl%{version}
rm -r compat/zlib

%build
pushd unix
autoconf
%configure \
%if %sdt
--enable-dtrace \
%endif
--enable-threads \
--enable-symbols \
--enable-shared

%make_build CFLAGS="%{optflags}" TCL_LIBRARY=%{_datadir}/tcl%{majorver}

%check
%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}

%if ! %{_without_check}
  cd unix
  make test
%endif

%install
make install -C unix INSTALL_ROOT=%{buildroot} TCL_LIBRARY=%{_datadir}/tcl%{majorver}

ln -s tclsh%{majorver} %{buildroot}%{_bindir}/tclsh8

# for linking with -libtcl
ln -s libtcl%{majorver}.so %{buildroot}%{_libdir}/libtcl.so

mkdir -p %{buildroot}/%{_libdir}/tcl%{majorver}

# postgresql and maybe other packages too need tclConfig.sh
# paths don't look at /usr/lib for efficiency, so we symlink into tcl8.6 for now
ln -s %{_libdir}/tclConfig.sh %{buildroot}/%{_libdir}/tcl%{majorver}/tclConfig.sh

mkdir -p %{buildroot}/%{_includedir}/tcl-private/{generic,unix}
find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}/%{_includedir}/tcl-private/'{}' ';'
( cd %{buildroot}/%{_includedir}
	for i in *.h ; do
		[ -f %{buildroot}/%{_includedir}/tcl-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{_includedir}/tcl-private/generic ;
	done
)

# remove buildroot traces
sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/tcl-private|" %{buildroot}/%{_libdir}/tclConfig.sh
rm -rf %{buildroot}/%{_datadir}/tcl%{majorver}/ldAix

# rename manual page
mv %{buildroot}/%{_mandir}/man1/tclsh.1 %{buildroot}/%{_mandir}/man1/tclsh8.1

# drop the API manual pages, not needed for the compat
rm -f %{buildroot}%{_mandir}/man3/* %{buildroot}%{_mandir}/mann/*
rmdir %{buildroot}%{_mandir}/man3 %{buildroot}%{_mandir}/mann

%if 0%{?flatpak}
mkdir -p %{buildroot}%{_usr}/bin
ln -s %{_bindir}/tclsh8 %{_bindir}/tclsh%{majorver} %{buildroot}%{_usr}/bin/
%endif

%files
%{_bindir}/tclsh8*
%{_datadir}/tcl%{majorver}
%exclude %{_datadir}/tcl%{majorver}/tclAppInit.c
%{_datadir}/tcl8
%{_libdir}/libtcl%{majorver}.so
%{_mandir}/man1/*
%if 0%{?flatpak}
%{_usr}/bin/tclsh8*
%endif
%dir %{_libdir}/tcl%{majorver}
%doc README.md changes
%license license.terms

%files devel
%{_includedir}/*
%{_libdir}/libtclstub%{majorver}.a
%{_libdir}/libtcl.so
%{_libdir}/tclConfig.sh
%{_libdir}/tclooConfig.sh
%{_libdir}/tcl%{majorver}/tclConfig.sh
%{_libdir}/pkgconfig/tcl.pc
%{_datadir}/tcl%{majorver}/tclAppInit.c

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Jaroslav Škarvada  <jskarvad@redhat.com> - 1:8.6.16-1
- New version
  Resolves: rhbz#2376818

* Sun Feb  2 2025 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.15-10
- Rebuilt for new gcc

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.15-8
- Updated according to the fedora review

* Thu Dec  5 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.15-7
- Initial version based on the tcl package
