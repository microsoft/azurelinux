# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-phpunit-php-invoker7
#
# SPDX-FileCopyrightText:  Copyright 2011-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_with          tests

%global gh_commit    42e5c5cae0c65df12d1b1a3ab52bf3f50f244d88
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-invoker
%global gh_date      2026-02-06
%global php_home     %{_datadir}/php
# Packagist
%global pk_vendor    phpunit
%global pk_project   %{gh_project}
%global major        7
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   Invoker

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        7.0.0
Release:        1%{?dist}
Summary:        Invoke callables with a timeout, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.4.1
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# From composer.json, require-dev
#        "ext-pcntl": "*"
#        "phpunit/phpunit": "^13.0"
BuildRequires:  php-pcntl
BuildRequires:  phpunit13
%endif

# From composer.json, require
#        "php": ">=8.4",
Requires:       php(language) >= 8.4
# From phpcompatinfo report for version 4.0.0
Requires:       php-pcntl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
phpunit/php-invoker provides the means to invoke a callable with a timeout.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%build
: Generate autoloader
%{_bindir}/phpab \
   --template fedora \
   --output  src/autoload.php \
   src


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%if %{with tests}
%check
: Generate tests autoloader
mkdir vendor
%{_bindir}/phpab --output vendor/autoload.php tests

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
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Fri Feb  6 2026 Remi Collet <remi@remirepo.net> - 7.0.0-1
- update to 7.0.0
- raise dependency on PHP 8.4
- rename to php-phpunit-php-invoker7
- move to /usr/share/php/SebastianBergmann/Invoker7

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 6.0.0-2
- enable test suite

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.3
- rename to php-phpunit-php-invoker6
- move to /usr/share/php/SebastianBergmann/Invoker6

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 5.0.1-2
- enable test suite

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 8.2
- rename to php-phpunit-php-invoker5
- move to /usr/share/php/SebastianBergmann/Invoker5

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 4.0.0-3
- Enable test suite

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 8.1
- rename to php-phpunit-php-invoker4
- move to /usr/share/php/SebastianBergmann/Invoker4

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 3.1.1-1
- update to 3.1.1 (no change)

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 3.1.0-1
- update to 3.1.0

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 3.0.2-1
- update to 3.0.2

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1
- sources from git snapshot

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- raise dependency on PHP 7.3
- rename to php-phpunit-php-invoker3
- move to /usr/share/php/SebastianBergmann/Invoker3

* Mon Jan 29 2018 Remi Collet <remi@remirepo.net> - 2.0.0-1
- Update to 2.0.0
- rename to php-phpunit-php-invoker2
- raise dependency on PHP 7.1
- move to PSR-0 tree (/usr/share/php/SebastianBergmann/Invoker)
- switch to phpunit6
- switch to fedora/autoloader

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- update to 1.1.4
- raise dependencies on PHP >= 5.3.3 and php-timer >= 1.0.6
- generate autoloader

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-6
- add composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-4
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-3
- get sources from github
- run test suite when build --with tests

* Tue Jul 16 2013 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3 (stable) - API 1.1.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 (stable) - API 1.1.0

* Mon Sep 24 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (stable) - API 1.1.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable) - API 1.1.0
- now requires PHP_Timer

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 (stable) - API 1.0.0

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-3
- fix provides

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- new tarball, with documentation

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial generated RPM by pear make-rpm-spec + cleanups
