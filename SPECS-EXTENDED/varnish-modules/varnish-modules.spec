Vendor:         Microsoft Corporation
Distribution:   Mariner
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

Name:    varnish-modules
Version: 0.16.0
Release: 4%{?dist}
Summary: A collection of modules ("vmods") extending Varnish VCL

License: BSD
URL:     https://github.com/varnish/%{name}
#Source:  https://download.varnish-software.com/varnish-modules/#{name}-#{version}.tar.gz
Source:  https://github.com/varnish/varnish-modules/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: python3-docutils

Requires: varnish = %varnishver

Provides: vmod-bodyaccess = %{version}-%{release}
Provides: vmod-header = %{version}-%{release}
Provides: vmod-saintmode = %{version}-%{release}
Provides: vmod-tcp = %{version}-%{release}
Provides: vmod-var = %{version}-%{release}
Provides: vmod-vsthrottle = %{version}-%{release}
Provides: vmod-xkey = %{version}-%{release}


%description
This is a collection of modules ("vmods") extending Varnish VCL used
for describing HTTP request/response policies with additional
capabilities. This collection contains the following vmods (previously
kept individually): vsthrottle, header, saintmode, softpurge,
tcp, var, xkey


%prep
%autosetup


%build
%configure 

# Build seems to suffer from race conditions during build.
%make_build -j1

%install
%make_install docdir=%_pkgdocdir
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'
rm %{buildroot}%{_pkgdocdir}/LICENSE # Rather use license macro

%check
%ifarch %ix86 %arm ppc
# 64-bit specific test
sed -i 's,tests/xkey/test12.vtc,,' src/Makefile
%endif
%make_build check VERBOSE=1


%files
%doc docs AUTHORS CHANGES.rst COPYING README.rst
%license LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*

%changelog
* Thu Jul 22 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.16.0-4
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Switching to single-threaded builds to avoid random build failures.
- Removed unnecessary 'rhel' macros.

* Mon Aug 17 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.16.0-3
- Rebuilt for varnish-6.4.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Mar 28 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.16.0-1
- New upstream release

* Tue Mar 17 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.16.0-0.1.20200317git21d0c84
- Snapshot from 6.4 branch, rebuilt against varnish-6.4.0
- Removed patches merged upstream
- Delete 64-bit specific test on 32-bit arches

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 29 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.15.0-7
- Added patch from Nils Goroll, compatibility for varnish-6.3, closes bz#1736943
- Rebuilt against varnish-6.3.0

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.15.0-5
- Install docs in correct docdir

* Fri Feb 15 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.15.0-4
- Added a simple patch from upstream, fixing a formatting bug trigged on 32bit
- Removed dependency on docutils. It is not necessary on released tarballs

* Thu Feb 14 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.15.0-3
- Added a proposed patch from Nils Goroll providing support for vmod_saintmode
  on varnish-6.1.1 (closes rhbz #1676183)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Dridi Boukelmoune <dridi@fedoraproject.org> 0.15.0-1
- Update to 0.15.0
- Drop EPEL and older Fedora releases support
- Drop broken manual ABI dependency to Varnish
- Drop commented out references to past patches
- Verbose test suite
- Simplified configure step
- Dependencies cleanup

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Oct 21 2017 Dridi Boukelmoune <dridi@fedoraproject.org> 0.12.1-5
- Update varnishabi requirement for f28

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.12.1-2
- Set correct varnishabi requirement for the different fedoras

* Wed May 31 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.12.1-1
- New uptream release
- Pull el5 support

* Mon Mar 20 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.11.0-1
- New upstream release

* Sat Sep 24 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.9.2-0.1.20160924gitdaa4f1d
- Upstream git checkout with support for varnish-5.0
- Removed patches that are included upstream
- el5 build fix

* Fri Aug 05 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.9.1-1
- New upstream release
- Build man pages, buildrequires python-docutils
- Added a patch for tests/cookie/08-overflow.vtc, upping workspace_client,
  the default is too small on 32bit
- Removed extra cflags for el5, fixed with patch from upstream
- Force readable docs and debug files, they tend to end up with mode 600

* Tue Apr 05 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.9.0-1
- First wrap for fedora
- Uses some old-style specfile components for el5 compatibility, including
  the usage of the BuildRoot header and cleaning the buildroot before install
