# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-phpunit-php-code-coverage13
#
# SPDX-FileCopyrightText:  Copyright 2013-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_without       tests

# Github
%global gh_commit    a8b58fde2f4fbc69a064e1f80ff917607cf7737c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    sebastianbergmann
%global gh_project   php-code-coverage
%global gh_date      2026-02-06
# Packagist
%global pk_vendor    phpunit
%global pk_project   php-code-coverage
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   CodeCoverage
%global php_home     %{_datadir}/php
%global ver_major    13

Name:           php-%{pk_vendor}-%{pk_project}%{ver_major}
Version:        13.0.1
Release: 3%{?dist}
Summary:        PHP code coverage information, version %{ver_major}

# SPDX: Main license is BSD-3-Clause
# BSD-3-Clause: D3
# MIT: boostrap, d3, holder, html5shiv, jquery, respond
# Apache-2.0: nvd3
License:        BSD-3-Clause AND MIT AND Apache-2.0
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.4.1
BuildRequires:  php-fedora-autoloader-devel >= 1.0.0
%if %{with tests}
BuildRequires:  (php-composer(nikic/php-parser)                   >= 5.7.0  with php-composer(nikic/php-parser)                   < 6)
BuildRequires:  (php-composer(phpunit/php-file-iterator)          >= 7.0    with php-composer(phpunit/php-file-iterator)          < 8)
BuildRequires:  (php-composer(phpunit/php-text-template)          >= 6.0    with php-composer(phpunit/php-text-template)          < 7)
BuildRequires:  (php-composer(sebastian/complexity)               >= 6.0    with php-composer(sebastian/complexity)               < 7)
BuildRequires:  (php-composer(sebastian/environment)              >= 9.0    with php-composer(sebastian/environment)              < 10)
BuildRequires:  (php-composer(sebastian/lines-of-code)            >= 5.0    with php-composer(sebastian/lines-of-code)            < 6)
BuildRequires:  (php-composer(sebastian/version)                  >= 7.0    with php-composer(sebastian/version)                  < 8)
BuildRequires:  (php-composer(theseer/tokenizer)                  >= 2.0.1  with php-composer(theseer/tokenizer)                  < 3)
BuildRequires:  php-dom
BuildRequires:  php-json
BuildRequires:  php-libxml
BuildRequires:  php-tokenizer
BuildRequires:  php-xmlwriter
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^13.0"
BuildRequires:  phpunit13
BuildRequires:  php-xdebug
%endif

# From composer.json, require
#        "php": ">=8.3",
#        "ext-dom": "*",
#        "ext-libxml": "*",
#        "ext-xmlwriter": "*",
#        "nikic/php-parser": "^5.7.0",
#        "phpunit/php-file-iterator": "^7.0",
#        "phpunit/php-text-template": "^6.0",
#        "sebastian/complexity": "^6.0",
#        "sebastian/environment": "^9.0",
#        "sebastian/lines-of-code": "^5.0",
#        "sebastian/version": "^7.0",
#        "theseer/tokenizer": "^2.0.1"
Requires:       php(language) >= 8.3
Requires:       php-dom
Requires:       php-libxml
Requires:       php-xmlwriter
Requires:       (php-composer(nikic/php-parser)                   >= 5.7.0  with php-composer(nikic/php-parser)                   < 6)
Requires:       (php-composer(phpunit/php-file-iterator)          >= 7.0    with php-composer(phpunit/php-file-iterator)          < 8)
Requires:       (php-composer(phpunit/php-text-template)          >= 6.0    with php-composer(phpunit/php-text-template)          < 7)
Requires:       (php-composer(sebastian/complexity)               >= 6.0    with php-composer(sebastian/complexity)               < 7)
Requires:       (php-composer(sebastian/environment)              >= 9.0    with php-composer(sebastian/environment)              < 10)
Requires:       (php-composer(sebastian/lines-of-code)            >= 5.0    with php-composer(sebastian/lines-of-code)            < 6)
Requires:       (php-composer(sebastian/version)                  >= 7.0    with php-composer(sebastian/version)                  < 8)
Requires:       (php-composer(theseer/tokenizer)                  >= 2.0.1  with php-composer(theseer/tokenizer)                  < 3)
# From composer.json, suggest
#        "ext-pcov": "*",
#        "ext-xdebug": "*"
Suggests:       php-xdebug
Recommends:     php-pcov
# From phpcompatinfo report for version 10.0.0
Requires:       php-json
Requires:       php-tokenizer
# Autoloader
Requires:       php-composer(fedora/autoloader)

# Composer
Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}
# Bundled assets in HTML template
Provides:       bundled(js-bootstrap) = 5.3.6
Provides:       bundled(js-jquery)    = 3.7.1
Provides:       bundled(js-billboard) = 3.15.1


%description
Library that provides collection, processing, and rendering functionality
for PHP code coverage information.

This package provides version %{ver_major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
%{_bindir}/phpab \
  --template fedora \
  --output src/autoload.php \
  src

cat << 'EOF' | tee -a src/autoload.php
\Fedora\Autoloader\Dependencies::required([
    '%{php_home}/PhpParser5/autoload.php',
    '%{php_home}/%{ns_vendor}/FileIterator7/autoload.php',
    '%{php_home}/%{ns_vendor}/Template6/autoload.php',
    '%{php_home}/%{ns_vendor}/Complexity6/autoload.php',
    '%{php_home}/%{ns_vendor}/Environment9/autoload.php',
    '%{php_home}/%{ns_vendor}/LinesOfCode5/autoload.php',
    '%{php_home}/%{ns_vendor}/Version7/autoload.php',
    '%{php_home}/TheSeer/Tokenizer2/autoload.php',
]);
EOF


%install
# Restore PSR-0 tree
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}


%if %{with tests}
%check
if ! php -v | grep Xdebug
then EXT="-d zend_extension=xdebug.so -d xdebug.mode=coverage"
fi
export XDEBUG_MODE=coverage

%{_bindir}/phpab \
  --template fedora \
  --output tests/bootstrap.php \
  --exclude 'tests/_files/*.php' \
  tests

cat << 'EOF' | tee -a tests/bootstrap.php
define('TEST_FILES_PATH', __DIR__ . '/_files/');
EOF

ret=0
# testCanBeCreatedFromDefaults rely on git layout

for cmd in php php84 php85; do
  if which $cmd; then
    $cmd $EXT \
      -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}/autoload.php \
        %{_bindir}/phpunit13 \
          --filter "^((?!(testCanBeCreatedFromDefaults)).)*$" \
          || ret=1
  fi
done
exit $ret
%endif


%files
%license LICENSE
%doc README.md
%doc ChangeLog-%{ver_major}.0.md
%doc composer.json
%{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}


%changelog
* Tue Feb 10 2026 Remi Collet <remi@remirepo.net> - 13.0.1-2
- enable test suite

* Fri Feb  6 2026 Remi Collet <remi@remirepo.net> - 13.0.1-1
- update to 13.0.1
- raise depdendency on PHP 8.4
- raise dependency on phpunit/php-file-iterator 7.0
- raise dependency on phpunit/php-text-template 6.0
- raise dependency on sebastian/complexity 6.0
- raise dependency on sebastian/environment 9.0
- raise dependency on sebastian/lines-of-code 5.0
- raise dependency on sebastian/version 7.0
- rename to php-phpunit-php-code-coverage13
- move to /usr/share/php/SebastianBergmann/CodeCoverage13

* Thu Dec 25 2025 Remi Collet <remi@remirepo.net> - 12.5.2-1
- update to 12.5.2

* Tue Dec  9 2025 Remi Collet <remi@remirepo.net> - 12.5.1-1
- update to 12.5.1
- raise dependency on nikic/php-parser 5.7.0
- raise dependency on theseer/tokenizer 2.0.1
- add upstream patch for theseer/tokenizer 2.x

* Tue Dec  2 2025 Remi Collet <remi@remirepo.net> - 12.5.0-1
- update to 12.5.0
- raise dependency on nikic/php-parser 5.6.1
- raise dependency on theseer/tokenizer 1.3.1

* Wed Sep 24 2025 Remi Collet <remi@remirepo.net> - 12.4.0-1
- update to 12.4.0

* Wed Sep 17 2025 Remi Collet <remi@remirepo.net> - 12.3.8-1
- update to 12.3.8

* Wed Sep 10 2025 Remi Collet <remi@remirepo.net> - 12.3.7-1
- update to 12.3.7

* Tue Sep  2 2025 Remi Collet <remi@remirepo.net> - 12.3.6-1
- update to 12.3.6

* Mon Sep  1 2025 Remi Collet <remi@remirepo.net> - 12.3.5-1
- update to 12.3.5
- raise dependency on nikic/php-parser 5.6.1
- raise dependency on sebastian/environment 8.0

* Fri Aug 29 2025 Remi Collet <remi@remirepo.net> - 12.3.4-1
- update to 12.3.4

* Thu Aug 28 2025 Remi Collet <remi@remirepo.net> - 12.3.3-1
- update to 12.3.3

* Tue Jul 29 2025 Remi Collet <remi@remirepo.net> - 12.3.2-1
- update to 12.3.2

* Thu Jun 19 2025 Remi Collet <remi@remirepo.net> - 12.3.1-1
- update to 12.3.1

* Mon May 26 2025 Remi Collet <remi@remirepo.net> - 12.3.0-1
- update to 12.3.0

* Mon May  5 2025 Remi Collet <remi@remirepo.net> - 12.2.1-1
- update to 12.2.1

* Thu Apr  3 2025 Remi Collet <remi@remirepo.net> - 12.1.2-1
- update to 12.1.2

* Thu Apr  3 2025 Remi Collet <remi@remirepo.net> - 12.1.1-1
- update to 12.1.1

* Tue Mar 18 2025 Remi Collet <remi@remirepo.net> - 12.1.0-1
- update to 12.1.0

* Mon Mar 17 2025 Remi Collet <remi@remirepo.net> - 12.0.5-1
- update to 12.0.5

* Wed Feb 26 2025 Remi Collet <remi@remirepo.net> - 12.0.4-1
- update to 12.0.4

* Tue Feb 18 2025 Remi Collet <remi@remirepo.net> - 12.0.3-1
- update to 12.0.3

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 12.0.2-2
- enable test suite

* Sun Feb  9 2025 Remi Collet <remi@remirepo.net> - 12.0.2-1
- update to 12.0.2

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 12.0.1-1
- update to 12.0.1

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 12.0.0-1
- update to 12.0.0
- raise depdendency on PHP 8.3
- raise dependency on nikic/php-parser 5.4
- raise dependency on phpunit/php-file-iterator 6.0
- raise dependency on phpunit/php-text-template 5.0
- raise dependency on sebastian/complexity 5.0
- raise dependency on sebastian/environment 8.0
- raise dependency on sebastian/lines-of-code 4.0
- raise dependency on sebastian/version 6.0
- drop dependency on sebastian/code-unit-reverse-lookup
- rename to php-phpunit-php-code-coverage12
- move to /usr/share/php/SebastianBergmann/CodeCoverage12

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 11.0.8-2
- enable test suite

* Wed Dec 11 2024 Remi Collet <remi@remirepo.net> - 11.0.8-1
- update to 11.0.8
- re-license spec file to CECILL-2.1

* Wed Oct  9 2024 Remi Collet <remi@remirepo.net> - 11.0.7-1
- update to 11.0.7
- raise dependency on nikic/php-parser 5.3.1
- raise dependency on phpunit/php-file-iterator 5.1.0
- raise dependency on sebastian/version 5.0.2

* Thu Aug 22 2024 Remi Collet <remi@remirepo.net> - 11.0.6-1
- update to 11.0.6 (no change)
- raise dependencies

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 11.0.5-1
- update to 11.0.5

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 11.0.4-1
- update to 11.0.4

* Wed Mar 13 2024 Remi Collet <remi@remirepo.net> - 11.0.3-1
- update to 11.0.3

* Mon Mar 11 2024 Remi Collet <remi@remirepo.net> - 11.0.2-1
- update to 11.0.2

* Tue Mar  5 2024 Remi Collet <remi@remirepo.net> - 11.0.1-1
- update to 11.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 11.0.0-2
- fix package URL

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 11.0.0-1
- update to 11.0.0
- raise depdendency on PHP 8.2
- raise dependency on nikic/php-parser 5.0
- raise dependency on phpunit/php-file-iterator 5.0
- raise dependency on phpunit/php-text-template 4.0
- raise dependency on sebastian/code-unit-reverse-lookup 4.0
- raise dependency on sebastian/complexity 4.0
- raise dependency on sebastian/environment 7.0
- raise dependency on sebastian/lines-of-code 3.0
- raise dependency on sebastian/version 5.0
- rename to php-phpunit-php-code-coverage11
- move to /usr/share/php/SebastianBergmann/CodeCoverage11

* Thu Dec 21 2023 Remi Collet <remi@remirepo.net> - 10.1.11-1
- update to 10.1.11
- raise dependency on nikic/php-parser 4.18 and allow 5.0

* Mon Dec 11 2023 Remi Collet <remi@remirepo.net> - 10.1.10-1
- update to 10.1.10

* Thu Nov 23 2023 Remi Collet <remi@remirepo.net> - 10.1.9-1
- update to 10.1.9

* Thu Nov 16 2023 Remi Collet <remi@remirepo.net> - 10.1.8-1
- update to 10.1.8

* Thu Oct  5 2023 Remi Collet <remi@remirepo.net> - 10.1.7-1
- update to 10.1.7

* Tue Sep 19 2023 Remi Collet <remi@remirepo.net> - 10.1.6-1
- update to 10.1.6

* Wed Sep 13 2023 Remi Collet <remi@remirepo.net> - 10.1.5-1
- update to 10.1.5

* Fri Sep  1 2023 Remi Collet <remi@remirepo.net> - 10.1.4-1
- update to 10.1.4

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 10.1.3-2
- Enable test suite

* Thu Jul 27 2023 Remi Collet <remi@remirepo.net> - 10.1.3-1
- update to 10.1.3

* Mon Jun 19 2023 Remi Collet <remi@remirepo.net> - 10.1.2-2
- fix dependencies, from review #2168110

* Wed May 24 2023 Remi Collet <remi@remirepo.net> - 10.1.2-1
- update to 10.1.2

* Wed Apr 19 2023 Remi Collet <remi@remirepo.net> - 10.1.1-1
- update to 10.1.1

* Thu Apr 13 2023 Remi Collet <remi@remirepo.net> - 10.1.0-1
- update to 10.1.0

* Mon Mar  6 2023 Remi Collet <remi@remirepo.net> - 10.0.2-1
- update to 10.0.2

* Tue Feb 28 2023 Remi Collet <remi@remirepo.net> - 10.0.1-1
- update to 10.0.1
- raise dependency on nikic/php-parser 4.15

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 10.0.0-1
- update to 10.0.0
- raise depdendency on PHP 8.1
- raise dependency on phpunit/php-file-iterator 4.0
- raise dependency on phpunit/php-text-template 3.0
- raise dependency on sebastian/code-unit-reverse-lookup 3.0
- raise dependency on sebastian/complexity 3.0
- raise dependency on sebastian/environment 6.0
- raise dependency on sebastian/lines-of-code 2.0
- raise dependency on sebastian/version 4.0
- rename to php-phpunit-php-code-coverage10
- move to /usr/share/php/SebastianBergmann/CodeCoverage10

* Thu Jan 26 2023 Remi Collet <remi@remirepo.net> - 9.2.24-1
- update to 9.2.24

* Mon Jan  2 2023 Remi Collet <remi@remirepo.net> - 9.2.23-1
- update to 9.2.23

* Mon Dec 19 2022 Remi Collet <remi@remirepo.net> - 9.2.22-1
- update to 9.2.22

* Wed Dec 14 2022 Remi Collet <remi@remirepo.net> - 9.2.21-1
- update to 9.2.21

* Tue Dec 13 2022 Remi Collet <remi@remirepo.net> - 9.2.20-1
- update to 9.2.20

* Fri Nov 18 2022 Remi Collet <remi@remirepo.net> - 9.2.19-1
- update to 9.2.19

* Fri Oct 28 2022 Remi Collet <remi@remirepo.net> - 9.2.18-1
- update to 9.2.18

* Thu Sep  1 2022 Remi Collet <remi@remirepo.net> - 9.2.17-1
- update to 9.2.17

* Tue Aug 30 2022 Remi Collet <remi@remirepo.net> - 9.2.16-1
- update to 9.2.16
- raise dependency on nikic/php-parser 4.14

* Mon Mar  7 2022 Remi Collet <remi@remirepo.net> - 9.2.15-1
- update to 9.2.15

* Mon Feb 28 2022 Remi Collet <remi@remirepo.net> - 9.2.14-1
- update to 9.2.14

* Thu Feb 24 2022 Remi Collet <remi@remirepo.net> - 9.2.13-1
- update to 9.2.13

* Wed Feb 23 2022 Remi Collet <remi@remirepo.net> - 9.2.12-1
- update to 9.2.12

* Fri Feb 18 2022 Remi Collet <remi@remirepo.net> - 9.2.11-1
- update to 9.2.11

* Tue Dec  7 2021 Remi Collet <remi@remirepo.net> - 9.2.10-1
- update to 9.2.10

* Sat Nov 20 2021 Remi Collet <remi@remirepo.net> - 9.2.9-1
- update to 9.2.9

* Tue Nov  2 2021 Remi Collet <remi@remirepo.net> - 9.2.8-1
- update to 9.2.8
- raise dependency on nikic/php-parser 4.13.0

* Tue Sep 21 2021 Remi Collet <remi@remirepo.net> - 9.2.7-1
- update to 9.2.7
- raise dependency on nikic/php-parser 4.12.0

* Mon Mar 29 2021 Remi Collet <remi@remirepo.net> - 9.2.6-1
- update to 9.2.6

* Mon Nov 30 2020 Remi Collet <remi@remirepo.net> - 9.2.5-1
- update to 9.2.5
- raise dependency on sebastian/lines-of-code 1.0.3

* Fri Nov 27 2020 Remi Collet <remi@remirepo.net> - 9.2.4-1
- update to 9.2.4

* Fri Oct 30 2020 Remi Collet <remi@remirepo.net> - 9.2.3-1
- update to 9.2.3 (no change)
- raise dependency on nikic/php-parser 4.10.2

* Wed Oct 28 2020 Remi Collet <remi@remirepo.net> - 9.2.2-1
- update to 9.2.2

* Tue Oct 27 2020 Remi Collet <remi@remirepo.net> - 9.2.1-1
- update to 9.2.1

* Fri Oct  2 2020 Remi Collet <remi@remirepo.net> - 9.2.0-1
- update to 9.2.0

* Sun Sep 20 2020 Remi Collet <remi@remirepo.net> - 9.1.11-1
- update to 9.1.11

* Fri Sep 18 2020 Remi Collet <remi@remirepo.net> - 9.1.10-1
- update to 9.1.10

* Tue Sep 15 2020 Remi Collet <remi@remirepo.net> - 9.1.9-1
- update to 9.1.9

* Mon Sep  7 2020 Remi Collet <remi@remirepo.net> - 9.1.8-1
- update to 9.1.8

* Thu Sep  3 2020 Remi Collet <remi@remirepo.net> - 9.1.7-1
- update to 9.1.7

* Mon Aug 31 2020 Remi Collet <remi@remirepo.net> - 9.1.6-1
- update to 9.1.6

* Thu Aug 27 2020 Remi Collet <remi@remirepo.net> - 9.1.5-1
- update to 9.1.5

* Fri Aug 14 2020 Remi Collet <remi@remirepo.net> - 9.1.4-1
- update to 9.1.4

* Tue Aug 11 2020 Remi Collet <remi@remirepo.net> - 9.1.3-1
- update to 9.1.3
- raise dependency on nikic/php-parser 4.8

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 9.1.2-1
- update to 9.1.2

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 9.1.1-1
- update to 9.1.1
- rename to php-phpunit-php-code-coverage9
- move to /usr/share/php/SebastianBergmann/CodeCoverage9
- add dependency on nikic/php-parser 4.7
- add dependency on sebastian/complexity 2.0
- add dependency on sebastian/lines-of-code 1.0
- drop dependency on phpunit/php-token-stream
- raise dependency on phpunit/php-file-iterator 3.0.3
- raise dependency on phpunit/php-text-template 2.0.2
- raise dependency on sebastian/code-unit-reverse-lookup 2.0.2
- raise dependency on sebastian/environment 5.1.2
- raise dependency on sebastian/version 3.0.1
- raise dependency on theseer/tokenizer 1.2.0

* Sun May 24 2020 Remi Collet <remi@remirepo.net> - 8.0.2-1
- update to 8.0.2
- sources from git snapshot

* Wed Feb 19 2020 Remi Collet <remi@remirepo.net> - 8.0.1-1
- update to 8.0.1

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 8.0.0-1
- update to 8.0.0
- raise depdendency on PHP 7.3
- raise depdendency on phpunit/php-file-iterator 3
- raise depdendency on phpunit/php-token-stream 4
- raise depdendency on phpunit/php-text-template 2
- raise depdendency on sebastian/code-unit-reverse-lookup 2
- raise depdendency on sebastian/environment 5
- raise depdendency on sebastian/version 3
- rename to php-phpunit-php-code-coverage8
- move to /usr/share/php/SebastianBergmann/CodeCoverage8

* Wed Nov 20 2019 Remi Collet <remi@remirepo.net> - 7.0.10-1
- update to 7.0.10

* Wed Nov 20 2019 Remi Collet <remi@remirepo.net> - 7.0.9-1
- update to 7.0.9

* Tue Sep 17 2019 Remi Collet <remi@remirepo.net> - 7.0.8-1
- update to 7.0.8
- raise dependency on phpunit/php-token-stream 3.1.1

* Thu Jul 25 2019 Remi Collet <remi@remirepo.net> - 7.0.7-1
- update to 7.0.7 (no change)
- raise dependency on phpunit/php-token-stream 3.1.0

* Mon Jul  8 2019 Remi Collet <remi@remirepo.net> - 7.0.6-1
- update to 7.0.6
- raise dependency on phpunit/php-token-stream 3.0.2
- raise dependency on sebastian/environment 4.2.2
- raise dependency on theseer/tokenizer 1.1.3

* Thu Jun  6 2019 Remi Collet <remi@remirepo.net> - 7.0.5-1
- update to 7.0.5

* Wed May 29 2019 Remi Collet <remi@remirepo.net> - 7.0.4-1
- update to 7.0.4

* Tue Feb 26 2019 Remi Collet <remi@remirepo.net> - 7.0.3-1
- update to 7.0.3

* Sat Feb 16 2019 Remi Collet <remi@remirepo.net> - 7.0.2-1
- update to 7.0.2

* Fri Feb  1 2019 Remi Collet <remi@remirepo.net> - 7.0.1-1
- update to 7.0.1
- add weak dependency on xdebug and pcov extension

* Fri Feb  1 2019 Remi Collet <remi@remirepo.net> - 7.0.0-1
- rename to php-phpunit-php-code-coverage7
- update to 7.0.0
- raise dependency on PHP 7.2
- raise dependency on phpunit/php-file-iterator 2.0.2
- raise dependency on phpunit/php-token-stream 3.0.1
- raise dependency on sebastian/environment 4.1
- use phpunit8

* Fri Feb  1 2019 Remi Collet <remi@remirepo.net> - 7.0.0-0
- boostrap build
- rename to php-phpunit-php-code-coverage7
- update to 7.0.0
- raise dependency on PHP 7.2
- raise dependency on phpunit/php-file-iterator 2.0.2
- raise dependency on phpunit/php-token-stream 3.0.1
- raise dependency on sebastian/environment 4.1

* Wed Oct 31 2018 Remi Collet <remi@remirepo.net> - 6.1.4-1
- update to 6.1.4

* Tue Oct 23 2018 Remi Collet <remi@remirepo.net> - 6.1.3-1
- update to 6.1.3

* Thu Oct 18 2018 Remi Collet <remi@remirepo.net> - 6.1.1-1
- update to 6.1.1
- allow sebastian/environment 4

* Tue Oct 16 2018 Remi Collet <remi@remirepo.net> - 6.1.0-1
- update to 6.1.0
- drop dependency on glyphicons-halflings-fonts

* Thu Oct  4 2018 Remi Collet <remi@remirepo.net> - 6.0.8-1
- update to 6.0.8

* Fri Jun  1 2018 Remi Collet <remi@remirepo.net> - 6.0.7-1
- update to 6.0.7

* Fri Jun  1 2018 Remi Collet <remi@remirepo.net> - 6.0.6-1
- update to 6.0.6
- raise dependency on phpunit/php-file-iterator 2.0

* Mon May 28 2018 Remi Collet <remi@remirepo.net> - 6.0.5-1
- update to 6.0.5

* Wed May  2 2018 Remi Collet <remi@remirepo.net> - 6.0.4-1
- update to 6.0.4

* Mon Apr  9 2018 Remi Collet <remi@remirepo.net> - 6.0.3-1
- update to 6.0.3
- raise dependency on sebastian/environment 3.1

* Wed Feb  7 2018 Remi Collet <remi@remirepo.net> - 6.0.1-1
- normal build

* Fri Feb  2 2018 Remi Collet <remi@remirepo.net> - 6.0.1-1
- Update to 6.0.1
- rename to php-phpunit-php-code-coverage6
- move to /usr/share/php/SebastianBergmann/CodeCoverage6
- raise dependency on PHP 7.1
- raise dependency on phpunit/php-token-stream 3.0
- use range dependencies on F27+
- use phpunit7
- use full path instead of relying on include_path
- bootstrap build

* Thu Dec  7 2017 Remi Collet <remi@remirepo.net> - 5.3.0-1
- Update to 5.3.0

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 5.2.4-1
- Update to 5.2.4
- raise dependency on phpunit/php-token-stream 2.0.1

* Mon Nov  6 2017 Remi Collet <remi@remirepo.net> - 5.2.3-1
- Update to 5.2.3
- raise dependency on phpunit/php-token-stream 2.0

* Fri Nov  3 2017 Remi Collet <remi@remirepo.net> - 5.2.2-3
- fix FTBFS from Koschei, add patch for PHP 7.2 from
  https://github.com/sebastianbergmann/php-code-coverage/pull/554
- ignore test failing, know by upstream (travis)

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 5.2.2-2
- allow phpunit/php-token-stream v2

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 5.2.2-1
- Update to 5.2.2
- raise dependency on phpunit/php-file-iterator 1.4.2
- raise dependency on phpunit/php-text-template 1.2.1
- raise dependency on sebastian/code-unit-reverse-lookup 1.0.1
- raise dependency on sebastian/version 2.0.1

* Sun Apr 23 2017 Remi Collet <remi@remirepo.net> - 5.2.1-1
- Update to 5.2.1
- raise dependency on sebastian/environment >= 3.0
- add dependency on theseer/tokenizer

* Wed Apr 12 2017 Remi Collet <remi@remirepo.net> - 5.1.1-1
- Update to 5.1.1

* Fri Apr  7 2017 Remi Collet <remi@remirepo.net> - 5.1.0-1
- Update to 5.1.0

* Sun Apr  2 2017 Remi Collet <remi@remirepo.net> - 5.0.4-1
- Update to 5.0.4
- use fedora2 autoloader template

* Mon Mar  6 2017 Remi Collet <remi@remirepo.net> - 5.0.3-1
- Update to 5.0.3

* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 5.0.2-2
- handle bundle assets
- fix license tag for bundled assets
- add dependency on glyphicons-halflings-fonts

* Wed Mar  1 2017 Remi Collet <remi@remirepo.net> - 5.0.2-1
- update to 5.0.2
- raise dependency on phpunit/php-token-stream 1.4.11

* Thu Feb 23 2017 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Tue Feb  7 2017 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- rename to php-phpunit-php-code-coverage5
- move to /usr/share/php/SebastianBergmann/CodeCoverage5

* Sun Jan 22 2017 Remi Collet <remi@fedoraproject.org> - 4.0.5-2
- Update to 4.0.5
- add upstream patch for test suite to fix
  https://github.com/sebastianbergmann/php-code-coverage/issues/495
- open https://github.com/sebastianbergmann/php-code-coverage/pull/504

* Fri Jan 20 2017 Remi Collet <remi@fedoraproject.org> - 4.0.5-1
- Update to 4.0.5

* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 4.0.4-1
- Update to 4.0.4
- ignore test suite for now
  https://github.com/sebastianbergmann/php-code-coverage/issues/495

* Mon Nov 28 2016 Remi Collet <remi@fedoraproject.org> - 4.0.3-1
- Update to 4.0.3

* Wed Nov 23 2016 Remi Collet <remi@fedoraproject.org> - 4.0.2-2
- set serialize_precision=14 for the test suite
  to fix FTBFS with PHP 7.1

* Tue Nov  1 2016 Remi Collet <remi@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2
- switch to fedora-autoloader

* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0
- namespace changed from PHP to SebastianBergmann
- raise build dependency on phpunit >= 5.4

* Sat May 28 2016 Remi Collet <remi@fedoraproject.org> - 3.3.3-1
- Update to 3.3.3

* Wed May 25 2016 Remi Collet <remi@fedoraproject.org> - 3.3.2-1
- Update to 3.3.2

* Wed May  4 2016 Remi Collet <remi@fedoraproject.org> - 3.3.1-2
- add upstream patch for environment 1.3.6
  https://github.com/sebastianbergmann/php-code-coverage/pull/435

* Fri Apr  8 2016 Remi Collet <remi@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 3.3.0-1
- Update to 3.3.0

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1
- raise dependency on php-token-stream >= 1.4.2

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0
- add dependency on sebastian/code-unit-reverse-lookup

* Thu Feb  4 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1
- allow sebastian/version ~2.0
- drop autoloader template

* Mon Jan 11 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Fri Nov 13 2015 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2
- run test suite with both PHP 5 and 7 when available

* Wed Oct  7 2015 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0
- Update to 3.0.0, boostrap build

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.1.20150924git12259bb
- rebuild (not boostrap)

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.0.20150924git12259bb
- update to 3.0.0-dev
- raise dependency on PHP >= 5.6
- bootstrap build

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- update to 2.2.3

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2
- raise dependency on sebastian/environment ^1.3.2

* Sun Aug  2 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1 (no change)
- raise dependency on sebastian/environment ~1.3.1

* Sat Aug  1 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0
- raise dependency on sebastian/environment ~1.3

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 2.1.9-1
- update to 2.1.9 (only cleanup)

* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 2.1.8-1
- update to 2.1.8

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 2.1.7-2
- fix autoloader

* Tue Jun 30 2015 Remi Collet <remi@fedoraproject.org> - 2.1.7-1
- update to 2.1.7

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 2.1.6-1
- update to 2.1.6

* Tue Jun  9 2015 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- update to 2.1.5

* Sun Jun  7 2015 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- update to 2.1.4

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- update to 2.1.3

* Mon Jun  1 2015 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- update to 2.1.2

* Sun May 31 2015 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- update to 2.1.1

* Mon May 25 2015 Remi Collet <remi@fedoraproject.org> - 2.0.17-1
- update to 2.0.17

* Mon Apr 13 2015 Remi Collet <remi@fedoraproject.org> - 2.0.16-1
- update to 2.0.16

* Sun Jan 25 2015 Remi Collet <remi@fedoraproject.org> - 2.0.15-1
- update to 2.0.15

* Fri Dec 26 2014 Remi Collet <remi@fedoraproject.org> - 2.0.14-1
- update to 2.0.14

* Wed Dec  3 2014 Remi Collet <remi@fedoraproject.org> - 2.0.13-1
- update to 2.0.13

* Tue Dec  2 2014 Remi Collet <remi@fedoraproject.org> - 2.0.12-1
- update to 2.0.12

* Thu Sep  4 2014 Remi Collet <remi@fedoraproject.org> - 2.0.11-2
- add BR on php-pecl-xdebug (thanks to Koschei)

* Sun Aug 31 2014 Remi Collet <remi@fedoraproject.org> - 2.0.11-1
- update to 2.0.11
- raise dependency on phpunit/php-token-stream ~1.3
- enable tests during build
- drop optional dependency on XDebug

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 2.0.10-1
- update to 2.0.10
- fix license handling

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 2.0.9-1
- update to 2.0.9

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 2.0.8-3
- composer dependencies

* Tue May 27 2014 Remi Collet <remi@fedoraproject.org> - 2.0.8-1
- update to 2.0.8

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- update to 2.0.6

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-2
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- update to 2.0.5
- sources from github

* Tue Apr 01 2014 Remi Collet <remi@fedoraproject.org> - 1.2.17-1
- Update to 1.2.17

* Tue Feb 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.16-1
- Update to 1.2.16

* Mon Feb 03 2014 Remi Collet <remi@fedoraproject.org> - 1.2.15-1
- Update to 1.2.15

* Fri Jan 31 2014 Remi Collet <remi@fedoraproject.org> - 1.2.14-1
- Update to 1.2.14
- raise dependency on Text_Template 1.2.0

* Tue Sep 10 2013 Remi Collet <remi@fedoraproject.org> - 1.2.13-1
- Update to 1.2.13

* Mon Jul 08 2013 Remi Collet <remi@fedoraproject.org> - 1.2.12-1
- Update to 1.2.12

* Fri May 24 2013 Remi Collet <remi@fedoraproject.org> - 1.2.11-1
- Update to 1.2.11

* Mon May 13 2013 Remi Collet <remi@fedoraproject.org> - 1.2.10-1
- Update to 1.2.10

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 1.2.9-1
- Update to 1.2.9

* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8

* Sun Dec  2 2012 Remi Collet <remi@fedoraproject.org> - 1.2.7-1
- Version 1.2.7 (stable) - API 1.2.0 (stable)

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 1.2.6-1
- Version 1.2.6 (stable) - API 1.2.0 (stable)

* Sun Oct  7 2012 Remi Collet <remi@fedoraproject.org> - 1.2.5-1
- Version 1.2.5 (stable) - API 1.2.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Version 1.2.3 (stable) - API 1.2.0 (stable)

* Fri Sep 21 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Version 1.2.2 (stable) - API 1.2.0 (stable)

* Thu Sep 20 2012 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Version 1.2.1 (stable) - API 1.2.0 (stable)
- raise dependency: php 5.3.3, PHP_TokenStream 1.1.3

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Version 1.1.3 (stable) - API 1.1.0 (stable)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Version 1.1.2 (stable) - API 1.1.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 04 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)
- no more phpcov script in bindir

* Fri Aug 19 2011 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Version 1.0.5 (stable) - API 1.0.3 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.4-2
- rebuild for doc in /usr/share/doc/pear

* Wed Feb 16 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.4-1
- Version 1.0.4 (stable) - API 1.0.3 (stable)
- LICENSE CHANGELOG now provided by upstream

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.3 (stable)

* Wed Nov 17 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)

* Thu Nov 04 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1.1
- lower PEAR dependency to allow f13 and el6 build
- fix URL

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean

