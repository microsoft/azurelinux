# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-recursion-context4
#
# SPDX-FileCopyrightText:  Copyright 2015-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    539c6691e0623af6dc6f9c20384c120f963465a0
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   recursion-context
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   RecursionContext
%global major        4
%global php_home     %{_datadir}/php

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        4.0.6
Release: 2%{?dist}
Summary:        Recursively process PHP variables, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 7.3
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^9.3"
BuildRequires:  phpunit9 >= 9.3
%endif

# from composer.json
#        "php": ">=7.3"
Requires:       php(language) >= 7.3
# from phpcompatinfo report for version 4.0.0
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Provides functionality to recursively process PHP variables.

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
touch vendor/autoload.php

: Run upstream test suite
ret=0
for cmd in php php81 php82 php83 php84 php85; do
  if which $cmd; then
    $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
      %{_bindir}/phpunit9  --verbose || ret=1
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
* Mon Aug 11 2025 Remi Collet <remi@remirepo.net> - 4.0.6-1
- update to 4.0.6

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 21 2023 Remi Collet <remi@remirepo.net> - 4.0.5-2
- improve description

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 4.0.5-1
- update to 4.0.5

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 26 2020 Remi Collet <remi@remirepo.net> - 4.0.4-1
- update to 4.0.4

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 4.0.3-1
- update to 4.0.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1
- sources from git snapshot

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 7.3
- rename to php-sebastian-recursion-context4
- move to /usr/share/php/SebastianBergmann/RecursionContext4

* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- rename to php-sebastian-recursion-context3
- raise dependency on PHP 7

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 (no change)

* Tue Nov 15 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3

* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- switch to fedora/autoloader

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2
- drop dependency on hash extension
- run test suite with both php 5 and 7 when available

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1 (only CS)

* Sat Jan 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
