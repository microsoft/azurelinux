# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1

%bcond_without python3
%if 0%{?rhel} > 7 || 0%{?fedora} > 29
%bcond_with    python2
%else
%bcond_without python2
%endif
%bcond_without  perl
%bcond_without  ecdsa
%if 0%{?fedora} >= 26 || 0%{?rhel} > 7
%bcond_without  eddsa
%bcond_without  dane_ta
%else
%bcond_with     eddsa
%bcond_with     dane_ta
%endif
# GOST is not allowed in Fedora/RHEL due to legal reasons (not NIST ECC)
%bcond_with     gost

%if %{with python2} || %{with python3}
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

%global forgeurl https://github.com/NLnetLabs/%{name}
%global downloadurl https://www.nlnetlabs.nl/downloads/%{name}

Summary: Low-level DNS(SEC) library with API
Name: ldns
Version: 1.9.0
Release: 2%{?dist}

License: BSD-3-Clause
Url: https://www.nlnetlabs.nl/%{name}/
Vcs: git:%{forgeurl}
Source0: %{downloadurl}/%{name}-%{version}.tar.gz
Source1: %{downloadurl}/%{name}-%{version}.tar.gz.asc
# Willem Toorop, https://www.nlnetlabs.nl/people/
Source2: https://keys.openpgp.org/vks/v1/by-fingerprint/DC34EE5DB2417BCC151E5100E5F8F8212F77A498#/wtoorop.asc
Patch1: ldns-1.7.0-multilib.patch
# https://github.com/NLnetLabs/ldns/pull/288
Patch8: ldns-1.9-std23-bool.patch

BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: autoconf-archive

BuildRequires: gcc, make
BuildRequires: libpcap-devel
%if %{with dane_ta}
BuildRequires: openssl-devel >= 1.1.0
%else
BuildRequires: openssl-devel >= 1.0.2k
%endif
BuildRequires: gcc-c++
BuildRequires: doxygen
BuildRequires: gnupg2

%if %{with python2}
BuildRequires: python2-devel, swig
%endif
%if %{with python3}
BuildRequires: python3-devel, swig
%endif
%if %{with perl}
BuildRequires: perl-devel
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-generators
BuildRequires: perl(Devel::CheckLib)
# workaround for koji / perl bug
BuildRequires: perl-interpreter
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


%if %{with python2}
%package -n python2-ldns
Summary: Python2 extensions for ldns
Requires: %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-ldns}

%description -n python2-ldns
Python2 extensions for ldns
%endif


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
%if 0%{?fedora}
%gpgverify -d 0 -s 1 -k 2
%endif

%autosetup -cn %{pkgname} -N
pushd %{pkgname}

%autopatch -p2

rm -f config.guess config.sub ltmain.sh
# Use ax_python_devel from autoconf-archive
cp -p %{_datadir}/aclocal/{ax_python_devel,ax_pkg_swig}.m4 .
aclocal
libtoolize -c --install
autoreconf --install

# copy common doc files - after here, since it may be patched
cp -pr doc LICENSE README* Changelog ../
cp -p contrib/ldnsx/LICENSE ../LICENSE.ldnsx
cp -p contrib/ldnsx/README ../README.ldnsx
popd

%if %{with python3}
cp -a %{pkgname} %{pkgname}_python3
%endif

%if %{with python2}
cp -a %{pkgname} %{pkgname}_python2
%endif


%build
CFLAGS="%{optflags} -fPIC -fno-strict-aliasing -DOPENSSL_NO_ENGINE"
CXXFLAGS="%{optflags} -fPIC -fno-strict-aliasing -DOPENSSL_NO_ENGINE"
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

%global common_args \\\
  --disable-rpath \\\
  %{enable_gost} %{enable_ecdsa} %{enable_eddsa} %{?disable_dane_ta} \\\
  --with-ca-file=/etc/pki/tls/certs/ca-bundle.trust.crt \\\
  --with-ca-path=/etc/pki/tls/certs/ \\\
  --with-trust-anchor=%{_sharedstatedir}/unbound/root.key \\\
  --disable-static \\\

%if 0%{with python3}
pushd %{pkgname}_python3
%else
pushd %{pkgname}
%endif

%configure \
  %{common_args} \
  --with-examples \
  --with-drill \
%if %{with python3}
  --with-pyldns PYTHON=%{__python3}
%endif

# Using 'make' instead of 'make_build' macro to prevent build from failing
make
%make_build doc

# Multilib conflict avoidance
sed -e "s,-L%{_libdir},," -i packaging/ldns-config

# We cannot use the built-in --with-p5-dns-ldns
%if %{with perl}
  pushd contrib/DNS-LDNS
  LD_LIBRARY_PATH="../../lib:$LD_LIBRARY_PATH" perl \
      Makefile.PL INSTALLDIRS=vendor  INC="-I. -I../.." LIBS="-L../../lib"
  %make_build -j1
  popd
%endif

# specfic hardening options should not end up in ldns-config
sed -i "s~$RPM_LD_FLAGS~~" packaging/ldns-config
mv doc/html ../doc
popd

%if %{with python2}
  pushd %{pkgname}_python2
  %configure \
    %{common_args} \
    --with-pyldns PYTHON=%{__python2}

  %make_build
  sed -e "s,-L%{_libdir},," -i packaging/ldns-config
  popd
%endif



%install
rm -rf %{buildroot}

%if %{with python3}
pushd %{pkgname}_python3
%else
pushd %{pkgname}
%endif

mkdir -p %{buildroot}%{_libdir}/pkgconfig
%make_install

# remove .la files
rm -rf %{buildroot}%{_libdir}/*.la
%if %{with python3}
rm -rf %{buildroot}%{python3_sitearch}/*.la
%endif

%if %{with perl}
  %make_install -j1 -C contrib/DNS-LDNS pure_install
  chmod 755 %{buildroot}%{perl_vendorarch}/auto/DNS/LDNS/LDNS.so
  rm -f %{buildroot}%{perl_vendorarch}/auto/DNS/LDNS/{.packlist,LDNS.bs}
  rm -f %{buildroot}%{perl_archlib}/perllocal.pod
%endif
popd

%if %{with python2}
  pushd %{pkgname}_python2
  %make_install install-pyldns install-pyldnsx
  rm -rf %{buildroot}%{_libdir}/*.la %{buildroot}%{python2_sitearch}/*.la
  popd
%endif

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
%{_libdir}/libldns.so.3*

%files utils
%{_bindir}/drill
%{_bindir}/ldnsd
%{_bindir}/ldns-chaos
%{_bindir}/ldns-compare-zones
%{_bindir}/ldns-[d-z]*
%{_mandir}/man1/drill*
%{_mandir}/man1/%{name}*

%files devel
%doc Changelog README.git
%{_libdir}/libldns.so
%{_libdir}/pkgconfig/ldns.pc
%{_bindir}/ldns-config
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_mandir}/man3/%{name}*.3*

%if %{with python2}
%files -n python2-ldns
%doc %{pkgname}_python2/contrib/python/Changelog README.ldnsx
%license LICENSE.ldnsx
%{python2_sitearch}/%{name}.py*
%{python2_sitearch}/%{name}x.py*
%{python2_sitearch}/_%{name}.so*
%endif

%if %{with python3}
%files -n python3-ldns
%doc %{pkgname}_python3/contrib/python/Changelog README.ldnsx
%license LICENSE.ldnsx
%pycached %{python3_sitearch}/%{name}.py
%pycached %{python3_sitearch}/%{name}x.py
%{python3_sitearch}/_%{name}.so*
%endif

%if %{with perl}
%files -n perl-ldns
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%{_mandir}/man3/DNS::LDNS*.3pm.gz
%endif

%files doc
%doc doc/dns-lib-implementations
%doc doc/TODO
%doc doc/*.css
%doc doc/images/
%doc doc/html/
%doc doc/*.dox

%changelog
* Thu Dec 04 2025 Petr Menšík <pemensik@redhat.com> - 1.9.0-1
- Update 1.9.0 (rhbz#2416980)

* Thu Dec 04 2025 Petr Menšík <pemensik@redhat.com> - 1.8.4-9
- Fix gcc std23 error in bool definition (rhbz#2416980)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.8.4-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Sep 16 2025 Petr Menšík <pemensik@redhat.com> - 1.8.4-7
- Correct include path in libldns.pc (rhbz#2338878)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.8.4-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.4-4
- Perl 5.42 rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.8.4-3
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 07 2024 Petr Menšík <pemensik@redhat.com> - 1.8.4-1
- Update to 1.8.4

* Wed Oct 16 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.3-18
- Fix for SWIG 4.3.0

* Fri Jul 19 2024 Petr Menšík <pemensik@redhat.com> - 1.8.3-17
- Remove unneeded openssl/engine.h causing build failures
- Explicitly disable openssl engine (rhbz#2295742)
- Correctly include generated HTML documentation

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.3-15
- Perl 5.40 rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.8.3-14
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Florian Weimer <fweimer@redhat.com> - 1.8.3-13
- SWIG 4.2 and i686 compatibility

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Petr Menšík <pemensik@redhat.com> - 1.8.3-10
- Update address of b.root-servers.net and some others (#2253462)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.3-8
- Perl 5.38 rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.8.3-7
- Rebuilt for Python 3.12

* Wed Jan 25 2023 Petr Menšík <pemensik@redhat.com> - 1.8.3-6
- Python packaging cleanups (#2155003)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Petr Menšík <pemensik@redhat.com> - 1.8.3-4
- Return back dist tag to release

* Tue Jan 03 2023 Petr Menšík <pemensik@redhat.com> - 1.8.3-3
- Use recent autoconf python detection (#2155003)
- Install python modules into separate directories

* Fri Sep 30 2022 Petr Menšík <pemensik@redhat.com> - 1.8.3-2
- Update License tag to SPDX identifier

* Fri Aug 19 2022 Paul Wouters <pwouters@redhat.com> - 1.8.3-1
- Update to 1.8.3
- Remove --enable-rrtype-svcb-https, it is now enabled by default
- Bugfix #183: Assertion failure with OPT record without rdata.
- minor other fixups

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.8.1-6
- Rebuilt for Python 3.11

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.1-5
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 08 2021 Richard Lescak <rlescak@redhat.com> - 1.8.1-3
- Replaced 'make_build' macro with 'make' to prevent build from failing

* Mon Dec 06 2021 Petr Menšík <pemensik@redhat.com> - 1.8.1-2
- Enable svcb and https record type support
- Remove multilib conflict in ldns-devel

* Mon Dec 06 2021 Paul Wouters <paul.wouters@aiven.io> - 1.8.1-1
- Resolves: rhbz#2028465 Heap out-of-bound read vulnerability in rr_frm_str_internal function
- Resolves: rhbz#2028468 Heap out-of-bound read vulnerability in ldns_nsec3_salt_data function
- Resolves: rhbz#2028472 Fixed time memory compare for Openssl 0.9.8

* Mon Oct 11 2021 Richard Lescak <rlescak@redhat.com> - 1.7.1-10
- Added patch for failing rebuild with OpenSSL 3.0.0 (#2010601)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.7.1-9
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Petr Menšík <pemensik@redhat.com> - 1.7.1-7
- Support python3.10 builds (#1948435)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.7.1-6
- Rebuilt for Python 3.10

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.1-5
- Perl 5.34 rebuild

* Thu May 20 2021 Paul Wouters <paul.wouters@aiven.io> - 1.7.1-4
- Resolves rhbz#1962010 drill fails on sig chase

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Petr Menšík <pemensik@redhat.com> - 1.7.1-2
- Use make_build and make_install macro instead of make
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Thu Oct 08 2020 Petr Menšík <pemensik@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.0-31
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-30
- Rebuilt for Python 3.9

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
