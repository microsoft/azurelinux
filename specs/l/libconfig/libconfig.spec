# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without check

Name:                   libconfig
Summary:                C/C++ configuration file library
Version:                1.7.3
Release:                12%{?dist}
# lib/grammar.* are GPL-3.0-or-later WITH Bison-exception-2.2
License:                LGPL-2.1-or-later AND GPL-3.0-or-later WITH Bison-exception-2.2
URL:                    http://www.hyperrealm.com/libconfig/
Source0:                https://hyperrealm.github.io/%name/dist/%name-%version.tar.gz
# Generated from libconfig 1.7.2 on Fedora 28 x86_64 (2018-07-18)
Source1:                libconfig-%version.pdf
# Helper script to generate Source1 (locally)
Source2:                generate-pdf.sh

# Backport of https://github.com/hyperrealm/libconfig/pull/249
Patch0:                 gcc15.patch

BuildRequires:          gcc, gcc-c++
BuildRequires:          texinfo
BuildRequires:          bison, flex
BuildRequires: make

%description
Libconfig is a simple library for manipulating structured configuration
files. This file format is more compact and more readable than XML. And
unlike XML, it is type-aware, so it is not necessary to do string parsing
in application code.


%package devel
Summary:                Development files for libconfig
Requires:               %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against
libconfig.


%prep
%setup -q
%patch -P0 -p1 -b .gcc15
iconv -f iso-8859-1 -t utf-8 -o AUTHORS{.utf8,}
mv AUTHORS{.utf8,}


%build
%configure \
  --disable-silent-rules \
  --disable-static

make %{?_smp_mflags}


%install
%make_install
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir
install -p %{SOURCE1} doc/


%if %{with check}
%check
make check
%endif


%ldconfig_scriptlets

%files
%license COPYING.LIB
%doc AUTHORS ChangeLog README
%{_libdir}/libconfig*.so.11*


%files devel
%doc doc/libconfig-%version.pdf
%{_includedir}/libconfig*
%{_libdir}/cmake/%{name}
%{_libdir}/cmake/%{name}++
%{_libdir}/libconfig*.so
%{_libdir}/pkgconfig/libconfig*.pc
%{_infodir}/libconfig.info*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar  3 2025 Tom Callaway <spot@fedoraproject.org> - 1.7.3-11
- merge pull request from yselkowitz (minus the autosetup, i like to be able to rediff patches on old things like this)
- applies upstream commit that resolves FTBFS

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Tom Callaway <spot@fedoraproject.org> - 1.7.3-1
- update to 1.7.3

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.7.2-2
- %%files: track library sonames, so bumps aren't a surprise
- %%build: --disable-silent-rules
- -devel: tighten subpkg dep with %%_isa, drop hard-coded pkgconfig dep
- use %%make_build %%make_install %%ldconfig_scriptlets

* Mon Jul 23 2018 Pavel Raiskup <praiskup@redhat.com> - 1.7.2-1
- new upstream release (rhbz#1602423)

* Mon Jul 23 2018 Pavel Raiskup <praiskup@redhat.com> - 1.5-12
- cleanup

* Sun Jul 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.5-11
- Add missing gcc-c++ dep, spec cleanups

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.5-8
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Tom Callaway <spot@fedoraproject.org> - 1.5-3
- fix pdf file by having a pre-generated pdf as source1 (bz 1292449)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 Tom Callaway <spot@fedoraproject.org> - 1.5-1
- update to 1.5

* Thu Apr 16 2015 Dominik Mierzejewski <rpm@greysector.net> - 1.4.9-8
- rebuilt for gcc-5.0.0-0.22.fc23

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep  4 2013 Tom Callaway <spot@fedoraproject.org> - 1.4.9-5
- handle everything with doc

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Pavel Raiskup <praiskup@redhat.com> - 1.4.9-3
- enable simple upstream test-suite during check phase

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct  1 2012 Tom Callaway <spot@fedoraproject.org> - 1.4.9-1
- update to 1.4.9

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.4.8-1
- update to 1.4.8

* Wed Mar 23 2011 Tom Callaway <spot@fedoraproject.org> - 1.4.7-1
- update to 1.4.7

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.6-1
- Update to 1.4.6
- Install libconfig_tests
- Fix rpmlint warnings

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May  5 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4.5-1
- update to 1.4.5

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.2-1
- update to 1.3.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.1-2
- prevent multilib conflicts with the generated pdf

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.1-1
- update to 1.3.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-2
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-1
- bump to 1.2.1

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-4
- nuke %%{_infodir}/dir, we handle it in %%post

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-3
- move all docs to devel
- move scriptlets around to match
- move requires around to match

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-2
- BR: texinfo-tex (not Requires)

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-1
- Initial package for Fedora
