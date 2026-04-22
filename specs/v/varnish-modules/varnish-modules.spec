# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

%if 0%{?rhel} == 7
%global docutils python34-docutils
%global rst2man rst2man-3.4
%else
%global docutils python3-docutils
%global rst2man rst2man
%endif

Name:    varnish-modules
Version: 0.26.0
Release: 4%{?dist}
Summary: A collection of modules ("vmods") extending Varnish VCL

License: BSD-2-Clause
URL:     https://github.com/varnish/varnish-modules
Source:  https://github.com/varnish/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish

# Build from a git checkout
#BuildRequires: automake
#BuildRequires: autoconf
#BuildRequires: libtool
BuildRequires: %docutils

Requires: varnish = %varnishver

Provides: vmod(accept)%{_isa} = %{version}-%{release}
Provides: vmod(bodyaccess)%{_isa} = %{version}-%{release}
Provides: vmod(header)%{_isa} = %{version}-%{release}
Provides: vmod(saintmode)%{_isa} = %{version}-%{release}
Provides: vmod(tcp)%{_isa} = %{version}-%{release}
Provides: vmod(var)%{_isa} = %{version}-%{release}
Provides: vmod(vsthrottle)%{_isa} = %{version}-%{release}
Provides: vmod(xkey)%{_isa} = %{version}-%{release}
Provides: vmod(str)%{_isa} = %{version}-%{release}

%description
This is a collection of modules ("vmods") extending Varnish VCL used
for describing HTTP request/response policies with additional
capabilities. This collection contains the following vmods:
bodyaccess, header, saintmode, tcp, var, vsthrottle, xkey


%prep
%autosetup


%build
#sh bootstrap
export RST2MAN=%{rst2man}
%configure 
%make_build


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
#doc docs AUTHORS CHANGES.rst COPYING README.rst
%doc AUTHORS CHANGES.rst COPYING README.md
%license LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun May 25 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.26.1-2
- Rebuilt for varnish-7.7.1

* Wed Mar 26 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.26.0-1
- New upstream release for varnish-7.7.0

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.25.0-2
- Rebuilt for varnish-7.6.1

* Tue Sep 17 2024 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.25.0-1
- New upsteam release matching varnish-7.6.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 02 2024 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.24.0
- New upstream release matching varnish-7.5.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 15 2023 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.22.0-4
- Rebuilt for varnish-7.4.2

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 06 2023 Luboš Uhliarik <luhliari@redhat.com> - 0.22.0-2
- SPDX migration

* Sun Mar 19 2023 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.22.0-1
- New upstream release
- Built for varnish-7.3.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 13 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.21.0-2
- Built for varnish-7.2.1

* Mon Sep 26 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.21.0-1
- New upstream release
- Removed unused macros from specfile
- Built for varnish-7.2.0

* Mon Aug 15 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.20.0-3
- Built for varnish-7.1.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 29 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.20.0-1
- Built for varnish-7.1.0
- Now provides vmod(name) instead of vmod-name, matching varnish' provides

* Thu Feb 10 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.19.0-4
- Built for varnish-7.0.2

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.19.0-2
- Built for varnish-7.0.1

* Thu Sep 23 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.19.0-1
- New upstream release
- Built for varnish-7.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 17 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.18.0-2
- Rebuilt for varnish-6.6.1

* Tue May 18 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.18.0-1
- New upstream release
- Rebuilt for varnish-6.6.0

* Wed Mar 17 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.17.1-1
- New upstream release
- Switched back to original varnish github upstream, as it has catched up
- Includes fix for CVE-2021-28543, VSV00006, bz#1939669

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-0.3.klarlack.20200916git4d6593c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 29 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.17.0-0.2.klarlack.20200916git
- Rebuilt for varnish-6.5.1

* Wed Sep 16 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.17.0-0.1.klarlack.20200916git
- Switched upstream to Nils Goroll's fork which is the defacto current upstream
- Synced description to reality
- This is a snapshot build that needs autotools for building
- Rebuilt for varnish-6.5.0

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
