# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-exporter8
#
# SPDX-FileCopyrightText:  Copyright 2013-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    dc31f1f8e0186c8f0bb3e48fd4d51421d8905fea
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   exporter
%global gh_date      2026-02-06
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   Exporter
%global major        8
%global php_home     %{_datadir}/php
%global pear_name    Exporter
%global pear_channel pear.phpunit.de

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        8.0.0
Release: 3%{?dist}
Summary:        Export PHP variables for visualization, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.4.1
BuildRequires:  php-mbstring
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^13.0",
BuildRequires:  phpunit13
BuildRequires:  (php-composer(%{pk_vendor}/recursion-context) >= 8.0 with php-composer(%{pk_vendor}/recursion-context) < 9)
%endif

# from composer.json
#        "php": ">=8.4.1",
#        "ext-mbstring": "*",
#        "sebastian/recursion-context": "^8.0"
Requires:       php(language) >= 8.4.1
Requires:       php-mbstring
Requires:       (php-composer(%{pk_vendor}/recursion-context) >= 8.0 with php-composer(%{pk_vendor}/recursion-context) < 9)
# from phpcompatinfo report for version 5.0.0
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Provides the functionality to export PHP variables for visualization.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# generate the Autoloader
phpab --template fedora --output src/autoload.php src

cat <<EOF | tee -a src/autoload.php
// Dependency' autoloader
require_once '%{php_home}/%{ns_vendor}/RecursionContext8/autoload.php';
EOF


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%if %{with tests}
%check
mkdir vendor
phpab --template fedora --output vendor/autoload.php tests/_fixture/

: Run upstream test suite
ret=0
for cmd in php php84 php85; do
  if which $cmd; then
    $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
      %{_bindir}/phpunit13 --bootstrap vendor/autoload.php || ret=1
  fi
done
exit $ret
%endif


%files
%license LICENSE
%doc README.md
%doc composer.json
%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Tue Feb 10 2026 Remi Collet <remi@remirepo.net> - 8.0.0-2
- enable test suite

* Fri Feb  6 2026 Remi Collet <remi@remirepo.net> - 8.0.0-1
- update to 8.0.0
- raise dependency on PHP 8.4
- raise dependency on sebastian/recursion-context 8
- rename to php-sebastian-exporter8
- move to /usr/share/php/SebastianBergmann/Exporter8

* Wed Sep 24 2025 Remi Collet <remi@remirepo.net> - 7.0.2-1
- update to 7.0.2

* Mon Sep 22 2025 Remi Collet <remi@remirepo.net> - 7.0.1-1
- update to 7.0.1

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 7.0.0-2
- enable test suite

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 7.0.0-1
- update to 7.0.0
- raise dependency on PHP 8.3
- raise dependency on sebastian/recursion-context 7
- rename to php-sebastian-exporter7
- move to /usr/share/php/SebastianBergmann/Exporter7

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 6.3.0-2
- enable test suite

* Thu Dec  5 2024 Remi Collet <remi@remirepo.net> - 6.3.0-1
- update to 6.3.0

* Thu Dec  5 2024 Remi Collet <remi@remirepo.net> - 6.2.0-1
- update to 6.2.0

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 6.1.3-1
- update to 6.1.3

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 6.1.2-1
- update to 6.1.2

* Tue Mar  5 2024 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.2
- raise dependency on sebastian/recursion-context 6
- rename to php-sebastian-exporter6
- move to /usr/share/php/SebastianBergmann/Exporter6

* Mon Sep 25 2023 Remi Collet <remi@remirepo.net> - 5.1.1-1
- update to 5.1.1

* Mon Sep 18 2023 Remi Collet <remi@remirepo.net> - 5.1.0-1
- update to 5.1.0

* Fri Sep  8 2023 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 5.0.0-3
- Enable test suite

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 8.1
- raise dependency on sebastian/recursion-context 5
- rename to php-sebastian-exporter5
- move to /usr/share/php/SebastianBergmann/Exporter5

* Wed Sep 14 2022 Remi Collet <remi@remirepo.net> - 4.0.5-1
- update to 4.0.5

* Mon Nov 15 2021 Remi Collet <remi@remirepo.net> - 4.0.4-1
- update to 4.0.4

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 4.0.3-1
- update to 4.0.3 (no change)

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1
- sources from git snapshot

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 7.3
- raise dependency on sebastian/recursion-context 4
- rename to php-sebastian-exporter4
- move to /usr/share/php/SebastianBergmann/Exporter4

* Sun Sep 15 2019 Remi Collet <remi@remirepo.net> - 3.1.2-1
- update to 3.1.2

* Mon Aug 12 2019 Remi Collet <remi@remirepo.net> - 3.1.1-1
- update to 3.1.1

* Thu Dec  6 2018 Remi Collet <remi@remirepo.net> - 3.1.0-5
- cleanup for EL-8

* Tue Feb  6 2018 Remi Collet <remi@remirepo.net> - 3.1.0-3
- use range dependencies on F27+

* Mon Apr  3 2017 Remi Collet <remi@remirepo.net> - 3.1.0-1
- Update to 3.1.0

* Fri Mar  3 2017 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0
- rename to php-sebastian-exporter3
- raise dependency on PHP 7
- raise dependency on recursion-context 3

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- raise dependency on sebastian/recursion-context 2.0
- switch to fedora/autoloader

* Fri Jun 17 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2
- run test suite with both PHP 5 and 7 when available

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1 (only CS)

* Fri Jan 30 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Sat Jan 24 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- add dependency on sebastian/recursion-context

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2
- enable test suite

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-4
- add composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- cleanup pear registry

* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- get sources from github
- run test suite when build --with tests

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- rename to lowercase

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
