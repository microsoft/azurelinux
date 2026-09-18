# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-environment6
#
# Copyright (c) 2014-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%bcond_without       tests

# Sources
%global gh_commit    8074dbcd93529b357029f5cc5058fd3e43666984
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   environment
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global major        6
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   Environment

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        6.1.0
Release:        4%{?dist}
Summary:        Handle HHVM/PHP environments, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh


BuildArch:      noarch
BuildRequires:  php(language) >= 8.1
BuildRequires:  php-pcre
BuildRequires:  php-posix
# Autoloader
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^10.0"
BuildRequires:  phpunit10
%endif

# from composer.json, "require": {
#        "php": ">=8.1"
Requires:       php(language) >= 8.1
# From phpcompatinfo report for 6.0.0
Requires:       php-pcre
Requires:       php-posix
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
This component provides functionality that helps writing PHP code that
has runtime-specific (PHP / HHVM) execution paths.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
%{_bindir}/phpab \
   --template fedora \
   --output src/autoload.php \
   src


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%if %{with tests}
%check
mkdir vendor
touch vendor/autoload.php

: Run tests
ret=0
for cmd in php php81 php82 php83; do
  if which $cmd; then
   $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
     -d pcov.enabled=1 \
     %{_bindir}/phpunit10 || ret=1
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
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 26 2024 Remi Collet <remi@remirepo.net> - 6.1.0-1
- update to 6.1.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 6.0.1-3
- Enable test suite

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 11 2023 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.1
- rename to php-sebastian-environment6
- move to /usr/share/php/SebastianBergmann/Environment6

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 5.1.5-1
- update to 5.1.5

* Mon Apr  4 2022 Remi Collet <remi@remirepo.net> - 5.1.4-1
- update to 5.1.4

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 5.1.3-1
- update to 5.1.3 (no change)

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 5.1.2-1
- update to 5.1.2

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 5.1.1-1
- update to 5.1.1
- sources from git snapshot

* Tue Apr 14 2020 Remi Collet <remi@remirepo.net> - 5.1.0-1
- update to 5.1.0

* Tue Mar 31 2020 Remi Collet <remi@remirepo.net> - 5.0.2-1
- update to 5.0.2
- switch to phpunit9

* Wed Feb 19 2020 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 7.3
- rename to php-sebastian-environment5
- move to /usr/share/php/SebastianBergmann/Environment5

* Wed Nov 20 2019 Remi Collet <remi@remirepo.net> - 4.2.3-1
- update to 4.2.3

* Mon May  6 2019 Remi Collet <remi@remirepo.net> - 4.2.2-1
- update to 4.2.2

* Thu Apr 25 2019 Remi Collet <remi@remirepo.net> - 4.2.1-1
- update to 4.2.1

* Fri Feb  1 2019 Remi Collet <remi@remirepo.net> - 4.1.0-1
- update to 4.1.0

* Wed Jan 30 2019 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2

* Mon Dec  3 2018 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1
- rename to php-sebastian-environment4
- move to /usr/share/php/SebastianBergmann/Environment4
- raise dependency on PHP 7.1
- use phpunit7

* Sun Jul  2 2017 Remi Collet <remi@remirepo.net> - 3.1.0-1
- Update to 3.1.0

* Wed Jun 21 2017 Remi Collet <remi@remirepo.net> - 3.0.4-1
- Update to 3.0.4

* Mon May 22 2017 Remi Collet <remi@remirepo.net> - 3.0.3-1
- Update to 3.0.3

* Sun Apr 30 2017 Remi Collet <remi@remirepo.net> - 3.0.2-0
- boostrap build for review #1444648

* Sun Apr 23 2017 Remi Collet <remi@remirepo.net> - 3.0.2-1
- rename to php-sebastian-environment3
- update to 3.0.2

* Sat Nov 26 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP 5.6
- switch to fedora/autoloader

* Wed Aug 31 2016 Remi Collet <remi@fedoraproject.org> - 1.3.8-1
- update to 1.3.8

* Tue May 17 2016 Remi Collet <remi@fedoraproject.org> - 1.3.7-1
- update to 1.3.7
- add explicit dependencies on pcre and posix

* Wed May  4 2016 Remi Collet <remi@fedoraproject.org> - 1.3.6-1
- update to 1.3.6

* Sun Feb 28 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-1
- update to 1.3.5

* Wed Dec  2 2015 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- update to 1.3.3 (no change on linux)
- run test suite with both php 5 and 7 when available

* Mon Aug  3 2015 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- update to 1.3.2

* Sun Aug  2 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2
- fix license handling

* Tue Dec  2 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Wed Oct  8 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- enable test suite

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-4
- composer dependencies

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add generated autoload.php

* Tue Apr  1 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
