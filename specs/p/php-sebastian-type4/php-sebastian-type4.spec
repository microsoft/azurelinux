# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-type4
#
# Copyright (c) 2019-2023 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%bcond_without       tests

# github
%global gh_commit    462699a16464c3944eefc02ebdd77882bd3925bf
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   type
# packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
%global major        4
# namespace
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   Type

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        4.0.0
Release:        8%{?dist}
Summary:        Collection of value objects that represent the types of the PHP type system, v%{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.1
BuildRequires:  php-reflection
# Autoloader
BuildRequires:  php-fedora-autoloader-devel >= 1.0.0
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^10.0"
BuildRequires:  phpunit10
%endif

# from composer.json, "require": {
#        "php": ">=8.1",
Requires:       php(language) >= 8.1
# from phpcompatinfo report for version 4.0.0
Requires:       php-reflection
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
for cmd in php php81 php82 php83; do
  if which $cmd; then
   $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
     %{_bindir}/phpunit10 || ret=1
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
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 4.0.0-3
- Enable test suite

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

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
