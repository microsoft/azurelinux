# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for phpunit11
#
# SPDX-FileCopyrightText:  Copyright 2010-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#


%bcond_without       tests

%if 0%{?fedora} == 41
%bcond_without       defcmd
%else
%bcond_with          defcmd
%endif

%global gh_commit    adc7262fccc12de2b30f12a8aa0b33775d814f00
%global gh_date      2026-02-18
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpunit
# Packagist
%global pk_vendor    phpunit
%global pk_project   phpunit
# Namespace
%global ns_vendor    PHPUnit11
%global php_home     %{_datadir}/php
%global ver_major    11
%global ver_minor    5

%global upstream_version 11.5.55
#global upstream_prever  dev

Name:           %{pk_project}%{ver_major}
Version:        %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:        1%{?dist}
Summary:        The PHP Unit Testing framework version %{ver_major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{upstream_version}-%{gh_short}.tgz
Source1:        makesrc.sh

# Fix command for autoload
Patch0:         %{name}-rpm.patch

BuildArch:      noarch
BuildRequires:  php(language) >= 8.2
BuildRequires:  (php-composer(myclabs/deep-copy) >= 1.13.4            with php-composer(myclabs/deep-copy) <  2)
BuildRequires:  (php-composer(phar-io/manifest) >= 2.0.4              with php-composer(phar-io/manifest) < 3)
BuildRequires:  (php-composer(phar-io/version) >= 3.2.1               with php-composer(phar-io/version) <  4)
BuildRequires:  (php-composer(phpunit/php-code-coverage) >= 11.0.12   with php-composer(phpunit/php-code-coverage) < 12)
BuildRequires:  (php-composer(phpunit/php-file-iterator) >= 5.1.1     with php-composer(phpunit/php-file-iterator) < 6)
BuildRequires:  (php-composer(phpunit/php-invoker) >= 5.0.1           with php-composer(phpunit/php-invoker) < 6)
BuildRequires:  (php-composer(phpunit/php-text-template) >= 4.0.1     with php-composer(phpunit/php-text-template) < 5)
BuildRequires:  (php-composer(phpunit/php-timer) >= 7.0.1             with php-composer(phpunit/php-timer) < 8)
BuildRequires:  (php-composer(sebastian/cli-parser) >= 3.0.2          with php-composer(sebastian/cli-parser) < 4)
BuildRequires:  (php-composer(sebastian/code-unit) >= 3.0.3           with php-composer(sebastian/code-unit) < 4)
BuildRequires:  (php-composer(sebastian/comparator) >= 6.3.3          with php-composer(sebastian/comparator) < 7)
BuildRequires:  (php-composer(sebastian/diff) >= 6.0.2                with php-composer(sebastian/diff) < 7)
BuildRequires:  (php-composer(sebastian/environment) >= 7.2.1         with php-composer(sebastian/environment) < 8)
BuildRequires:  (php-composer(sebastian/exporter) >= 6.3.2            with php-composer(sebastian/exporter) < 7)
BuildRequires:  (php-composer(sebastian/global-state) >= 7.0.2        with php-composer(sebastian/global-state) < 8)
BuildRequires:  (php-composer(sebastian/object-enumerator) >= 6.0.1   with php-composer(sebastian/object-enumerator) < 7)
BuildRequires:  (php-composer(sebastian/recursion-context) >= 6.0.3   with php-composer(sebastian/recursion-context) < 7)
BuildRequires:  (php-composer(sebastian/type) >= 5.1.3                with php-composer(sebastian/type) < 6)
BuildRequires:  (php-composer(sebastian/version) >= 5.0.2             with php-composer(sebastian/version) < 6)
BuildRequires:  (php-composer(staabm/side-effects-detector) >= 1.0.5  with php-composer(staabm/side-effects-detector) < 2)
BuildRequires:  php-dom
BuildRequires:  php-json
BuildRequires:  php-mbstring
BuildRequires:  php-xml
BuildRequires:  php-libxml
BuildRequires:  php-xmlwriter
# Autoloader
BuildRequires:  php-fedora-autoloader-devel >= 1.0.0

# From composer.json, "require": {
#        "php": ">=8.2",
#        "ext-dom": "*",
#        "ext-json": "*",
#        "ext-libxml": "*",
#        "ext-mbstring": "*",
#        "ext-xml": "*",
#        "ext-xmlwriter": "*",
#        "myclabs/deep-copy": "^1.13.4",
#        "phar-io/manifest": "^2.0.4",
#        "phar-io/version": "^3.2.1",
#        "phpunit/php-code-coverage": "^11.0.12",
#        "phpunit/php-file-iterator": "^5.1.1",
#        "phpunit/php-invoker": "^5.0.1",
#        "phpunit/php-text-template": "^4.0.1",
#        "phpunit/php-timer": "^7.0.1",
#        "sebastian/cli-parser": "^3.0.2",
#        "sebastian/code-unit": "^3.0.3",
#        "sebastian/comparator": "^6.3.3",
#        "sebastian/diff": "^6.0.2",
#        "sebastian/environment": "^7.2.1",
#        "sebastian/exporter": "^6.3.2",
#        "sebastian/global-state": "^7.0.2",
#        "sebastian/object-enumerator": "^6.0.1",
#        "sebastian/recursion-context": "^6.0.3",
#        "sebastian/type": "^5.1.3",
#        "sebastian/version": "^5.0.2",
#        "staabm/side-effects-detector": "^1.0.5"
Requires:       php(language) >= 8.2
Requires:       php-cli
Requires:       php-dom
Requires:       php-json
Requires:       php-libxml
Requires:       php-mbstring
Requires:       php-xml
Requires:       php-xmlwriter
Requires:       (php-composer(myclabs/deep-copy) >= 1.13.4            with php-composer(myclabs/deep-copy) <  2)
Requires:       (php-composer(phar-io/manifest) >= 2.0.4              with php-composer(phar-io/manifest) < 3)
Requires:       (php-composer(phar-io/version) >= 3.2.1               with php-composer(phar-io/version) < 4)
Requires:       (php-composer(phpunit/php-code-coverage) >= 11.0.12   with php-composer(phpunit/php-code-coverage) < 12)
Requires:       (php-composer(phpunit/php-file-iterator) >= 5.1.1     with php-composer(phpunit/php-file-iterator) < 6)
Requires:       (php-composer(phpunit/php-invoker) >= 5.0.1           with php-composer(phpunit/php-invoker) < 6)
Requires:       (php-composer(phpunit/php-text-template) >= 4.0.1     with php-composer(phpunit/php-text-template) < 5)
Requires:       (php-composer(phpunit/php-timer) >= 7.0.1             with php-composer(phpunit/php-timer) < 8)
Requires:       (php-composer(sebastian/cli-parser) >= 3.0.2          with php-composer(sebastian/cli-parser) < 4)
Requires:       (php-composer(sebastian/code-unit) >= 3.0.3           with php-composer(sebastian/code-unit) < 4)
Requires:       (php-composer(sebastian/comparator) >= 6.3.3          with php-composer(sebastian/comparator) < 7)
Requires:       (php-composer(sebastian/diff) >= 6.0.2                with php-composer(sebastian/diff) < 7)
Requires:       (php-composer(sebastian/environment) >= 7.2.1         with php-composer(sebastian/environment) < 8)
Requires:       (php-composer(sebastian/exporter) >= 6.3.2            with php-composer(sebastian/exporter) < 7)
Requires:       (php-composer(sebastian/global-state) >= 7.0.2        with php-composer(sebastian/global-state) < 8)
Requires:       (php-composer(sebastian/object-enumerator) >= 6.0.1   with php-composer(sebastian/object-enumerator) < 7)
Requires:       (php-composer(sebastian/recursion-context) >= 6.0.3   with php-composer(sebastian/recursion-context) < 7)
Requires:       (php-composer(sebastian/type) >= 5.1.3                with php-composer(sebastian/type) < 6)
Requires:       (php-composer(sebastian/version) >= 5.0.2             with php-composer(sebastian/version) < 6)
Requires:       (php-composer(staabm/side-effects-detector) >= 1.0.5  with php-composer(staabm/side-effects-detector) < 2)
# From composer.json, "suggest": {
#        "ext-soap": "*",
Suggests:       php-soap
# recommends latest versions
Recommends:     phpunit12
Recommends:     phpunit13
# Autoloader
Requires:       php-composer(fedora/autoloader)
# From phpcompatinfo report for version 10.0.0
Requires:       php-openssl
Requires:       php-pcntl
Requires:       php-phar

%if 0%{?fedora} >= 39 || 0%{?rhel} >= 10
Provides:       php-composer(phpunit/phpunit) = %{version}
%endif
%if %{with defcmd}
Provides:       phpunit                       = %{version}-%{release}
%endif


%description
PHPUnit is a programmer-oriented testing framework for PHP.
It is an instance of the xUnit architecture for unit testing frameworks.

This package provides the version %{ver_major} of PHPUnit,
available using the %{name} command.

Documentation: https://phpunit.de/documentation.html


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch -P0 -p0 -b .rpm

find . -name \*.rpm -delete -print


%build
%{_bindir}/phpab \
  --template fedora2 \
  --output   src/autoload.php \
  src

cat << 'EOF' | tee -a src/autoload.php
// Dependencies
\Fedora\Autoloader\Dependencies::required([
    '%{php_home}/SebastianBergmann/CodeCoverage11/autoload.php',
    '%{php_home}/SebastianBergmann/FileIterator5/autoload.php',
    '%{php_home}/SebastianBergmann/Template4/autoload.php',
    '%{php_home}/SebastianBergmann/Timer7/autoload.php',
    '%{php_home}/SebastianBergmann/CliParser3/autoload.php',
    '%{php_home}/SebastianBergmann/CodeUnit3/autoload.php',
    '%{php_home}/SebastianBergmann/Invoker5/autoload.php',
    '%{php_home}/SebastianBergmann/Diff6/autoload.php',
    '%{php_home}/SebastianBergmann/Comparator6/autoload.php',
    '%{php_home}/SebastianBergmann/Environment7/autoload.php',
    '%{php_home}/SebastianBergmann/Exporter6/autoload.php',
    '%{php_home}/SebastianBergmann/GlobalState7/autoload.php',
    '%{php_home}/SebastianBergmann/ObjectEnumerator6/autoload.php',
    '%{php_home}/SebastianBergmann/RecursionContext6/autoload.php',
    '%{php_home}/SebastianBergmann/Type5/autoload.php',
    '%{php_home}/SebastianBergmann/Version5/autoload.php',
    '%{php_home}/staabm/SideEffectsDetector/autoload.php',
    '%{php_home}/DeepCopy/autoload.php',
    '%{php_home}/PharIo/Manifest2/autoload.php',
    '%{php_home}/PharIo/Version3/autoload.php',
    __DIR__ . '/Framework/Assert/Functions.php',
]);
// Extensions
\Fedora\Autoloader\Dependencies::optional(
    glob("%{php_home}/%{ns_vendor}/Extensions/*/autoload.php")
);
EOF
cat src/autoload.php

%{_bindir}/phpab \
  --output   tests/autoload.php \
  tests/_files
cat << 'EOF' | tee -a tests/autoload.php
// Dependencies
\Fedora\Autoloader\Dependencies::required([
  __DIR__ . '/_files/deprecation-trigger/trigger_deprecation.php',
  __DIR__ . '/unit/Event/AbstractEventTestCase.php',
  __DIR__ . '/unit/Framework/MockObject/TestDoubleTestCase.php',
  __DIR__ . '/unit/Metadata/Parser/AnnotationParserTestCase.php',
  __DIR__ . '/unit/Metadata/Parser/AttributeParserTestCase.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyArrayTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyBoolTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyCallableTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyFloatTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyInstancesOfTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyIntTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyIterableTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyNullTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyNumericTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyObjectTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyResourceTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyClosedResourceTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyScalarTest.php',
  __DIR__ . '/unit/Framework/Assert/assertContainsOnlyStringTest.php',
  __DIR__ . '/unit/Framework/Assert/assertDirectoryExistsTest.php',
  __DIR__ . '/unit/Framework/Assert/assertFileExistsTest.php',
  __DIR__ . '/unit/Framework/Assert/assertIsNumericTest.php',
  __DIR__ . '/unit/Framework/Assert/assertIsObjectTest.php',
  __DIR__ . '/unit/Framework/Assert/assertIsReadableTest.php',
  __DIR__ . '/unit/Framework/Assert/assertIsResourceTest.php',
  __DIR__ . '/unit/Framework/Assert/assertIsScalarTest.php',
  __DIR__ . '/unit/Framework/Assert/assertIsStringTest.php',
  __DIR__ . '/unit/Framework/Assert/assertIsWritableTest.php',
  __DIR__ . '/unit/Framework/Assert/assertMatchesRegularExpressionTest.php',
  __DIR__ . '/unit/Framework/Assert/assertNullTest.php',
  __DIR__ . '/unit/Framework/Assert/assertSameSizeTest.php',
  __DIR__ . '/unit/Framework/Assert/assertSameTest.php',
  __DIR__ . '/_files/CoverageNamespacedFunctionTest.php',
  __DIR__ . '/_files/CoveredFunction.php',
  __DIR__ . '/_files/Generator.php',
  __DIR__ . '/_files/NamespaceCoveredFunction.php',
  __DIR__ . '/end-to-end/_files/listing-tests-and-groups/ExampleAbstractTestCase.php',
]);
EOF

%install
mkdir -p       %{buildroot}%{php_home}
cp -pr src     %{buildroot}%{php_home}/%{ns_vendor}
cp -pr schema  %{buildroot}%{php_home}/%{ns_vendor}/schema
mkdir          %{buildroot}%{php_home}/%{ns_vendor}/Extensions

install -D -p -m 755 phpunit %{buildroot}%{_bindir}/%{name}
install -p -m 644 phpunit.xsd %{buildroot}%{php_home}/%{ns_vendor}/phpunit.xsd

%if %{with defcmd}
ln -s %{name} %{buildroot}%{_bindir}/phpunit
%endif


%if %{with tests}
%check
# ignore tests relying on git layout
OPT='--filter "^((?!(testIsInitialized|testExclusionOfFileCanBeQueried)).)*$" --testsuite=unit --no-coverage'
sed -e 's:@PATH@:%{buildroot}%{php_home}/%{ns_vendor}:' -i tests/bootstrap.php
sed -e 's:%{php_home}/%{ns_vendor}:%{buildroot}%{php_home}/%{ns_vendor}:' -i phpunit

ret=0
for cmd in php php82 php83 php84 php85; do
  if which $cmd; then
     $cmd ./phpunit $OPT || ret=1
  fi
done
exit $ret
%endif


%files
%license LICENSE
%doc README.md ChangeLog-%{ver_major}.%{ver_minor}.md
%doc composer.json
%{_bindir}/%{name}
%if %{with defcmd}
%{_bindir}/phpunit
%endif
%{php_home}/%{ns_vendor}


%changelog
* Wed Feb 18 2026 Remi Collet <remi@remirepo.net> - 11.5.55-1
- update to 11.5.55

* Wed Feb 18 2026 Remi Collet <remi@remirepo.net> - 11.5.54-1
- update to 11.5.54

* Tue Feb 10 2026 Remi Collet <remi@remirepo.net> - 11.5.53-1
- update to 11.5.53

* Mon Feb  9 2026 Remi Collet <remi@remirepo.net> - 11.5.52-1
- update to 11.5.52

* Thu Feb  5 2026 Remi Collet <remi@remirepo.net> - 11.5.51-1
- update to 11.5.51
- raise dependency on phpunit/php-file-iterator 5.1.1
- re-add dependency on sebastian/recursion-context 6.0.3

* Tue Jan 27 2026 Remi Collet <remi@remirepo.net> - 11.5.50-1
- update to 11.5.50

* Mon Jan 26 2026 Remi Collet <remi@remirepo.net> - 11.5.49-1
- update to 11.5.49
- raise dependency on sebastian/comparator 6.3.3

* Sat Jan 17 2026 Remi Collet <remi@remirepo.net> - 11.5.48-1
- update to 11.5.48

* Thu Jan 15 2026 Remi Collet <remi@remirepo.net> - 11.5.47-1
- update to 11.5.47
- raise dependency on phpunit/php-code-coverage 11.0.12

* Tue Dec  2 2025 Remi Collet <remi@remirepo.net> - 11.5.45-1
- update to 11.5.45

* Thu Nov 13 2025 Remi Collet <remi@remirepo.net> - 11.5.44-1
- update to 11.5.44

* Thu Oct 30 2025 Remi Collet <remi@remirepo.net> - 11.5.43-1
- update to 11.5.43

* Mon Sep 29 2025 Remi Collet <remi@remirepo.net> - 11.5.42-1
- update to 11.5.42

* Wed Sep 24 2025 Remi Collet <remi@remirepo.net> - 11.5.41-1
- update to 11.5.41 (no change)
- raise dependency on sebastian/exporter 6.3.2

* Mon Sep 15 2025 Remi Collet <remi@remirepo.net> - 11.5.39-1
- update to 11.5.39

* Thu Sep 11 2025 Remi Collet <remi@remirepo.net> - 11.5.38-1
- update to 11.5.38

* Thu Sep 11 2025 Remi Collet <remi@remirepo.net> - 11.5.37-1
- update to 11.5.37

* Wed Sep  3 2025 Remi Collet <remi@remirepo.net> - 11.5.36-1
- update to 11.5.36

* Thu Aug 28 2025 Remi Collet <remi@remirepo.net> - 11.5.35-1
- update to 11.5.35
- raise dependency on phpunit/php-code-coverage 11.0.11

* Thu Jul 31 2025 Remi Collet <remi@remirepo.net> - 11.5.28-1
- update to 11.5.28

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.5.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Remi Collet <remi@remirepo.net> - 11.5.27-1
- update to 11.5.27
- raise dependency on myclabs/deep-copy 1.13.3

* Mon Jul  7 2025 Remi Collet <remi@remirepo.net> - 11.5.26-1
- update to 11.5.26

* Sat Jun 28 2025 Remi Collet <remi@remirepo.net> - 11.5.25-1
- update to 11.5.25

* Sat Jun 21 2025 Remi Collet <remi@remirepo.net> - 11.5.24-1
- update to 11.5.24
- raise dependency on phpunit/php-code-coverage 11.0.10

* Mon Jun 16 2025 Remi Collet <remi@remirepo.net> - 11.5.23-1
- update to 11.5.23

* Fri Jun  6 2025 Remi Collet <remi@remirepo.net> - 11.5.22-1
- update to 11.5.22

* Thu May 22 2025 Remi Collet <remi@remirepo.net> - 11.5.21-1
- update to 11.5.21
- raise dependency on sebastian/environment 7.2.1

* Mon May 12 2025 Remi Collet <remi@remirepo.net> - 11.5.20-1
- update to 11.5.20

* Sun May  4 2025 Remi Collet <remi@remirepo.net> - 11.5.19-1
- update to 11.5.19
- raise dependency on myclabs/deep-copy 1.13.1

* Wed Apr 23 2025 Remi Collet <remi@remirepo.net> - 11.5.18-1
- update to 11.5.18

* Mon Mar 24 2025 Remi Collet <remi@remirepo.net> - 11.5.15-1
- update to 11.5.15
- raise dependency on sebastian/code-unit 3.0.2

* Tue Mar 18 2025 Remi Collet <remi@remirepo.net> - 11.5.13-1
- update to 11.5.13
- raise dependency on sebastian/type 5.1.2

* Sat Mar  8 2025 Remi Collet <remi@remirepo.net> - 11.5.12-1
- update to 11.5.12
- raise dependency on sebastian/comparator 6.3.1

* Wed Mar  5 2025 Remi Collet <remi@remirepo.net> - 11.5.11-1
- update to 11.5.11
- raise dependency on phpunit/php-code-coverage 11.0.9

* Tue Feb 25 2025 Remi Collet <remi@remirepo.net> - 11.5.10-1
- update to 11.5.10

* Tue Feb 18 2025 Remi Collet <remi@remirepo.net> - 11.5.8-1
- update to 11.5.8

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 11.5.7-1
- update to 11.5.7

* Mon Feb  3 2025 Remi Collet <remi@remirepo.net> - 11.5.6-2
- F-40: drop phpunit command, provided by phpunit10
- EL-10: drop phpunit command, provided by phpunit12
- recommend phpunit12

* Fri Jan 31 2025 Remi Collet <remi@remirepo.net> - 11.5.6-1
- update to 11.5.6

* Wed Jan 29 2025 Remi Collet <remi@remirepo.net> - 11.5.5-1
- update to 11.5.5

* Wed Jan 29 2025 Remi Collet <remi@remirepo.net> - 11.5.4-1
- update to 11.5.4

* Mon Jan 13 2025 Remi Collet <remi@remirepo.net> - 11.5.3-1
- update to 11.5.3
- raise dependency on sebastian/comparator 6.3.0

* Sun Dec 22 2024 Remi Collet <remi@remirepo.net> - 11.5.2-1
- update to 11.5.2
- raise dependency on phpunit/php-code-coverage 11.0.8
- raise dependency on sebastian/code-unit 3.0.2

* Wed Dec 11 2024 Remi Collet <remi@remirepo.net> - 11.5.1-1
- update to 11.5.1

* Fri Dec  6 2024 Remi Collet <remi@remirepo.net> - 11.5.0-1
- update to 11.5.0
- raise dependency on sebastian/exporter 6.3.0
- add dependency on staabm/side-effects-detector
- re-license spec file to CECILL-2.1

* Thu Nov 28 2024 Remi Collet <remi@remirepo.net> - 11.4.4-1
- update to 11.4.4
- raise dependency on myclabs/deep-copy 1.12.1
- raise dependency on sebastian/comparator 6.2.1

* Mon Oct 28 2024 Remi Collet <remi@remirepo.net> - 11.4.3-2
- update to 11.4.3

* Mon Oct 21 2024 Remi Collet <remi@remirepo.net> - 11.4.2-1
- update to 11.4.2
- raise dependency on phpunit/php-code-coverage 11.0.7
- raise dependency on sebastian/comparator 6.1.1
- raise dependency on sebastian/version 5.0.2

* Wed Oct  9 2024 Remi Collet <remi@remirepo.net> - 11.4.1-1
- update to 11.4.1

* Sun Oct  6 2024 Remi Collet <remi@remirepo.net> - 11.4.0-1
- update to 11.4.0

* Thu Sep 19 2024 Remi Collet <remi@remirepo.net> - 11.3.6-1
- update to 11.3.6
- raise dependency on sebastian/type 5.1.0

* Fri Sep 13 2024 Remi Collet <remi@remirepo.net> - 11.3.5-1
- update to 11.3.5
- raise dependency on sebastian/comparator 6.1.0

* Mon Sep  9 2024 Remi Collet <remi@remirepo.net> - 11.3.4-1
- update to 11.3.4

* Thu Sep  5 2024 Remi Collet <remi@remirepo.net> - 11.3.3-1
- update to 11.3.3

* Tue Sep  3 2024 Remi Collet <remi@remirepo.net> - 11.3.2-1
- update to 11.3.2
- raise dependency on phpunit/php-code-coverage 11.0.6
- raise dependency on phpunit/php-file-iterator 5.1.0

* Tue Aug 13 2024 Remi Collet <remi@remirepo.net> - 11.3.1-1
- update to 11.3.1
- raise dependency on sebastian/comparator 6.0.2

* Fri Aug  2 2024 Remi Collet <remi@remirepo.net> - 11.3.0-1
- update to 11.3.0

* Tue Jul 30 2024 Remi Collet <remi@remirepo.net> - 11.2.9-1
- update to 11.2.9

* Fri Jul 19 2024 Remi Collet <remi@remirepo.net> - 11.2.8-1
- update to 11.2.8

* Thu Jul 11 2024 Remi Collet <remi@remirepo.net> - 11.2.7-1
- update to 11.2.7
- raise dependencies

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 11.2.6-1
- update to 11.2.6

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 11.2.5-1
- update to 11.2.5
- raise dependency on sebastian/exporter 6.1.2

* Tue Jun 11 2024 Remi Collet <remi@remirepo.net> - 11.2.1-1
- update to 11.2.1

* Fri Jun  7 2024 Remi Collet <remi@remirepo.net> - 11.2.0-1
- update to 11.2.0

* Wed Apr 24 2024 Remi Collet <remi@remirepo.net> - 11.1.3-1
- update to 11.1.3

* Mon Apr 15 2024 Remi Collet <remi@remirepo.net> - 11.1.2-1
- update to 11.1.2

* Sun Apr  7 2024 Remi Collet <remi@remirepo.net> - 11.1.1-1
- update to 11.1.1

* Fri Apr  5 2024 Remi Collet <remi@remirepo.net> - 11.1.0-1
- update to 11.1.0

* Thu Mar 28 2024 Remi Collet <remi@remirepo.net> - 11.0.9-1
- update to 11.0.9

* Fri Mar 22 2024 Remi Collet <remi@remirepo.net> - 11.0.8-1
- update to 11.0.8

* Thu Mar 21 2024 Remi Collet <remi@remirepo.net> - 11.0.7-1
- update to 11.0.7

* Wed Mar 13 2024 Remi Collet <remi@remirepo.net> - 11.0.6-1
- update to 11.0.6

* Sat Mar  9 2024 Remi Collet <remi@remirepo.net> - 11.0.5-1
- update to 11.0.5

* Wed Mar  6 2024 Remi Collet <remi@remirepo.net> - 11.0.4-2
- improve --check-version for RPM

* Fri Mar  1 2024 Remi Collet <remi@remirepo.net> - 11.0.4-1
- update to 11.0.4

* Sat Feb 10 2024 Remi Collet <remi@remirepo.net> - 11.0.3-1
- update to 11.0.3

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 11.0.2-1
- update to 11.0.2
- raise dependency on PHP 8.2
- drop dependency on sebastian/recursion-context
- raise dependency on phpunit/php-code-coverage 11
- raise dependency on phpunit/php-file-iterator 5
- raise dependency on phpunit/php-invoker 5
- raise dependency on phpunit/php-text-template 4
- raise dependency on phpunit/php-timer 7
- raise dependency on sebastian/cli-parser 3
- raise dependency on sebastian/code-unit 3
- raise dependency on sebastian/comparator 6
- raise dependency on sebastian/diff 6
- raise dependency on sebastian/environment 7
- raise dependency on sebastian/exporter 6
- raise dependency on sebastian/global-state 7
- raise dependency on sebastian/object-enumerator 6
- raise dependency on sebastian/type 5
- raise dependency on sebastian/version 5
- rename to phpunit11
- move to /usr/share/php/PHPUnit11

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 10.5.10-1
- update to 10.5.10

* Tue Jan 23 2024 Remi Collet <remi@remirepo.net> - 10.5.9-1
- update to 10.5.9

* Fri Jan 19 2024 Remi Collet <remi@remirepo.net> - 10.5.8-1
- update to 10.5.8

* Mon Jan 15 2024 Remi Collet <remi@remirepo.net> - 10.5.7-1
- update to 10.5.7

* Sun Jan 14 2024 Remi Collet <remi@remirepo.net> - 10.5.6-1
- update to 10.5.6

* Thu Dec 28 2023 Remi Collet <remi@remirepo.net> - 10.5.5-1
- update to 10.5.5

* Wed Dec 13 2023 Remi Collet <remi@remirepo.net> - 10.5.3-1
- update to 10.5.3

* Wed Dec  6 2023 Remi Collet <remi@remirepo.net> - 10.5.2-1
- update to 10.5.2

* Sat Dec  2 2023 Remi Collet <remi@remirepo.net> - 10.5.1-1
- update to 10.5.1

* Fri Dec  1 2023 Remi Collet <remi@remirepo.net> - 10.5.0-1
- update to 10.5.0
- provide phpunit command

* Thu Oct 26 2023 Remi Collet <remi@remirepo.net> - 10.4.2-1
- update to 10.4.2

* Sun Oct  8 2023 Remi Collet <remi@remirepo.net> - 10.4.1-1
- update to 10.4.1

* Fri Oct  6 2023 Remi Collet <remi@remirepo.net> - 10.4.0-1
- update to 10.4.0

* Tue Sep 19 2023 Remi Collet <remi@remirepo.net> - 10.3.5-1
- update to 10.3.5
- raise dependency on sebastian/exporter 5

* Wed Sep 13 2023 Remi Collet <remi@remirepo.net> - 10.3.4-1
- update to 10.3.4
- raise dependency on phpunit/php-code-coverage 10.1.5

* Tue Sep  5 2023 Remi Collet <remi@remirepo.net> - 10.3.3-1
- update to 10.3.3

* Fri Aug 18 2023 Remi Collet <remi@remirepo.net> - 10.3.2-1
- update to 10.3.2

* Fri Aug  4 2023 Remi Collet <remi@remirepo.net> - 10.3.1-1
- update to 10.3.1

* Fri Aug  4 2023 Remi Collet <remi@remirepo.net> - 10.3.0-1
- update to 10.3.0

* Wed Aug  2 2023 Remi Collet <remi@remirepo.net> - 10.2.7-1
- update to 10.2.7
- raise dependency on sebastian/global-state 6.0.1

* Tue Jul 18 2023 Remi Collet <remi@remirepo.net> - 10.2.6-1
- update to 10.2.6

* Fri Jul 14 2023 Remi Collet <remi@remirepo.net> - 10.2.5-1
- update to 10.2.5

* Mon Jul 10 2023 Remi Collet <remi@remirepo.net> - 10.2.4-1
- update to 10.2.4

* Fri Jun 30 2023 Remi Collet <remi@remirepo.net> - 10.2.3-1
- update to 10.2.3

* Mon Jun 12 2023 Remi Collet <remi@remirepo.net> - 10.2.2-1
- update to 10.2.2

* Mon Jun  5 2023 Remi Collet <remi@remirepo.net> - 10.2.1-1
- update to 10.2.1

* Fri Jun  2 2023 Remi Collet <remi@remirepo.net> - 10.2.0-1
- update to 10.2.0

* Thu May 11 2023 Remi Collet <remi@remirepo.net> - 10.1.3-1
- update to 10.1.3

* Sun Apr 23 2023 Remi Collet <remi@remirepo.net> - 10.1.2-1
- update to 10.1.2

* Wed Apr 19 2023 Remi Collet <remi@remirepo.net> - 10.1.1-1
- update to 10.1.1
- raise dependency on phpunit/php-code-coverage 10.1.1

* Fri Apr 14 2023 Remi Collet <remi@remirepo.net> - 10.1.0-1
- update to 10.1.0
- raise dependency on phpunit/php-code-coverage 10.1

* Mon Mar 27 2023 Remi Collet <remi@remirepo.net> - 10.0.19-1
- update to 10.0.19

* Wed Mar 22 2023 Remi Collet <remi@remirepo.net> - 10.0.18-1
- update to 10.0.18

* Tue Mar 21 2023 Remi Collet <remi@remirepo.net> - 10.0.17-1
- update to 10.0.17

* Mon Mar 13 2023 Remi Collet <remi@remirepo.net> - 10.0.16-1
- update to 10.0.16

* Thu Mar  9 2023 Remi Collet <remi@remirepo.net> - 10.0.15-1
- update to 10.0.15

* Thu Mar  2 2023 Remi Collet <remi@remirepo.net> - 10.0.14-1
- update to 10.0.14

* Tue Feb 28 2023 Remi Collet <remi@remirepo.net> - 10.0.13-1
- update to 10.0.13

* Tue Feb 21 2023 Remi Collet <remi@remirepo.net> - 10.0.11-1
- update to 10.0.11

* Mon Feb 20 2023 Remi Collet <remi@remirepo.net> - 10.0.10-1
- update to 10.0.10

* Mon Feb 20 2023 Remi Collet <remi@remirepo.net> - 10.0.9-1
- update to 10.0.9

* Thu Feb  9 2023 Remi Collet <remi@remirepo.net> - 10.0.7-1
- update to 10.0.7

* Wed Feb  8 2023 Remi Collet <remi@remirepo.net> - 10.0.6-1
- update to 10.0.6

* Tue Feb  7 2023 Remi Collet <remi@remirepo.net> - 10.0.5-1
- update to 10.0.5

* Mon Feb  6 2023 Remi Collet <remi@remirepo.net> - 10.0.4-1
- update to 10.0.4

* Sat Feb  4 2023 Remi Collet <remi@remirepo.net> - 10.0.2-1
- update to 10.0.2

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 10.0.1-1
- update to 10.0.1

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 10.0.0-1
- update to 10.0.0
- raise dependency on PHP 8.1
- add dependency on sebastian/recursion-context
- drop dependency on doctrine/instantiator
- drop dependency on sebastian/resource-operations
- drop dependency on phpspec/prophecy
- raise dependency on phpunit/php-code-coverage 10
- raise dependency on phpunit/php-file-iterator 4
- raise dependency on phpunit/php-invoker 4
- raise dependency on phpunit/php-text-template 3
- raise dependency on phpunit/php-timer 6
- raise dependency on sebastian/cli-parser 2
- raise dependency on sebastian/code-unit 2
- raise dependency on sebastian/comparator 5
- raise dependency on sebastian/diff 5
- raise dependency on sebastian/environment 6
- raise dependency on sebastian/exporter 5
- raise dependency on sebastian/global-state 6
- raise dependency on sebastian/object-enumerator 5
- raise dependency on sebastian/type 4
- raise dependency on sebastian/version 3
- rename to phpunit10
- move to /usr/share/php/PHPUnit10

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 9.6.0-1
- update to 9.6.0

* Mon Jan 16 2023 Remi Collet <remi@remirepo.net> - 9.5.28-1
- update to 9.5.28
- allow doctrine/instantiator v2

* Fri Dec  9 2022 Remi Collet <remi@remirepo.net> - 9.5.27-1
- update to 9.5.27

* Fri Oct 28 2022 Remi Collet <remi@remirepo.net> - 9.5.26-1
- update to 9.5.26

* Sun Sep 25 2022 Remi Collet <remi@remirepo.net> - 9.5.25-1
- update to 9.5.25
- raise dependency on sebastian/comparator 4.0.8
- raise dependency on sebastian/exporter 4.0.5
- raise dependency on sebastian/type 3.2

* Thu Sep  1 2022 Remi Collet <remi@remirepo.net> - 9.5.24-1
- update to 9.5.24
- raise dependency on sebastian/type 3.1

* Tue Aug 30 2022 Remi Collet <remi@remirepo.net> - 9.5.23-1
- update to 9.5.23
- keep dependency on phpspec/prophecy (optional)

* Mon Jun 20 2022 Remi Collet <remi@remirepo.net> - 9.5.21-1
- update to 9.5.21

* Mon Apr  4 2022 Remi Collet <remi@remirepo.net> - 9.5.20-1
- update to 9.5.20

* Tue Mar 15 2022 Remi Collet <remi@remirepo.net> - 9.5.19-1
- update to 9.5.19
- raise dependency on sebastian/type 3.0

* Tue Mar  8 2022 Remi Collet <remi@remirepo.net> - 9.5.18-1
- update to 9.5.18

* Sun Mar  6 2022 Remi Collet <remi@remirepo.net> - 9.5.17-1
- update to 9.5.17 #StandWithUkraine

* Thu Feb 24 2022 Remi Collet <remi@remirepo.net> - 9.5.16-1
- update to 9.5.16
- raise dependency on phpunit/php-code-coverage 9.2.13

* Wed Feb 23 2022 Remi Collet <remi@remirepo.net> - 9.5.15-1
- update to 9.5.15
- raise dependency on phpunit/php-code-coverage 9.2.12

* Fri Feb 18 2022 Remi Collet <remi@remirepo.net> - 9.5.14-1
- update to 9.5.14

* Mon Jan 24 2022 Remi Collet <remi@remirepo.net> - 9.5.13-1
- update to 9.5.13

* Fri Jan 21 2022 Remi Collet <remi@remirepo.net> - 9.5.12-1
- update to 9.5.12

* Thu Dec 30 2021 Remi Collet <remi@remirepo.net> - 9.5.11-1
- update to 9.5.11

* Mon Sep 27 2021 Remi Collet <remi@remirepo.net> - 9.5.10-1
- update to 9.5.10
- raise dependency on phpunit/php-code-coverage 9.2.7

* Wed Sep  1 2021 Remi Collet <remi@remirepo.net> - 9.5.9-1
- update to 9.5.9

* Mon Aug  2 2021 Remi Collet <remi@remirepo.net> - 9.5.8-1
- update to 9.5.8
- raise dependency on phar-io/manifest 2.0.3

* Mon Jul 19 2021 Remi Collet <remi@remirepo.net> - 9.5.7-1
- update to 9.5.7

* Wed Jun 23 2021 Remi Collet <remi@remirepo.net> - 9.5.6-1
- update to 9.5.6

* Mon Jun  7 2021 Remi Collet <remi@remirepo.net> - 9.5.5-1
- update to 9.5.5
- raise dependency on sebastian/type 2.3.2

* Tue Mar 23 2021 Remi Collet <remi@remirepo.net> - 9.5.4-1
- update to 9.5.4

* Wed Mar 17 2021 Remi Collet <remi@remirepo.net> - 9.5.3-1
- update to 9.5.3

* Wed Feb  3 2021 Remi Collet <remi@remirepo.net> - 9.5.2-1
- update to 9.5.2

* Fri Dec  4 2020 Remi Collet <remi@remirepo.net> - 9.5.0-1
- update to 9.5.0
- raise dependency on phpunit/php-code-coverage 9.2.3

* Tue Dec  1 2020 Remi Collet <remi@remirepo.net> - 9.4.4-1
- update to 9.4.4

* Tue Nov 10 2020 Remi Collet <remi@remirepo.net> - 9.4.3-1
- update to 9.4.3

* Mon Oct 19 2020 Remi Collet <remi@remirepo.net> - 9.4.2-1
- update to 9.4.2

* Mon Oct 12 2020 Remi Collet <remi@remirepo.net> - 9.4.1-1
- update to 9.4.1

* Fri Oct  2 2020 Remi Collet <remi@remirepo.net> - 9.4.0-1
- update to 9.4.0
- raise dependency on phpunit/php-code-coverage 9.2

* Thu Sep 24 2020 Remi Collet <remi@remirepo.net> - 9.3.11-1
- update to 9.3.11 (no change)
- raise dependency on phpunit/php-code-coverage 9.1.11

* Sun Sep 13 2020 Remi Collet <remi@remirepo.net> - 9.3.10-1
- update to 9.3.10

* Fri Sep 11 2020 Remi Collet <remi@remirepo.net> - 9.3.9-1
- update to 9.3.9

* Thu Aug 27 2020 Remi Collet <remi@remirepo.net> - 9.3.8-1
- update to 9.3.8
- raise dependency on phpunit/php-code-coverage 9.1.5
- add dependency on sebastian/cli-parser

* Wed Aug 12 2020 Remi Collet <remi@remirepo.net> - 9.3.7-1
- update to 9.3.7

* Tue Aug 11 2020 Remi Collet <remi@remirepo.net> - 9.3.6-1
- update to 9.3.6

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 9.3.5-1
- update to 9.3.5

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 9.3.3-1
- update to 9.3.3
- raise dependency on myclabs/deep-copy 1.10.1
- raise dependency on phar-io/manifest 2.0.1
- raise dependency on phar-io/version 3.0.2
- raise dependency on phpspec/prophecy 1.11.1
- raise dependency on phpunit/php-code-coverage 9.0
- raise dependency on phpunit/php-file-iterator 3.0.4
- raise dependency on phpunit/php-invoker 3.1
- raise dependency on sebastian/diff 4.0.2
- raise dependency on sebastian/global-state 5.0
- raise dependency on sebastian/type 2.2.1

* Tue Jul 14 2020 Remi Collet <remi@remirepo.net> - 9.2.6-1
- update to 9.2.6
- raise dependency on latest minor version available
  for all libraries

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 9.2.5-2
- cleanup dependencies

* Mon Jun 22 2020 Remi Collet <remi@remirepo.net> - 9.2.5-1
- update to 9.2.5

* Mon Jun 22 2020 Remi Collet <remi@remirepo.net> - 9.2.4-1
- update to 9.2.4

* Mon Jun 15 2020 Remi Collet <remi@remirepo.net> - 9.2.3-1
- update to 9.2.3

* Mon Jun  8 2020 Remi Collet <remi@remirepo.net> - 9.2.2-1
- update to 9.2.2
- raise dependency on phpunit/php-timer 4.0

* Fri Jun  5 2020 Remi Collet <remi@remirepo.net> - 9.2.1-1
- update to 9.2.1

* Fri Jun  5 2020 Remi Collet <remi@remirepo.net> - 9.2.0-1
- update to 9.2.0
- raise dependency on phpunit/php-timer 4.0
- raise dependency on sebastian/type 2.1

* Sat May 23 2020 Remi Collet <remi@remirepo.net> - 9.1.5-1
- update to 9.1.5
- sources from git snapshot

* Thu Apr 30 2020 Remi Collet <remi@remirepo.net> - 9.1.4-1
- update to 9.1.4
- raise dependency on sebastian/code-unit 1.0.2

* Thu Apr 23 2020 Remi Collet <remi@remirepo.net> - 9.1.3-1
- update to 9.1.3

* Mon Apr 20 2020 Remi Collet <remi@remirepo.net> - 9.1.2-1
- update to 9.1.2
- raise dependency on phpunit/php-timer 3.1.4

* Sat Apr  4 2020 Remi Collet <remi@remirepo.net> - 9.1.1-1
- update to 9.1.1

* Fri Apr  3 2020 Remi Collet <remi@remirepo.net> - 9.1.0-1
- update to 9.1.0
- add dependency on sebastian/code-unit

* Tue Mar 31 2020 Remi Collet <remi@remirepo.net> - 9.0.2-1
- update to 9.0.2
- own /usr/share/php/PHPUnit9/Extensions
- raise dependency on phpunit/php-code-coverage 8.0.1
- raise dependency on sebastian/environment 5.0.1

* Fri Feb 14 2020 Remi Collet <remi@remirepo.net> - 9.0.1-1
- update to 9.0.1

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 9.0.0-1
- update to 9.0.0
- raise dependency on PHP 7.3
- raise dependency on phpunit/php-code-coverage 8
- raise dependency on phpunit/php-file-iterator 3
- raise dependency on phpunit/php-text-template 2
- raise dependency on phpunit/php-timer 3
- raise dependency on sebastian/comparator 4
- raise dependency on sebastian/diff 4
- raise dependency on sebastian/environment 5
- raise dependency on sebastian/exporter 4
- raise dependency on sebastian/global-state 4
- raise dependency on sebastian/object-enumerator 4
- raise dependency on sebastian/resource-operations 3
- raise dependency on sebastian/type 2
- raise dependency on sebastian/version 3
- add dependency on phpunit/php-invoker 3
- rename to phpunit9
- move to /usr/share/php/PHPUnit9

* Wed Jan  8 2020 Remi Collet <remi@remirepo.net> - 8.5.2-1
- update to 8.5.2

* Thu Jan  2 2020 Remi Collet <remi@remirepo.net> - 8.5.1-1
- update to 8.5.1

* Fri Dec  6 2019 Remi Collet <remi@remirepo.net> - 8.5.0-1
- update to 8.5.0

* Wed Nov  6 2019 Remi Collet <remi@remirepo.net> - 8.4.3-1
- update to 8.4.3

* Mon Oct 28 2019 Remi Collet <remi@remirepo.net> - 8.4.2-1
- update to 8.4.2

* Tue Oct  8 2019 Remi Collet <remi@remirepo.net> - 8.4.1-1
- update to 8.4.1

* Fri Oct  4 2019 Remi Collet <remi@remirepo.net> - 8.4.0-1
- update to 8.4.0

* Sun Sep 15 2019 Remi Collet <remi@remirepo.net> - 8.3.5-1
- update to 8.3.5
- raise dependency on sebastian/exporter 3.1.1

* Mon Aug 12 2019 Remi Collet <remi@remirepo.net> - 8.3.4-1
- update to 8.3.4

* Sun Aug  4 2019 Remi Collet <remi@remirepo.net> - 8.3.3-1
- update to 8.3.3

* Sat Aug  3 2019 Remi Collet <remi@remirepo.net> - 8.3.2-1
- update to 8.3.2

* Fri Aug  2 2019 Remi Collet <remi@remirepo.net> - 8.3.0-1
- update to 8.3.0
- raise dependency on phpunit/php-code-coverage 7.0.7

* Mon Jul 15 2019 Remi Collet <remi@remirepo.net> - 8.2.5-1
- update to 8.2.5

* Wed Jul  3 2019 Remi Collet <remi@remirepo.net> - 8.2.4-1
- update to 8.2.4
- raise dependency on sebastian/type 1.1.3

* Wed Jun 19 2019 Remi Collet <remi@remirepo.net> - 8.2.3-1
- update to 8.2.3

* Sun Jun 16 2019 Remi Collet <remi@remirepo.net> - 8.2.2-1
- update to 8.2.2 (no change)
- raise dependency on phpspec/prophecy 1.8.1

* Sat Jun  8 2019 Remi Collet <remi@remirepo.net> - 8.2.1-1
- update to 8.2.1
- raise dependency on sebastian/type 1.1.0

* Fri Jun  7 2019 Remi Collet <remi@remirepo.net> - 8.2.0-1
- update to 8.2.0
- add dependency on sebastian/type
- raise dependency on doctrine/instantiator 1.2.0
- raise dependency on myclabs/deep-copy 1.9.1
- raise dependency on phar-io/manifest 1.0.3
- raise dependency on phar-io/version 2.0.1
- raise dependency on phpspec/prophecy 1.8.0
- raise dependency on phpunit/php-code-coverage 7.0.5
- raise dependency on phpunit/php-file-iterator 2.0.2
- raise dependency on phpunit/php-timer 2.1.2
- raise dependency on sebastian/comparator 3.0.2
- raise dependency on sebastian/diff 3.0.2
- raise dependency on sebastian/environment 4.2.2
- raise dependency on sebastian/resource-operations 2.0.1

* Tue May 28 2019 Remi Collet <remi@remirepo.net> - 8.1.6-1
- update to 8.1.6

* Tue May 14 2019 Remi Collet <remi@remirepo.net> - 8.1.5-1
- update to 8.1.5

* Fri May 10 2019 Remi Collet <remi@remirepo.net> - 8.1.4-1
- update to 8.1.4

* Tue Apr 23 2019 Remi Collet <remi@remirepo.net> - 8.1.3-1
- update to 8.1.3

* Tue Apr  9 2019 Remi Collet <remi@remirepo.net> - 8.1.2-1
- update to 8.1.2

* Mon Apr  8 2019 Remi Collet <remi@remirepo.net> - 8.1.1-1
- update to 8.1.1

* Fri Apr  5 2019 Remi Collet <remi@remirepo.net> - 8.1.0-1
- update to 8.1.0

* Wed Mar 27 2019 Remi Collet <remi@remirepo.net> - 8.0.6-1
- update to 8.0.6

* Sat Mar 16 2019 Remi Collet <remi@remirepo.net> - 8.0.5-1
- update to 8.0.5
- raise dependency on phpunit/php-timer 2.1

* Mon Feb 18 2019 Remi Collet <remi@remirepo.net> - 8.0.4-1
- update to 8.0.4

* Sat Feb 16 2019 Remi Collet <remi@remirepo.net> - 8.0.3-1
- update to 8.0.3

* Fri Feb  8 2019 Remi Collet <remi@remirepo.net> - 8.0.2-1
- update to 8.0.2

* Mon Feb  4 2019 Remi Collet <remi@remirepo.net> - 8.0.1-1
- update to 8.0.1

* Fri Feb  1 2019 Remi Collet <remi@remirepo.net> - 8.0.0-1
- rename to phpunit8
- update to 8.0.0
- add dependency on xmlwriter extension
- add weak dependency on soap, xdebug extension
- raise dependency on PHP 7.2
- raise dependency on phpunit/php-code-coverage 7.0
- raise dependency on sebastian/environment 4.1
- raise dependency on sebastian/global-state 3.0

* Fri Feb  1 2019 Remi Collet <remi@remirepo.net> - 7.5.3-1
- update to 7.5.3

* Tue Jan 15 2019 Remi Collet <remi@remirepo.net> - 7.5.2-1
- update to 7.5.2

* Wed Dec 12 2018 Remi Collet <remi@remirepo.net> - 7.5.1-1
- update to 7.5.1

* Fri Dec  7 2018 Remi Collet <remi@remirepo.net> - 7.5.0-1
- update to 7.5.0

* Mon Dec  3 2018 Remi Collet <remi@remirepo.net> - 7.4.5-1
- update to 7.4.5
- raise dependency on sebastian/environment 4.0

* Thu Nov 15 2018 Remi Collet <remi@remirepo.net> - 7.4.4-1
- update to 7.4.4

* Tue Oct 23 2018 Remi Collet <remi@remirepo.net> - 7.4.3-1
- update to 7.4.3
- drop patch merged upstream

* Thu Oct 18 2018 Remi Collet <remi@remirepo.net> - 7.4.1-2
- add patch for https://github.com/sebastianbergmann/phpunit/issues/3354
  from https://github.com/sebastianbergmann/phpunit/pull/3355

* Thu Oct 18 2018 Remi Collet <remi@remirepo.net> - 7.4.1-1
- update to 7.4.1
- allow sebastian/environment 4

* Fri Oct  5 2018 Remi Collet <remi@remirepo.net> - 7.4.0-1
- update to 7.4.0
- raise dependency on sebastian/resource-operations 2.0

* Sun Sep  9 2018 Remi Collet <remi@remirepo.net> - 7.3.5-1
- update to 7.3.5

* Wed Sep  5 2018 Remi Collet <remi@remirepo.net> - 7.3.4-1
- update to 7.3.4

* Sun Sep  2 2018 Remi Collet <remi@remirepo.net> - 7.3.3-1
- update to 7.3.3

* Wed Aug 22 2018 Remi Collet <remi@remirepo.net> - 7.3.2-1
- update to 7.3.2

* Thu Aug  9 2018 Remi Collet <remi@remirepo.net> - 7.3.1-1
- update to 7.3.1

* Mon Jul 16 2018 Remi Collet <remi@remirepo.net> - 7.2.7-1
- update to 7.2.7
- allow phar-io/version 2.0

* Thu Jun 21 2018 Remi Collet <remi@remirepo.net> - 7.2.6-1
- update to 7.2.6

* Thu Jun 21 2018 Remi Collet <remi@remirepo.net> - 7.2.5-1
- update to 7.2.5
- raise dependency on phpunit/php-file-iterator 2.0.1

* Tue Jun  5 2018 Remi Collet <remi@remirepo.net> - 7.2.4-1
- update to 7.2.4

* Sun Jun  3 2018 Remi Collet <remi@remirepo.net> - 7.2.3-1
- update to 7.2.3

* Fri Jun  1 2018 Remi Collet <remi@remirepo.net> - 7.2.2-2
- manage php-doctrine-instantiator11

* Fri Jun  1 2018 Remi Collet <remi@remirepo.net> - 7.2.2-1
- update to 7.2.2
- raise dependency on phpunit/php-code-coverage 6.0.7

* Fri Jun  1 2018 Remi Collet <remi@remirepo.net> - 7.2.1-1
- update to 7.2.1

* Fri Jun  1 2018 Remi Collet <remi@remirepo.net> - 7.2.0-1
- update to 7.2.0
- add dependency on doctrine/instantiator 1.1
- raise dependency on myclabs/deep-copy 1.7
- raise dependency on phpunit/php-code-coverage 6.0.6
- raise dependency on phpunit/php-file-iterator 2.0
- phpunit/phpunit-mock-objects is merged
- open https://github.com/sebastianbergmann/phpunit/issues/3155
  TypeError: Return value of PHPUnit\Framework\TestCase::getStatus()...

* Wed May  2 2018 Remi Collet <remi@remirepo.net> - 7.1.5-1
- update to 7.1.5
- raise dependency on sebastian/comparator 3.0

* Wed Apr 18 2018 Remi Collet <remi@remirepo.net> - 7.1.4-1
- update to 7.1.4
- allow sebastian/comparator 3.0

* Mon Apr 16 2018 Remi Collet <remi@remirepo.net> - 7.1.3-1
- update to 7.1.3 (no change)
- raise dependency on phpunit/phpunit-mock-objects 6.1.1

* Tue Apr 10 2018 Remi Collet <remi@remirepo.net> - 7.1.2-1
- update to 7.1.2

* Mon Apr  9 2018 Remi Collet <remi@remirepo.net> - 7.1.1-1
- update to 7.1.1
- raise dependency on phpunit/phpunit-mock-objects 6.1

* Mon Mar 26 2018 Remi Collet <remi@remirepo.net> - 7.0.3-1
- update to 7.0.3
- raise dependency on phpunit/php-code-coverage 6.0.1

* Mon Feb 26 2018 Remi Collet <remi@remirepo.net> - 7.0.2-1
- Update to 7.0.2

* Tue Feb 13 2018 Remi Collet <remi@remirepo.net> - 7.0.1-1
- Update to 7.0.1

* Wed Feb  7 2018 Remi Collet <remi@remirepo.net> - 7.0.0-4
- fix weak dependency on php-phpunit-dbunit4

* Wed Feb  7 2018 Remi Collet <remi@remirepo.net> - 7.0.0-3
- re add undefine __brp_mangle_shebangs

* Tue Feb  6 2018 Remi Collet <remi@remirepo.net> - 7.0.0-2
- remove undefine __brp_mangle_shebangs for review #1541346

* Fri Feb  2 2018 Remi Collet <remi@remirepo.net> - 7.0.0-1
- Update to 7.0.0
- rename to phpunit7
- move to /usr/share/php/PHPUnit7
- raise dependency on PHP 7.1
- raise dependency on phpunit/php-code-coverage 6.0
- raise dependency on phpunit/php-timer 2.0
- raise dependency on phpunit/phpunit-mock-objects 6.0
- raise dependency on sebastian/diff 3.0
- raise dependency on phpunit/php-invoker 2.0
- use range dependencies on F27+
- use full path instead of relying on include_path

* Thu Feb  1 2018 Remi Collet <remi@remirepo.net> - 6.5.6-1
- Update to 6.5.6
- undefine __brp_mangle_shebangs
- use range dependencies on F27+

* Mon Dec 18 2017 Remi Collet <remi@remirepo.net> - 6.5.5-1
- Update to 6.5.5

* Mon Dec 11 2017 Remi Collet <remi@remirepo.net> - 6.5.4-1
- Update to 6.5.4
- raise dependency on phpunit/phpunit-mock-objects 5.0.5

* Thu Dec  7 2017 Remi Collet <remi@remirepo.net> - 6.5.3-1
- Update to 6.5.3
- raise dependency on phpunit/php-code-coverage 5.3

* Mon Dec  4 2017 Remi Collet <remi@remirepo.net> - 6.5.2-1
- Update to 6.5.2
- raise dependency on phpunit/phpunit-mock-objects 5.0.4

* Fri Dec  1 2017 Remi Collet <remi@remirepo.net> - 6.5.0-1
- Update to 6.5.0
- raise dependency on phpunit/php-code-coverage 5.2.3
- raise dependency on phpunit/php-file-iterator 1.4.3
- raise dependency on phpunit/phpunit-mock-objects 5.0

* Thu Nov  9 2017 Remi Collet <remi@remirepo.net> - 6.4.4-1
- Update to 6.4.4

* Tue Oct 17 2017 Remi Collet <remi@remirepo.net> - 6.4.3-1
- Update to 6.4.3

* Sun Oct 15 2017 Remi Collet <remi@remirepo.net> - 6.4.2-1
- Update to 6.4.2

* Sun Oct  8 2017 Remi Collet <remi@remirepo.net> - 6.4.1-1
- Update to 6.4.1

* Sun Sep 24 2017 Remi Collet <remi@remirepo.net> - 6.3.1-1
- Update to 6.3.1

* Mon Aug 21 2017 Remi Collet <remi@remirepo.net> - 6.3.0-2
- add optional dependency on php-phpunit-selenium

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 6.3.0-1
- Update to 6.3.0

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 6.2.4-1
- Update to 6.2.4

* Tue Jul  4 2017 Remi Collet <remi@remirepo.net> - 6.2.3-1
- Update to 6.2.3

* Tue Jun 13 2017 Remi Collet <remi@remirepo.net> - 6.2.2-1
- Update to 6.2.2

* Mon Jun  5 2017 Remi Collet <remi@remirepo.net> - 6.2.1-1
- Update to 6.2.1

* Mon May 22 2017 Remi Collet <remi@remirepo.net> - 6.1.4-1
- Update to 6.1.4 (no change)
- raise dependency on sebastian/diff 1.4.3 and allow v2
- raise dependency on sebastian/environment 3.0.2

* Sat Apr 29 2017 Remi Collet <remi@remirepo.net> - 6.1.3-1
- Update to 6.1.3
- raise dependency to only use sebastian/global-state v2

* Wed Apr 26 2017 Remi Collet <remi@remirepo.net> - 6.1.2-1
- Update to 6.1.2

* Sun Apr 23 2017 Remi Collet <remi@remirepo.net> - 6.1.1-1
- Update to 6.1.1
- raise dependency on phpunit/php-code-coverage >= 5.2
- raise dependency on sebastian/environment >= 3.0

* Fri Apr  7 2017 Remi Collet <remi@remirepo.net> - 6.1.0-1
- Update to 6.1.0
- add dependency on phar-io/manifest
- add dependency on phar-io/version
- raise dependency on sebastian/exporter 3.1

* Mon Apr  3 2017 Remi Collet <remi@remirepo.net> - 6.0.13-1
- Update to 6.0.13

* Thu Mar 30 2017 Remi Collet <remi@remirepo.net> - 6.0.11-2
- use fedora2 autoloader template

* Wed Mar 29 2017 Remi Collet <remi@remirepo.net> - 6.0.11-1
- Update to 6.0.11

* Mon Mar 20 2017 Remi Collet <remi@remirepo.net> - 6.0.10-1
- Update to 6.0.10

* Wed Mar 15 2017 Remi Collet <remi@remirepo.net> - 6.0.9-1
- Update to 6.0.9
- raise dependency on phpspec/prophecy 1.7
- raise dependency on sebastian/comparator 2.0
- raise dependency on sebastian/exporter 3.0
- raise dependency on sebastian/object-enumerator 3.0.2
- more explicit dependencies
- fix autoloader to only rely on include_path

* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 6.0.8-2
- fix autoloader for dep. with multiple versions

* Thu Mar  2 2017 Remi Collet <remi@remirepo.net> - 6.0.8-1
- Update to 6.0.8

* Sun Feb 19 2017 Remi Collet <remi@fedoraproject.org> - 6.0.7-1
- update to 6.0.7

* Wed Feb  8 2017 Remi Collet <remi@fedoraproject.org> - 6.0.6-2
- cleanup autoloader (Symfony no more used)
- fix autoloader for dbunit
- fix description

* Wed Feb  8 2017 Remi Collet <remi@fedoraproject.org> - 6.0.6-1
- update to 6.0.6

* Tue Feb  7 2017 Remi Collet <remi@fedoraproject.org> - 6.0.5-1
- rename to phpunit6
- move to /usr/share/php/PHPUnit6
- raise dependency on phpunit/php-code-coverage 5.0.0
- raise dependency on phpunit/phpunit-mock-objects 4.0.0
- change spec license to CC-BY-SA

* Tue Feb  7 2017 Remi Collet <remi@fedoraproject.org> - 5.7.11-2
- add max version for some build dependencies
- only allow Symfony 2
- handle redirect to composer installed PHPUnit v6

* Sun Feb  5 2017 Remi Collet <remi@fedoraproject.org> - 5.7.11-1
- update to 5.7.11
- raise dependency on sebastian/comparator 1.2.4
- raise dependency on sebastian/global-state 1.1

* Sat Jan 28 2017 Remi Collet <remi@fedoraproject.org> - 5.7.9-1
- update to 5.7.9

* Fri Jan 27 2017 Remi Collet <remi@fedoraproject.org> - 5.7.8-2
- add upstream patch

* Thu Jan 26 2017 Remi Collet <remi@fedoraproject.org> - 5.7.8-1
- update to 5.7.8
- temporary ignore testNoTestCases

* Thu Jan 26 2017 Remi Collet <remi@fedoraproject.org> - 5.7.7-1
- update to 5.7.7

* Mon Jan 23 2017 Remi Collet <remi@fedoraproject.org> - 5.7.6-1
- update to 5.7.6

* Thu Dec 29 2016 Remi Collet <remi@fedoraproject.org> - 5.7.5-1
- update to 5.7.5

* Wed Dec 14 2016 Remi Collet <remi@fedoraproject.org> - 5.7.4-1
- update to 5.7.4

* Fri Dec  9 2016 Remi Collet <remi@fedoraproject.org> - 5.7.3-1
- update to 5.7.3
- raise dependency on phpspec/prophecy 1.6.2

* Sun Dec  4 2016 Remi Collet <remi@fedoraproject.org> - 5.7.2-1
- update to 5.7.2

* Fri Dec  2 2016 Remi Collet <remi@fedoraproject.org> - 5.7.1-1
- update to 5.7.1

* Fri Dec  2 2016 Remi Collet <remi@fedoraproject.org> - 5.7.0-1
- update to 5.7.0

* Mon Nov 28 2016 Remi Collet <remi@fedoraproject.org> - 5.6.7-1
- update to 5.6.7

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 5.6.5-1
- update to 5.6.5
- raise dependency on sebastian/comparator 1.2.2
- raise dependency on sebastian/exporter 2.0
- raise dependency on sebastian/object-enumerator 2.0

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 5.6.3-1
- update to 5.6.3

* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 5.6.2-2
- fix autoloader (don't use symfony one for symfony components)

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 5.6.2-1
- update to 5.6.2 (no change)
- switch to fedora/autoloader

* Fri Oct  7 2016 Remi Collet <remi@fedoraproject.org> - 5.6.1-1
- update to 5.6.1

* Fri Oct  7 2016 Remi Collet <remi@fedoraproject.org> - 5.6.0-1
- update to 5.6.0
- drop dependency on php-tidy

* Mon Oct  3 2016 Remi Collet <remi@fedoraproject.org> - 5.5.7-1
- Update to 5.5.7 (no change)
- sources from github

* Mon Oct  3 2016 Remi Collet <remi@fedoraproject.org> - 5.5.6-1
- Update to 5.5.6
- sources from a git snapshot

* Wed Sep 21 2016 Remi Collet <remi@fedoraproject.org> - 5.5.5-1
- Update to 5.5.5

* Wed Aug 31 2016 Remi Collet <remi@fedoraproject.org> - 5.5.4-1
- Update to 5.5.4

* Fri Aug  5 2016 Remi Collet <remi@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0

* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 5.4.8-1
- Update to 5.4.8 (no change)
- raise dependency on phpunit/php-code-coverage >= 4.0.1

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 5.4.7-1
- Update to 5.4.7

* Thu Jun 16 2016 Remi Collet <remi@fedoraproject.org> - 5.4.6-1
- Update to 5.4.6 (no change)

* Wed Jun 15 2016 Remi Collet <remi@fedoraproject.org> - 5.4.5-1
- Update to 5.4.5

* Thu Jun  9 2016 Remi Collet <remi@fedoraproject.org> - 5.4.4-1
- Update to 5.4.4

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 5.4.2-1
- Update to 5.4.2

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 5.4.0-1
- Update to 5.4.0
- raise dependency on phpunit/php-code-coverage >= 4.0
- raise dependency on phpunit/phpunit-mock-objects >= 3.2

* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 5.3.4-1
- Update to 5.3.4

* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 5.3.2-1
- Update to 5.3.2

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 5.3.1-1
- Update to 5.3.1

* Fri Apr  1 2016 Remi Collet <remi@fedoraproject.org> - 5.3.0-1
- Update to 5.3.0
- add dependency on sebastian/object-enumerator
- raise dependency on phpunit/phpunit-mock-objects >= 3.1

* Tue Mar 15 2016 Remi Collet <remi@fedoraproject.org> - 5.2.12-1
- Update to 5.2.12

* Mon Mar 14 2016 Remi Collet <remi@fedoraproject.org> - 5.2.11-1
- Update to 5.2.11

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 5.2.10-1
- Update to 5.2.10
- raise dependency on phpunit/php-code-coverage >= 3.3.0

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 5.2.9-1
- Update to 5.2.9

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> - 5.2.8-1
- Update to 5.2.8
- raise dependency on phpunit/php-code-coverage >= 3.2.1

* Tue Feb 16 2016 Remi Collet <remi@fedoraproject.org> - 5.2.6-1
- Update to 5.2.6

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 5.2.5-1
- Update to 5.2.5
- raise dependency on phpunit/php-code-coverage >= 3.2

* Thu Feb 11 2016 Remi Collet <remi@fedoraproject.org> - 5.2.4-1
- Update to 5.2.4
- lower dependency on phpunit/php-code-coverage >= 3.0

* Sun Feb  7 2016 Remi Collet <remi@fedoraproject.org> - 5.2.2-1
- Update to 5.2.2

* Fri Feb  5 2016 Remi Collet <remi@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Fri Feb  5 2016 Remi Collet <remi@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0
- raise dependency on phpunit/php-code-coverage >= 3.1

* Tue Feb  2 2016 Remi Collet <remi@fedoraproject.org> - 5.1.7-1
- Update to 5.1.7

* Fri Jan 29 2016 Remi Collet <remi@fedoraproject.org> - 5.1.6-1
- Update to 5.1.6

* Fri Jan 29 2016 Remi Collet <remi@fedoraproject.org> - 5.1.5-1
- Update to 5.1.5

* Mon Jan 11 2016 Remi Collet <remi@fedoraproject.org> - 5.1.4-1
- Update to 5.1.4

* Thu Dec 10 2015 Remi Collet <remi@fedoraproject.org> - 5.1.3-1
- Update to 5.1.3
- obsolete php-phpunit-PHPUnit-Selenium

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 5.1.2-1
- Update to 5.1.2

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0

* Mon Nov 30 2015 Remi Collet <remi@fedoraproject.org> - 5.0.10-1
- Update to 5.0.10
- run test suite with both PHP 5 and 7 when available

* Wed Nov 11 2015 Remi Collet <remi@fedoraproject.org> - 5.0.9-1
- Update to 5.0.9

* Fri Oct 23 2015 Remi Collet <remi@fedoraproject.org> - 5.0.8-1
- Update to 5.0.8 (no change)

* Thu Oct 22 2015 Remi Collet <remi@fedoraproject.org> - 5.0.7-1
- Update to 5.0.7

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 5.0.6-1
- Update to 5.0.6

* Mon Oct 12 2015 Remi Collet <remi@fedoraproject.org> - 5.0.5-1
- Update to 5.0.5

* Wed Oct  7 2015 Remi Collet <remi@fedoraproject.org> - 5.0.4-1
- Update to 5.0.4

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 5.0.3-1
- Update to 5.0.3 (no change)

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2

* Tue Sep 29 2015 Remi Collet <remi@fedoraproject.org> - 5.0.0-0.1.20150927gite3b3f36
- update to 5.0.0-dev
- raise dependency on PHP >= 5.6
- raise dependency on phpunit/php-code-coverage ~3.0
- raise dependency on phpunit/phpunit-mock-objects ~3.0
- add dependency on sebastian/resource-operations ~1.0
- add dependency on myclabs/deep-copy ~1.3

* Sun Sep 27 2015 Remi Collet <remi@fedoraproject.org> - 4.8.9-2
- add --atleast-version command option, backported from 5.0

* Mon Sep 21 2015 Remi Collet <remi@fedoraproject.org> - 4.8.9-1
- Update to 4.8.9

* Sun Sep 20 2015 Remi Collet <remi@fedoraproject.org> - 4.8.8-1
- Update to 4.8.8

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 4.8.7-1
- Update to 4.8.7 (no change)

* Tue Aug 25 2015 Remi Collet <remi@fedoraproject.org> - 4.8.6-1
- Update to 4.8.6

* Fri Aug 21 2015 Remi Collet <remi@fedoraproject.org> - 4.8.5-1
- Update to 4.8.5 (no change)

* Sat Aug 15 2015 Remi Collet <remi@fedoraproject.org> - 4.8.4-1
- Update to 4.8.4

* Mon Aug 10 2015 Remi Collet <remi@fedoraproject.org> - 4.8.3-1
- Update to 4.8.3

* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2

* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 4.8.1-1
- Update to 4.8.1 (no change)

* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 4.8.0-1
- Update to 4.8.0
- raise dependency on sebastian/environment 1.3
- rely on include_path for all dependencies
- add Changelog in documentation

* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 4.7.7-1
- Update to 4.7.7 (no change)

* Tue Jun 30 2015 Remi Collet <remi@fedoraproject.org> - 4.7.6-1
- Update to 4.7.6

* Tue Jun 30 2015 Remi Collet <remi@fedoraproject.org> - 4.7.5-2
- use $fedoraClassLoader autoloader

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Thu Jun 18 2015 Remi Collet <remi@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4
- raise dependency on phpunit/php-timer >= 1.0.6

* Thu Jun 11 2015 Remi Collet <remi@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3

* Sun Jun  7 2015 Remi Collet <remi@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2

* Fri Jun  5 2015 Remi Collet <remi@fedoraproject.org> - 4.7.1-1
- Update to 4.7.1
- raise dependency on phpunit/php-code-coverage ~2.1
- improve autoloader

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 4.6.10-1
- Update to 4.6.10

* Fri May 29 2015 Remi Collet <remi@fedoraproject.org> - 4.6.9-1
- Update to 4.6.9

* Thu May 28 2015 Remi Collet <remi@fedoraproject.org> - 4.6.8-1
- Update to 4.6.8 (no change)

* Tue May 26 2015 Remi Collet <remi@fedoraproject.org> - 4.6.7-3
- ensure compatibility with SCL

* Tue May 26 2015 Remi Collet <remi@fedoraproject.org> - 4.6.7-2
- detect and redirect to composer installed version #1157910

* Mon May 25 2015 Remi Collet <remi@fedoraproject.org> - 4.6.7-1
- Update to 4.6.7 (no change)

* Thu Apr 30 2015 Remi Collet <remi@fedoraproject.org> - 4.6.6-1
- Update to 4.6.6

* Wed Apr 29 2015 Remi Collet <remi@fedoraproject.org> - 4.6.5-1
- Update to 4.6.5

* Fri Apr 17 2015 Remi Collet <remi@fedoraproject.org> - 4.6.4-2
- keep upstream shebang with /usr/bin/env (for SCL)

* Mon Apr 13 2015 Remi Collet <remi@fedoraproject.org> - 4.6.4-1
- Update to 4.6.4

* Tue Apr  7 2015 Remi Collet <remi@fedoraproject.org> - 4.6.2-1
- Update to 4.6.2

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 4.6.1-1
- Update to 4.6.1

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 4.6.0-1
- Update to 4.6.0
- raise dependencies on file-iterator 1.4 and diff 1.2

* Sun Mar 29 2015 Remi Collet <remi@fedoraproject.org> - 4.5.1-1
- Update to 4.5.1

* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 4.5.0-1
- Update to 4.5.0
- add dependency on phpspec/prophecy
- raise dependencies on sebastian/comparator >= 1.1,
  sebastian/environment >= 1.2, sebastian/exporter >= 1.2
  and doctrine/instantiator >= 1.0.4 (for autoloader file)

* Tue Jan 27 2015 Remi Collet <remi@fedoraproject.org> - 4.4.5-1
- Update to 4.4.5 (no change)

* Tue Jan 27 2015 Remi Collet <remi@fedoraproject.org> - 4.4.4-2
- add dependency on sebastian/recursion-context

* Sun Jan 25 2015 Remi Collet <remi@fedoraproject.org> - 4.4.4-1
- Update to 4.4.4

* Sun Jan 18 2015 Remi Collet <remi@fedoraproject.org> - 4.4.2-1
- Update to 4.4.2

* Sun Dec 28 2014 Remi Collet <remi@fedoraproject.org> - 4.4.1-1
- Update to 4.4.1

* Fri Dec  5 2014 Remi Collet <remi@fedoraproject.org> - 4.4.0-1
- Update to 4.4.0
- add dependency on sebastian/global-state

* Tue Nov 11 2014 Remi Collet <remi@fedoraproject.org> - 4.3.5-1
- Update to 4.3.5
- define date.timezone in phpunit command to avoid warning

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 4.3.4-1
- Update to 4.3.4
- raise dependency on phpunit/php-file-iterator >= 1.3.2

* Fri Oct 17 2014 Remi Collet <remi@fedoraproject.org> - 4.3.3-1
- Update to 4.3.3

* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> - 4.3.2-1
- Update to 4.3.2

* Wed Oct  8 2014 Remi Collet <remi@fedoraproject.org> - 4.3.1-2
- new upstream patch for "no colors" patch
- raise dependency on sebastian/environment >= 1.1

* Mon Oct  6 2014 Remi Collet <remi@fedoraproject.org> - 4.3.1-1
- Update to 4.3.1 (no change)

* Mon Oct  6 2014 Remi Collet <remi@fedoraproject.org> - 4.3.0-2
- only enable colors when output to a terminal (from 4.4)
- open https://github.com/sebastianbergmann/phpunit/pull/1458

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> - 4.3.0-1
- Update to 4.3.0
- drop dependencies on ocramius/instantiator and ocramius/lazy-map
- add dependency on doctrine/instantiator
- raise dependency on phpunit/phpunit-mock-objects >= 2.3

* Sun Sep 14 2014 Remi Collet <remi@fedoraproject.org> - 4.2.6-1
- Update to 4.2.6 (no change)

* Sun Sep  7 2014 Remi Collet <remi@fedoraproject.org> - 4.2.5-1
- Update to 4.2.5 (no change)

* Sun Aug 31 2014 Remi Collet <remi@fedoraproject.org> - 4.2.4-1
- Update to 4.2.4

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> - 4.2.3-1
- Update to 4.2.3

* Mon Aug 18 2014 Remi Collet <remi@fedoraproject.org> - 4.2.2-1
- Update to 4.2.2

* Sun Aug 17 2014 Remi Collet <remi@fedoraproject.org> - 4.2.1-1
- Update to 4.2.1

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 4.2.0-1
- Update to 4.2.0
- raise dependency on phpunit/phpunit-mock-objects >= 2.2
- add dependency on ocramius/instantiator, ocramius/lazy-map
  and symfony/class-loader

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 4.1.4-1
- Update to 4.1.4
- composer dependencies
- add missing documentation and license

* Fri Jun 13 2014 Remi Collet <remi@fedoraproject.org> - 4.1.3-1
- Update to 4.1.3

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> - 4.1.2-1
- Update to 4.1.2 (no change)
- improve test suite bootstraping
- add composer provide

* Mon May 26 2014 Remi Collet <remi@fedoraproject.org> - 4.1.1-1
- Update to 4.1.1

* Tue May  6 2014 Remi Collet <remi@fedoraproject.org> - 4.1.0-2
- fix some autoload issues

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 4.1.0-1
- Update to 4.1.0

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 4.0.18-2
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 4.0.18-1
- update to 4.0.18
- sources from github

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> - 3.7.35-2
- remove message about deprecated PEAR channel

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> - 3.7.35-1
- Update to 3.7.35

* Sun Apr 06 2014 Remi Collet <remi@fedoraproject.org> - 3.7.34-1
- Update to 3.7.34

* Tue Feb 25 2014 Remi Collet <remi@fedoraproject.org> - 3.7.32-1
- Update to 3.7.32 (no change)

* Mon Feb 03 2014 Remi Collet <remi@fedoraproject.org> - 3.7.31-1
- Update to 3.7.31 (no change)

* Fri Jan 31 2014 Remi Collet <remi@fedoraproject.org> - 3.7.30-1
- Update to 3.7.30

* Wed Jan 15 2014 Remi Collet <remi@fedoraproject.org> - 3.7.29-1
- Update to 3.7.29 (stable)

* Thu Oct 17 2013 Remi Collet <remi@fedoraproject.org> - 3.7.28-1
- Update to 3.7.28
- add Spec license header
- open https://github.com/sebastianbergmann/phpunit/issues/1029

* Mon Sep 16 2013 Remi Collet <remi@fedoraproject.org> - 3.7.27-1
- Update to 3.7.27 (no change)

* Fri Sep 13 2013 Remi Collet <remi@fedoraproject.org> - 3.7.26-1
- Update to 3.7.26 (no change)

* Tue Sep 10 2013 Remi Collet <remi@fedoraproject.org> - 3.7.25-1
- Update to 3.7.25 (no change)

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> - 3.7.24-1
- Update to 3.7.24

* Mon Aug 05 2013 Remi Collet <remi@fedoraproject.org> - 3.7.23-1
- Update to 3.7.23
- raise dependency on phpunit/PHP_Timer 1.0.4

* Mon Jul 08 2013 Remi Collet <remi@fedoraproject.org> - 3.7.22-1
- Update to 3.7.22

* Fri May 24 2013 Remi Collet <remi@fedoraproject.org> - 3.7.21-1
- Update to 3.7.21

* Mon May 13 2013 Remi Collet <remi@fedoraproject.org> - 3.7.20-1
- Update to 3.7.20

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 3.7.19-1
- Update to 3.7.19
- requires pear.symfony.com/Yaml >= 2.0.0, <= 2.2.99

* Fri Mar 08 2013 Remi Collet <remi@fedoraproject.org> - 3.7.18-1
- Update to 3.7.18

* Thu Mar 07 2013 Remi Collet <remi@fedoraproject.org> - 3.7.17-1
- Update to 3.7.17

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 3.7.16-1
- Update to 3.7.16

* Tue Mar 05 2013 Remi Collet <remi@fedoraproject.org> - 3.7.15-1
- Update to 3.7.15

* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 3.7.14-1
- Update to 3.7.14

* Sun Jan 13 2013 Remi Collet <remi@fedoraproject.org> - 3.7.13-1
- Version 3.7.13 (stable) - API 3.7.0 (stable)

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 3.7.12-1
- Version 3.7.12 (stable) - API 3.7.0 (stable)

* Wed Jan  9 2013 Remi Collet <remi@fedoraproject.org> - 3.7.11-1
- Version 3.7.11 (stable) - API 3.7.0 (stable)

* Sun Dec  2 2012 Remi Collet <remi@fedoraproject.org> - 3.7.10-1
- Version 3.7.10 (stable) - API 3.7.0 (stable)

* Wed Nov 07 2012 Remi Collet <remi@fedoraproject.org> - 3.7.9-1
- Version 3.7.9 (stable) - API 3.7.0 (stable)

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 3.7.8-1
- Version 3.7.8 (stable) - API 3.7.0 (stable)

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 3.7.7-1
- Version 3.7.7 (stable) - API 3.7.0 (stable)

* Sun Oct  7 2012 Remi Collet <remi@fedoraproject.org> - 3.7.6-1
- Version 3.7.6 (stable) - API 3.7.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 3.7.5-1
- Version 3.7.5 (stable) - API 3.7.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 3.7.4-1
- Version 3.7.4 (stable) - API 3.7.0 (stable)
- add Conflicts for max version of PHP_CodeCoverage and PHPUnit_MockObject

* Thu Sep 20 2012 Remi Collet <remi@fedoraproject.org> - 3.7.1-1
- Version 3.7.1 (stable) - API 3.7.0 (stable)
- raise dependencies: php 5.3.3, PHP_CodeCoverage 1.2.1,
  PHP_Timer 1.0.2, Yaml 2.1.0 (instead of YAML from symfony 1)

* Sat Aug 04 2012 Remi Collet <remi@fedoraproject.org> - 3.6.12-1
- Version 3.6.12 (stable) - API 3.6.0 (stable)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Remi Collet <remi@fedoraproject.org> - 3.6.11-1
- Version 3.6.11 (stable) - API 3.6.0 (stable)

* Fri Jan 27 2012 Remi Collet <remi@fedoraproject.org> - 3.6.10-1
- Version 3.6.10 (stable) - API 3.6.0 (stable)
- raise PHP_Invokers >= 1.1.0

* Tue Jan 24 2012 Remi Collet <remi@fedoraproject.org> - 3.6.9-1
- Version 3.6.9 (stable) - API 3.6.0 (stable)

* Sat Jan 21 2012 Remi Collet <remi@fedoraproject.org> - 3.6.8-1
- Version 3.6.8 (stable) - API 3.6.0 (stable)

* Thu Jan 05 2012 Remi Collet <remi@fedoraproject.org> - 3.6.7-1
- Version 3.6.7 (stable) - API 3.6.0 (stable)

* Mon Jan 02 2012 Remi Collet <remi@fedoraproject.org> - 3.6.6-1
- Version 3.6.6 (stable) - API 3.6.0 (stable)

* Mon Dec 19 2011 Remi Collet <remi@fedoraproject.org> - 3.6.5-1
- Version 3.6.5 (stable) - API 3.6.0 (stable)

* Sat Nov 26 2011 Remi Collet <remi@fedoraproject.org> - 3.6.4-1
- Version 3.6.4 (stable) - API 3.6.0 (stable)

* Fri Nov 11 2011 Remi Collet <remi@fedoraproject.org> - 3.6.3-1
- Version 3.6.3 (stable) - API 3.6.0 (stable)

* Fri Nov 04 2011 Remi Collet <remi@fedoraproject.org> - 3.6.2-1
- Version 3.6.2 (stable) - API 3.6.0 (stable)

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 3.6.0-1
- Version 3.6.0 (stable) - API 3.6.0 (stable)

* Fri Aug 19 2011 Remi Collet <remi@fedoraproject.org> - 3.5.15-1
- Version 3.5.15 (stable) - API 3.5.7 (stable)
- raise PEAR dependency to 1.9.3

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.14-1
- Version 3.5.14 (stable) - API 3.5.7 (stable)

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.13-2
- rebuild for doc in /usr/share/doc/pear

* Tue Mar  8 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.13-1
- Version 3.5.13 (stable) - API 3.5.7 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2
- remove duplicate dependency (YAML)

* Thu Feb 24 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.12-1
- Version 3.5.12 (stable) - API 3.5.7 (stable)

* Wed Feb 16 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.11-1
- Version 3.5.11 (stable) - API 3.5.7 (stable)
- new dependency on php-pear(XML_RPC2)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.10-1
- Version 3.5.10 (stable) - API 3.5.7 (stable)

* Tue Jan 18 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.9-1
- Version 3.5.9 (stable) - API 3.5.7 (stable)

* Tue Jan 11 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.7-1
- Version 3.5.7 (stable) - API 3.5.7 (stable)
- README, CHANGELOG and LICENSE are now in the tarball

* Mon Dec 20 2010 Remi Collet <Fedora@famillecollet.com> - 3.5.6-1
- Version 3.5.6 (stable) - API 3.5.4 (stable)
- move README.mardown to README (was Changelog, now links to doc)
- add CHANGELOG
- not more doc provided by upstream

* Mon Nov 22 2010 Remi Collet <Fedora@famillecollet.com> - 3.5.5-1
- Version 3.5.5 (stable) - API 3.5.4 (stable)

* Wed Nov 17 2010 Remi Collet <Fedora@famillecollet.com> - 3.5.4-1
- Version 3.5.4 (stable) - API 3.5.4 (stable)

* Wed Oct 27 2010 Remi Collet <Fedora@famillecollet.com> - 3.5.3-1
- Update to 3.5.3
- new requires and new packages for extensions of PHPUnit
  PHPUnit_MockObject, PHPUnit_Selenium, DbUnit
- lower PEAR dependency to allow el6 build
- define timezone during build

* Thu Jul 22 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.15-1
- Update to 3.4.15

* Sat Jun 19 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.14-1
- Update to 3.4.14

* Sat May 22 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.13-1
- Update to 3.4.13
- add README.markdown (Changelog)

* Wed Apr 07 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.12-1
- Update to 3.4.12

* Thu Feb 18 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.11-1.1
- Update to 3.4.11

* Wed Feb 10 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.10-1
- Update to 3.4.10

* Sun Jan 24 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.9-1
- Update to 3.4.9

* Sat Jan 16 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.7-1
- Update to 3.4.7
- rename from php-pear-PHPUnit to php-phpunit-PHPUnit
- update dependencies (PEAR 1.8.1, YAML, php-soap)

* Sat Sep 12 2009 Christopher Stone <chris.stone@gmail.com> 3.3.17-1
- Upstream sync

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 02 2009 Remi Collet <Fedora@famillecollet.com> - 3.3.16-1
- Upstream sync
- Fix requires (remove hint) and raise PEAR version to 1.7.1
- rename %%{pear_name}.xml to %%{name}.xml

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov  8 2008 Christopher Stone <chris.stone@gmail.com> 3.3.4-1
- Upstream sync

* Thu Oct 23 2008 Christopher Stone <chris.stone@gmail.com> 3.3.2-1
- Upstream sync
- Remove no longer needed Obsolete/Provides

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 3.3.1-1
- Upstream sync

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 3.2.21-1
- Upstream sync
- Add php-xml to Requires (bz #464758)

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 3.2.19-1
- Upstream sync

* Thu Feb 21 2008 Christopher Stone <chris.stone@gmail.com> 3.2.15-1
- Upstream sync

* Wed Feb 13 2008 Christopher Stone <chris.stone@gmail.com> 3.2.13-1
- Upstream sync

* Sun Nov 25 2007 Christopher Stone <chris.stone@gmail.com> 3.2.1-1
- Upstream sync

* Sat Sep 08 2007 Christopher Stone <chris.stone@gmail.com> 3.1.8-1
- Upstream sync

* Sun May 06 2007 Christopher Stone <chris.stone@gmail.com> 3.0.6-1
- Upstream sync

* Thu Mar 08 2007 Christopher Stone <chris.stone@gmail.com> 3.0.5-3
- Fix testdir
- Fix Provides version

* Wed Mar 07 2007 Christopher Stone <chris.stone@gmail.com> 3.0.5-2
- Add Obsoletes/Provides for php-pear(PHPUnit2)
- Requires php-pear(PEAR) >= 1.5.0
- Own %%{pear_testdir}/%%{pear_name}
- Remove no longer needed manual channel install
- Simplify %%doc
- Only unregister old phpunit on upgrade

* Mon Feb 26 2007 Christopher Stone <chris.stone@gmail.com> 3.0.5-1
- Upstream sync

* Wed Feb 21 2007 Christohper Stone <chris.stone@gmail.com> 3.0.4-1
- Upstream sync

* Mon Jan 29 2007 Christopher Stone <chris.stone@gmail.com> 3.0.3-1
- Upstream sync

* Sun Jan 14 2007 Christopher Stone <chris.stone@gmail.com> 3.0.2-1
- Upstream sync

* Fri Jan 05 2007 Christopher Stone <chris.stone@gmail.com> 3.0.1-1
- Upstream sync

* Wed Dec 27 2006 Christopher Stone <chris.stone@gmail.com> 3.0.0-1
- Initial Release
