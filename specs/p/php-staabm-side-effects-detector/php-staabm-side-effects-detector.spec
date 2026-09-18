# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-staabm-side-effects-detector
#
# SPDX-FileCopyrightText:  Copyright 2024 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    d8334211a140ce329c13726d4a715adbddd0a163
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     staabm
%global gh_project   side-effects-detector
%global php_home     %{_datadir}/php
%global ns_owner     staabm
%global ns_project   SideEffectsDetector

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.5
Release:        3%{?dist}
Summary:        A static analysis tool to detect side effects in PHP code

License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snapshot to get everything, despite .gitattributes
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
%if %{with tests}
BuildRequires:  php(language) >= 7.4
BuildRequires:  php-tokenizer
# From composer.json, "require-dev": {
#        "phpstan/extension-installer": "^1.4.3",
#        "phpstan/phpstan": "^1.12.6",
#        "phpunit/phpunit": "^9.6.21",
#        "symfony/var-dumper": "^5.4.43",
#        "tomasvotruba/type-coverage": "1.0.0",
#        "tomasvotruba/unused-public": "1.0.0"
BuildRequires:  phpunit9 >= 9.6.21
%endif
# Autoloader
BuildRequires:  php-fedora-autoloader-devel

# From composer.json, "require": {
#        "php": "^7.4 || ^8.0",
#        "ext-tokenizer": "*"
Requires:       php(language) >= 7.4
Requires:       php-tokenizer
# From phpcompatinfo report for version 1.0.5
#nothing
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Analyzes php-code for side-effects.

When code has no side-effects it can e.g. be used with eval($code)
in the same process without interfering.

Side-effects are classified into categories to filter them more easily
depending on your use-case.

This library is used e.g. in PHPUnit to improve performance of PHPT test-cases.

Autoloader: %{php_home}/%{ns_owner}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate autoloader
phpab --template fedora --output lib/autoload.php lib


%install
: Library
mkdir -p   %{buildroot}%{php_home}/%{ns_owner}
cp -pr lib %{buildroot}%{php_home}/%{ns_owner}/%{ns_project}


%check
%if %{with tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{buildroot}%{php_home}/%{ns_owner}/%{ns_project}/autoload.php';
EOF

ret=0
for cmd in php php81 php82 php83 php84; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit9 --no-coverage || ret=1
  fi
done
exit $ret
%else
: Test suite disabled
%endif


%files
%license LICENSE
%doc composer.json
%doc *.md
%dir %{php_home}/%{ns_owner}
     %{php_home}/%{ns_owner}/%{ns_project}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec  6 2024 Remi Collet <remi@remirepo.net> - 1.0.5-1
- initial package
