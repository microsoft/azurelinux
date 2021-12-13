%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global lualibdir %{_libdir}/lua/%{luaver}

%define luacompatver 5.1
%define luacompatlibdir %{_libdir}/lua/%{luacompatver}
%define luacompatpkgdir %{_datadir}/lua/%{luacompatver}
%define lua51dir %{_builddir}/lua51-%{name}-%{version}-%{release}

%global commit 8014725009e195ffb502bcd65ca4e93b60a1b21c
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           lua-filesystem
Version:        1.6.3
Release:        13%{?dist}
Summary:        File System Library for the Lua Programming Language

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://keplerproject.github.io/luafilesystem/
Source0:	https://github.com/keplerproject/luafilesystem/archive/%{commit}/luafilesystem-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  lua-devel >= %{luaver}
Requires:       lua(abi) = %{luaver}

BuildRequires:  compat-lua >= %{luacompatver}, compat-lua-devel >= %{luacompatver}

%description
LuaFileSystem is a Lua library developed to complement the set of functions
related to file systems offered by the standard Lua distribution.

LuaFileSystem offers a portable way to access the underlying directory
structure and file attributes.

%package compat
Summary:        File System Library for the Lua Programming Language 5.1

%description compat
LuaFileSystem is a Lua library developed to complement the set of functions
related to file systems offered by the standard Lua distribution.

LuaFileSystem offers a portable way to access the underlying directory
structure and file attributes.

%prep
%setup -q -n luafilesystem-%{commit}

rm -rf %{lua51dir}
cp -a . %{lua51dir}

%build
make %{?_smp_mflags} PREFIX=%{_prefix} LUA_LIBDIR=%{lualibdir} CFLAGS="%{optflags} -fPIC"

pushd %{lua51dir}
make %{?_smp_mflags} PREFIX=%{_prefix} LUA_LIBDIR=%{luacompatlibdir} CFLAGS="-I%{_includedir}/lua-%{luacompatver} %{optflags} -fPIC"
popd

%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT%{_prefix} LUA_LIBDIR=$RPM_BUILD_ROOT%{lualibdir}

pushd %{lua51dir}
make install PREFIX=$RPM_BUILD_ROOT%{_prefix} LUA_LIBDIR=$RPM_BUILD_ROOT%{luacompatlibdir}
popd

%check
LUA_CPATH=$RPM_BUILD_ROOT%{lualibdir}/\?.so lua tests/test.lua

%files
%license LICENSE
%doc doc/us/*
%doc README
%{lualibdir}/*

%files compat
%license LICENSE
%doc doc/us/*
%doc README
%{luacompatlibdir}/*

%changelog
* Fri Jan 08 2021 Joe Schmitt <joschmit@microsoft.com> - 1.6.3-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora/RHEL version checks

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-5
- Handle lua not being in the default buildroot

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Tom Callaway <spot@fedoraproject.org> - 1.6.3-1
- update to 1.6.3
- rebuild for lua 5.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Jan Kaluza <jkaluza@redhat.com> - 1.6.2-5
- build -compat subpackage against compat-lua

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Tom Callaway <spot@fedoraproject.org> - 1.6.2-3
- rebuild for lua 5.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct  8 2012 Michel Salim <salimma@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2
- Spec cleanup

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Michel Salim <salimma@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0
- Enable tests

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 29 2009 Tim Niemueller <tim@niemueller.de> - 1.4.2-1
- Upgrade to latest stable release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 08 2008 Tim Niemueller <tim@niemueller.de> - 1.4.1-1
- Upgrade to latest stable release

* Sat Apr 05 2008 Tim Niemueller <tim@niemueller.de> - 1.4.0-3
- Add patch to add missing include of stdlib.h

* Sat Apr 05 2008 Tim Niemueller <tim@niemueller.de> - 1.4.0-2
- Pass correct CFLAGS to make to produce proper debuginfo

* Fri Apr 04 2008 Tim Niemueller <tim@niemueller.de> - 1.4.0-1
- Initial package

