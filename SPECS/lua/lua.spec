%define LICENSE_PATH LICENSE.PTR
%global major_version 5.4

# If you are incrementing major_version, enable bootstrapping and adjust accordingly.
# Version should be the latest prior build. If you don't do this, RPM will break.
%global bootstrap 0
%global bootstrap_major_version 5.3
%global bootstrap_version %{bootstrap_major_version}.6

Summary:        Programming language
Name:           lua
Version:        5.4.3
Release:        1%{?dist}
License:        MIT
URL:            http://www.lua.org
Group:          Development/Tools
Vendor:		Microsoft Corporation
Distribution:	Mariner

Source0:        http://www.lua.org/ftp/%{name}-%{version}.tar.gz

%if 0%{?bootstrap}
Source1:       http://www.lua.org/ftp/lua-%{bootstrap_version}.tar.gz
%endif
Source2:       %{LICENSE_PATH}

Patch0:	       lua-%{version}-shared-library.patch

%if 0%{?bootstrap}
Patch1:        lua-%{bootstrap_version}-shared-library.patch
%endif

Patch2:        CVE-2021-43519.patch

BuildRequires:  readline-devel
Requires:       readline

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%package devel
Summary:    Development files for %{name}
Requires:	%{name} = %{version}

%description devel
This package contains development files for %{name}.

%prep
prep_lua_src() {
  local fname="$1"

  sed -i '/#define LUA_ROOT/s:/usr/local/:/usr/:' src/luaconf.h
  sed -i 's/CFLAGS= -fPIC -O2 /CFLAGS= -fPIC -O2 -DLUA_COMPAT_MODULE /' src/Makefile
  patch -p1 < ${fname}
}

%if 0%{?bootstrap}
# Using autosetup is not feasible
%setup -q -a0 -a1 -n %{name}-%{version}
pushd lua-%{bootstrap_version}
prep_lua_src %{PATCH1}
popd
%else
# Using autosetup is not feasible
%setup -q
%endif

prep_lua_src %{PATCH0}
prep_lua_src %{PATCH2}
cp %{SOURCE2} ./

%build
make VERBOSE=1 %{?_smp_mflags} linux

%if 0%{?bootstrap}
pushd lua-%{bootstrap_version}
make VERBOSE=1 %{?_smp_mflags} linux
popd
%endif

%install
lua_make_install() {
  local loc="$1"
  local v1="$2"
  local v2="$3"

  make %{?_smp_mflags} \
      INSTALL_TOP=${loc} TO_LIB="liblua.so liblua.so.${v1} liblua.so.${v2}" \
      INSTALL_DATA="cp -d" \
      INSTALL_MAN=${loc}/share/man/man1 \
      install
}

lua_make_install %{buildroot}/usr %{major_version} %{version}
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig

cat > %{buildroot}%{_libdir}/pkgconfig/lua.pc <<- "EOF"
	V=%{major_version}
	R=%{version}
	prefix=/usr
	INSTALL_BIN=${prefix}/bin
	INSTALL_INC=${prefix}/include
	INSTALL_LIB=${prefix}/lib
	INSTALL_MAN=${prefix}/man/man1
	exec_prefix=${prefix}
	libdir=${exec_prefix}/lib
	includedir=${prefix}/include
	Name: Lua
	Description: An Extensible Extension Language
	Version: ${R}
	Requires:
	Libs: -L${libdir} -llua -lm
	Cflags: -I${includedir}
EOF

rmdir %{buildroot}%{_libdir}/lua/%{major_version} %{buildroot}%{_libdir}/lua

%if 0%{?bootstrap}
pushd lua-%{bootstrap_version}
mkdir -p %{buildroot}/installdir
lua_make_install %{buildroot}/installdir/usr %{bootstrap_major_version} %{bootstrap_version}
cp -a %{buildroot}/installdir/%{_libdir}/liblua.so.%{bootstrap_version} %{buildroot}%{_libdir}
cp -a %{buildroot}/installdir/%{_libdir}/liblua.so.%{bootstrap_major_version} %{buildroot}%{_libdir}
rm -rf %{buildroot}/installdir
popd
%endif

%check
make test %{?_smp_mflags}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license %{LICENSE_PATH}
%{_bindir}/*
%{_libdir}/liblua.so.*
%{_mandir}/*/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/lua.pc
%{_libdir}/liblua.so

%changelog
*   Mon Jan 03 2022 Daniel McIlvaney <damcilva@microsoft.com> 5.4.3-1
-   Update to version 5.4.3
-   Apply patch CVE-2021-43519

*   Thu Oct 01 2020 Daniel McIlvaney <damcilva@microsoft.com> 5.3.5-8
-   Nopatch CVE-2020-24342
-   Apply patch for CVE-2019-6706 from Lua mailing list
-   Apply patch for CVE-2020-15888 from Open Embedded

*   Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> 5.3.5-7
-   Nopatch CVE-2020-15889 since it only affects 5.4.0

*   Tue Aug 11 2020 Mateusz Malisz <mamalisz@microsoft.com> 5.3.5-6
-   Append -fPIC and -O2 to CFLAGS to fix build issues.

*   Fri Jul 31 2020 Leandro Pereira <leperei@microsoft.com> 5.3.5-5
-   Don't stomp on CFLAGS.

*   Thu Jun 06 2020 Joe Schmitt <joschmit@microsoft.com> 5.3.5-4
-   Added %%license macro.

*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 5.3.5-3
-   Verified License. Fixed Source0 download URL. Fixed URL.  Fixed Formatting.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 5.3.5-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 5.3.5-1
-   Update to version 5.3.5

*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 5.3.4-1
-   Update package version

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.2-2
-   GA - Bump release of all rpms

*   Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 5.3.2-1
-   Update to version 5.3.2.

*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2.3-1
-   Initial build.	First version
