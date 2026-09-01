# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-type7
#
# SPDX-FileCopyrightText:  Copyright 2019-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_with          tests

# github
%global gh_commit    42412224607bd3931241bbd17f38e0f972f5a916
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   type
%global gh_date      2026-02-06
# packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
%global major        7
# namespace
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   Type

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        7.0.0
Release:        1%{?dist}
Summary:        Collection of value objects that represent the types of the PHP type system, v%{major}

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
#        "php": ">=8.3",
Requires:       php(language) >= 8.4.1
# from phpcompatinfo report for version 4.0.0
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Collection of value objects that represent the types of the PHP type system.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --template fedora --output src/autoload.php src

# For the test suite
phpab --template fedora --output tests/autoload.php tests/_fixture/


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with tests}
mkdir vendor
cat <<EOF | tee vendor/autoload.php
<?php
require_once 'tests/autoload.php';
require_once 'tests/_fixture/callback_function.php';
require_once 'tests/_fixture/functions_that_declare_return_types.php';
EOF

: Run upstream test suite
ret=0
for cmd in php php84 php85; do
  if which $cmd; then
   $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
     %{_bindir}/phpunit13 --bootstrap vendor/autoload.php --no-coverage || ret=1
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
* Fri Feb  6 2026 Remi Collet <remi@remirepo.net> - 7.0.0-1
- update to 7.0.0
- raise dependency on PHP 8.4
- rename to php-sebastian-type7
- move to /usr/share/php/SebastianBergmann/Type7

* Sun Aug 10 2025 Remi Collet <remi@remirepo.net> - 6.0.3-1
- update to 6.0.3 (no change)

* Tue Mar 18 2025 Remi Collet <remi@remirepo.net> - 6.0.2-1
- update to 6.0.2

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 6.0.0-2
- enable test suite

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.3
- rename to php-sebastian-type6
- move to /usr/share/php/SebastianBergmann/Type6

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 5.1.0-2
- enable test suite

* Wed Sep 18 2024 Remi Collet <remi@remirepo.net> - 5.1.0-1
- update to 5.1.0

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 8.2
- rename to php-sebastian-type5
- move to /usr/share/php/SebastianBergmann/Type5

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 4.0.0-3
- Enable test suite

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 8.1
- rename to php-sebastian-type4
- move to /usr/share/php/SebastianBergmann/Type4

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 3.2.1-1
- update to 3.2.1

* Tue Sep 13 2022 Remi Collet <remi@remirepo.net> - 3.2.0-1
- update to 3.2.0

* Tue Aug 30 2022 Remi Collet <remi@remirepo.net> - 3.1.0-1
- update to 3.1.0

* Mon Jun 27 2022 Remi Collet <remi@remirepo.net> - 3.0.0-2
- improve package description and summary

* Tue Mar 15 2022 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- rename to php-sebastian-type3
- install to /usr/share/php/SebastianBergmann/Type3

* Tue Jun 15 2021 Remi Collet <remi@remirepo.net> - 2.3.4-1
- update to 2.3.4

* Fri Jun  4 2021 Remi Collet <remi@remirepo.net> - 2.3.2-1
- update to 2.3.2

* Mon Oct 26 2020 Remi Collet <remi@remirepo.net> - 2.3.1-1
- update to 2.3.1

* Tue Oct  6 2020 Remi Collet <remi@remirepo.net> - 2.3.0-1
- update to 2.3.0

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 2.2.2-1
- update to 2.2.2 (no change)

* Mon Jul  6 2020 Remi Collet <remi@remirepo.net> - 2.2.1-1
- update to 2.2.1

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 2.1.1-1
- update to 2.1.1

* Tue Jun  2 2020 Remi Collet <remi@remirepo.net> - 2.1.0-1
- update to 2.1.0
- sources from git snapshot
- switch to phpunit9

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP 7.3
- rename to php-sebastian-type2
- move to /usr/share/php/SebastianBergmann/Type2

* Tue Jul  2 2019 Remi Collet <remi@remirepo.net> - 1.1.3-1
- update to 1.1.3

* Wed Jun 19 2019 Remi Collet <remi@remirepo.net> - 1.1.2-1
- update to 1.1.2

* Sat Jun  8 2019 Remi Collet <remi@remirepo.net> - 1.1.1-1
- update to 1.1.1

* Sat Jun  8 2019 Remi Collet <remi@remirepo.net> - 1.1.0-1
- update to 1.1.0

* Fri Jun  7 2019 Remi Collet <remi@remirepo.net> - 1.0.0-1
- initial package
