# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/Fedora spec file for php-webmozart-assert
#
# Copyright (c) 2020-2025 Remi Collet
# Copyright (c) 2016-2020 Shawn Iwinski
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

# enable bootstrap when need to provide a new autoloader
%global bootstrap 0
%global github_owner     webmozart
%global github_name      assert
%global github_version   2.1.5
%global github_commit    79155f94852fa27e2f73b459f6503f5e87e2c188
%global github_short     %(c=%{github_commit}; echo ${c:0:7})
%global major            2

%global composer_vendor  webmozart
%global composer_project assert

# "php": "^8.2"
%global php_min_ver 8.2

# PHPUnit
%global phpunit_require phpunit11
%global phpunit_exec    phpunit11

%if %{bootstrap}
# Build using "--with tests" to enable tests
%global with_tests 0%{?_with_tests:1}
%else
# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}
%endif

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}%{major}
Version:       %{github_version}
Release: 2%{?github_release}%{?dist}
Summary:       Assertions to validate method input/output with nice error messages

License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}

# GitHub export does not include tests.
# Run php-webmozart-assert-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_short}.tar.gz
Source1:       %{name}-get-source.sh

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-ctype
BuildRequires: %{phpunit_require}
## phpcompatinfo (computed from version 1.7.0)
BuildRequires: php-mbstring
BuildRequires: php-simplexml
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-ctype
# phpcompatinfo (computed from version 1.7.0)
Requires:      php-mbstring
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This library contains efficient assertions to test the input and output of your
methods. With these assertions, you can greatly reduce the amount of coding
needed to write a safe implementation.

All assertions in the Assert class throw an \InvalidArgumentException if they
fail.

Autoloader: %{phpdir}/Webmozart/Assert%{major}/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Webmozart\\Assert\\', __DIR__);
AUTOLOAD


%install
mkdir -p %{buildroot}%{phpdir}/Webmozart
cp -rp src %{buildroot}%{phpdir}/Webmozart/Assert%{major}


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
\Fedora\Autoloader\Autoload::addPsr4('Webmozart\\Assert\\Tests\\', __DIR__.'/tests');
\Fedora\Autoloader\Autoload::addPsr4('Webmozart\\Assert\\Bin\\', __DIR__.'/bin/src');
BOOTSTRAP

: Upstream tests
RETURN_CODE=0
PHPUNIT=$(which %{phpunit_exec})
for PHP_EXEC in php82 php83 php84 php85; do
    if [ -z "$PHP_EXEC" ] || which $PHP_EXEC; then
        $PHP_EXEC \
            -d auto_prepend_file=%{buildroot}%{phpdir}/Webmozart/Assert%{major}/autoload.php \
            $PHPUNIT \
                --bootstrap bootstrap.php \
                || RETURN_CODE=1
    fi
done
exit $RETURN_CODE
%else
: Tests skipped
%endif


%files
%license LICENSE
%doc *.md
%doc composer.json
%dir %{phpdir}/Webmozart
     %{phpdir}/Webmozart/Assert%{major}


%changelog
* Thu Feb 19 2026 Remi Collet <remi@remirepo.net> - 2.1.5-1
- update to 2.1.5

* Tue Feb 17 2026 Remi Collet <remi@remirepo.net> - 2.1.4-1
- update to 2.1.4

* Sat Feb 14 2026 Remi Collet <remi@remirepo.net> - 2.1.3-1
- update to 2.1.3

* Tue Jan 13 2026 Remi Collet <remi@remirepo.net> - 2.1.2-1
- update to 2.1.2

* Thu Jan  8 2026 Remi Collet <remi@remirepo.net> - 2.1.1-1
- update to 2.1.1

* Thu Dec 25 2025 Remi Collet <remi@remirepo.net> - 2.0.0-1
- update to 2.0.0
- rename to php-webmozart-assert2
- install in /usr/share/php/Webmozart/Assert2
- raise dependency on PHP 8.2

* Thu Oct 30 2025 Remi Collet <remi@remirepo.net> - 1.12.1-1
- update to 1.12.1 (no change)

* Tue Oct 21 2025 Remi Collet <remi@remirepo.net> - 1.12.0-1
- update to 1.12.0

* Mon Aug  8 2022 Remi Collet <remi@remirepo.net> - 1.11.0-1
- update to 1.11.0
- raise dependency on PHP 7.2
- switch to phpunit8

* Fri Sep 24 2021 Remi Collet <remi@remirepo.net> - 1.10.0-1
- update to 1.10.0

* Tue Jul 21 2020 Remi Collet <remi@remirepo.net> - 1.9.1-1
- update to 1.9.1

* Sun Feb 23 2020 Shawn Iwinski <shawn@iwin.ski> - 1.7.0-1
- Update to 1.7.0 (RHBZ #1746998)
- Disable bootstrap so tests run by default
- Conditionally use PHPUnit 7

* Sun May 19 2019 Shawn Iwinski <shawn@iwin.ski> - 1.4.0-1
- Update to 1.4.0

* Fri Oct 19 2018 Remi Collet <remi@remirepo.net> - 1.3.0-3
- fix autoloader, use PSR-4 to avoid duplicated definition
- prepend autoloader to ensure we use current version in tests
- fix FTBFS #1605449

* Fri Oct 19 2018 Remi Collet <remi@remirepo.net> - 1.3.0-2
- fix autoloader, use PSR-4 to avoid duplicated definition
- prepend autoloader to ensure we use current version in tests
- fix FTBFS #1605449
- bootstrap build

* Sun Apr 22 2018 Shawn Iwinski <shawn@iwin.ski> - 1.3.0-1
- Update to 1.3.0 (RHBZ #1539946)
- Add get source script
- Add composer.json to repo
- Update running of tests

* Tue Dec 27 2016 Shawn Iwinski <shawn@iwin.ski> - 1.2.0-1
- Update to 1.2.0 (RHBZ #1398043)
- Use php-composer(fedora/autoloader)
- Run upstream tests with SCLs if they are available

* Thu Oct  6 2016 Remi Collet <remi@remirepo.net> - 1.1.0-1
- backport for remi repo, add EL-5 stuff

* Wed Sep 28 2016 Shawn Iwinski <shawn@iwin.ski> - 1.1.0-1
- Initial package
