# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-complexity4
#
# SPDX-FileCopyrightText:  Copyright 2020-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

# disabled until phpunit11 available
%bcond_without       tests

# github
%global gh_commit    ee41d384ab1906c68852636b6de493846e13e5a0
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   complexity
%global gh_date      2024-07-03
# packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
%global major        4
# namespace
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   Complexity

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        4.0.1
Release:        4%{?dist}
Summary:        Calculating the complexity of PHP code units, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.2
BuildRequires: (php-composer(nikic/php-parser)     >= 5.0   with php-composer(nikic/php-parser)     < 6)
# Autoloader
BuildRequires:  php-fedora-autoloader-devel >= 1.0.0
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^11.0"
BuildRequires:  phpunit11
%endif

# from composer.json, "require": {
#        "php": ">=8.2",
#        "nikic/php-parser": "^4.18 || ^5.0"
Requires:       php(language) >= 8.2
Requires:      (php-composer(nikic/php-parser)     >= 5.0   with php-composer(nikic/php-parser)     < 6)
# from phpcompatinfo report for version 3.0.0
# none
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Library for calculating the complexity of PHP code units.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --template fedora --output src/autoload.php src

cat <<EOF | tee -a src/autoload.php
\Fedora\Autoloader\Dependencies::required([
    '%{php_home}/PhpParser5/autoload.php',
]);
EOF


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with tests}
mkdir vendor
touch vendor/autoload.php

: Run upstream test suite
ret=0
for cmd in php php82 php83 php84; do
  if which $cmd; then
   $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
     %{_bindir}/phpunit11 || ret=1
  fi
done
exit $ret
%else
: bootstrap build with test suite disabled
%endif


%files
%license LICENSE
%doc *.md
%doc composer.json
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 4.0.1-3
- enable test suite

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 8.2
- raise dependency on nikic/php-parser 5.0
- rename to php-sebastian-complexity4
- move to /usr/share/php/SebastianBergmann/Complexity4

* Thu Dec 21 2023 Remi Collet <remi@remirepo.net> - 3.2.0-1
- update to 3.2.0
- raise dependency on nikic/php-parser 4.18 and allow 5.0

* Thu Sep 28 2023 Remi Collet <remi@remirepo.net> - 3.1.0-1
- update to 3.1.0

* Thu Aug 31 2023 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 3.0.0-3
- Enable test suite

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- raise dependency on PHP 8.1
- raise dependency on nikic/php-parser 4.10
- rename to php-sebastian-complexity3
- move to /usr/share/php/SebastianBergmann/Complexity3

* Tue Oct 27 2020 Remi Collet <remi@remirepo.net> - 2.0.2-1
- update to 2.0.2

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 2.0.1-1
- update to 2.0.1 (no change)

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 2.0.0-1
- initial package
