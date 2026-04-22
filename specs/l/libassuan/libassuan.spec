# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:    libassuan
Summary: GnuPG IPC library
Version: 2.5.7
Release: 5%{?dist}

# The library is LGPLv2+, the documentation GPLv3+
License: GPL-3.0-or-later AND LGPL-2.1-or-later AND LGPL-3.0-or-later
Source0: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2
Source1: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2.sig
URL:     https://www.gnupg.org/

Patch1:  libassuan-2.5.2-multilib.patch
Patch2:  libassuan-2.5.5-coverity.patch

BuildRequires: gcc
BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8
BuildRequires: make

%description
This is the IPC library used by GnuPG 2, GPGME and a few other
packages.

%package devel 
Summary: GnuPG IPC library 
Provides: libassuan2-devel = %{version}-%{release}
Provides: libassuan2-devel%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
%description devel 
This is the IPC static library used by GnuPG 2, GPGME and a few other
packages.

This package contains files needed to develop applications using %{name}.


%prep
%setup -q

%patch 1 -p1 -b .multilib
%patch 2 -p1 -b .coverity


%build
%configure \
  --includedir=%{_includedir}/libassuan2

%make_build


%install
%make_install

## Unpackaged files
rm -fv %{buildroot}%{_infodir}/dir
rm -fv %{buildroot}%{_libdir}/lib*.la


%check
make check


%ldconfig_scriptlets

%files
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README
%{_libdir}/libassuan.so.0*

%files devel 
%{_bindir}/libassuan-config
%{_includedir}/libassuan2/
%{_libdir}/libassuan.so
%{_libdir}/pkgconfig/libassuan.pc
%{_datadir}/aclocal/libassuan.m4
%{_infodir}/assuan.info*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Mar 07 2024 Jakub Jelen <jjelen@redhat.com> - 2.5.7-1
- New upstream release (#2268182)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Jakub Jelen <jjelen@redhat.com> - 2.5.6-1
- New upstream release (#2215873)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Apr 07 2021 Jakub Jelen <jjelen@redhat.com> - 2.5.5-2
- Address non-important coverity scan issues

* Mon Mar 22 2021 Jakub Jelen <jjelen@redhat.com> - 2.5.5-1
- New upstream release (#1941663)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 01 2020 Jakub Jelen <jjelen@redhat.com> - 2.5.4-1
- New upstream release (#1891067)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Tomáš Mráz <tmraz@redhat.com> 2.5.3-2
- add includedir to pkg-config --cflags (#1742986)

* Sat Aug  3 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2.5.3-1
- new upstream release 2.5.3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Tomáš Mráz <tmraz@redhat.com> 2.5.2-1
- new upstream release 2.5.2
- drop obsolete install-info scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.1-2
- Switch to %%ldconfig_scriptlets

* Fri Dec 08 2017 Tomáš Mráz <tmraz@redhat.com> 2.5.1-1
- new upstream release 2.5.1

* Fri Nov 24 2017 Tomáš Mráz <tmraz@redhat.com> 2.4.4-1
- new upstream release 2.4.4

* Mon Aug 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.4.3-6
- .spec cosmetics, update source URLs

* Mon Aug 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.3-5
- Drop unneeded pth-devel dependencies

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Tomáš Mráz <tmraz@redhat.com> 2.4.3-1
- new upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec  3 2015 Tomáš Mráz <tmraz@redhat.com> 2.4.2-1
- new upstream release

* Tue Nov 24 2015 Tomáš Mráz <tmraz@redhat.com> 2.4.1-1
- new upstream release

* Wed Sep  2 2015 Tomáš Mráz <tmraz@redhat.com> 2.3.0-1
- new upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Tomáš Mráz <tmraz@redhat.com> 2.2.0-1
- new upstream release

* Thu Sep 11 2014 Tomáš Mráz <tmraz@redhat.com> 2.1.2-1
- new upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 2.1.0-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Tomáš Mráz <tmraz@redhat.com> 2.1.0-1
- new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec  3 2012 Tomáš Mráz <tmraz@redhat.com> 2.0.3-4
- multilib conflict in libassuan-config fixed

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Tomáš Mráz <tmraz@redhat.com> 2.0.3-2
- add missing requires of base package

* Wed Apr 18 2012 Tomáš Mráz <tmraz@redhat.com> 2.0.3-1
- new upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Tomáš Mráz <tmraz@redhat.com> 2.0.1-1
- new upstream release

* Thu Apr 14 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-4
- Missing ldconfig calls (#696787)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-2
- -devel: Provides: libassuan2-devel

* Tue Jul 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-1
- libassuan-2.0.0 (#573796)

* Thu Dec 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-4
- better versioning for Obsoletes
- better (upstreamable) multilib patch

* Thu Dec 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.5-3
- Fix license tag - the documentation is GPLv3+

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-1
- libassuan-1.0.5

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-3
- multiarch conflicts (#341911)

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-2
- respin (gcc43)

* Wed Dec 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.4-1
- libassuan-1.0.4
- License: LGPLv2+
- disable useless -debuginfo (static libs only)

* Sun Aug 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.3-2
- BR: gawk (to reenable pth support)

* Fri Aug 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.3-1
- libassuan-1.0.3
- License: LGPLv2

* Thu Aug 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.2-2
- License: LGPLv3 (clarification, changed from LGPLv2 1.0.1 -> 1.0.2)

* Fri Jul 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.2-1
- libassuan-1.0.2
- rename -static -> -devel

* Sat Nov 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.0.1-1
- libassuan-1.0.1

* Mon Nov 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.0.0-1
- libassuan-1.0.0
- rename -devel -> -static (+Obsoletes/Provides: %%name-devel)

* Wed Oct 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.3-2
- another libassuan.m4 patch

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.3-1
- 0.9.3
- BR: pth-devel, -devel: Requires: pth-devel

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.2-1
- 0.9.2

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.ne> - 0.9.0-3
- respin

* Tue Sep 26 2006 Rex Dieter <rexdieter[AT]users.sf.net - 0.9.0-2
- -devel: Provides: %%name-static
- 0.9.0

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.10-3
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Mon Jul  4 2005 Michael Schwendt <mschwendt[at]users.sf.net> - 0.6.10-2
- Build PIC only for x86_64.

* Fri Jul  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.6.10-1
- 0.6.10, macro patch no longer needed (#162262).

* Sun May  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.9-4
- rebuilt

* Fri Mar 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.6.9-3
- Fix FC4 build and source URLs.

* Thu Feb  3 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.9-2
- Build PIC to fix x86_64 linking.

* Thu Jan 06 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.9-1
- 0.6.9

* Sat Oct 23 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.3
- *really* fix description this time.

* Fri Oct 22 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.2
- remove "We decided..." part of description
- remove hard-coded .gz info references
- Req(preun)->Preq(postun): /sbin/install-info

* Thu Oct 21 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.1
- cleanup, make presentable.

* Tue Oct 19 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.0
- first try
