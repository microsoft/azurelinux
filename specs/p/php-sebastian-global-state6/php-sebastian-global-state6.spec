# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# spec file for php-sebastian-global-state6
#
# Copyright (c) 2014-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    987bafff24ecc4c9ac418cab1145b96dd6e9cbd9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   global-state
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   GlobalState
%global major        6
%global php_home     %{_datadir}/php

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        6.0.2
Release: 5%{?dist}
Summary:        Snapshotting of global state, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.1
BuildRequires:  php-reflection
BuildRequires:  php-spl
# Autoloader
BuildRequires:  php-fedora-autoloader-devel >= 1.0.0
%if %{with tests}
BuildRequires:  (php-composer(sebastian/object-reflector)  >= 3.0     with php-composer(sebastian/object-reflector)  < 4)
BuildRequires:  (php-composer(sebastian/recursion-context) >= 5.0     with php-composer(sebastian/recursion-context) < 6)
# from composer.json, "require-dev": {
#        "ext-dom": "*",
#        "phpunit/phpunit": "^10.0"
BuildRequires:  php-dom
BuildRequires:  phpunit10
%endif

# from composer.json, "require": {
#        "php": ">=8.1",
#        "sebastian/object-reflector": "^3.0",
#        "sebastian/recursion-context": "^5.0"
Requires:       php(language) >= 7.3
Requires:       (php-composer(sebastian/object-reflector)  >= 3.0     with php-composer(sebastian/object-reflector)  < 4)
Requires:       (php-composer(sebastian/recursion-context) >= 5.0     with php-composer(sebastian/recursion-context) < 6)
# from phpcompatinfo report for version 6.0.0
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Snapshotting of global state,
factored out of PHPUnit into a stand-alone component.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --template fedora --output src/autoload.php src
cat << 'EOF' | tee -a src/autoload.php
\Fedora\Autoloader\Dependencies::required([
    '%{php_home}/%{ns_vendor}/ObjectReflector3/autoload.php',
    '%{php_home}/%{ns_vendor}/RecursionContext5/autoload.php',
]);
EOF

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
require_once 'tests/_fixture/SnapshotFunctions.php';
EOF

: Run upstream test suite
ret=0
for cmd in php php81 php82 php83; do
  if which $cmd; then
   $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
     %{_bindir}/phpunit10 \
       || ret=1
  fi
done
exit $ret

%else
: bootstrap build with test suite disabled
%endif


%files
%license LICENSE
%doc README.md
%doc composer.json
%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar  5 2024 Remi Collet <remi@remirepo.net> - 6.0.2-1
- update to 6.0.2

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 6.0.1-3
- Enable test suite

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 19 2023 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.1
- raise dependency on sebastian/object-reflector 3
- raise dependency on sebastian/recursion-context 5
- rename to php-sebastian-global-state6
- move to /usr/share/php/SebastianBergmann/GlobalState6

* Mon Feb 14 2022 Remi Collet <remi@remirepo.net> - 5.0.5-1
- update to 5.0.5

* Thu Feb 10 2022 Remi Collet <remi@remirepo.net> - 5.0.4-1
- update to 5.0.4

* Mon Jun 14 2021 Remi Collet <remi@remirepo.net> - 5.0.3-1
- update to 5.0.3

* Tue Oct 27 2020 Remi Collet <remi@remirepo.net> - 5.0.2-1
- update to 5.0.2

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1 (no change)

* Fri Aug 28 2020 Remi Collet <remi@remirepo.net> - 5.0.0-2
- enable test suite

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- rename to php-sebastian-global-state5
- move to /usr/share/php/SebastianBergmann/GlobalState5

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 7.3
- raise dependency on sebastian/object-reflector 2
- raise dependency on sebastian/recursion-context 4
- rename to php-sebastian-global-state4
- move to /usr/share/php/SebastianBergmann/GlobalState4

* Fri Feb 22 2019 Remi Collet <remi@remirepo.net> - 3.0.0-2
- normal build

* Tue Feb 12 2019 Remi Collet <remi@remirepo.net> - 3.0.0-0.1
- fix directory ownership, from review #1671662

* Fri Feb  1 2019 Remi Collet <remi@remirepo.net> - 3.0.0-0
- boostrap build
- rename to php-sebastian-global-state3
- update to 3.0.0
- raise dependency on PHP 7.2
- add dependency on sebastian/object-reflector
- add dependency on sebastian/recursion-context

* Fri Apr 28 2017 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- rename to php-sebastian-global-state2
- update to 2.0.0
- raise dependency on PHP 7.0

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-4
- switch to fedora/autoloader

* Thu Oct 13 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-3
- add optional dependency on uopz extension

* Mon Oct 12 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Fri Dec  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
