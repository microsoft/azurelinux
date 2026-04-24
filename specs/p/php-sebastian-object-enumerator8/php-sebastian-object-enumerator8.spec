# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-object-enumerator8
#
# SPDX-FileCopyrightText:  Copyright 2015-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_with          tests

%global gh_commit    b39ab125fd9a7434b0ecbc4202eebce11a98cfc5
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   object-enumerator
%global gh_date      2026-02-06
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   ObjectEnumerator
%global major        8
%global php_home     %{_datadir}/php

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        8.0.0
Release: 2%{?dist}
Summary:        Traverses array and object to enumerate all referenced objects, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.4.1
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
BuildRequires:  (php-composer(%{pk_vendor}/object-reflector) >= 6.0   with php-composer(%{pk_vendor}/object-reflector) < 7)
BuildRequires:  (php-composer(sebastian/recursion-context)   >= 8.0   with php-composer(sebastian/recursion-context)   < 9)
# From composer.json"require-dev": {
#        "phpunit/phpunit": "^13.0"
BuildRequires:  phpunit13
%endif

# from composer.json
#        "php": ">=8.4.1",
#        "sebastian/object-reflector": "^6.0",
#        "sebastian/recursion-context": "^8.0"
Requires:       php(language) >= 8.3
Requires:       (php-composer(%{pk_vendor}/object-reflector) >= 6.0   with php-composer(%{pk_vendor}/object-reflector) < 7)
Requires:       (php-composer(sebastian/recursion-context)   >= 8.0   with php-composer(sebastian/recursion-context)   < 9)
# from phpcompatinfo report for version 5.0.0:
#nothing
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Traverses array structures and object graphs to enumerate all
referenced objects.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader, from composer.json "autoload": {
#        "classmap": [
#            "src/"
%{_bindir}/phpab --template fedora --output src/autoload.php src
cat << 'EOF' | tee -a src/autoload.php
\Fedora\Autoloader\Dependencies::required([
    '%{php_home}/%{ns_vendor}/ObjectReflector6/autoload.php',
    '%{php_home}/%{ns_vendor}/RecursionContext8/autoload.php',
]);
EOF


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with tests}
mkdir vendor
%{_bindir}/phpab --template fedora --output vendor/autoload.php tests/_fixture

: Run upstream test suite
ret=0
for cmd in php php84 php85; do
  if which $cmd; then
   $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
     %{_bindir}/phpunit13 --bootstrap vendor/autoload.php || ret=1
  fi
done
exit $ret
%else
: bootstrap build with test suite disabled
%endif


%files
%license LICENSE
%doc README.md composer.json
%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Fri Feb  6 2026 Remi Collet <remi@remirepo.net> - 8.0.0-1
- update to 8.0.0
- raise dependency on PHP 8.4
- raise dependency on sebastian/object-reflector 6
- raise dependency on sebastian/recursion-context 8
- rename to php-sebastian-object-enumerator8
- move to /usr/share/php/SebastianBergmann/ObjectEnumerator8

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 7.0.0-2
- enable test suite

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 7.0.0-1
- update to 7.0.0
- raise dependency on PHP 8.3
- raise dependency on sebastian/object-reflector 5
- raise dependency on sebastian/recursion-context 7
- rename to php-sebastian-object-enumerator7
- move to /usr/share/php/SebastianBergmann/ObjectEnumerator7

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 6.0.1-2
- enable test suite

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.2
- raise dependency on sebastian/object-reflector 4
- raise dependency on sebastian/recursion-context 6
- rename to php-sebastian-object-enumerator6
- move to /usr/share/php/SebastianBergmann/ObjectEnumerator6

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 5.0.0-4
- Enable test suite

* Mon Jun 19 2023 Remi Collet <remi@remirepo.net> - 5.0.0-2
- fix dependencies, from review #2168095

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 8.1
- raise dependency on sebastian/object-reflector 3
- raise dependency on sebastian/recursion-context 5
- rename to php-sebastian-object-enumerator5
- move to /usr/share/php/SebastianBergmann/ObjectEnumerator5

* Mon Oct 26 2020 Remi Collet <remi@remirepo.net> - 4.0.4-1
- update to 4.0.4

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 4.0.3-1
- update to 4.0.3 (no change)

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1
- sources from git snapshot
- drop patch merged upstream

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 7.3
- raise dependency on sebastian/object-reflector 2
- raise dependency on sebastian/recursion-context 4
- rename to php-sebastian-object-enumerator4
- move to /usr/share/php/SebastianBergmann/ObjectEnumerator4
- fix test suite with patch from
  https://github.com/sebastianbergmann/object-enumerator/pull/8

* Thu Dec  6 2018 Remi Collet <remi@remirepo.net> - 3.0.3-3
- cleanup for EL-8

* Tue Feb  6 2018 Remi Collet <remi@remirepo.net> - 3.0.3-2
- use range dependencies on F27+

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 3.0.3-1
- Update to 3.0.3 - no change
- raise dependency on sebastian/object-reflector 1.1.1

* Sun Mar 12 2017 Remi Collet <remi@remirepo.net> - 3.0.2-1
- Update to 3.0.2
- add dependency on sebastian/object-reflector

* Sun Mar 12 2017 Remi Collet <remi@remirepo.net> - 3.0.1-1
- Update to 3.0.1

* Fri Mar  3 2017 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0
- rename to php-sebastian-object-enumerator3
- raise dependency on PHP 7
- raise dependency on recursion-context 3

* Sat Feb 18 2017 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 (no change)
- raise dependency on sebastian/recursion-context 2.0

* Wed Nov 16 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- raise dependency on sebastian/recursion-context 1.0.4

* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- switch to fedora/autoloader

* Wed Mar 23 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

