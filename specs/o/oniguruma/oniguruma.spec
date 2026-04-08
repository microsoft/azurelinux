# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine	_changelog_trimtime

%global git_snapshot 0

%if 0%{?git_snapshot}
%define apply_git_patch git am
%else
%define apply_git_patch patch -p1
%endif

%if 0%{?git_snapshot}
%global         gitdate       20230501
%global         gitcommit     41a3b802af2155eef6d648aa3608e39605110642
%global         shortcommit   %(c=%{gitcommit}; echo ${c:0:7})

%global         gitversion    %{gitdate}git%{shortcommit}
%endif

%global	mainver	6.9.10
#%%global	postver	1
#%%global	betaver	rc4
#%%define	prerelease	1

%global	baserelease	3

Name:		oniguruma
Version:	%{mainver}%{?postver:.%postver}%{?gitversion:^%{?gitversion}}
Release:	%{?prerelease:0.}%{baserelease}%{?dist}
Summary:	Regular expressions library

# SPDX confirmed
License:	BSD-2-Clause
URL:		https://github.com/kkos/oniguruma/
Source0:	https://github.com/kkos/oniguruma/releases/download/v%{mainver}%{?betaver:_%betaver}/onig-%{mainver}%{?postver:.%postver}%{?betaver:-%betaver}%{?gitversion:-%{?gitversion}}.tar.gz
Source1:	create-tarball-from-git.sh

BuildRequires:	make
BuildRequires:	gcc
%if 0%{?git_snapshot}
BuildRequires:  automake
BuildRequires:  libtool
%endif

%description
Oniguruma is a regular expressions library.
The characteristics of this library is that different character encoding
for every regular expression object can be specified.
(supported APIs: GNU regex, POSIX and Oniguruma native)


%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n onig-%{mainver}%{?gitversion:-%{?gitversion}}
%{__sed} -i.multilib -e 's|-L@libdir@||' onig-config.in

%build
# This package fails its testsuite when compiled with LTO, but the real problem
# is that it ends up mixing and matching regexp bits between itself and glibc.
# Disable LTO
%define _lto_cflags %{nil}

%if 0%{?git_snapshot}
autoreconf -fi
%endif

%configure \
	--enable-posix-api \
	--enable-binary-compatible-posix-api \
	--disable-silent-rules \
	--disable-static \
	--with-rubydir=%{_bindir} \
	%{nil}
%make_build

%install
%make_install

%check
%{__make} check

%ldconfig_scriptlets


%files
%defattr(-,root,root,-)
%doc	AUTHORS
%license	COPYING
%doc	HISTORY
%doc	README.md
%doc	index.html
%lang(ja)	%doc	README_japanese
%lang(ja)	%doc	index_ja.html

%{_libdir}/libonig.so.5*

%files devel
%defattr(-,root,root,-)
%doc	doc/API
%doc	doc/CALLOUTS.API
%doc	doc/CALLOUTS.BUILTIN
%doc	doc/FAQ
%doc	doc/RE
%doc	doc/SYNTAX.md
%doc	doc/UNICODE_PROPERTIES
%lang(ja)	%doc	doc/API.ja
%lang(ja)	%doc	doc/CALLOUTS.API.ja
%lang(ja)	%doc	doc/CALLOUTS.BUILTIN.ja
%lang(ja)	%doc	doc/FAQ.ja
%lang(ja)	%doc	doc/RE.ja

%{_bindir}/onig-config

%{_libdir}/libonig.so
%{_includedir}/onig*.h
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 01 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.10-1
- 6.9.10

* Mon Nov 18 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.9-5
- Apply upstream patch for C23 compliance

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 17 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.9-1
- 6.9.9

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.8^20230501git41a3b80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat May  6 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.8^20230501git41a3b80-1
- Update to the latest git

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.8-2.D20220919gitb041f6d.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 23 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.8-2.D20220919gitb041f6d
- Update to the latest git, expecially:
  - Update to Unicode 15.0 (upstream #272)
  - [[:punct:]] behavoir change (upsteam #268)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.8-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 30 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.8-1
- 6.9.8

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.7.1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.7.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May  1 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.7.1-1
- 6.9.7.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.6-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.6-1
- 6.9.6

* Wed Oct 21 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.6-0.4.rc4
- 6.9.6 rc4

* Tue Oct 20 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.6-0.3.rc3
- Apply upstream patch for upstream bug 221
  - Revert change for false CVE-2020-26159 issue
    https://github.com/kkos/oniguruma/issues/221

* Sat Oct 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.6-0.2.rc3
- 6.9.6 rc3

* Mon Oct 12 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.6-0.1.rc2
- 6.9.6 rc2
- Apply upstream patch to keep binary compatibility with 6.9.5

* Thu Oct  1 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.5-3.rev1
- Apply upstream fix for CVE-2020-26159

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.5-2.rev1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 6.9.5-2.rev1.1
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jul  1 2020 Jeff Law <law@redhat.com> - 6.9.5-2.rev1
- Disable LTO

* Thu May  7 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.5-1.rev1
- 6.9.5 revised 1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 29 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.4-1
- 6.9.4 final

* Fri Nov 29 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.4-0.2.rc3
- 6.9.4 rc3 (CVE-2019-19204 CVE-2019-19203 CVE-2019-19012)

* Sat Nov  9 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.4-0.1.rc1
- 6.9.4 rc1 (CVE-2019-19246)

* Sun Aug 11 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.3-1
- 6.9.3 (CVE-2019-13224 CVE-2019-13225 CVE-2019-16163)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 12 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.2-2
- Upstream patch for CVE-2019-13225 (#1728966)
- NON-upstream patch for CVE-2019-13224 (#1728971)

* Tue May  7 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.2-1
- rc3 released as 6.9.2 final release

* Wed Apr 24 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.2-0.1.rc3
- 6.9.2-rc3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.1-1
- 6.9.1

* Wed Sep 12 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.0-2
- 6.9.0

* Sat Sep  8 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.8.2-3
- Bump release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 23 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.8.2-1
- 6.8.2

* Sun Apr  1 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.8.1-1
- 6.8.1

* Fri Feb  9 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.7.1-1
- 6.7.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 31 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.7.0-1
- 6.7.0

* Tue Sep  5 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.6.1-1
- 6.6.1

* Sun Aug 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.5.0-1
- 6.5.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul  5 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.4.0-1
- 6.4.0

* Tue May 30 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.3.0-1
- 6.3.0
  - CVEs 2017-9226 CVE-2017-9225 CVE-2017-9224 CVE-2017-9227 CVE-2017-9229 CVE-2017-9228

* Wed Apr 26 2017 Nils Philippsen <nils@redhat.com> - 6.2.0-2
- remove unnecessary BR: ruby

* Fri Apr 21 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.1.3-1
- 6.1.3

* Fri Nov 11 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.1.2-1
- 6.1.2

* Sun Oct 30 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.1.1-1
- 6.1.1

* Mon Jul 11 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan  2 2015 <mtasaka@fedoraproject.org> - 5.9.6-1
- 5.9.6

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.5-1
- 5.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.3-1
- 5.9.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 5.9.2-3
- F-17: rebuild against gcc47

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 15 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.2-1
- 5.9.2

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-3
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-2
- F-11: Mass rebuild

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against gcc43

* Thu Dec 27 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-1
- 5.9.1

* Wed Dec  5 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.0-1
- Initial packaging

