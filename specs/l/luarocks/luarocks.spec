# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           luarocks
Version:        3.9.2
Release: 9%{?dist}
Summary:        A deployment and management system for Lua modules

License:        MIT
URL:            http://luarocks.org
Source0:        http://luarocks.org/releases/luarocks-%{version}.tar.gz
Source1:        config-5.1.lua

# Use /usr/lib64 as default LUA_LIBDIR
Patch0:         luarocks-3.9.1-dynamic_libdir.patch

BuildArch:      noarch
# this package was previously arched, and needs to be obsoleted
# to have an upgrade path
Obsoletes:      luarocks < 3.5.0-1

BuildRequires:  lua-devel
BuildRequires:  make
%if 0%{?el7}
BuildRequires:  lua-rpm-macros
%endif
%if 0%{?rhel} && 0%{?rhel} < 9
Requires:       lua(abi) = %{lua_version}
%endif
Requires:       unzip
Requires:       zip
Requires:       gcc

%if 0%{?fedora}
Recommends:     lua-sec
Recommends:     lua-devel
Recommends:     compat-lua-devel
Recommends:     make
Recommends:     cmake
%endif

%description
LuaRocks allows you to install Lua modules as self-contained packages
called "rocks", which also contain version dependency
information. This information is used both during installation, so
that when one rock is requested all rocks it depends on are installed
as well, and at run time, so that when a module is required, the
correct version is loaded. LuaRocks supports both local and remote
repositories, and multiple local rocks trees.


%prep
%autosetup -p1


%build
./configure \
  --prefix=%{_prefix} \
  --lua-version=%{lua_version} \
  --with-lua=%{_prefix}
%make_build


%install
%make_install

mkdir -p %{buildroot}%{_prefix}/lib/luarocks/rocks-%{lua_version}

install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/luarocks/config-5.1.lua

%check
# TODO - find how to run this without having to pre-download entire rocks tree
# ./test/run_tests.sh


%files
%license COPYING
%doc README.md
%dir %{_sysconfdir}/luarocks
%config(noreplace) %{_sysconfdir}/luarocks/config-%{lua_version}.lua
%config(noreplace) %{_sysconfdir}/luarocks/config-5.1.lua
%{_bindir}/luarocks
%{_bindir}/luarocks-admin
%{_prefix}/lib/luarocks
%{lua_pkgdir}/luarocks


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 15 2024 Andreas Schneider <asn@redhat.com> - 3.9.2-5
- Add support for lua 5.1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Apr 29 2023 FeRD (Frank Dana) <ferdnyc@gmail.com> - 3.9.2-1
- New upstream release
- Restore mistakenly-dropped libdir patch & refresh for 3.9.1 sources

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 14 2022 FeRD (Frank Dana) <ferdnyc@gmail.com> - 3.9.1-1
- New upstream release, drop upstreamed patch
- Raise lua-devel from Suggests to Recommends, add new Requires: gcc
  and Recommends: make and cmake (rhbz#2091484)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 3.7.0-1
- Update to 3.7.0

* Wed Jan 27 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 3.5.0-1
- Update to 3.5.0
- This package is now noarch, tested on x86_64 and i386

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-2
- Rebuilt for Lua 5.4

* Tue Mar  3 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 15 2018 Tom Callaway <spot@fedoraproject.org> - 3.0.3-1
- update to 3.0.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 13 2017 Tom Callaway <spot@fedoraproject.org> - 2.4.3-1
- update to 2.4.3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul  5 2016 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0
- Use license macro
- On Fedora, add weak dependencies on lua-sec (recommended)
  and lua-devel (suggested)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-0.3.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 10 2015 Tom Callaway <spot@fedoraproject.org> - 2.2.3-0.2.rc2
- update to 2.2.3-rc2
- fix another case of /usr/lib pathing

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2
- Add runtime dependencies on unzip and zip (h/t Ignacio Burgueño)

* Thu Jan 15 2015 Tom Callaway <spot@fedoraproject.org> - 2.2.0-2
- rebuild for lua 5.3

* Fri Oct 17 2014 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Michel Salim <salimma@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 12 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.13-2
- rebuild for lua 5.2

* Mon Apr 22 2013 Michel Salim <salimma@fedoraproject.org> - 2.0.13-1
- Update to 2.0.13

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov  5 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.12-1.1
- Fix macro problem affecting EPEL builds

* Mon Nov  5 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.12-1
- Update to 2.0.12

* Fri Sep 28 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.11-1
- Update to 2.0.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 11 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.8-2
- Add support for RHEL's older lua packaging

* Tue May  8 2012 Michel Salim <salimma@fedoraproject.org> - 2.0.8-1
- Initial package
