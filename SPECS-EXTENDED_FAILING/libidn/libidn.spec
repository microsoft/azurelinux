Vendor:         Microsoft Corporation
Distribution:   Mariner
# Build with Emacs support
%bcond_without libidn_enables_emacs
# Build with Java support
%bcond_with libidn_enables_java

Summary: Internationalized Domain Name support library
Name: libidn
Version: 1.35
Release: 8%{?dist}
URL: http://www.gnu.org/software/libidn/
License: LGPLv2+ and GPLv3+ and GFDL
Source0: http://ftp.gnu.org/gnu/libidn/libidn-%{version}.tar.gz
# Allow disabling Emacs support
Patch0: libidn-1.33-Allow-disabling-Emacs-support.patch

BuildRequires: autoconf autoconf-archive
BuildRequires: automake
BuildRequires: libtool
BuildRequires: texinfo
BuildRequires: gcc
BuildRequires: gettext gettext-devel
%if %{with libidn_enables_emacs}
BuildRequires: emacs
%endif
BuildRequires: pkgconfig
BuildRequires: help2man
# gnulib is a copylib, bundling is allowed
Provides: bundled(gnulib)
%if %{with libidn_enables_emacs}
# emacs-libidn merged with main package in 1.30-4
Obsoletes: emacs-libidn < 1.30-4
Provides: emacs-libidn = %{version}-%{release}
Requires: emacs-filesystem >= %{_emacs_version}
%endif

%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package devel
Summary: Development files for the libidn library
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes header files and libraries necessary for
developing programs which use the GNU libidn library.

%if %{with libidn_enables_java}
%package java
Summary:       Java port of the GNU Libidn library
BuildRequires: java-devel
BuildRequires: javapackages-local
BuildRequires: mvn(com.google.code.findbugs:annotations)
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(junit:junit)
BuildArch:     noarch

%description java
GNU Libidn is a fully documented implementation of the Stringprep,
Punycode and IDNA specifications. Libidn's purpose is to encode
and decode internationalized domain names.

This package contains the native Java port of the library.

%package javadoc
Summary:       Javadoc for %{name}-java
BuildArch:     noarch

%description javadoc
This package contains javadoc for %{name}-java.
%endif

%prep
%setup -q
%patch0 -p1
autoreconf -vif
# Prevent from regenerating sources by gengetopt because it's broken.
touch src/idn_cmd.c src/idn_cmd.h

# Cleanup
find . -name '*.jar' -print -delete
find . -name '*.class' -print -delete

%if %{with libidn_enables_java}
# Not available test dep
%pom_remove_dep com.google.caliper:caliper java/pom.xml.in
%endif

%build
%configure --disable-csharp --disable-static \
%if %{with libidn_enables_emacs}
    --enable-emacs \
    --with-lispdir=%{_emacs_sitelispdir}/%{name} \
%else
    --disable-emacs \
%endif
%if %{with libidn_enables_java}
    --enable-java
%else
    --disable-java
%endif

# remove RPATH hardcoding
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# without RPATH this needs to be set for idn executed by help2man
export LD_LIBRARY_PATH=$(pwd)/lib/.libs

make %{?_smp_mflags} V=1

%check
# without RPATH this needs to be set to test the compiled library
export LD_LIBRARY_PATH=$(pwd)/lib/.libs
make %{?_smp_mflags} -C tests check VALGRIND=env

%install
make install DESTDIR=$RPM_BUILD_ROOT pkgconfigdir=%{_libdir}/pkgconfig \
%if %{with libidn_enables_java}
    libidn_jardir=%{_javadir} \
%endif
    ;

# provide more examples
make %{?_smp_mflags} -C examples distclean

# clean up docs
find doc -name "Makefile*" | xargs rm
rm -rf $RPM_BUILD_ROOT%{_datadir}/info/dir

# Make multilib safe:
sed -i '/gnu compiler/d' $RPM_BUILD_ROOT%{_includedir}/idn-int.h

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la \
      $RPM_BUILD_ROOT%{_datadir}/info/*.png

%if %{with libidn_enables_emacs}
%{_emacs_bytecompile} $RPM_BUILD_ROOT%{_emacs_sitelispdir}/%{name}/*.el
%endif

%if %{with libidn_enables_java}
# regenerate java documentation
rm -rf doc/java/*
%javadoc -source 1.6 -d doc/java $(find java/src/main/java -name "*.java")
# generate maven depmap
rm -rf $RPM_BUILD_ROOT%{_javadir}/libidn*.jar
%mvn_artifact java/pom.xml java/libidn-%{version}.jar
%mvn_file org.gnu.inet:libidn libidn
%mvn_install -J doc/java
%endif

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING*
%doc AUTHORS NEWS FAQ README THANKS
%{_bindir}/idn
%{_mandir}/man1/idn.1*
%{_libdir}/libidn.so.12*
%{_infodir}/%{name}.info*
%if %{with libidn_enables_emacs}
%{_emacs_sitelispdir}/%{name}
%endif

%files devel
%doc doc/libidn.html examples
%{_libdir}/libidn.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%if %{with libidn_enables_java}
%files java -f .mfiles
%license COPYING* java/LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%license COPYING* java/LICENSE-2.0.txt
%endif

%changelog
* Thu Aug 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.35-8
- Conditionally disabled build of Java-dependent components.
- Fixed "Provides" tag for "emacs-libidn".
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Owen Taylor <otaylor@redhat.com> - 1.35-4
- Handle uncompressed info pages

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.35-2
- drop obsolete fixes of info file
- drop obsolete install-info scriptlets

* Tue May 15 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.35-1
- update to 1.35

* Mon May 14 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.34-3
- ignore install-info errors in post scriptlet (#1573966)

* Fri May 04 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.34-2
- fix ABI compatibility with libidn-1.33 and earlier (#1566414 #1573961)
- add texinfo to build requirements

* Wed Apr 04 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.34-1
- update to 1.34 (CVE-2017-14062)
- include soname in file list
- use macros for ldconfig
- add gcc to build requirements

* Tue Feb 20 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.33-6
- Add missing libtool dep, minor cleanups

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Miroslav Lichvar <mlichvar@redhat.com> - 1.33-1
- update to 1.33 (CVE-2015-8948 CVE-2016-6261 CVE-2016-6262 CVE-2016-6263)

* Sat Jun 18 2016 gil cattaneo <puntogil@libero.it> 1.32-3
- rebuilt for re-generate maven depmap

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 03 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.32-1
- update to 1.32

* Mon Jul 13 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.31-1
- update to 1.31 (CVE-2015-2059)

* Thu Jun 25 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.30-4
- merge emacs-libidn with main package (#1234563)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 gil cattaneo <puntogil@libero.it> 1.30-2
- build java libidn library

* Mon Mar 02 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.30-1
- update to 1.30

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.29-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.29-1
- update to 1.29

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 1.28-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.28-1
- update to 1.28
- remove RPATH hardcoding
- move library to /usr

* Fri Jun 07 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.27-1
- update to 1.27
- make devel dependency arch-specific
- remove obsolete macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Miroslav Lichvar <mlichvar@redhat.com> - 1.26-1
- update to 1.26

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Joe Orton <jorton@redhat.com> - 1.25-2
- update to 1.25

* Tue May 15 2012 Miroslav Lichvar <mlichvar@redhat.com> - 1.24-2
- provide bundled(gnulib) (#821768)

* Sun Jan 15 2012 Robert Scheck <robert@fedoraproject.org> - 1.24-1
- Update to 1.24 (#781379)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.23-1
- update to 1.23

* Tue May 31 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.22-3
- Split emacs-libidn subpackage to avoid *.elc arch conflicts (#709136).

* Sun May 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.22-2
- Byte compile Emacs lisp files, require emacs-filesystem for dir ownership.

* Thu May 05 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.22-1
- update to 1.22

* Tue Apr 26 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.21-1
- update to 1.21

* Thu Mar 03 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.20-1
- update to 1.20
- fix requires

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 24 2010 Joe Orton <jorton@redhat.com> - 1.19-1
- update to 1.19 (#595086)

* Tue Mar 30 2010 Joe Orton <jorton@redhat.com> - 1.18-2
- add GFDL to License

* Mon Mar 29 2010 Joe Orton <jorton@redhat.com> - 1.18-1
- update to 1.18
- fix Source0 to reference gnu.org repository

* Fri Jan 29 2010 Joe Orton <jorton@redhat.com> - 1.16-1
- update to 1.16

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 10 2009 Joe Orton <jorton@redhat.com> 1.9-4
- update to 1.9 (#302111)
- update License to reflect GPLv3+ binaries, LGPLv2+ library

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Kedar Sovani <kedars@marvell.com> 0.6.14-9
- fix the problem with #include_next

* Tue Jun 10 2008 Joe Orton <jorton@redhat.com> 0.6.14-8
- fix build with latest autoconf (#449440)

* Mon Mar 31 2008 Joe Orton <jorton@redhat.com> 0.6.14-7
- fix libidn.pc for correct libdir (#439549)

* Fri Mar  7 2008 Joe Orton <jorton@redhat.com> 0.6.14-6
- drop libidn.a
- move shared library to /lib{,64} (#283651)

* Thu Feb  7 2008 Joe Orton <jorton@redhat.com> 0.6.14-5
- fix DT_RPATH in /usr/bin/idn
- convert libidn.iconv to UTF-8 (Jon Ciesla, #226029)
- fix BuildRoot tag (Jon Ciesla, #226029)

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 0.6.14-4
- drop contrib directory from docs

* Mon Aug 20 2007 Joe Orton <jorton@redhat.com> 0.6.14-3
- fix License

* Mon Jun 18 2007 Joe Orton <jorton@redhat.com> 0.6.14-2
- update to 0.6.14

* Mon Jan 29 2007 Joe Orton <jorton@redhat.com> 0.6.9-2
- update to 0.6.9
- make install-info use failsafe (Ville Skyttä, #223707)

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 0.6.8-4
- use non-GNU section in info directory (#209491)

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 0.6.8-3
- update to 0.6.8

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.5-1.1
- rebuild

* Fri Jul  7 2006 Joe Orton <jorton@redhat.com> 0.6.5-1
- update to 0.6.5

* Fri Jul  7 2006 Joe Orton <jorton@redhat.com> 0.6.4-1
- update to 0.6.4

* Thu Jun  1 2006 Joe Orton <jorton@redhat.com> 0.6.3-1
- update to 0.6.3
- fix some places where gettext() was not getting used

* Thu Jun  1 2006 Joe Orton <jorton@redhat.com> 0.6.2-4
- remove the libidn.la (#172639)

* Thu May 11 2006 Joe Orton <jorton@redhat.com> 0.6.2-3
- make idn-int.h multilib-safe

* Wed Feb 22 2006 Joe Orton <jorton@redhat.com> 0.6.2-2
- disable C# support (#182393)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.2-1.1
- bump again for double-long bug on ppc(64)

* Mon Feb 06 2006 Florian La Roche <laroche@redhat.com>
- 0.6.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Dec  4 2005 Joe Orton <jorton@redhat.com> 0.6.0-1
- update to 0.6.0

* Mon Oct 24 2005 Joe Orton <jorton@redhat.com> 0.5.20-1
- update to 0.5.20

* Mon Sep 19 2005 Joe Orton <jorton@redhat.com> 0.5.19-1
- update to 0.5.19

* Fri May 27 2005 Joe Orton <jorton@redhat.com> 0.5.17-1
- update to 0.5.17

* Fri May  6 2005 Joe Orton <jorton@redhat.com> 0.5.16-1
- update to 0.5.16

* Thu May  5 2005 Joe Orton <jorton@redhat.com> 0.5.15-2
- constify data tables in pr29.c
- clean up pre/post/postun requires

* Sun Mar 20 2005 Joe Orton <jorton@redhat.com> 0.5.15-1
- update to 0.5.15

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 0.5.13-2
- rebuild

* Mon Jan 31 2005 Joe Orton <jorton@redhat.com> 0.5.13-1
- update to 0.5.13

* Sun Dec  5 2004 Joe Orton <jorton@redhat.com> 0.5.12-1
- update to 0.5.12

* Mon Nov 29 2004 Joe Orton <jorton@redhat.com> 0.5.11-1
- update to 0.5.11 (#141094)

* Tue Nov  9 2004 Joe Orton <jorton@redhat.com> 0.5.10-1
- update to 0.5.10
- buildroot cleanup fix (Robert Scheck)

* Mon Nov  8 2004 Joe Orton <jorton@redhat.com> 0.5.9-1
- update to 0.5.9 (#138296)

* Thu Oct  7 2004 Joe Orton <jorton@redhat.com> 0.5.6-1
- update to 0.5.6 (#134343)

* Thu Sep 30 2004 Miloslav Trmac <mitr@redhat.com> - 0.5.4-3
- Fix Group: (#134068)

* Tue Aug 31 2004 Joe Orton <jorton@redhat.com> 0.5.4-2
- move ldconfig from preun to postun (#131280)

* Sun Aug  8 2004 Joe Orton <jorton@redhat.com> 0.5.4-1
- update to 0.5.4 (#129341)

* Thu Jul 15 2004 Robert Scheck <redhat@linuxnetz.de> 0.5.2-1
- upgrade to 0.5.2, enabled i18n support and info files (#127906)

* Fri Jul  9 2004 Joe Orton <jorton@redhat.com> 0.5.1-1
- update to 0.5.1 (#127496)

* Mon Jun 28 2004 Joe Orton <jorton@redhat.com> 0.5.0-1
- update to 0.5.0 (#126836)

* Tue Jun 22 2004 Than Ngo <than@redhat.com> 0.4.9-2
- add prereq: /sbin/ldconfig
- move la file in main package

* Tue Jun 15 2004 Robert Scheck <redhat@linuxnetz.de> 0.4.9-1
- upgrade to 0.4.9 (#126353)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 29 2004 Joe Orton <jorton@redhat.com> 0.4.4-1
- update to 0.4.4; remove contrib from -devel docs

* Thu Apr 29 2004 Joe Orton <jorton@redhat.com> 0.4.3-1
- update to 0.4.3, remove -rpath patch

* Tue Jan 27 2004 Joe Orton <jorton@redhat.com> 0.3.7-1
- update to 0.3.7, simplify

* Wed Jan 07 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.3.6-1mdk
- 0.3.6

* Mon Dec 15 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.3.5-1mdk
- 0.3.5

* Sun Oct 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.3.3-2mdk
- drop the "soname fix" and use the correct way...

* Sat Oct 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.3.3-1mdk
- 0.3.3

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.3.2-1mdk
- initial cooker contrib
- used the package from PLD as a start point
