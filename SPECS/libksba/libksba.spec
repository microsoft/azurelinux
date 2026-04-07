# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

Summary: CMS and X.509 library
Name:    libksba
Version: 1.6.7
Release: 4%{?dist}

# The library is licensed under LGPLv3+ or GPLv2+,
# the rest of the package under GPLv3+
License: GPL-3.0-or-later AND LGPL-2.1-or-later AND (LGPL-3.0-or-later OR GPL-2.0-or-later)
URL:     https://www.gnupg.org/
Source0: https://www.gnupg.org/ftp/gcrypt/libksba/libksba-%{version}.tar.bz2
Source1: https://www.gnupg.org/ftp/gcrypt/libksba/libksba-%{version}.tar.bz2.sig
Source2: https://gnupg.org/signature_key.asc

Patch1: libksba-1.3.0-multilib.patch

BuildRequires: gcc
BuildRequires: gawk
%if %{without bootstrap}
# Require gnupg2 to verify sources, unless bootstrapping
BuildRequires: gnupg2
%endif
BuildRequires: libgpg-error-devel >= 1.8
BuildRequires: libgcrypt-devel >= 1.2.0
BuildRequires: make

%description
KSBA (pronounced Kasbah) is a library to make X.509 certificates as
well as the CMS easily accessible by other applications.  Both
specifications are building blocks of S/MIME and TLS.

%package devel
Summary: Development headers and libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
%{summary}.


%prep
%if %{without bootstrap}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%endif
%setup -q

%patch 1 -p1 -b .multilib

# Convert to utf-8
for file in THANKS; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%configure \
  --disable-dependency-tracking \
  --disable-static

%make_build


%install
%make_install

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
make check


%ldconfig_scriptlets

%files
%license COPYING COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv3
%doc AUTHORS ChangeLog NEWS README* THANKS TODO
%{_libdir}/libksba.so.8*

%files devel
%{_bindir}/ksba-config
%{_libdir}/libksba.so
%{_includedir}/ksba.h
%{_datadir}/aclocal/ksba.m4
%{_libdir}/pkgconfig/ksba.pc
%{_infodir}/ksba.info*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Jakub Jelen <jjelen@redhat.com> - 1.6.7-1
- New upstream release (#2265627)

* Mon Feb 26 2024 Jakub Jelen <jjelen@redhat.com> - 1.6.6-1
- New upstream release (#2265627)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 16 2023 Jakub Jelen <jjelen@redhat.com> - 1.6.5-1
- New upstream release (#2250046)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Jakub Jelen <jjelen@redhat.com> - 1.6.4-1
- New upstream release (#2215873)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Todd Zullinger <tmz@pobox.com> - 1.6.3-1
- New upstream release (#2155172)

* Fri Oct 07 2022 Jakub Jelen <jjelen@redhat.com> - 1.6.2-1
- New upstream release (#2132953)

* Mon Sep 19 2022 Jakub Jelen <jjelen@redhat.com> - 1.6.1-1
- New upstream release (#2127464)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Jakub Jelen <jjelen@redhat.com> - 1.6.0-1
- New upstream release (#1970445)

* Thu Apr 15 2021 Jakub Jelen <jjelen@redhat.com> - 1.5.1-2
- Address issues reported by coverity

* Wed Apr 07 2021 Jakub Jelen <jjelen@redhat.com> - 1.5.1-1
- New upstream release (#1946544)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 01 2020 Jakub Jelen <jjelen@redhat.com> - 1.5.0-1
- New upstream release (#1899183)

* Tue Oct  6 2020 Tomas Mraz <tmraz@redhat.com> - 1.4.0-1
- New upstream version 1.4.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.3.5-12
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.5-6
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb  2 2017 Tomáš Mráz <tmraz@redhat.com> - 1.3.5-2
- mark license files as such in the file list (#1418513)

* Mon Aug 29 2016 Tomáš Mráz <tmraz@redhat.com> - 1.3.5-1
- new upstream release fixing minor security issues

* Thu May 12 2016 Tomáš Mráz <tmraz@redhat.com> - 1.3.4-1
- new upstream release fixing minor security issues

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Tomáš Mráz <tmraz@redhat.com> - 1.3.3-1
- new upstream release fixing minor security issues

* Wed Nov 26 2014 Tomáš Mráz <tmraz@redhat.com> - 1.3.2-1
- new upstream release fixing a security issue

* Fri Sep 19 2014 Tomáš Mráz <tmraz@redhat.com> - 1.3.1-1
- new upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec  3 2012 Tomas Mraz <tmraz@redhat.com> - 1.3.0-2
- fix multilib conflict in libksba-config

* Wed Nov 21 2012 Tomas Mraz <tmraz@redhat.com> - 1.3.0-1
- new upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Tomas Mraz <tmraz@redhat.com> - 1.2.0-1
- new upstream version

* Thu Jun 02 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.8-3
- libksba-devel multilib conflict (#601976)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.8-1
- libksba-1.0.8

* Fri Jan  8 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.7-1
- new upstream version

* Thu Dec 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.6-4
- better (upstreamable) multilib patch
- tighten %%files a bit

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.0.6-3
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Rex Dieter <rdieter@fedorproject.org> - 1.0.6-1
- libksba-1.0.6
- -devel: fix info scriptlet

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 09 2009 Rex Dieter <rdieter@fedoraproject.org> 1.0.5-1
- libksba-1.0.5

* Tue Sep 23 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-1
- libksba-1.0.4

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-2
- multiarch conflicts (#342201)

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-1
- libksba-1.0.3

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.2-4
- respin (gcc43)

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-3
- BR: gawk

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-2
- respin (ppc32, BuildID)
- License: GPLv3

* Fri Jul 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-1
- libksba-1.0.2

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.1-1
- libksba-1.0.1

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.0-1.1
- respin

* Thu Aug 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.0-1
- libksba-1.0.0

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.15-3
- fc6 respin

* Tue Jun 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.15-2
- 0.9.15

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.13-2.1
- fc5: gcc/glibc respin

* Wed Nov 30 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.13-2
- remove hacks
- drop self Obsoletes

* Wed Nov 30 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.13-1
- 0.9.13

* Fri Aug 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.11-3
- botched Obsoletes good, let's try again.

* Fri Aug 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.11-2
- revert to 0.9.11 (0.9.12 makes gnupg2 fail on x86_64) using Obsoletes
  to avoid Epoch or other ugly means.

* Mon Aug  8 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.12-1
- 0.9.12
- --disable-static

* Thu Apr 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.11-1
- 0.9.11
- drop upstreamed acquote patch

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.9-2
- rebuilt

* Tue Feb  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9.9-1
- Minus BR libtool, add epoch to -devel req, fix underquoted ksba.m4.

* Fri Oct 22 2004 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.9.9-0.fdr.2
- remove hard-coded .gz from %%post/%%postun
- add %%check section

* Tue Oct 19 2004 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.9.9-0.fdr.1
- 0.9.9

* Thu Mar 20 2003 Ville Skyttä <ville.skytta@iki.fi> - 0.4.7-0.fdr.1
- Update to 0.4.7, and to current Fedora guidelines.
- Exclude %%{_libdir}/*.la.

* Wed Feb 12 2003 Warren Togami <warren@togami.com> 0.4.6-1.fedora.3
- temporary workaround to lib/dir conflict problem

* Sat Feb  8 2003 Ville Skyttä <ville.skytta@iki.fi> - 0.4.6-1.fedora.1
- First Fedora release.
