%global		gittag	4_1_1
%global         __requires_exclude ^libtcl.so.*$
Summary:        Open Geographic Datastore Interface
Name:		ogdi
Version:	4.1.1
Release:	4%{?dist}
License:	BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://ogdi.sourceforge.net/
# new project location is https://github.com/libogdi/ogdi
Source0:	https://github.com/libogdi/ogdi/archive/%{name}_%{gittag}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	https://ogdi.sourceforge.net/ogdi.pdf
Patch0:		ogdi-4.1.0-sailer.patch

BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	zlib-devel
BuildRequires:	expat-devel
BuildRequires:	tcl-devel
BuildRequires:	libtirpc-devel

# ODBC driver has been removed in 4.1.1 without replacement
Obsoletes:	%{name}-odbc < 4.1.1

%description
OGDI is the Open Geographic Datastore Interface. OGDI is an
application programming interface (API) that uses a standardized
access methods to work in conjunction with GIS software packages (the
application) and various geospatial data products. OGDI uses a
client/server architecture to facilitate the dissemination of
geospatial data products over any TCP/IP network, and a
driver-oriented approach to facilitate access to several geospatial
data products/formats.


%package devel
Summary:	OGDI header files and documentation
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	zlib-devel
Requires:      expat-devel

%description devel
OGDI header files and developer's documentation.


%package tcl
Summary:	TCL wrapper for OGDI
Requires:       tcl >= 8.6
Requires:	%{name} = %{version}-%{release}
%description tcl
TCL wrapper for OGDI.


%prep
%autosetup -p1 -n %{name}-%{name}_%{gittag}

# include documentation
%{__cp} -p %{SOURCE1} .


%build
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET
INST_LIB=%{_libdir}/;export INST_LIB
export CFG=debug # for -g

# removal of -D_FORTIFY_SOURCE from preprocessor flags seems not needed any more
# ogdits-3.1 test suite produces same result with and without the flag
export CFLAGS="$RPM_OPT_FLAGS -DDONT_TD_VOID -DUSE_TERMIO"
%configure \
	--with-binconfigs \
	--with-expat \
	--with-zlib

# WARNING !!!
# using %{?_smp_mflags} may break build
%{__make}

# build tcl interface
%{__make} -C ogdi/tcl_interface \
	TCL_LINKLIB="-ltcl"

# build contributions
%{__make} -C contrib/gdal


%install
# export env
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET

%{__make} install \
	INST_INCLUDE=%{buildroot}%{_includedir}/%{name} \
	INST_LIB=%{buildroot}%{_libdir} \
	INST_BIN=%{buildroot}%{_bindir}

# install plugins olso
%{__make} install -C ogdi/tcl_interface \
	INST_LIB=%{buildroot}%{_libdir}
%{__make} install -C contrib/gdal \
	INST_LIB=%{buildroot}%{_libdir}

# remove example binary
%{__rm} %{buildroot}%{_bindir}/example?

# we have multilib ogdi-config
%if "%{_lib}" == "lib"
%global cpuarch 32
%else
%global cpuarch 64
%endif

# fix file(s) for multilib issue
touch -r ogdi-config.in ogdi-config

# install pkgconfig file and ogdi-config
%{__mkdir} -p %{buildroot}%{_libdir}/pkgconfig
%{__install} -p -m 644 ogdi.pc %{buildroot}%{_libdir}/pkgconfig/
%{__install} -p -m 755 ogdi-config %{buildroot}%{_bindir}/ogdi-config-%{cpuarch}
# ogdi-config wrapper for multiarch
cat > %{buildroot}%{_bindir}/%{name}-config <<EOF
#!/bin/bash

ARCH=\$(uname -m)
case \$ARCH in
x86_64 | ppc64 | ppc64le | ia64 | s390x | sparc64 | alpha | alphaev6 | aarch64 )
ogdi-config-64 \${*}
;;
*)
ogdi-config-32 \${*}
;;
esac
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}-config
touch -r ogdi-config.in %{buildroot}%{_bindir}/%{name}-config


%files
%doc LICENSE NEWS ChangeLog README
%{_bindir}/gltpd
%{_bindir}/ogdi_*
%{_libdir}/libogdi.so.*
%dir %{_libdir}/ogdi
%exclude %{_libdir}/%{name}/libecs_tcl.so
%{_libdir}/%{name}/lib*.so

%files devel
%doc ogdi.pdf
%doc ogdi/examples/example1/example1.c
%doc ogdi/examples/example2/example2.c
%{_bindir}/%{name}-config
%{_bindir}/%{name}-config-%{cpuarch}
%{_libdir}/pkgconfig/%{name}.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/libogdi.so

%files tcl
%{_libdir}/%{name}/libecs_tcl.so


%changelog
* Mon Feb 02 2026 Aditya Singh <v-aditysing@microsoft.com> - 4.1.1-4
- Rebuilt with updated tcl version dependency for ogdi-tcl subpackage
- to resolve installation failure.

* Wed Dec 11 2024 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 4.1.1-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 01 2024 Dan Horák <dan[at]danny.cz> - 4.1.1-1
- Update to 4.1.1 (fixes rhbz#2261412)
- Remove odbc subpackage

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Feb 05 2023 Florian Weimer <fweimer@redhat.com> - 4.1.0-10
- Fix C99 compatibility issue

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 10 2019 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-2
- Remove PROJ dependency. The new OGDI does not use it.

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1
- Initial packaging for EPEL 8
- Update to 4.1.0
