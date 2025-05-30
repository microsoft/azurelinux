Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%{!?lua_version: %global lua_version %{lua: print(string.sub(_VERSION, 5))}}
%{!?lua_libdir: %global lua_libdir %{_libdir}/lua/%{lua_version}}
%{!?lua_pkgdir: %global lua_pkgdir %{_datadir}/lua/%{lua_version}}

%{!?lua_compat_version: %global lua_compat_version 5.1}
%{!?lua_compat_libdir: %global lua_compat_libdir %{_libdir}/lua/%{lua_compat_version}}
%{!?lua_compat_pkgdir: %global lua_compat_pkgdir %{_datadir}/lua/%{lua_compat_version}}
%{!?lua_compat_builddir: %global lua_compat_builddir %{_builddir}/compat-lua-%{name}-%{version}-%{release}}

Summary:        SAX XML parser based on the Expat library
Name:           lua-expat
Version:        1.3.0
Release:        19%{?dist}
License:        MIT
URL:            https://matthewwild.co.uk/projects/luaexpat/
Source0:        https://matthewwild.co.uk/projects/luaexpat/luaexpat-%{version}.tar.gz
Source1:        https://matthewwild.co.uk/projects/luaexpat/luaexpat-%{version}.tar.gz.asc
Source2:        gpgkey-32A9EDDE3609931EB98CEAC315907E8E7BDD6BFE.gpg

Requires:       lua(abi) = %{lua_version}



BuildRequires:  gcc, lua-devel >= %{lua_version}, expat-devel
BuildRequires:  gnupg2

%description
LuaExpat is a SAX XML parser based on the Expat library.


%package -n lua%{lua_compat_version}-expat
Summary:        SAX XML parser based on the Expat library for Lua %{lua_compat_version}
Obsoletes:      lua-expat-compat < 1.3.0-16
Provides:       lua-expat-compat = %{version}-%{release}
Provides:       lua-expat-compat%{?_isa} = %{version}-%{release}
Requires:       lua(abi) = %{lua_compat_version}
BuildRequires:  compat-lua-devel >= %{lua_compat_version}

%description -n lua%{lua_compat_version}-expat
LuaExpat is a SAX XML parser based on the Expat library for Lua %{lua_compat_version}.


%prep
gpgv2 --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%setup -q -n luaexpat-%{version}


rm -rf %{lua_compat_builddir}
cp -a . %{lua_compat_builddir}


%build
%make_build \
  CFLAGS="%{optflags} -fPIC -std=c99" LDFLAGS="%{?__global_ldflags}" \
  LUA_V=%{lua_version} LUA_CDIR=%{lua_libdir} LUA_LDIR=%{lua_pkgdir} LUA_INC=-I%{_includedir} \
  EXPAT_INC=-I%{_includedir}


pushd %{lua_compat_builddir}
%make_build \
  CFLAGS="%{optflags} -fPIC -std=c99" LDFLAGS="%{?__global_ldflags}" \
  LUA_V=%{lua_compat_version} LUA_CDIR=%{lua_compat_libdir} LUA_LDIR=%{lua_compat_pkgdir} LUA_INC=-I%{_includedir}/lua-%{lua_compat_version} \
  EXPAT_INC=-I%{_includedir}
popd


%install
%make_install LUA_CDIR=%{lua_libdir} LUA_LDIR=%{lua_pkgdir}


pushd %{lua_compat_builddir}
%make_install LUA_CDIR=%{lua_compat_libdir} LUA_LDIR=%{lua_compat_pkgdir}
popd


%check
lua -e 'package.cpath="./src/?.so;"..package.cpath; dofile("tests/test.lua");'
lua -e 'package.cpath="./src/?.so;" .. package.cpath; package.path="./src/?.lua;" .. package.path; dofile("tests/test-lom.lua");'

%files
%doc README doc/us/*
%{lua_libdir}/*
%{lua_pkgdir}/*


%files -n lua%{lua_compat_version}-expat
%doc README doc/us/*
%{lua_compat_libdir}/*
%{lua_compat_pkgdir}/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.0-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 09 2019 Jan Beran <jaberan@redhat.com> - 1.3.0-17
- Add -std=c99 flag when building

* Sat Jul 27 2019 Robert Scheck <robert@fedoraproject.org> - 1.3.0-16
- Spec file cleanups

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 11 2018 Robert Scheck <robert@fedoraproject.org> - 1.3.0-12
- Build flags injection is only partially successful (#1565997)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Robert Scheck <robert@fedoraproject.org> - 1.3.0-5
- Rebuilt for lua 5.3 (#1225902)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Matěj Cepl <mcepl@redhat.com> - 1.3.0-2
- Apply patch by jkaluza (fix RHBZ# 1100238) to build -compat subpackage
  against compat-lua

* Wed Apr 23 2014 Robert Scheck <robert@fedoraproject.org> - 1.3.0-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Tom Callaway <spot@fedoraproject.org> - 1.2.0-5
- fix for lua 5.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 03 2011 Matěj Cepl <mcepl@redhat.com> - 1.2-1
- New upstream release, fixing "The Billion Laughs Attack" for XMPP servers.
- Fix tests so that we actually pass them.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 05 2008 Tim Niemueller <tim@niemueller.de> - 1.1-2
- Minor spec fixes for guideline compliance
- Added %%check macro to execute tests

* Wed Jun 04 2008 Tim Niemueller <tim@niemueller.de> - 1.1-1
- Initial package

