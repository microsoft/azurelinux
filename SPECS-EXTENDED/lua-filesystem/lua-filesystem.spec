%{!?lua_compat_version: %global lua_compat_version 5.1}
%{!?lua_compat_libdir: %global lua_compat_libdir %{_libdir}/lua/%{lua_compat_version}}
%{!?lua_compat_builddir: %global lua_compat_builddir %{_builddir}/compat-lua-%{name}-%{version}-%{release}}

Name:           lua-filesystem
Version:        1.8.0
Release:        1%{?dist}
Summary:        File System Library for the Lua Programming Language

%global gitowner keplerproject
%global gitproject luafilesystem
%global gittag %(echo %{version} | sed -e 's/\\./_/g')

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://%{gitowner}.github.io/%{gitproject}/
Source0:        https://github.com/%{gitowner}/%{gitproject}/archive/v%{gittag}/%{gitproject}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  lua-devel >= 5.1
BuildRequires:  lua-rpm-macros
BuildRequires:  compat-lua >= %{lua_compat_version}
BuildRequires:  compat-lua-devel >= %{lua_compat_version}
Requires:       lua(abi) = %{lua_version}

%global _description %{expand:
LuaFileSystem is a Lua library developed to complement the set of functions
related to file systems offered by the standard Lua distribution.

LuaFileSystem offers a portable way to access the underlying directory
structure and file attributes.}

%description %{_description}


%package -n lua%{lua_compat_version}-filesystem
Summary:        File System Library for the Lua Programming Language %{lua_compat_version}
Requires:       lua(abi) = %{lua_compat_version}
Obsoletes:      lua-filesystem-compat < 1.8.0-3
Provides:       lua-filesystem-compat = %{version}-%{release}
Provides:       lua-filesystem-compat%{?_isa} = %{version}-%{release}

%description -n lua%{lua_compat_version}-filesystem %{_description}

%prep
%autosetup -n %{gitproject}-%{gittag}

rm -rf %{lua_compat_builddir}
cp -a . %{lua_compat_builddir}

%build
%make_build LUA_LIBDIR=%{lua_libdir} CFLAGS="%{optflags} -fPIC %{?__global_ldflags}"

pushd %{lua_compat_builddir}
%make_build LUA_LIBDIR=%{lua_compat_libdir} CFLAGS="-I%{_includedir}/lua-%{lua_compat_version} %{optflags} -fPIC %{?__global_ldflags}"
popd

%install
%make_install LUA_LIBDIR=%{lua_libdir}

pushd %{lua_compat_builddir}
%make_install LUA_LIBDIR=%{lua_compat_libdir}
popd

%check
LUA_CPATH=%{buildroot}%{lua_libdir}/\?.so lua tests/test.lua

LUA_CPATH=%{buildroot}%{lua_compat_libdir}/\?.so lua-%{lua_compat_version} tests/test.lua

%files
%license LICENSE
%doc doc/us/*
%doc README.md
%{lua_libdir}/*

%files -n lua%{lua_compat_version}-filesystem
%license LICENSE
%doc doc/us/*
%doc README.md
%{lua_compat_libdir}/*

%changelog
* Wed Dec 11 2024 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.8.0-1
- Upgraded to version 1.8.0
- License verified.

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

