# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-phpunit-php-text-template6
#
# SPDX-FileCopyrightText:  Copyright 2010-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_with          tests

%global gh_commit    a47af19f93f76aa3368303d752aa5272ca3299f4
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-text-template
%global gh_date      2026-02-06
# Packagist
%global pk_vendor    phpunit
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   Template
%global php_home     %{_datadir}/php
%global ver_major    6

Name:           php-%{pk_vendor}-%{pk_project}%{ver_major}
Version:        6.0.0
Release: 2%{?dist}
Summary:        Simple template engine, version %{ver_major}

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
#        "phpunit/phpunit": "^13.0"
BuildRequires:  phpunit13
%endif

# From composer.json
#        "php": ">=8.4"
Requires:       php(language) >= 8.4
# From phpcompatinfo report for version 3.0.0

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Simple template engine.

This package provides version %{ver_major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
%{_bindir}/phpab --template fedora --output src/autoload.php src


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}


%if %{with tests}
%check
: Generate tests autoloader
mkdir vendor
%{_bindir}/phpab --output vendor/autoload.php tests

: Run upstream test suite
ret=0
for cmd in php php84 php85; do
  if which $cmd; then
    $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}/autoload.php \
      %{_bindir}/phpunit13 || ret=1
  fi
done
exit $ret
%endif


%files
%license LICENSE
%doc *.md
%doc composer.json
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}


%changelog
* Fri Feb  6 2026 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.4
- rename to php-phpunit-php-text-template6
- move to /usr/share/php/SebastianBergmann/Template6

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 5.0.0-2
- enable test suite

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 8.3
- rename to php-phpunit-php-text-template5
- move to /usr/share/php/SebastianBergmann/Template5

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 4.0.1-2
- enable test suite

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 8.2
- rename to php-phpunit-php-text-template4
- move to /usr/share/php/SebastianBergmann/Template4

* Fri Sep  1 2023 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 3.0.0-3
- Enable test suite

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- raise dependency on PHP 8.1
- rename to php-phpunit-php-text-template3
- move to /usr/share/php/SebastianBergmann/Template3

* Mon Oct 26 2020 Remi Collet <remi@remirepo.net> - 2.0.4-1
- update to 2.0.4

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 2.0.3-1
- update to 2.0.3 (no change)

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 2.0.2-1
- update to 2.0.2

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 2.0.1-1
- update to 2.0.1
- sources from git snapshot
- run upstream test suite

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP 7.3
- rename to php-phpunit-php-text-template2
- move to /usr/share/php/SebastianBergmann/Template2

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1
- generate autoloader

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-4
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-3
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- sources from github

* Thu Jan 30 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Version 1.1.4 (stable) - API 1.1.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Version 1.1.3 (stable) - API 1.1.0 (stable)

* Mon Sep 24 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Version 1.1.2 (stable) - API 1.1.0 (stable)
- LICENSE is now provided in upstream tarball

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)
- raise dependencies, PEAR 1.9.4 and PHP 5.2.7

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)
- remove README.mardown (which is only install doc)

* Fri Nov 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-2
- fix URL

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean
