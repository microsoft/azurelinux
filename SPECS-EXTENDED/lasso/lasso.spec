Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global with_java 0
%global with_php 0
%global with_perl 1
%global with_python3 1
%global with_wsf 0
%global default_sign_algo "rsa-sha1"
%global min_hash_algo "sha1"

%if %{with_php}
%global ini_name     40-%{name}.ini
%endif

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

%if !%{with_python3}
  %global configure_args %{configure_args} --disable-python
%endif


Summary: Liberty Alliance Single Sign On
Name: lasso
Version: 2.9.0
Release: 1%{?dist}
License: GPL-2.0-or-later
URL: https://lasso.entrouvert.org/
Source0: https://git.entrouvert.org/entrouvert/lasso/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

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
%autosetup -n %{name}

# Remove any python script shebang lines (unless they refer to python3)
sed -i -E -e '/^#![[:blank:]]*(\/usr\/bin\/env[[:blank:]]+python[^3]?\>)|(\/usr\/bin\/python[^3]?\>)/d' \
  `grep -r -l -E '^#![[:blank:]]*(/usr/bin/python[^3]?)|(/usr/bin/env[[:blank:]]+python[^3]?)' *`

%build
%if 0%{?with_java}
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
%endif
echo %{version} > .tarball-version
./autogen.sh
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

%if %{with_python3}
%files -n python3-%{name}
%{python3_sitearch}/lasso.py*
%{python3_sitearch}/_lasso.so
%{python3_sitearch}/__pycache__/*
%endif

%changelog
* Wed Dec 24 2025 Sumit Jena <v-sumitjena@microsoft.com> - 2.9.0-1
- Upgrade to version 2.9.0

* Wed Feb 05 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 2.8.2-15
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Mon Sep 12 2022 Muhammad Falak <mwani@microsoft.com> - 2.8.0-1
- Bump version to 2.8.0
- Drop un-needed patches
- License verfied

* Wed Mar 02 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.0-25
- Removed Python 2 bits.
- Disabling Java subpackage as it's no needed.
- Adding a missing BR on 'libsxlt-devel'.

* Wed Jan 05 2022 Thomas Crain <thcrain@microsoft.com> - 2.6.0-24
- Rename java-headless dependency to java
- License verified

* Wed Jul 14 2021 Muhammad Falak Wani <mwani@microsoft.com> - 2.6.0-23
- Add explict provides 'lasso-python'

* Thu Mar 18 2021 Henry Li <lihl@microsoft.com> - 2.6.0-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Fix condition check to enable python3 build
