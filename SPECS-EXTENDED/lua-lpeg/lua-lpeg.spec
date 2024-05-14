Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global lua_pkg_name lpeg

%global lua_version 5.4
%global lua_libdir %{_libdir}/lua/%{lua_version}
%global lua_pkgdir %{_datadir}/lua/%{lua_version}

%global lua_compat_version 5.1
%global lua_compat_libdir %{_libdir}/lua/%{lua_compat_version}
%global lua_compat_pkgdir %{_datadir}/lua/%{lua_compat_version}
%global lua_compat_builddir %{_builddir}/lua%{lua_compat_version}-%{lua_pkg_name}-%{version}-%{release}

Name:           lua-%{lua_pkg_name}
Version:        1.0.2
Release:        4%{?dist}
Summary:        Parsing Expression Grammars for Lua

License:        MIT
URL:            https://www.inf.puc-rio.br/~roberto/%{lua_pkg_name}/
Source0:        https://www.inf.puc-rio.br/~roberto/%{lua_pkg_name}/%{lua_pkg_name}-%{version}.tar.gz
Patch1:         0001-inject-ldflags.patch

BuildRequires:  gcc
BuildRequires:  lua-devel >= %{lua_version}
Requires:       lua(abi) = %{lua_version}


%description
LPeg is a new pattern-matching library for Lua, based on Parsing Expression
Grammars (PEGs).

%package -n lua%{lua_compat_version}-%{lua_pkg_name}
Summary:        Parsing Expression Grammars for Lua %{lua_compat_version}
Provides:       compat-%{name}
BuildRequires:  compat-lua-devel >= %{lua_compat_version}
Requires:       lua(abi) = %{lua_compat_version}

%description -n lua%{lua_compat_version}-%{lua_pkg_name}
LPeg is a new pattern-matching library for Lua %{lua_compat_version}

%prep
%autosetup -n %{lua_pkg_name}-%{version}

rm -rf %{lua_compat_builddir}
cp -a . %{lua_compat_builddir}

%build
make %{?_smp_mflags} COPT="%{optflags}" LDFLAGS="%{build_ldflags}"

pushd %{lua_compat_builddir}
make %{?_smp_mflags} COPT="-I%{_includedir}/lua-%{lua_compat_version} %{optflags}" LDFLAGS="-L%{lua_compat_libdir} %{build_ldflags}"
popd

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{lua_libdir}
%{__mkdir_p} %{buildroot}%{lua_pkgdir}
%{__install} -p lpeg.so %{buildroot}%{lua_libdir}/lpeg.so.%{version}
%{__ln_s} lpeg.so.%{version} %{buildroot}%{lua_libdir}/lpeg.so
%{__install} -p -m 0644 re.lua %{buildroot}%{lua_pkgdir}

pushd %{lua_compat_builddir}
%{__mkdir_p} %{buildroot}%{lua_compat_libdir}
%{__mkdir_p} %{buildroot}%{lua_compat_pkgdir}
%{__install} -p lpeg.so %{buildroot}%{lua_compat_libdir}/lpeg.so.%{version}
%{__ln_s} lpeg.so.%{version} %{buildroot}%{lua_compat_libdir}/lpeg.so
%{__install} -p -m 0644 re.lua %{buildroot}%{lua_compat_pkgdir}
popd


%check
lua test.lua

%files
%license lpeg.html re.html
%doc HISTORY lpeg-128.gif test.lua
%{lua_libdir}/*
%{lua_pkgdir}/*

%files -n lua%{lua_compat_version}-%{lua_pkg_name}
%license lpeg.html re.html
%{lua_compat_libdir}/*
%{lua_compat_pkgdir}/*


%changelog
* Fri Feb 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-4
- Fixing run-time dependencies.
- License verified.

* Fri Jan 08 2021 Joe Schmitt <joschmit@microsoft.com> - 1.0.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora/RHEL version checks

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 Tomas Krizek <tomas.krizek@nic.cz> - 1.0.2-1
- Update to latest upstream release (BZ#1375680)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Tomas Krizek <tomas.krizek@nic.cz> - 1.0.1-10
- Use lua5.1-lpeg as Lua 5.1 naming convetion
  https://pagure.io/packaging-committee/issue/878

* Mon Mar 11 2019 Aron Griffis <aron@scampersand.com> - 1.0.1-9
- Add compat 5.1 build for neovim, rhbz #1685783

* Mon Mar 11 2019 Rafael dos Santos <rdossant@redhat.com> - 1.0.1-6
- Use standard Fedora linker flags (bug #1548714)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 15 2017 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jul 26 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.12.2-1
- Update to 0.12.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Tom Callaway <spot@fedoraproject.org> - 0.12.1-1
- update to 0.12.1
- rebuild for lua 5.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Tom Callaway <spot@fedoraproject.org> - 0.12-1
- update to 0.12, lua 5.2

* Wed Apr  3 2013 Michel Alexandre Salim <michel@verity.localdomain> - 0.11-1
- Update to 0.11

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Michel Salim <salimma@fedoraproject.org> - 0.10.2-1
- Update to 0.10.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Tim Niemueller <tim@niemueller.de> - 0.9-1
- Update to 0.9

* Fri Jun 13 2008 Tim Niemueller <tim@niemueller.de> - 0.8.1-2
- Consistent macro usage, moved sed/chmod to prep

* Thu Jun 12 2008 Tim Niemueller <tim@niemueller.de> - 0.8.1-1
- Initial package

