# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-phpspec-prophecy
#
# SPDX-FileCopyrightText:  Copyright 2015-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#
%global gh_commit    7ab965042096282307992f1b9abff020095757f0
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpspec
%global gh_project   prophecy

%bcond_without       tests
%bcond_with          phpspec

Name:           php-phpspec-prophecy
Version:        1.25.0
Release:        1%{?dist}
Summary:        Highly opinionated mocking framework for PHP

License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source2:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.2
%if %{with tests}
BuildRequires:  (php-composer(phpdocumentor/reflection-docblock) >= 5.2   with php-composer(phpdocumentor/reflection-docblock) < 6)
BuildRequires:  (php-composer(sebastian/comparator)              >= 3.0   with php-composer(sebastian/comparator)              < 9)
BuildRequires:  (php-composer(sebastian/recursion-context)       >= 3.0   with php-composer(sebastian/recursion-context)       < 9)
BuildRequires:  (php-composer(doctrine/instantiator)             >= 1.2   with php-composer(doctrine/instantiator)             < 3)
# from composer.json, "require-dev": {
#        "php-cs-fixer/shim": "^3.93.1",
#        "phpspec/phpspec": "^6.0 || ^7.0 || ^8.0",
#        "phpstan/phpstan": "^2.1.13, <2.1.34 || ^2.1.39",
#        "phpunit/phpunit": "^11.0 || ^12.0 || ^13.0"
%if %{with phpspec}
BuildRequires:  php-composer(phpspec/phpspec) >= 6.0
%endif
BuildRequires:  phpunit11
BuildRequires:  phpunit12
BuildRequires:  phpunit13
%endif
# Autoloader
BuildRequires:  php-fedora-autoloader-devel

# from composer.json, "requires": {
#        "php":                               "8.2.* || 8.3.* || 8.4.*",
#        "phpdocumentor/reflection-docblock": "^5.2",
#        "sebastian/comparator":              "^3.0 || ^4.0 || ^5.0 || ^6.0 || ^7.0 || ^8.0",
#        "doctrine/instantiator":             "^1.2 || ^2.0",
#        "sebastian/recursion-context":       "^3.0 || ^4.0 || ^5.0 || ^6.0 || ^7.0 || ^8.0",
#        "symfony/deprecation-contracts":     "^2.5 || ^3.1"
Requires:       php(language) >= 8.2
Requires:       (php-composer(phpdocumentor/reflection-docblock) >= 5.2   with php-composer(phpdocumentor/reflection-docblock) < 6)
Requires:       (php-composer(sebastian/comparator)              >= 3.0   with php-composer(sebastian/comparator)              < 9)
Requires:       (php-composer(sebastian/recursion-context)       >= 3.0   with php-composer(sebastian/recursion-context)       < 9)
Requires:       (php-composer(doctrine/instantiator)             >= 1.2   with php-composer(doctrine/instantiator)             < 3)
# From phpcompatinfo report for version 1.11.0
# only pcre, reflection and spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(phpspec/prophecy) = %{version}


%description
Prophecy is a highly opinionated yet very powerful and flexible PHP object
mocking framework.

Though initially it was created to fulfil phpspec2 needs, it is flexible enough
to be used inside any testing framework out there with minimal effort.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
phpab --template fedora --output src/Prophecy/autoload.php src
cat << 'EOF' | tee -a src/Prophecy/autoload.php

if (PHP_VERSION_ID > 80400) {
	$inst = [
        '%{_datadir}/php/Doctrine/Instantiator2/autoload.php',
        '%{_datadir}/php/Doctrine/Instantiator/autoload.php',
    ];
} else {
	$inst = '%{_datadir}/php/Doctrine/Instantiator/autoload.php';
}
\Fedora\Autoloader\Dependencies::required([
    $inst,
    '%{_datadir}/php/phpDocumentor/Reflection/DocBlock5/autoload.php',
]);
if (!class_exists('SebastianBergmann\\Comparator\\Comparator')) { // v2 from phpunit, v1 from phpspec
	$inst = [
        '%{_datadir}/php/SebastianBergmann/Comparator6/autoload.php',
        '%{_datadir}/php/SebastianBergmann/Comparator5/autoload.php',
        '%{_datadir}/php/SebastianBergmann/Comparator4/autoload.php',
        '%{_datadir}/php/SebastianBergmann/Comparator3/autoload.php',
	];
	if (PHP_VERSION_ID > 80300) {
		array_unshift($inst, '%{_datadir}/php/SebastianBergmann/Comparator7/autoload.php');
	}
	if (PHP_VERSION_ID > 80400) {
		array_unshift($inst, '%{_datadir}/php/SebastianBergmann/Comparator8/autoload.php');
	}
    \Fedora\Autoloader\Dependencies::required([$inst]);
}
if (!class_exists('SebastianBergmann\\RecursionContext\\Context')) { // v2 from phpunit, v1 from phpspec
    $inst = [
            '%{_datadir}/php/SebastianBergmann/RecursionContext6/autoload.php',
            '%{_datadir}/php/SebastianBergmann/RecursionContext5/autoload.php',
            '%{_datadir}/php/SebastianBergmann/RecursionContext4/autoload.php',
            '%{_datadir}/php/SebastianBergmann/RecursionContext3/autoload.php',
    ];
	if (PHP_VERSION_ID > 80300) {
		array_unshift($inst, '%{_datadir}/php/SebastianBergmann/RecursionContext7/autoload.php');
	}
	if (PHP_VERSION_ID > 80400) {
		array_unshift($inst, '%{_datadir}/php/SebastianBergmann/RecursionContext8/autoload.php');
	}
    \Fedora\Autoloader\Dependencies::required([$inst]);
}
// from https://github.com/symfony/deprecation-contracts
if (!function_exists('trigger_deprecation')) {
    function trigger_deprecation(string $package, string $version, string $message, mixed ...$args): void
    {
        @trigger_error(($package || $version ? "Since $package $version: " : '').($args ? vsprintf($message, $args) : $message), \E_USER_DEPRECATED);
    }
}
EOF


%install
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php


%check
%if %{with tests}
: Dev autoloader
mkdir vendor
phpab --output vendor/autoload.php fixtures tests

cat << 'EOF' | tee -a vendor/autoload.php
require_once '%{buildroot}%{_datadir}/php/Prophecy/autoload.php';
EOF

: check autoloader
php %{buildroot}%{_datadir}/php/Prophecy/autoload.php

%if %{with phpspec}
: check phpspec
phpspec --version
%endif

ret=0
for cmd in php php82 php83 php84 php85; do
  if which $cmd; then
    $cmd -d auto_prepend_file=vendor/autoload.php \
       %{_bindir}/phpunit11 \
         || ret=1
  fi
done
if [ -x %{_bindir}/phpunit12 ]; then
for cmd in php php83 php84 php85; do
  if which $cmd; then
    $cmd -d auto_prepend_file=vendor/autoload.php \
       %{_bindir}/phpunit12 \
         || ret=1
  fi
done
fi
if [ -x %{_bindir}/phpunit13 ]; then
for cmd in php php84 php85; do
  if which $cmd; then
    $cmd -d auto_prepend_file=vendor/autoload.php \
       %{_bindir}/phpunit13 \
         || ret=1
  fi
done
fi
exit $ret
%else
: Test suite disabled
%endif


%files
%license LICENSE
%doc *.md
%doc composer.json
%{_datadir}/php/Prophecy


%changelog
* Tue Feb 10 2026 Remi Collet <remi@remirepo.net> - 1.25.0-1
- update to 1.25.0
- allow phpunit13

* Mon Jan 12 2026 Remi Collet <remi@remirepo.net> - 1.24.0-2
- update to 1.24.0
- use doctrine/instantiator v2 only with PHP 8.4+
- raise dependency on PHP 8.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Apr 30 2025 Remi Collet <remi@remirepo.net> - 1.22.0-1
- update to 1.22.0
- re-license spec file to CECILL-2.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 21 2024 Remi Collet <remi@remirepo.net> - 1.20.0-1
- update to 1.20.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 29 2024 Remi Collet <remi@remirepo.net> - 1.19.0-1
- update to 1.19.0
- allow doctrine/instantiator 6
- allow sebastian/recursion-context 6

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec  8 2023 Remi Collet <remi@remirepo.net> - 1.18.0-1
- update to 1.18.0
- run test suite with phpunit8, phpunit9 and phpunit10

* Wed Sep 27 2023 Remi Collet <remi@remirepo.net> - 1.17.0-4
- disable phpspec tests

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 1.17.0-2
- fix autoloader

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 1.17.0-1
- update to 1.17.0
- allow doctrine/instantiator v2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec  1 2022 Remi Collet <remi@remirepo.net> - 1.16.0-1
- update to 1.16.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec  8 2021 Remi Collet <remi@remirepo.net> - 1.15.0-1
- update to 1.15.0

* Fri Sep 10 2021 Remi Collet <remi@remirepo.net> - 1.14.0-1
- update to 1.14.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 18 2021 Remi Collet <remi@remirepo.net> - 1.13.0-1
- update to 1.13.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 21 2020 Remi Collet <remi@remirepo.net> - 1.12.2-1
- update to 1.12.2
- switch to phpunit9

* Tue Sep 29 2020 Remi Collet <remi@remirepo.net> - 1.12.1-1
- update to 1.12.1

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 1.12.0-2
- switch to classmap autoloader

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 1.12.0-1
- update to 1.12.0
- raise dependency on phpdocumentor/reflection-docblock 5.2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul  8 2020 Remi Collet <remi@remirepo.net> - 1.11.1-1
- update to 1.11.1

* Wed Jul  8 2020 Remi Collet <remi@remirepo.net> - 1.11.0-1
- update to 1.11.0
- raise dependency on PHP 7.2
- raise dependency on phpdocumentor/reflection-docblock 5.0
- raise dependency on sebastian/comparator 3.0
- raise dependency on doctrine/instantiator 1.2
- raise dependency on sebastian/recursion-context 3.0

* Fri Mar  6 2020 Remi Collet <remi@remirepo.net> - 1.10.3-1
- update to 1.10.3
- allow phpdocumentor/reflection-docblock 5.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Remi Collet <remi@remirepo.net> - 1.10.2-1
- update to 1.10.2
- allow sebastian/comparator 4 and sebastian/recursion-context 4

* Fri Jan  3 2020 Remi Collet <remi@remirepo.net> - 1.10.1-1
- update to 1.10.1

* Fri Oct  4 2019 Remi Collet <remi@remirepo.net> - 1.9.0-1
- update to 1.9.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 13 2019 Remi Collet <remi@remirepo.net> - 1.8.1-1
- update to 1.8.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 20 2018 Remi Collet <remi@remirepo.net> - 1.8.0-1
- update to 1.8.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 19 2018 Remi Collet <remi@remirepo.net> - 1.7.6-1
- update to 1.7.6

* Tue Feb 20 2018 Remi Collet <remi@remirepo.net> - 1.7.5-1
- Update to 1.7.5

* Mon Feb 12 2018 Remi Collet <remi@remirepo.net> - 1.7.4-1
- Update to 1.7.4
- use range dependency on F27+

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 27 2017 Remi Collet <remi@remirepo.net> - 1.7.3-1
- Update to 1.7.3

* Tue Sep  5 2017 Remi Collet <remi@remirepo.net> - 1.7.2-1
- Update to 1.7.2

* Mon Sep  4 2017 Remi Collet <remi@remirepo.net> - 1.7.1-1
- Update to 1.7.1
- use git snapshot for sources
- skip test with phpspec v4

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 13 2017 Shawn Iwinski <shawn@iwin.ski> - 1.7.0-4
- Prepare for php-phpdocumentor-reflection-docblock =>
  php-phpdocumentor-reflection-docblock2 dependency rename
- Update autoloader to try loading newest
  php-composer(phpdocumentor/reflection-docblock), then try loading older v2,
  then trigger an error if neither are found in include path

* Sat Mar  4 2017 Remi Collet <remi@remirepo.net> - 1.7.0-3
- drop implicit dependency on sebastian/recursion-context

* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 1.7.0-2
- fix autoloader for dep. with multiple versions

* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 1.7.0-1
- Update to 1.7.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- update to 1.6.2
- allow sebastian/recursion-context 2.0
- switch to fedora/autoloader

* Tue Jun  7 2016 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- update to 1.6.1

* Mon Feb 15 2016 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0
- add dependency on sebastian/recursion-context
- run test suite with both PHP 5 and 7 when available
- ignore 1 failed spec with PHP 7
  open https://github.com/phpspec/prophecy/issues/258

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 28 2015 Remi Collet <remi@fedoraproject.org> - 1.5.0-2
- fix autolaoder, rely on include_path for symfony/class-loader

* Thu Aug 13 2015 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-4
- use symfony/class-loader
- enable test suite

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May  5 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-2
- enable test suite

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Sun Mar 29 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0
- add dependency on sebastian/comparator

* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- initial package
