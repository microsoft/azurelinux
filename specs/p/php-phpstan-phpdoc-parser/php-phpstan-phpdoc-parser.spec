# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/Fedora spec file for php-phpstan-phpdoc-parser
#
# SPDX-FileCopyrightText:  Copyright 2024-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    a004701b11273a26cd7955a61d67a7f1e525a45a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpstan
%global gh_project   phpdoc-parser
%global php_home     %{_datadir}/php
%global namespace    PHPStan
%global library      PhpDocParser
%global major        %nil

Name:           php-%{gh_owner}-%{gh_project}%{major}
Version:        2.3.2
Release: 2%{?dist}
Summary:        PHPDoc parser with support for nullable, intersection and generic types

License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snapshot to retrieve test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
# Tests
%if %{with tests}
BuildRequires:  php(language) >= 7.4
BuildRequires:  php-json
BuildRequires:  php-pcre
# From composer, "require-dev": {
# "doctrine/annotations": "^2.0",
# "nikic/php-parser": "^5.3.0",
# "php-parallel-lint/php-parallel-lint": "^1.2",
# "phpstan/extension-installer": "^1.0",
# "phpstan/phpstan": "^2.0",
# "phpstan/phpstan-phpunit": "^2.0",
# "phpstan/phpstan-strict-rules": "^2.0",
# "phpunit/phpunit": "^9.6",
# "symfony/process": "^5.2"
%global phpunit %{_bindir}/phpunit9
BuildRequires:  phpunit9 >= 9.6
%endif
BuildRequires: (php-composer(nikic/php-parser)     >= 5.3  with php-composer(nikic/php-parser)     < 6)
# Autoloader
BuildRequires:  php-fedora-autoloader-devel

# From composer, "require": {
# "php": "^7.4 || ^8.0"
Requires:       php(language) >= 7.4
# Autoloader
Requires:       php-composer(fedora/autoloader)
# From phpcompatinfo report for version 2.4.2
Requires:       php-json
Requires:       php-pcre

Provides:       php-composer(%{gh_owner}/%{gh_project})   = %{version}


%description
Next generation phpDoc parser with support for intersection types and generics.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
phpab --template fedora --output src/autoload.php src


%install
: library
mkdir -p   %{buildroot}%{php_home}/%{namespace}/
cp -pr src %{buildroot}%{php_home}/%{namespace}/%{library}%{major}


%check
%if %{with tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
// to avoid v5 from PHPUnit
require_once '%{php_home}/PhpParser5/autoload.php';
require_once '%{buildroot}%{php_home}/%{namespace}/%{library}%{major}/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('%{namespace}\\%{library}\\', dirname(__DIR__) . '/tests/%{namespace}');
EOF

: ignore tests using symfony/process and abnfgen
rm tests/PHPStan/Parser/FuzzyTest.php
sed -e 's:exec://exec:' -i tests/bootstrap.php

: upstream test suite
# use auto_prepend_file to ensure we use new version (not old one pulled by PHPUnit)
# ignore test using doctrine/annotations
ret=0
for cmdarg in "php %{phpunit}" php82 php83 php84 php85; do
  if which $cmdarg; then
    set $cmdarg
    $1 -d auto_prepend_file=vendor/autoload.php \
      ${2:-%{_bindir}/phpunit9} \
        -d memory_limit=1G \
        --filter '^((?!(testDoctrine)).)*$' \
        --no-coverage \
        --verbose || ret=1
  fi
done
exit $ret
%else
: Test suite disabled
%endif


%files
%license LICENSE
%doc *.md
%doc composer.json
%dir %{php_home}/%{namespace}
     %{php_home}/%{namespace}/%{library}%{major}


%changelog
* Mon Jan 26 2026 Remi Collet <remi@remirepo.net> - 2.3.2-1
- update to 2.3.2

* Mon Jan 12 2026 Remi Collet <remi@remirepo.net> - 2.3.1-1
- update to 2.3.1

* Mon Sep  1 2025 Remi Collet <remi@remirepo.net> - 2.3.0-1
- update to 2.3.0

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Remi Collet <remi@remirepo.net> - 2.2.0-1
- update to 2.2.0

* Wed Feb 19 2025 Remi Collet <remi@remirepo.net> - 2.1.0-1
- update to 2.1.0

* Tue Feb 18 2025 Remi Collet <remi@remirepo.net> - 2.0.2-1
- update to 2.0.2

* Thu Feb 13 2025 Remi Collet <remi@remirepo.net> - 2.0.1-1
- update to 2.0.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 23 2024 Remi Collet <remi@remirepo.net> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP 7.4
- raise dependency on nikic/php-parser 5.3

* Tue Dec 17 2024 Remi Collet <remi@remirepo.net> - 1.33.0-2
- drop abnfgen from archive
- re-license spec file to CECILL-2.1

* Mon Oct 14 2024 Remi Collet <remi@remirepo.net> - 1.33.0-1
- update to 1.33.0

* Thu Sep 26 2024 Remi Collet <remi@remirepo.net> - 1.32.0-1
- update to 1.32.0

* Mon Sep 23 2024 Remi Collet <remi@remirepo.net> - 1.31.0-1
- update to 1.31.0

* Mon Sep  9 2024 Remi Collet <remi@remirepo.net> - 1.30.1-1
- update to 1.30.1

* Thu Aug 29 2024 Remi Collet <remi@remirepo.net> - 1.30.0-1
- update to 1.30.0

* Fri May 31 2024 Remi Collet <remi@remirepo.net> - 1.29.1-1
- update to 1.29.1

* Mon May 13 2024 Remi Collet <remi@remirepo.net> - 1.29.0-1
- update to 1.29.0

* Thu Apr  4 2024 Remi Collet <remi@remirepo.net> - 1.28.0-1
- update to 1.28.0

* Thu Mar 21 2024 Remi Collet <remi@remirepo.net> - 1.27.0-1
- update to 1.27.0

* Mon Feb 26 2024 Remi Collet <remi@remirepo.net> - 1.26.0-1
- update to 1.26.0

* Fri Jan  5 2024 Remi Collet <remi@remirepo.net> - 1.25.0-1
- update to 1.25.0

* Mon Dec 18 2023 Remi Collet <remi@remirepo.net> - 1.24.5-1
- update to 1.24.5

* Mon Nov 27 2023 Remi Collet <remi@remirepo.net> - 1.24.4-1
- update to 1.24.4

* Mon Nov 20 2023 Remi Collet <remi@remirepo.net> - 1.24.3-1
- update to 1.24.3

* Wed Sep 27 2023 Remi Collet <remi@remirepo.net> - 1.24.2-1
- update to 1.24.2

* Tue Sep 19 2023 Remi Collet <remi@remirepo.net> - 1.24.1-1
- update to 1.24.1

* Fri Sep  8 2023 Remi Collet <remi@remirepo.net> - 1.24.0-1
- update to 1.24.0

* Fri Aug  4 2023 Remi Collet <remi@remirepo.net> - 1.23.1-1
- update to 1.23.1

* Mon Jul 24 2023 Remi Collet <remi@remirepo.net> - 1.23.0-1
- update to 1.23.0

* Mon Jul  3 2023 Remi Collet <remi@remirepo.net> - 1.22.1-1
- update to 1.22.1

* Fri Jun  2 2023 Remi Collet <remi@remirepo.net> - 1.22.0-1
- update to 1.22.0

* Tue May 30 2023 Remi Collet <remi@remirepo.net> - 1.21.3-1
- update to 1.21.3

* Wed May 17 2023 Remi Collet <remi@remirepo.net> - 1.21.0-1
- update to 1.21.0

* Wed May  3 2023 Remi Collet <remi@remirepo.net> - 1.20.4-1
- update to 1.20.4

* Tue Apr 25 2023 Remi Collet <remi@remirepo.net> - 1.20.3-1
- update to 1.20.3

* Tue Apr 25 2023 Remi Collet <remi@remirepo.net> - 1.20.2-1
- update to 1.20.2

* Sun Apr 23 2023 Remi Collet <remi@remirepo.net> - 1.20.1-1
- update to 1.20.1

* Thu Apr 20 2023 Remi Collet <remi@remirepo.net> - 1.20.0-1
- update to 1.20.0

* Wed Apr 19 2023 Remi Collet <remi@remirepo.net> - 1.19.1-1
- update to 1.19.1

* Fri Apr  7 2023 Remi Collet <remi@remirepo.net> - 1.18.1-1
- update to 1.18.1

* Thu Apr  6 2023 Remi Collet <remi@remirepo.net> - 1.18.0-1
- update to 1.18.0

* Tue Apr  4 2023 Remi Collet <remi@remirepo.net> - 1.17.1-1
- update to 1.17.1

* Mon Mar 20 2023 Remi Collet <remi@remirepo.net> - 1.16.1-1
- initial package
