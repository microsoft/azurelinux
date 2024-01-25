%global _hardened_build 1

%bcond_without python3

%bcond_without  perl
%bcond_without  ecdsa

%bcond_without  eddsa
%bcond_without  dane_ta

# GOST is not allowed in Fedora/RHEL due to legal reasons (not NIST ECC)
%bcond_with     gost

%{?!snapshot:         %global snapshot        0}

%if %{with python3}
%{?filter_setup:
%global _ldns_internal_filter /^_ldns[.]so.*/d;
%filter_from_requires %{_ldns_internal_filter}
%filter_from_provides %{_ldns_internal_filter}
%filter_setup
}
%global _ldns_internal _ldns[.]so[.].*
%global __requires_exclude ^(%{_ldns_internal})$
%global __provides_exclude ^(%{_ldns_internal})$
%endif

%if %{with perl}
%{?perl_default_filter}
%endif


Summary:        Low-level DNS(SEC) library with API
Name:           ldns
Version:        1.8.3
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
Url:            http://www.nlnetlabs.nl/%{name}/
Source0:        http://www.nlnetlabs.nl/downloads/%{name}/%{name}-%{version}.tar.gz
Patch1:         ldns-1.7.0-multilib.patch
Patch2:         ldns-1.7.0-parse-limit.patch
Patch3:         ldns-1.7.0-realloc.patch
Patch4:         ldns-1.7.0-Update-for-SWIG-4.patch

# Only needed for builds from svn snapshot
%if 0%{snapshot}
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
%endif

BuildRequires: gcc, make
BuildRequires: libpcap-devel
%if %{with dane_ta}
BuildRequires: openssl-devel >= 1.1.0
%else
BuildRequires: openssl-devel >= 1.0.2k
%endif
BuildRequires: gcc-c++
BuildRequires: doxygen

# for snapshots only
# BuildRequires: libtool, autoconf, automake
%if %{with python3}
BuildRequires: python3-devel, swig
%endif
%if %{with perl}
BuildRequires: perl-devel
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-generators
BuildRequires: perl(Devel::CheckLib)
%endif
Requires: ca-certificates

%description
ldns is a library with the aim to simplify DNS programming in C. All
low-level DNS/DNSSEC operations are supported. We also define a higher
level API which allows a programmer to (for instance) create or sign
packets.

%package devel
Summary: Development package that includes the ldns header files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig openssl-devel

%description devel
The devel package contains the ldns library and the include files

%package utils
Summary: DNS(SEC) utilities for querying dns
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Collection of tools to get, check or alter DNS(SEC) data.


%if %{with python3}
%package -n python3-ldns
Summary: Python3 extensions for ldns
Requires: %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-ldns}

%description -n python3-ldns
Python3 extensions for ldns
%endif


%if %{with perl}
%package -n perl-ldns
Summary: Perl extensions for ldns
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-ldns
Perl extensions for ldns
%endif

%package doc
Summary: Documentation for the ldns library
BuildArch: noarch

%description doc
This package contains documentation for the ldns library

%prep
%{?extra_version:%global pkgname %{name}-%{version}%{extra_version}}%{!?extra_version:%global pkgname %{name}-%{version}}

%setup -qcn %{pkgname}
pushd %{pkgname}

%patch1 -p2 -b .multilib
%patch2 -p1 -b .limit
%patch3 -p1 -b .realloc
%patch4 -p2 -b .swig4
# To built svn snapshots
%if 0%{snapshot}
  rm config.guess config.sub ltmain.sh
  aclocal
  libtoolize -c --install
  autoreconf --install
%endif

# fixup .pc file
sed -i "s/@includedir@/@includedir@\/ldns/" packaging/libldns.pc.in

# copy common doc files - after here, since it may be patched
cp -pr doc LICENSE README* Changelog ../
cp -p contrib/ldnsx/LICENSE ../LICENSE.ldnsx
cp -p contrib/ldnsx/README ../README.ldnsx
popd

%if %{with python3}
mv %{pkgname} %{pkgname}_python3
%endif


%build
CFLAGS="%{optflags} -fPIC"
CXXFLAGS="%{optflags} -fPIC"
LDFLAGS="$RPM_LD_FLAGS -Wl,-z,now -pie"
export CFLAGS CXXFLAGS LDFLAGS

%if %{with gost}
  %global enable_gost --enable-gost
%else
  %global enable_gost --disable-gost
%endif

%if %{with ecdsa}
  %global enable_ecdsa --enable-ecdsa
%else
  %global enable_ecdsa --disable-ecdsa
%endif

%if %{with eddsa}
  %global enable_eddsa --enable-ed25519 --enable-ed448
%else
  %global enable_eddsa --disable-ed25519 --disable-ed448
%endif

%if ! %{with dane_ta}
  %global disable_dane_ta --disable-dane-ta-usage
%endif

%if 0%{with python3}
pushd %{pkgname}_python3
%else
pushd %{pkgname}
%endif # with python3

%configure \
  --disable-rpath \
  %{enable_gost} %{enable_ecdsa} %{enable_eddsa} %{?disable_dane_ta} \
  --with-ca-file=/etc/pki/tls/certs/ca-bundle.trust.crt \
  --with-ca-path=/etc/pki/tls/certs/ \
  --disable-static \
  --with-examples \
  --with-drill \
%if %{with python3}
  --with-pyldns PYTHON=%{__python3}
%endif

make %{?_smp_mflags}
make %{?_smp_mflags} doc

# We cannot use the built-in --with-p5-dns-ldns
%if %{with perl}
  pushd contrib/DNS-LDNS
  LD_LIBRARY_PATH="../../lib:$LD_LIBRARY_PATH" perl \
      Makefile.PL INSTALLDIRS=vendor  INC="-I. -I../.." LIBS="-L../../lib"
  make
  popd
%endif

# specfic hardening options should not end up in ldns-config
sed -i "s~$RPM_LD_FLAGS~~" packaging/ldns-config
popd

%install
rm -rf %{buildroot}

%if %{with python3}
pushd %{pkgname}_python3
%else
pushd %{pkgname}
%endif

make DESTDIR=%{buildroot} INSTALL="%{__install} -p" install
make DESTDIR=%{buildroot} INSTALL="%{__install} -p" install-doc

# remove .la files
rm -rf %{buildroot}%{_libdir}/*.la
%if %{with python3}
rm -rf %{buildroot}%{python3_sitearch}/*.la
%endif

# install pkg-config file
install -D -m644  packaging/libldns.pc %{buildroot}%{_libdir}/pkgconfig/ldns.pc
%if %{with perl}
  make -C contrib/DNS-LDNS DESTDIR=%{buildroot} pure_install
  chmod 755 %{buildroot}%{perl_vendorarch}/auto/DNS/LDNS/LDNS.so
  rm -f %{buildroot}%{perl_vendorarch}/auto/DNS/LDNS/{.packlist,LDNS.bs}
%endif
popd

# don't package xml files
rm doc/*.xml
# don't package building script for install-doc in doc section
rm doc/doxyparse.pl
# remove double set of man pages
rm -rf doc/man

%ldconfig_scriptlets

%files
%doc README
%license LICENSE
%{_libdir}/libldns.so.2*

%files utils
%{_bindir}/drill
%{_bindir}/ldnsd
%{_bindir}/ldns-chaos
%{_bindir}/ldns-compare-zones
%{_bindir}/ldns-[d-z]*
%{_mandir}/man1/*

%files devel
%doc Changelog README.git
%{_libdir}/libldns.so
%{_libdir}/pkgconfig/ldns.pc
%{_bindir}/ldns-config
%dir %{_includedir}/ldns
%{_includedir}/ldns/*.h
%{_mandir}/man3/*.3.gz

%if %{with python3}
%files -n python3-ldns
%doc %{pkgname}_python3/contrib/python/Changelog README.ldnsx
%license LICENSE.ldnsx
%{python3_sitearch}/*
%endif

%if %{with perl}
%files -n perl-ldns
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%{_mandir}/man3/*.3pm.gz
%endif

%files doc
%doc doc

%changelog
* Thu Jan 25 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.3-1
- Auto-upgrade to 1.8.3 - Upgrade for Azure Linux 3.0

* Mon Jul 25 2022 Rachel Menge <rachelmenge@microsoft.com> - 1.7.0-32
- Move from SPECS-EXTENDED to SPECS

* Tue Mar 22 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.0-31
- Fixing configuration step in %%build.
- Removing content related to Python 2 builds.
- Removed config option to trust "*unbound/root.key".
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.0-30
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-28
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-27
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.0-25
- Perl 5.30 rebuild

* Mon May 20 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.0-24
- Fixed build for SWIG 4.0.0 (#1707450)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 26 2018 Petr Menšík <pemensik@redhat.com> - 1.7.0-22
- Do not build python2 subpackage on Fedora 30 (#1629800)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Petr Menšík <pemensik@redhat.com> - 1.7.0-20
- Add all depends, spec cleanup, use full python interpreter

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 1.7.0-19
- Perl 5.28 rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.0-18
- Perl 5.28 rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-17
- Rebuilt for Python 3.7

* Wed Apr 11 2018 Petr Menšík <pemensik@redhat.com> - 1.7.0-16
- Make DANE TA usage more clear, autoconfigure for old fedora

* Wed Feb 21 2018 Petr Menšík <pemensik@redhat.com> - 1.7.0-15
- Experimental support for ed25519 and ed448

* Wed Feb 21 2018 Petr Menšík <pemensik@redhat.com> - 1.7.0-14
- Add only extra flags to default RPM LDFLAGS
- Fix multilib conflict of ldns-config (#1463423)
- Make primary python3 in primary build, python2 in optional

* Wed Feb 21 2018 Petr Menšík <pemensik@redhat.com> - 1.7.0-13
- Support for python3 package (#1323248)
- Moved perl manual pages to perl-ldns

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.7.0-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Nov 09 2017 Petr Menšík <pemensik@redhat.com> - 1.7.0-10
- Fix memory corruption in ldns_str2rdf_long_str (#1511046)

* Thu Nov 09 2017 Petr Menšík <pemensik@redhat.com> - 1.7.0-9
- Fix memory corruption in ldns_rr_new_frm_fp_l (#1511046)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.7.0-8
- Python 2 binary package renamed to python2-ldns
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.7.0-5
- Rebuild due to bug in RPM (RHBZ #1468476)

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.0-4
- Perl 5.26 rebuild

* Sat Mar 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.7.0-3
- explicitly track library soname (so bumps aren't a surprise)
- use %%license, drop dup'd README in -devel
- BR: openssl-devel >= 1.1.0 (required for DANE verification)

* Wed Mar 01 2017 Petr Menšík <pemensik@redhat.com> - 1.7.0-2
- Update to 1.7.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.17-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.17-20
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.17-19
- Perl 5.24 rebuild

* Thu Apr 21 2016 Paul Wouters <pwouters@redhat.com> - 1.6.17-18
- Resolves: rhbz#1190724 Missing dependency - openssl-devel

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.17-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 16 2015 Tomas Hozza <thozza@redhat.com> - 1.6.17-16
- Fix FTBFS on F23+ (#1230140)

* Wed Jun 17 2015 Paul Wouters <pwouters@redhat.com> - 1.6.17-15
- Remove obsoleted Obsolete:s
- Fix for man page generation

* Sat Jun 06 2015 Paul Wouters <pwouters@redhat.com> - 1.6.17-14
- rebuilt with --enable-rrtype-cds --enable-rrtype-uri enabled

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.17-13
- Perl 5.22 rebuild

* Mon Apr 27 2015 Paul Wouters <pwouters@redhat.com> - 1.6.17-12
- Split with_ecc macro in with_ecdsa and with_gost - and disable gost

* Mon Nov 24 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-11
- Only cond_without sets "with ", so use underscores
- multilib.patch was setting LIBDIR_SEC once without leading /

* Thu Oct 02 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-10
- Fix and install the .pc (pkg-config) file

* Wed Oct 01 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-9
- Remove hardening options from ldns-config (rhbz#1147972)

* Tue Sep 30 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-8
- Fix ldns-config (rhbz#1147972) [Florian Lehner]

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.17-7
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-4
- Rename ldns-python to python-ldns
- Rename ldns-perl to perl-ldns
- Ensure ldns-utils is dragged it so an upgrade does not remove utils

* Tue May 06 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-3
- CVE-2014-3209 ldns: ldns-keygen generates keys with world readable permissions
- Fix 1017958 - 32 and 64 bit ldns conflicts on some manual pages
- Fix rhbz#1062874 - cannot install ldns.x86_64 in parallel to ldns.i686
- Incorporate fixes from Tuomo Soini <tis@foobar.fi>
- hardened build
- fix ldns internal provides and requires filter
- fix perl-ldns requirement to include %%_isa
- setup filters for perl and python bindings for internal stuff
- split utils to separate package

* Mon Mar 24 2014 Tomas Hozza <thozza@redhat.com> - 1.6.17-2
- Fix error causing ldns to sometimes produce faulty DSA sign (#1077776)
- Fix FTBFS due to perl modules

* Fri Jan 10 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-1
- Updated to 1.6.17
- Enable perl bindings via new ldns-perl sub-package
- Enable ECDSA/GOST which is now allowed in Fedora
- Removed patches merged upstream, ported multilib patch to 1.6.17

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Tomas Hozza <thozza@redhat.com> - 1.6.16-5
- Fix compiler warnings and one uninitialized value
- make ldns-config multilib clean
- Fix man pages and usages errors

* Mon Jun 03 2013 Paul Wouters <pwouters@redhat.com> - 1.6.16-4
- Use /var/lib/unbound/root.key for --with-trust-anchor

* Fri Apr 19 2013 Adam Tkac <atkac redhat com> - 1.6.16-3
- make package multilib clean

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Paul Wouters <pwouters@redhat.com> - 1.6.16-1
- Updated to 1.6.16
- Addresses bug in 1.6.14 and 1.6.15 that affects opendnssec
  (if you have empty non-terminals and use NSEC3)

* Fri Oct 26 2012 Paul Wouters <pwouters@redhat.com> - 1.6.15-1
- Updated to 1.6.15, as 1.6.14 accidentally broke ABI
  (We never released 1.6.14)

* Tue Oct 23 2012 Paul Wouters <pwouters@redhat.com> - 1.6.14-1
- [pulled before release]
- Updated to 1.6.14
- Removed merged in patch
- Added new dependancy on ca-certificates for ldns-dane PKIX validation

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 01 2012 Paul Wouters <pwouters@redhat.com> - 1.6.13-2
- Added reworked ldns-read-zone patch from trunk
  (adds -p for SOA padding, and -o for zeroizing timestamps/sigs)

* Mon May 21 2012 Paul Wouters <pwouters@redhat.com> - 1.6.13-1
- Upgraded to 1.6.13, bugfix release
- Added --disable-ecdsa as ECC is still banned
- Removed --with-sha2 - it is always enabled and option was removed

* Wed Jan 11 2012 Paul Wouters <paul@nohats.ca> - 1.6.12-1
- Upgraded to 1.6.12, fixes important end of year handling date bug

* Wed Oct  5 2011 Paul Wouters <paul@xelerance.com> - 1.6.11-2
- Updated to 1.6.11, fixes rhbz#741026 which is CVE-2011-3581
- Python goes into sitearch, not sitelib
- Fix source link and spelling errors in description

* Mon Sep 19 2011 Paul Wouters <paul@xelerance.com> - 1.6.10-2
- Fix for losing nameserver when it drops UDP fragments in
  ldns_resolver_send_pkt [Willem Toorop <willem@NLnetLabs.nl>]
- Added ldnsx module (to be merged into ldns soon)
  http://git.xelerance.com/cgi-bin/gitweb.cgi?p=ldnsx.git;a=summary

* Wed Jun 08 2011 Paul Wouters <paul@xelerance.com> - 1.6.10-1
- Upodated to 1.6.10
- Commented out dependancies that are only needed for snapshots

* Sun Mar 27 2011 Paul Wouters <paul@xelerance.com> - 1.6.9-1
- Updated to 1.6.9

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Paul Wouters <paul@xelerance.com> - 1.6.8-1
- Updated to 1.6.8

* Thu Aug 26 2010 Paul Wouters <paul@xelerance.com> - 1.6.6-2
- Bump for EVR

* Mon Aug 09 2010 Paul Wouters <paul@xelerance.com> - 1.6.6-1
- Upgraded to 1.6.6

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Paul Wouters <paul@xelerance.com> - 1.6.5-1
- Updated to 1.6.5

* Fri Jan 22 2010 Paul Wouters <paul@xelerance.com> - 1.6.4-2
- Fix missing _ldns.so causing ldns-python to not work
- Patch for installing ldns-python files
- Patch for rpath in ldns-python
- Don't install .a file for ldns-python

* Wed Jan 20 2010 Paul Wouters <paul@xelerance.com> - 1.6.4-1
- Upgraded to 1.6.4
- Added ldns-python sub package

* Fri Dec 04 2009 Paul Wouters <paul@xelerance.com> - 1.6.3-1
- Upgraded to 1.6.3, which has minor bugfixes

* Fri Nov 13 2009 Paul Wouters <paul@xelerance.com> - 1.6.2-1
- Upgraded to 1.6.2. This fixes various bugs.
  (upstream released mostly to default with sha2 for the imminent
   signed root, but we already enabled that in our builds)

* Tue Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 1.6.1-3
- rebuilt with new openssl

* Sun Aug 16 2009 Paul Wouters <paul@xelerance.com> - 1.6.1-2
- Added openssl dependancy back in, since we get more functionality
 when using openssl. Especially in 'drill'.

* Sun Aug 16 2009 Paul Wouters <paul@xelerance.com> - 1.6.1-1
- Updated to 1.6.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Paul Wouters <paul@xelerance.com> - 1.6.0-4
- Fixed the ssl patch so it can now compile --without-ssl

* Sat Jul 11 2009 Paul Wouters <paul@xelerance.com> - 1.6.0-3
- Added patch to compile with --without-ssl
- Removed openssl dependancies
- Recompiled with --without-ssl

* Sat Jul 11 2009 Paul Wouters <paul@xelerance.com> - 1.6.0-2
- Updated to 1.6.0
- (did not yet compile with --without-ssl due to compile failures)

* Fri Jul 10 2009 Paul Wouters <paul@xelerance.com> - 1.6.0-1
- Updated to 1.6.0
- Compile without openssl

* Thu Apr 16 2009 Paul Wouters <paul@xelerance.com> - 1.5.1-4
- Memory management bug when generating a sha256 key, see:
  https://bugzilla.redhat.com/show_bug.cgi?id=493953

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Paul Wouters <paul@xelerance.com> - 1.5.1-1
- Updated to new version, 1.5.0 had a bug preventing
  zone signing.

* Mon Feb  9 2009 Paul Wouters <paul@xelerance.com> - 1.5.0-1
- Updated to new version

* Thu Feb 05 2009 Adam Tkac <atkac redhat com> - 1.4.0-3
- fixed configure flags

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.0-2
- rebuild with new openssl

* Fri Nov  7 2008 Paul Wouters <paul@xelerance.com> - 1.4.0-1
- Updated to 1.4.0

* Wed May 28 2008 Paul Wouters <paul@xelerance.com> - 1.3.0-3
- enable SHA2 functionality

* Wed May 28 2008 Paul Wouters <paul@xelerance.com> - 1.3.0-2
- re-tag (don't do builds while renaming local repo dirs)

* Wed May 28 2008 Paul Wouters <paul@xelerance.com> - 1.3.0-1
- Updated to latest release

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.2-3
- Autorebuild for GCC 4.3

* Wed Dec  5 2007 Paul Wouters <paul@xelerance.com> - 1.2.2-2
- Rebuild for new libcrypto

* Thu Nov 29 2007 Paul Wouters <paul@xelerance.com> - 1.2.2-1
- Upgraded to 1.2.2. Removed no longer needed race workaround

* Tue Nov 13 2007 Paul Wouters <paul@xelerance.com> - 1.2.1-4
- Try to fix racing ln -s statements in parallel builds

* Fri Nov  9 2007 Paul Wouters <paul@xelerance.com> - 1.2.1-3
- Added patch for ldns-read-zone that does not put @. in RRDATA

* Fri Oct 19 2007 Paul Wouters <paul@xelerance.com> - 1.2.1-2
- Use install -p to work around multilib conflicts for .h files

* Wed Oct 10 2007 Paul Wouters <paul@xelerance.com> - 1.2.1-1
- Updated to 1.2.1
- Removed patches that got moved into upstream

* Wed Aug  8 2007 Paul Wouters <paul@xelerance.com> 1.2.0-11
- Patch for ldns-key2ds to write to stdout
- Again remove extra set of man pages from doc
- own /usr/include/ldns (bug 233858)

* Wed Aug  8 2007 Paul Wouters <paul@xelerance.com> 1.2.0-10
- Added sha256 DS record patch to ldns-key2ds
- Minor tweaks for proper doc/man page installation.
- Workaround for parallel builds

* Mon Aug  6 2007 Paul Wouters <paul@xelerance.com> 1.2.0-2
- Own the /usr/include/ldns directory (bug #233858)
- Removed obsoleted patch
- Remove files form previous libtool run accidentally packages by upstream

* Mon Sep 11 2006 Paul Wouters <paul@xelerance.com> 1.0.1-4
- Commented out 1.1.0 make targets, put make 1.0.1 targets.

* Mon Sep 11 2006 Paul Wouters <paul@xelerance.com> 1.0.1-3
- Fixed changelog typo in date
- Rebuild requested for PT_GNU_HASH support from gcc
- Did not upgrade to 1.1.0 due to compile issues on x86_64

* Fri Jan  6 2006 Paul Wouters <paul@xelerance.com> 1.0.1-1
- Upgraded to 1.0.1. Removed temporary clean hack from spec file.

* Sun Dec 18 2005 Paul Wouters <paul@xelerance.com> 1.0.0-8
- Cannot use make clean because there are no Makefiles. Use hardcoded rm.

* Sun Dec 18 2005 Paul Wouters <paul@xelerance.com> 1.0.0-7
- Patched 'make clean' target to get rid of object files shipped with 1.0.0

* Tue Dec 13 2005 Paul Wouters <paul@xelerance.com> 1.0.0-6
- added a make clean for 2.3.3 since .o files were left behind upstream,
  causing failure on ppc platform

* Sun Dec 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.0-5
- minor cleanups

* Wed Oct  5 2005 Paul Wouters <paul@xelerance.com> 0.70_1205
- reworked for svn version

* Sun Sep 25 2005 Paul Wouters <paul@xelerance.com> - 0.70
- Initial version
