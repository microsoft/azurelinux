# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-cli-parser5
#
# SPDX-FileCopyrightText:  Copyright 2020-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_with          tests

# github
%global gh_commit    48a4654fa5e48c1c81214e9930048a572d4b23ca
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   cli-parser
%global gh_date      2026-02-06
# packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
%global major        5
# namespace
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   CliParser

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        5.0.0
Release:        1%{?dist}
Summary:        Library for parsing CLI options, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.4.1
# Autoloader
BuildRequires:  php-fedora-autoloader-devel >= 1.0.0
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^13.0"
BuildRequires:  phpunit13
%endif

# from composer.json, "require": {
#        "php": ">=8.4",
Requires:       php(language) >= 8.4
# from phpcompatinfo report for version 2.0.0
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Library for parsing $_SERVER['argv'], extracted from phpunit/phpunit.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --template fedora --output src/autoload.php src


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with tests}
mkdir vendor
touch vendor/autoload.php

: Run upstream test suite
ret=0
for cmd in php php84 php85; do
  if which $cmd; then
   $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
     %{_bindir}/phpunit13 || ret=1
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
* Fri Feb  6 2026 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 8.4
- rename to php-sebastian-cli-parser5
- move to /usr/share/php/SebastianBergmann/CliParser5

* Mon Sep 15 2025 Remi Collet <remi@remirepo.net> - 4.2.0-1
- update to 4.2.0

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 4.0.0-2
- enable test suite

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 8.3
- rename to php-sebastian-cli-parser4
- move to /usr/share/php/SebastianBergmann/CliParser4

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 3.0.2-2
- enable test suite

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 3.0.2-1
- update to 3.0.2

* Tue Mar  5 2024 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- raise dependency on PHP 8.2
- rename to php-sebastian-cli-parser3
- move to /usr/share/php/SebastianBergmann/CliParser3

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 2.0.0-3
- Enable test suite

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP 8.1
- rename to php-sebastian-cli-parser2
- move to /usr/share/php/SebastianBergmann/CliParser2

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 1.0.1-1
- update to 1.0.1

* Thu Aug 13 2020 Remi Collet <remi@remirepo.net> - 1.0.0-1
- initial package
