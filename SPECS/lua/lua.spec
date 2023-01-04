%define LICENSE_PATH LICENSE.PTR
%define majmin %(echo %{version} | cut -d. -f1-2)

Summary:        Programming language
Name:           lua
Version:        5.3.5
Release:        10%{?dist}
License:        MIT
URL:            https://www.lua.org
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.lua.org/ftp/%{name}-%{version}.tar.gz
Source1:        %{LICENSE_PATH}
Patch0:         lua-5.3.4-shared_library-1.patch
# CVE-2020-15888 patch taken from Open Embedded's Lua meta layer https://github.com/openembedded/meta-openembedded/blob/master/meta-oe/recipes-devtools/lua/lua/CVE-2020-15888.patch
# NOTE: Upstream patches needed if updating to 5.4:
#   - eb41999461b6f428186c55abd95f4ce1a76217d5
#   - 6298903e35217ab69c279056f925fb72900ce0b7
Patch1:         CVE-2020-15888.patch
# CVE-2020-15889 is in the Lua generational garbage collection code, which is new to 5.4.0. 5.3.5 is not affected.
# NOTE: Patches needed if updating to 5.4:
#   - 127e7a6c8942b362aa3c6627f44d660a4fb75312
Patch2:         CVE-2020-15889.nopatch
# CVE-2020-24342 appears to not affect 5.3.5 (no repro of exploit)
# NOTE: Patches needed if updating to 5.4:
#   - 34affe7a63fc5d842580a9f23616d057e17dfe27
Patch3:         CVE-2020-24342.nopatch
# From http://lua.2524044.n2.nabble.com/CVE-2019-6706-use-after-free-in-lua-upvaluejoin-function-tt7685575.html
Patch4:         CVE-2019-6706-use-after-free-lua_upvaluejoin.patch
Patch5:         CVE-2022-28805.patch
Patch6:    CVE-2020-15945.patch

BuildRequires:  readline-devel
Requires:       readline

%description
Lua is a powerful, light-weight programming language designed for extending
applications. Lua is also frequently used as a general-purpose, stand-alone
language. Lua is free software

%package devel
Summary:    Libraries and header files for lua
Requires:   %{name} = %{version}
%description devel
Static libraries and header files for the support library for lua

%prep
%autosetup -p1
sed -i '/#define LUA_ROOT/s:/usr/local/:/usr/:' src/luaconf.h
sed -i 's/CFLAGS= -fPIC -O2 /CFLAGS+= -fPIC -O2 -DLUA_COMPAT_MODULE /' src/Makefile
cp %{SOURCE1} ./

%build
make V=%{majmin} R=%{version} VERBOSE=1 %{?_smp_mflags} linux

%install
make %{?_smp_mflags} \
    V=%{majmin} \
    R=%{version} \
    INSTALL_TOP=%{buildroot}/usr TO_LIB="liblua.so \
    liblua.so.%{majmin} liblua.so.%{version}" \
    INSTALL_DATA="cp -d" \
    INSTALL_MAN=%{buildroot}/usr/share/man/man1 \
    install
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/lua.pc <<- "EOF"
    V=%{majmin}
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
rmdir %{buildroot}%{_libdir}/lua/5.3
rmdir %{buildroot}%{_libdir}/lua

%check
make test

%clean
rm -rf %{buildroot}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblua.so.*
%{_mandir}/*/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/lua.pc
%{_libdir}/liblua.so

%changelog
* Wed Jan 04 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.3.5-10
- Add patch for CVE-2020-15945

*   Wed Apr 20 2022 Henry Beberman <henry.beberman@microsoft.com> 5.3.5-9
-   Patch CVE-2022-28805
-   Remove contents of nopatch files so autosetup works
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
