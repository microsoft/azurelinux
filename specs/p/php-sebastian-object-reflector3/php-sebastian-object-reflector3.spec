# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-object-reflector3
#
# Copyright (c) 2017-2023 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    24ed13d98130f0e7122df55d06c5c4942a577957
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   object-reflector
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   ObjectReflector
%global major        3
%global php_home     %{_datadir}/php

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        3.0.0
Release:        8%{?dist}
Summary:        Allows reflection of object attributes, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.1
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^10.0"
BuildRequires:  phpunit10
%endif

# from composer.json
#        "php": ">=8.1"
Requires:       php(language) >= 8.1
# from phpcompatinfo report for version 2.0.0
#nothing
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Allows reflection of object attributes, including inherited
and non-public ones.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
%{_bindir}/phpab --template fedora --output src/autoload.php src


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with tests}
mkdir vendor
%{_bindir}/phpab --output vendor/autoload.php tests/_fixture
cat << 'EOF' | tee -a vendor/autoload.php
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php';
EOF

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
%doc README.md composer.json
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
- rename to php-sebastian-object-reflector3
- move to /usr/share/php/SebastianBergmann/ObjectReflector3

* Mon Oct 26 2020 Remi Collet <remi@remirepo.net> - 2.0.4-1
- update to 2.0.4

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
- rename to php-sebastian-object-reflector2
- move to /usr/share/php/SebastianBergmann/ObjectReflector2

* Wed Mar 29 2017 Remi Collet <remi@remirepo.net> - 1.1.1-1
- Update to 1.1.1

* Thu Mar 16 2017 Remi Collet <remi@remirepo.net> - 1.1.0-1
- Update to 1.1.0

* Sun Mar 12 2017 Remi Collet <remi@remirepo.net> - 1.0.0-1
- initial package
