Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global with_java 0
%global with_php 0
%global with_perl 1
%global with_python2 0
%global with_python3 0
%global with_wsf 0
%global obsolete_old_lang_subpackages 0
%global default_sign_algo "rsa-sha1"
%global min_hash_algo "sha1"
%global default_sign_algo "rsa-sha256"
%global min_hash_algo "sha256"

%if %{with_php}
%if "%{php_version}" < "5.6"
%global ini_name     %{name}.ini
%else
%global ini_name     40-%{name}.ini
%endif
%endif

%global with_python3 1

%global configure_args %{nil}
%global configure_args %{configure_args}

%if %{default_sign_algo}
  %global configure_args %{configure_args} --with-default-sign-algo=%{default_sign_algo}
%endif

%if %{min_hash_algo}
  %global configure_args %{configure_args} --with-min-hash-algo=%{min_hash_algo}
%endif

%if !%{with_java}
  %global configure_args %{configure_args} --disable-java
%endif

%if !%{with_perl}
  %global configure_args %{configure_args} --disable-perl
%endif

%if %{with_php}
  %global configure_args %{configure_args} --enable-php5=no --enable-php7=yes --with-php7-config-dir=%{php_inidir}
%else
  %global configure_args %{configure_args} --enable-php5=no --enable-php7=no
%endif

%if %{with_wsf}
  %global configure_args %{configure_args} --enable-wsf --with-sasl2=%{_prefix}/sasl2
%endif

%if !%{with_python2} && !%{with_python3}
  %global configure_args %{configure_args} --disable-python
%endif


Summary: Liberty Alliance Single Sign On
Name: lasso
Version: 2.8.2
Release: 15%{?dist}
License: GPL-2.0-or-later
URL: https://lasso.entrouvert.org/
Source: https://dev.entrouvert.org/lasso/lasso-%{version}.tar.gz

Patch01: fix-removed-xmlsec-deprecations.patch
Patch02: fix-openssl-implicit-declarations.patch
Patch3: lasso-libxml2.patch
# https://git.entrouvert.org/entrouvert/lasso/commit/253e8abe7b83d4d8f3d8dd5f886a54f4e173cc28
Patch4: 253e8abe7b83d4d8f3d8dd5f886a54f4e173cc28.patch
# https://git.entrouvert.org/entrouvert/lasso/commit/625bf7d9c11ec366c45514d5ec12ab1cdd8ce094
Patch5: 625bf7d9c11ec366c45514d5ec12ab1cdd8ce094.patch
# https://git.entrouvert.org/entrouvert/lasso/commit/3e6f9076e19368b29a932373955a5dccd2f3cc46
Patch6: 3e6f9076e19368b29a932373955a5dccd2f3cc46.patch
# https://dev.entrouvert.org/issues/92106
Patch7: lasso-2.8.2-python_313.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: check-devel
BuildRequires: gcc
BuildRequires: glib2-devel
BuildRequires: gtk-doc
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
BuildRequires: libxml2-devel
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: python3
BuildRequires: python3-six
BuildRequires: (python3-setuptools if python3 >= 3.12)
BuildRequires: swig
BuildRequires: xmlsec1-devel
BuildRequires: xmlsec1-openssl-devel
BuildRequires: zlib-devel
%if %{with_wsf}
BuildRequires: cyrus-sasl-devel
%endif

Requires: xmlsec1

# lasso upstream no longer supports java bindings
# see https://dev.entrouvert.org/issues/45876#change-289747
# and https://dev.entrouvert.org/issues/51418
Obsoletes: java-lasso < %{version}-%{release}

%description
Lasso is a library that implements the Liberty Alliance Single Sign On
standards, including the SAML and SAML2 specifications. It allows to handle
the whole life-cycle of SAML based Federations, and provides bindings
for multiple languages.

%package devel
Summary: Lasso development headers and documentation
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for Lasso.

%if %{with_perl}
%package -n perl-%{name}
Summary: Liberty Alliance Single Sign On (lasso) Perl bindings
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl-interpreter
BuildRequires: perl(Error)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(strict)
BuildRequires: perl(Test::More)
BuildRequires: perl(warnings)
BuildRequires: perl(XSLoader)
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n perl-%{name}
Perl language bindings for the lasso (Liberty Alliance Single Sign On) library.
%endif

%if %{with_java}
%package -n java-%{name}
Summary: Liberty Alliance Single Sign On (lasso) Java bindings
Buildrequires: java-1.8.0-openjdk-devel
BuildRequires: jpackage-utils
Requires: java-headless
Requires: jpackage-utils
Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{obsolete_old_lang_subpackages}
Provides: %{name}-java = %{version}-%{release}
Provides: %{name}-java%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-java < %{version}-%{release}
%endif

%description -n java-%{name}
Java language bindings for the lasso (Liberty Alliance Single Sign On) library.
%endif

%if %{with_php}
%package -n php-%{name}
Summary: Liberty Alliance Single Sign On (lasso) PHP bindings
BuildRequires: expat-devel
BuildRequires: php-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}

%description -n php-%{name}
PHP language bindings for the lasso (Liberty Alliance Single Sign On) library.

%endif

%if %{with_python2}
%package -n python2-%{name}
%{?python_provide:%python_provide python2-%{name}}
Summary: Liberty Alliance Single Sign On (lasso) Python bindings
BuildRequires: python2-devel

Requires: python2
Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{obsolete_old_lang_subpackages}
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
%endif

%description -n python2-%{name}
Python language bindings for the lasso (Liberty Alliance Single Sign On)
library.
%endif

%if %{with_python3}
%package -n python3-%{name}
%{?python_provide:%python_provide python3-%{name}}
Summary: Liberty Alliance Single Sign On (lasso) Python bindings
BuildRequires: python3-devel
BuildRequires: python3-lxml
Requires: python3
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
Python language bindings for the lasso (Liberty Alliance Single Sign On)
library.
%endif

%prep
%setup -q
%{!?el7:%patch -P 01 -p1}
%patch -P 02 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1

# Remove any python script shebang lines (unless they refer to python3)
sed -i -E -e '/^#![[:blank:]]*(\/usr\/bin\/env[[:blank:]]+python[^3]?\>)|(\/usr\/bin\/python[^3]?\>)/d' \
  `grep -r -l -E '^#![[:blank:]]*(/usr/bin/python[^3]?)|(/usr/bin/env[[:blank:]]+python[^3]?)' *`

%build
%{?with_java:export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk}
./autogen.sh
%if 0%{?with_python2}
  %configure %{configure_args} --with-python=%{__python2}
  pushd lasso
  %make_build CFLAGS="%{optflags}"
  popd
  pushd bindings/python
  %make_build CFLAGS="%{optflags}"
  make check CK_TIMEOUT_MULTIPLIER=5
  mkdir py2
  mv lasso.py .libs/_lasso.so py2
  popd
  make clean
%endif

%if 0%{?with_python3}
  %configure %{configure_args} --with-python=%{__python3}
%else
  %configure %{configure_args}
%endif
%make_build CFLAGS="%{optflags}"

%check
make check CK_TIMEOUT_MULTIPLIER=10

%install
%make_install exec_prefix=%{_prefix}
find %{buildroot} -type f -name '*.la' -exec rm -f {} \;
find %{buildroot} -type f -name '*.a' -exec rm -f {} \;

%if 0%{?with_python2}
  # Install Python 2 files saved from first build
  install -d -m 0755 %{buildroot}/%{python2_sitearch}
  install -m 0644 bindings/python/py2/lasso.py %{buildroot}/%{python2_sitearch}
  install -m 0755 bindings/python/py2/_lasso.so %{buildroot}/%{python2_sitearch}
%endif

# Perl subpackage
%if %{with_perl}
find %{buildroot} \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;
%endif

# PHP subpackage
%if %{with_php}
install -m 755 -d %{buildroot}%{_datadir}/php/%{name}
mv %{buildroot}%{_datadir}/php/lasso.php %{buildroot}%{_datadir}/php/%{name}

# rename the PHP config file when needed (PHP 5.6+)
if [ "%{name}.ini" != "%{ini_name}" ]; then
  mv %{buildroot}%{php_inidir}/%{name}.ini \
     %{buildroot}%{php_inidir}/%{ini_name}
fi
%endif

# Remove bogus doc files
rm -fr %{buildroot}%{_docdir}/%{name}

%ldconfig_scriptlets

%files
%{_libdir}/liblasso.so.3*
%doc AUTHORS NEWS README
%license COPYING

%files devel
%{_libdir}/liblasso.so
%{_libdir}/pkgconfig/lasso.pc
%{_includedir}/%{name}

%if %{with_perl}
%files -n perl-%{name}
%{perl_vendorarch}/Lasso.pm
%{perl_vendorarch}/auto/Lasso/
%endif

%if %{with_java}
%files -n java-%{name}
%{_libdir}/java/libjnilasso.so
%{_javadir}/lasso.jar
%endif

%if %{with_php}
%files -n php-%{name}
%{php_extdir}/lasso.so
%config(noreplace) %{php_inidir}/%{ini_name}
%dir %{_datadir}/php/%{name}
%{_datadir}/php/%{name}/lasso.php
%endif

%if %{with_python2}
%files -n python2-%{name}
%{python2_sitearch}/lasso.py*
%{python2_sitearch}/_lasso.so
%endif

%if %{with_python3}
%files -n python3-%{name}
%{python3_sitearch}/lasso.py*
%{python3_sitearch}/_lasso.so
%{python3_sitearch}/__pycache__/*
%endif

%changelog
* Wed Feb 05 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 2.8.2-14
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 20 2024 Xavier Bachelot <xavier@bachelot.org> - 2.8.2-13
- Spec file cleanup:
  - Fix changelog entry date to restore chronological order
  - Convert License to SPDX
  - Don't set JAVA_HOME when not building java bindings
  - Explicitely list perl sub-package files
  - make is always needed
  - Simplify conditionals
  - fix-removed-xmlsec-deprecations.patch is not suitable for EL7
  - python interpreter is always needed to build
  - BuildRequires gcc
  - BuildRequires perl-interpreter for perl bindings
  - Use %%make_build
  - Use %%make_install
  - Drop spurious comment
  - Use %%_docdir instead of %%_defaultdocdir
- Make use of --with-min-hash-algo
- Add several upstream patches to fix build with GCC 14
- Add patch to fix python binding tests with python 3.13 (RHBZ#2256949)

* Tue Jun 18 2024 Python Maint <python-maint@redhat.com> - 2.8.2-12
- Rebuilt for Python 3.13

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.8.2-11
- Perl 5.40 rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.8.2-10
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Florian Weimer <fweimer@redhat.com> - 2.8.2-8
- libxml2 2.12 fix for incompatible-pointer-types errors
- Add conditional BuildRequires: on python3-setuptools for unbundled distutils

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.8.2-5
- Perl 5.38 rebuild

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 2.8.2-4
- Rebuilt for Python 3.12

* Tue Jun 27 2023 Francois Andrieu <darknao@fedoraproject.org> - 2.8.2-3
- Set default signing algorithm to RSA-SHA256

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.8.2-2
- Rebuilt for Python 3.12

* Thu Mar 30 2023 Xavier Bachelot <xavier@bachelot.org> - 2.8.2-1
- Update to 2.8.2
- Disable PHP bindings for PHP8, which is not supported yet

* Thu Mar 09 2023 Xavier Bachelot <xavier@bachelot.org> - 2.8.1-1
- Update to 2.8.1 (fixes RHBZ#2142849)
- Enable php bindings
- Update URL: and Source: tags to https

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.7.0-8
- Rebuilt for Python 3.11

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.7.0-7
- Perl 5.36 rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.7.0-6
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.7.0-4
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.7.0-2
- Rebuilt for Python 3.10

* Wed Jun  2 2021 Jakub Hrozek <jhrozek@redhat.com> - 2.7.0
- Lasso 2.7.0
- https://listes.entrouvert.com/arc/lasso/2021-06/msg00000.html
- don't package java bindings as they are not maintained upstream
  anymore and there seem to be no users
- Resolves: rhbz#1966607 - CVE-2021-28091 lasso: XML signature wrapping
                           vulnerability when parsing SAML responses

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.1-9
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 13 2020 Jakub Hrozek <jhrozek@redhat.com> - 2.6.1-7
- Temporarily build with OpenJDK 8
- upstream ticket for OpenJDK11 support: https://dev.entrouvert.org/issues/45876

* Fri Aug 07 2020 Jeff Law <law@redhat.com> - 2.6.1-6
- Revert last change.  I lost the patchfile and I can't reproduce the gcc-11
  problem which almost certainly prompted it

* Fri Aug 07 2020 Jeff Law <law@redhat.com> - 2.6.1-5
- Fix format string problem

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.6.1-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jul 03 2020 Xavier Bachelot <xavier@bachelot.org> - 2.6.1-1
- Update to 2.6.1

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.0-23
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-22
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jakub Hrozek <jhrozek@redhat.com>
- Resolves: #1778645 - lasso-2.6.0-19.fc32 FTBFS:
                       non_regression_tests.c:240:51: error: initializer
                       element is not constant

* Mon Sep  2 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-19
- Resolves: #1730010 - lasso includes "Destination" attribute in SAML
                       AuthnRequest populated with SP
                       AssertionConsumerServiceURL when ECP workflow
                       is used which leads to IdP-side errors

* Sun Sep  1 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-18
- Let tests run longer
- Resolves: #1743888 - lasso unit tests time out on slower arches (e.g. arm)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-17
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-15
- Use the upstream patch that uses a self-signed cert in tests
- Related: #1705700 - lasso FTBFS because an expired certificate is
                      used in the tests
- Resolves: #1634266 - ECP signature check fails with
                       LASSO_DS_ERROR_SIGNATURE_NOT_FOUND when assertion
                       signed instead of response

* Tue Jun 04 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.0-14
- Perl 5.30 re-rebuild updated packages

* Mon Jun  3 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-13
- Don't use the expired certificate the tarball provides for tests
- Resolves: #1705700 - lasso FTBFS because an expired certificate is
            used in the tests

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.0-12
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 04 2018 Xavier Bachelot <xavier@bachelot.org> - 2.6.0-10
- Specfile clean up:
  - Consolidate BuildRequires
  - Remove Group: tags
  - Uppercase and move Url: tag
  - Use %%license for COPYING
  - Use %%make_build
  - Use %%autosetup
  - Don't glob soname to prevent unintentionnal soname bump
  - Use %%ldconfig_scriptlets
  - Specify all perl dependencies in BR:s
  - Drop useless %%attr in php-lasso sub-package

* Mon Dec 03 2018 Xavier Bachelot <xavier@bachelot.org> - 2.6.0-9
- Generate perl requires/provides.

* Tue Jul 17 2018  <jdennis@redhat.com> - 2.6.0-8
- more py2/py3 build dependencies fixes

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul  7 2018  <jdennis@redhat.com> - 2.6.0-6
- Modify configure to search for versioned python
- Resolves: rhbz#1598047

* Wed Jul 04 2018 Petr Pisar <ppisar@redhat.com> - 2.6.0-5
- Perl 5.28 rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-4
- Rebuilt for Python 3.7

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.0-3
- Perl 5.28 rebuild

* Wed Jun 27 2018  <jdennis@redhat.com> - 2.6.0-2
- fix language bindings package names to comply with guidelines,
  instead of %%{name}-lang use lang-%%{name}
- fix conditional logic used to build on rhel

* Tue Jun 26 2018  <jdennis@redhat.com> - 2.6.0-1
- Upgrade to latest upstream
- Build using Python3, add python3 subpackage
- Resolves: rhbz#1592416 Enable perl subpackage

* Wed May  2 2018 John Dennis <jdennis@redhat.com> - 2.5.1-13
- add xmlsec1 version dependency

* Tue May  1 2018 John Dennis <jdennis@redhat.com> - 2.5.1-12
- Resolves: rhbz#1542126, rhbz#1556016
- xmlsec removed SOAP support, reimplement missing xmlSecSoap* in Lasso

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.5.1-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.1-9
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.1-8
- Python 2 binary package renamed to python2-lasso
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 30 2016 John Dennis <jdennis@redhat.com> - 2.5.1-3
- disbable PHP binding because PHP-7 is now the default and lasso
  only knows how to build with PHP-5

* Wed Jun 15 2016 John Dennis <jdennis@redhat.com> - 2.5.1-2
- fix CFLAGS override in configure

* Mon Feb 22 2016 John Dennis <jdennis@redhat.com> - 2.5.1-1
- Upgrade to upstream 2.5.1 release
  See Changelog for details, mostly bugs fixes,
  most signficant is proper support of SHA-2
  Resolves: #1295472
  Resolves: #1303573
- Add java_binding_lasso_log.patch to fix "make check" failure during rpmbuild
  upstream commit d8e3ae8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 14 2015 John Dennis <jdennis@redhat.com> - 2.5.0-1
- Upgrade to new upstream 2.5.0 release
  Includes ECP support

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Rob Crittenden <rcritten@redhat.com> - 2.4.1-3
- Add BuildRequires on libtool
- Add -fPIC to LDFLAGS
- Disable perl bindings, it fails to build on x86.

* Fri Jan 23 2015 Simo Sorce <simo@redhat.com> - 2.4.1-2
- Enable perl bindings
- Also add support for building with automake 1.15
- Fix build issues on rawhide due to missing build dep on perl(Error)

* Thu Aug 28 2014 Simo Sorce <simo@redhat.com> - 2.4.1-1
- New upstream relase 2.4.1
- Drop patches as they have all been integrated upstream

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 20 2014 Remi Collet <rcollet@redhat.com> - 2.4.0-4
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to extension configuration file
- drop unneeded dependency on pecl
- add provides php-lasso

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Simo Sorce <simo@redhat.com> - 2.4.0-2
- Fixes for arches where pointers and integers do not have the same size
  (ppc64, s390, etc..)

* Mon Apr 14 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4.0-1
- Use OpenJDK instead of GCJ for java bindings

* Sat Jan 11 2014 Simo Sorce <simo@redhat.com> 2.4.0-0
- Update to final 2.4.0 version
- Drop all patches, they are now included in 2.4.0
- Change Source URI

* Mon Dec  9 2013 Simo Sorce <simo@redhat.com> 2.3.6-0.20131125.5
- Add patches to fix rpmlint license issues
- Add upstream patches to fix some build issues

* Thu Dec  5 2013 Simo Sorce <simo@redhat.com> 2.3.6-0.20131125.4
- Add patch to support automake-1.14 for rawhide

* Mon Nov 25 2013 Simo Sorce <simo@redhat.com> 2.3.6-0.20131125.3
- Initial packaging
- Based on the spec file by Jean-Marc Liger <jmliger@siris.sorbonne.fr>
- Code is updated to latest master via a jumbo patch while waiting for
  official upstream release.
- Jumbo patch includes also additional patches sent to upstream list)
  to build on Fedora 20
- Perl bindings are disabled as they fail to build
- Disable doc building as it doesn't ork correctly for now
