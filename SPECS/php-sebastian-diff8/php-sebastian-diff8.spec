# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-diff8
#
# SPDX-FileCopyrightText:  Copyright 2013-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_with          tests

%global gh_commit    a2b6d09d7729ee87d605a439469f9dcc39be5ea3
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   diff
%global gh_date      2026-02-06
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   Diff

%global major        8
%global php_home     %{_datadir}/php

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        8.0.0
Release:        1%{?dist}
Summary:        Diff implementation, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
# php-symfony7 not available, only used for tests
%global symfony_version 7.3.11
Source2:        https://github.com/symfony/process/archive/v%{symfony_version}/php-symfony-process-%{symfony_version}.tar.gz

BuildArch:      noarch
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
BuildRequires:  php(language) >= 8.4.1
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^13.0",
#        "symfony/process": "^7.2"
BuildRequires:  phpunit13
%endif

# from composer.json
#        "php": ">=8.4.1"
Requires:       php(language) >= 8.4.1
# from phpcompatinfo report for version 5.0.0
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Diff implementation.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit} -a 2


%build
# Generate the Autoloader
%{_bindir}/phpab --template fedora --output src/autoload.php src


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with tests}
mkdir vendor
%{_bindir}/phpab --output vendor/autoload.php tests process-%{symfony_version}

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
%doc composer.json
%doc *.md
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Fri Feb  6 2026 Remi Collet <remi@remirepo.net> - 8.0.0-1
- update to 8.0.0
- raise dependency on PHP 8.4
- rename to php-sebastian-diff8
- move to /usr/share/php/SebastianBergmann/Diff8

* Thu Jun 26 2025 Remi Collet <remi@remirepo.net> - 7.0.0-3
- add upstream patch for test suite with phpunit 12.2

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 7.0.0-2
- enable test suite

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 7.0.0-1
- update to 7.0.0
- raise dependency on PHP 8.3
- rename to php-sebastian-diff7
- move to /usr/share/php/SebastianBergmann/Diff7

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 6.0.2-2
- enable test suite

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 6.0.2-1
- update to 6.0.2

* Tue Mar  5 2024 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.2
- rename to php-sebastian-diff6
- move to /usr/share/php/SebastianBergmann/Diff6

* Fri Dec 22 2023 Remi Collet <remi@remirepo.net> - 5.1.0-1
- update to 5.1.0

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 5.0.3-3
- Enable test suite

* Tue May  2 2023 Remi Collet <remi@remirepo.net> - 5.0.3-1
- update to 5.0.3

* Thu Mar 23 2023 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 8.1
- rename to php-sebastian-diff5
- move to /usr/share/php/SebastianBergmann/Diff5
- use bundled symfony/process for test suite

* Mon Oct 26 2020 Remi Collet <remi@remirepo.net> - 4.0.4-1
- update to 4.0.4

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 4.0.3-1
- update to 4.0.3 (no change)

* Tue Jun 30 2020 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2

* Fri May  8 2020 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1
- sources from git snapshot
- switch to phpunit9

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 7.3
- rename to php-sebastian-diff4
- move to /usr/share/php/SebastianBergmann/Diff4

* Mon Feb  4 2019 Remi Collet <remi@remirepo.net> - 3.0.2-1
- update to 3.0.2

* Mon Jun 11 2018 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1 (no change)
- ignore integration tests with old git command

* Wed Feb  7 2018 Remi Collet <remi@remirepo.net> - 3.0.0-1
- normal build

* Fri Feb  2 2018 Remi Collet <remi@remirepo.net> - 3.0.0-0
- update to 3.0.0
- renamed to php-sebastian-diff3
- move to /usr/share/php/SebastianBergmann/Diff3
- raise dependency on PHP 7.1
- use phpunit7
- boostrap build

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 2.0.1-1
- update to 2.0.1
- renamed to php-sebastian-diff2
- raise dependency on PHP 7.0

* Mon May 22 2017 Remi Collet <remi@remirepo.net> - 1.4.3-1
- Update to 1.4.3

* Mon May 22 2017 Remi Collet <remi@remirepo.net> - 1.4.2-1
- Update to 1.4.2
- switch to fedora/autoloader
- use PHPUnit 6 when available

* Sun Dec  6 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.1 (no change)
- run test suite with both php 5 and 7 when available

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- run test suite during build
- generate autoload.php for compatibility
- fix license handling

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-6
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-4
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- get sources from github
- run test suite when build --with tests

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-2
- rename to lowercase

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package
