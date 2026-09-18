# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-code-unit3
#
# SPDX-FileCopyrightText:  Copyright 2020-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

# disabled until phpunit11 available
%bcond_without       tests

# Sources
%global gh_commit    54391c61e4af8078e5b276ab082b6d3c54c9ad64
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   code-unit
%global gh_date      2025-03-19
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global major        3
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   CodeUnit

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        3.0.3
Release:        2%{?dist}
Summary:        Collection of value objects that represent the PHP code units, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.2
# Autoloader
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^11.5"
BuildRequires:  phpunit11 >= 11.5
%endif

# from composer.json, "require": {
#        "php": ">=8.2"
Requires:       php(language) >= 8.2
# From phpcompatinfo report for 2.0.0
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Collection of value objects that represent the PHP code units.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the library Autoloader
%{_bindir}/phpab \
   --template fedora \
   --output src/autoload.php \
   src

# Generate the fixture Autoloader
%{_bindir}/phpab \
   --template fedora \
   --output tests/_fixture/autoload.php \
   tests/_fixture


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%if %{with tests}
%check
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php

require_once dirname(__DIR__) . '/tests/_fixture/autoload.php';
require_once dirname(__DIR__) . '/tests/_fixture/file_with_multiple_code_units.php';
require_once dirname(__DIR__) . '/tests/_fixture/function.php';
require_once dirname(__DIR__) . '/tests/_fixture/issue_9.php';
EOF

: Run tests
ret=0
for cmd in php php82 php83 php84; do
  if which $cmd; then
   $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
     %{_bindir}/phpunit11 --bootstrap vendor/autoload.php || ret=1
  fi
done
exit $ret
%endif


%files
%license LICENSE
%doc README.md composer.json
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 19 2025 Remi Collet <remi@remirepo.net> - 3.0.3-1
- update to 3.0.3

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 3.0.2-3
- enable test suite

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 12 2024 Remi Collet <remi@remirepo.net> - 3.0.2-1
- update to 3.0.2
- re-license spec file to CECILL-2.1

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- raise dependency on PHP 8.2
- rename to php-sebastian-code-unit3
- move to /usr/share/php/SebastianBergmann/CodeUnit3

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 2.0.0-3
- Enable test suite

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP 8.1
- rename to php-sebastian-code-unit2
- move to /usr/share/php/SebastianBergmann/CodeUnit2

* Mon Oct 26 2020 Remi Collet <remi@remirepo.net> - 1.0.8-1
- update to 1.0.8

* Sat Oct  3 2020 Remi Collet <remi@remirepo.net> - 1.0.7-1
- update to 1.0.7

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 1.0.6-1
- update to 1.0.6 (no change)

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 1.0.5-1
- update to 1.0.5

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 1.0.3-1
- update to 1.0.3 (no change)
- sources from git snapshot

* Thu Apr 30 2020 Remi Collet <remi@remirepo.net> - 1.0.2-1
- update to 1.0.2

* Mon Apr 27 2020 Remi Collet <remi@remirepo.net> - 1.0.1-1
- update to 1.0.1

* Fri Apr  3 2020 Remi Collet <remi@remirepo.net> - 1.0.0-1
- initial package
