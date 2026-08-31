# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-code-unit-reverse-lookup3
#
# Copyright (c) 2016-2023 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    5e3a687f7d8ae33fb362c5c0743794bbb2420a1d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   code-unit-reverse-lookup
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   CodeUnitReverseLookup
%global major        3
%global php_home     %{_datadir}/php

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        3.0.0
Release:        8%{?dist}
Summary:        Looks up which function or method a line of code belongs to, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.1
BuildRequires:  php-reflection
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^10.0"
BuildRequires:  phpunit10
%endif

# from composer.json, "require": {
#        "php": ">=8.1"
Requires:       php(language) >= 8.1
# From phpcompatinfo report for version 3.0.0
Requires:       php-reflection
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Looks up which function or method a line of code belongs to.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --template fedora --output src/autoload.php src


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with tests}
mkdir vendor
touch vendor/autoload.php

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
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 3.0.0-3
- Enable test suite

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- raise dependency on PHP 8.1
- rename to php-sebastian-code-unit-reverse-lookup3
- move to /usr/share/php/SebastianBergmann/CodeUnitReverseLookup3

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 2.0.3-1
- update to 2.0.3 (no change)

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 2.0.2-1
- update to 2.0.2

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 2.0.1-1
- update to 2.0.1
- sources from git snapshot

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP 7.3
- rename to php-sebastian-code-unit-reverse-lookup2
- move to /usr/share/php/SebastianBergmann/CodeUnitReverseLookup2

* Sat Mar  4 2017 Remi Collet <remi@remirepo.net> - 1.0.1-1
- Update to 1.0.1 (no change)

* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- switch to fedora/autoloader

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
