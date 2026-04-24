# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-zetacomponents-console-tools
#
# Copyright (c) 2015-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    de081f422b574d638e62e15661bf833d80fac61a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zetacomponents
%global gh_project   ConsoleTools
%global cname        console-tools
%global ezcdir       %{_datadir}/php/ezc

%if 0%{?fedora}
%bcond_without  tests
%else
%bcond_with     tests
%endif
%bcond_without  phpab

Name:           php-%{gh_owner}-%{cname}
Version:        1.7.5
Release: 4%{?dist}
Summary:        Zeta %{gh_project} Component

License:        Apache-2.0
URL:            http://zetacomponents.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz
Source1:        autoloader.php

BuildArch:      noarch
%if %{with phpab}
BuildRequires:  %{_bindir}/phpab
%endif
%if %{with tests}
BuildRequires: (php-composer(%{gh_owner}/base) >= 1.8   with php-composer(%{gh_owner}/base) < 2)
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~9.0",
#        "zetacomponents/unit-test": "*"
BuildRequires:  phpunit9
BuildRequires:  php-composer(%{gh_owner}/unit-test) >= 1.2.4
%endif

# From composer.json, "require": {
#            "zetacomponents/base": "~1.8"
Requires:      (php-composer(%{gh_owner}/base) >= 1.8   with php-composer(%{gh_owner}/base) < 2)
# From phpcompatinfo report for 1.7
Requires:       php(language) > 5.3
Requires:       php-iconv
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{cname}) = %{version}


%description
A set of classes to do different actions with the console, also called shell.
It can render a progress bar, tables and a status bar and contains a class for
parsing command line options.

Documentation is available in the %{name}-doc package.


%package doc
Summary:  Documentation for %{name}
Group:    Documentation
# For License
Requires: %{name} = %{version}-%{release}

%description doc
%{summary}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
%if %{with phpab}
: Generate a simple autoloader
%{_bindir}/phpab \
   --output src/autoloader.php \
   src
cat <<EOF | tee -a  src/autoloader.php
# Dependencies
require_once '%{ezcdir}/Base/autoloader.php';
EOF
%else
cp %{SOURCE1} src/autoloader.php
%endif


%install
mkdir -p %{buildroot}%{ezcdir}/autoload

: The library
cp -pr src \
       %{buildroot}%{ezcdir}/%{gh_project}
: For ezcBase autoloader
cp -pr src/*_autoload.php \
       %{buildroot}%{ezcdir}/autoload


%check
%if %{with tests}
: Create test autoloader
mkdir vendor
cat <<EOF | tee vendor/autoload.php
<?php
require '%{ezcdir}/UnitTest/autoloader.php';
require '%{buildroot}%{ezcdir}/%{gh_project}/autoloader.php';
EOF

: Drop assertion which rely on path in sources dir
sed -e '/realpath/d' -i tests/statusbar_test.php


: Run test test suite
for cmd in php php81 php82 php83 php84
do
  if which $cmd;
  then
    $cmd %{_bindir}/phpunit9 --exclude-group interactive
  fi
done
%else
: Test suite disabled
%endif


%files
%license LICENSE* CREDITS
%doc ChangeLog
%doc composer.json
%{ezcdir}/autoload/*
%{ezcdir}/%{gh_project}

%files doc
%doc docs design


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct  7 2024 Remi Collet <remi@remirepo.net> - 1.7.5-1
- update to 1.7.5

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 31 2024 Remi Collet <remi@remirepo.net> - 1.7.4-1
- update to 1.7.4
- drop patch merged upstream

* Wed Jan 31 2024 Remi Collet <remi@remirepo.net> - 1.7.3-8
- add upstream patch for PHP 8.2
- add patch for PHP 8.3 from https://github.com/zetacomponents/ConsoleTools/pull/26
- fix FTBFS #2261516

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Remi Collet <remi@remirepo.net> - 1.7.3-3
- switch to phpunit9

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Remi Collet <remi@remirepo.net> - 1.7.3-1
- update to 1.7.3

* Mon Dec  6 2021 Remi Collet <remi@remirepo.net> - 1.7.2-4
- disable test suite on EL
- add autoloader from sources on EL

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 30 2020 Remi Collet <remi@remirepo.net> - 1.7.2-1
- update to 1.7.2
- switch to phpunit7

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 16 2020 Remi Collet <remi@remirepo.net> - 1.7.1-1
- update to 1.7.1
- use range dependencies
- drop patches, merged upstream

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 1.7-3
- create subpackage for documentation
- minor improvments, from review #1228091 comments

* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.7-2
- fix summary

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 1.7-1
- initial package
- open https://github.com/zetacomponents/ConsoleTools/pull/8 interactive
