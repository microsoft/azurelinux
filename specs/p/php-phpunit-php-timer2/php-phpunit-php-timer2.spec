# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-phpunit-php-timer2
#
# Copyright (c) 2010-2024 Christof Damian, Remi Collet
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    a691211e94ff39a34811abd521c31bd5b305b0bb
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-timer
# Packagist
%global pk_vendor    phpunit
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   Timer

%global major        2
%global php_home     %{_datadir}/php
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        2.1.4
Release: 5%{?dist}
Summary:        PHP Utility class for timing

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 7.2
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
# From composer.json"require-dev": {
#        "phpunit/phpunit": "^8.5"
BuildRequires:  phpunit8 >= 8.5
%endif

# From composer.json
#        "php": ">=7.1"
Requires:       php(language) >= 7.1
# From phpcompatinfo report for version 2.0.0
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Utility class for timing things, factored out of PHPUnit into a stand-alone
component.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
phpab \
   --template fedora \
   --output  src/autoload.php \
   src


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}


%if %{with_tests}
%check
mkdir vendor
touch vendor/autoload.php

: Run upstream test suite
ret=0
for cmd in php php81 php82 php83; do
  if which $cmd; then
    $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php \
      %{_bindir}/phpunit8 --verbose || ret=1
  fi
done
exit $ret
%endif


%files
%license LICENSE
%doc README.md
%doc composer.json
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar  1 2024 Remi Collet <remi@remirepo.net> - 2.1.4-1
- update to 2.1.4 (no change)
- sources from git snapshot

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 20 2023 Remi Collet <remi@remirepo.net> - 2.1.3-7
- use SPDX license ID

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Remi Collet <remi@remirepo.net> - 2.1.3-1
- update to 2.1.3 (no change)
- switch to phpunit8

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun  7 2019 Remi Collet <remi@remirepo.net> - 2.1.2-1
- update to 2.1.2
- drop patch merged upstream

* Wed Feb 20 2019 Remi Collet <remi@remirepo.net> - 2.1.1-2
- add patch from https://github.com/sebastianbergmann/php-timer/pull/21
  fix for 32-bit where large value are converted to float

* Wed Feb 20 2019 Remi Collet <remi@remirepo.net> - 2.1.1-1
- update to 2.1.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb  7 2018 Remi Collet <remi@remirepo.net> - 2.0.0-1
- normal build

* Fri Feb  2 2018 Remi Collet <remi@remirepo.net> - 2.0.0-0
- update to 2.0.0
- rename to php-phpunit-php-timer2
- move to /usr/share/php/SebastianBergmann/Timer
- raise dependency on PHP 7.1
- use phpunit 7
- bootstrap build

* Sun Feb 26 2017 Remi Collet <remi@fedoraproject.org> - 1.0.9-1
- update to 1.0.9
- switch to fedora/autoloader

* Fri May 13 2016 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8
- run test with both PHP 5 and 7 when available

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- update to 1.0.7 (only CS)

* Mon Jun 15 2015 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- update to 1.0.6
- generate autoloader, no more provided by upstream
- enable test suite during build
- add explicit spec license header

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.5-5
- add composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.0.5-3
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.0.5-2
- get sources from github
- run test suite when build --with tests

* Fri Aug 02 2013 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Sat Oct  6 2012 Remi Collet <rpms@famillecollet.com> 1.0.4-1
- update to 1.0.4

* Mon Sep 24 2012 Remi Collet <rpms@famillecollet.com> 1.0.3-1
- update to 1.0.3

* Sun Oct 23 2011 Remi Collet <rpms@famillecollet.com> 1.0.2-1
- update to 1.0.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 26 2010 Christof Damian <christof@damian.net> - 1.0.0-2
- fix timezone warnings

* Thu Jul 15 2010 Christof Damian <christof@damian.net> - 1.0.0-1
- initial package
