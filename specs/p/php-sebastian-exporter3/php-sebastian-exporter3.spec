# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-exporter3
#
# SPDX-FileCopyrightText:  Copyright 2013-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    64cfeaa341951ceb2019d7b98232399d57bb2296
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   exporter
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
%global ns_vendor    SebastianBergmann
%global ns_project   Exporter
%global major        3
%global php_home     %{_datadir}/php
%global pear_name    Exporter
%global pear_channel pear.phpunit.de
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

# NOTICE: used by phpunit 6, 7 and 8

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        3.1.8
Release:        1%{?dist}
Summary:        Export PHP variables for visualization, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 7.2
BuildRequires:  php-fedora-autoloader-devel >= 1.0.0
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^8.5",
#        "ext-mbstring": "*"
BuildRequires:  phpunit8
BuildRequires:  php-mbstring
BuildRequires:  (php-composer(%{pk_vendor}/recursion-context) >= 3.0 with php-composer(%{pk_vendor}/recursion-context) < 4)
%endif

# from composer.json
#        "php": ">=7.2",
#        "sebastian/recursion-context": "^3.0"
Requires:       php(language) >= 7.2
Requires:       (php-composer(%{pk_vendor}/recursion-context) >= 3.0 with php-composer(%{pk_vendor}/recursion-context) < 4)
# from phpcompatinfo report for version 3.0.0
Requires:       php-mbstring
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Provides the functionality to export PHP variables for visualization.

This package provides the version %{major} of the library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# generate the Autoloader
phpab --template fedora --output src/autoload.php src

# Rely on include_path as in PHPUnit dependencies
cat <<EOF | tee -a src/autoload.php
// Dependency' autoloader
require_once '%{php_home}/%{ns_vendor}/RecursionContext3/autoload.php';
EOF


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%if %{with_tests}
%check
mkdir vendor
touch vendor/autoload.php

: Run upstream test suite
ret=0
for cmd in php php81 php82 php83 php84 php85; do
  if which $cmd; then
    %{_bindir}/php -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
    %{_bindir}/phpunit8	  --verbose || ret=1
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
* Wed Sep 24 2025 Remi Collet <remi@remirepo.net> - 3.1.8-1
- update to 3.1.8

* Mon Sep 22 2025 Remi Collet <remi@remirepo.net> - 3.1.7-1
- update to 3.1.7

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar  5 2024 Remi Collet <remi@remirepo.net> - 3.1.6-1
- update to 3.1.6
- raise dependency on PHP 7.2

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 21 2023 Remi Collet <remi@remirepo.net> - 3.1.5-3
- use SPDX license ID

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 14 2022 Remi Collet <remi@remirepo.net> - 3.1.5-1
- update to 3.1.5

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 15 2021 Remi Collet <remi@remirepo.net> - 3.1.4-1
- update to 3.1.4
- sources from git snapshot

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 10 2021 Remi Collet <remi@remirepo.net> - 3.1.3-2
- switch to phpunit8

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Remi Collet <remi@remirepo.net> - 3.1.3-1
- update to 3.1.3 (no change)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 15 2019 Remi Collet <remi@remirepo.net> - 3.1.2-1
- update to 3.1.2

* Mon Aug 12 2019 Remi Collet <remi@remirepo.net> - 3.1.1-1
- update to 3.1.1

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec  6 2018 Remi Collet <remi@remirepo.net> - 3.1.0-5
- cleanup for EL-8

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb  6 2018 Remi Collet <remi@remirepo.net> - 3.1.0-3
- use range dependencies on F27+

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr  3 2017 Remi Collet <remi@remirepo.net> - 3.1.0-1
- Update to 3.1.0

* Mon Mar 13 2017 Remi Collet <remi@remirepo.net> - 3.0.0-2
- non bootstrap build

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
