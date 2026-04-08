# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-doctrine-deprecations
#
# SPDX-FileCopyrightText:  Copyright 2021-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    d4fe3e6fd9bb9e72557a19674f44d8ac7db4c6ca
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     doctrine
%global gh_project   deprecations
# packagist
%global pk_vendor    %{gh_owner}
%global pk_project   %{gh_project}
# Namespace
%global ns_vendor    Doctrine
%global ns_project   Deprecations

Name:           php-%{pk_vendor}-%{pk_project}
Version:        1.1.6
Release:        1%{?dist}
Summary:        A small layer on top of triggeFr_error or PSR-3 logging

License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 7.1
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# From composer.json
#    "require-dev": {
#        "doctrine/coding-standard": "^9 || ^12 || ^14",
#        "phpstan/phpstan": "1.4.10 || 2.1.30",
#        "phpstan/phpstan-phpunit": "^1.0 || ^2",
#        "phpunit/phpunit": "^7.5 || ^8.5 || ^9.6 || ^10.5 || ^11.5 || ^12.4 || ^13.0",
#        "psr/log": "^1 || ^2 || ^3"
BuildRequires: (php-composer(psr/log) >= 1.0   with php-composer(psr/log) < 4)
%global phpunit %{_bindir}/phpunit12
BuildRequires:  phpunit12
%endif

# From composer.json
#    "require": {
#        "php": "^7.1 || ^8.0",
#    "suggest": {
#        "psr/log": "Allows logging deprecations via PSR-3 logger implementation"

Requires:       php(language) >= 7.1
Requires:      (php-composer(psr/log) >= 1.0   with php-composer(psr/log) < 4)
# From phpcompatinfo report for version 0.5.3
# Only core and standard

# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
A small (side-effect free by default) layer on top of
trigger_error(E_USER_DEPRECATED) or PSR-3 logging.

* no side-effects by default, making it a perfect fit for libraries
  that don't know how the error handler works they operate under
* options to avoid having to rely on error handlers global state by
  using PSR-3 logging
* deduplicate deprecation messages to avoid excessive triggering and
  reduce overhead

We recommend to collect Deprecations using a PSR logger instead of
relying on the global error handler.

Autoloader: %{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a simple autoloader
%{_bindir}/phpab \
    --output src/autoload.php \
    --template fedora \
    src

cat << 'EOF' | tee -a src/autoload.php

\Fedora\Autoloader\Dependencies::required([
    [
        '%{_datadir}/php/Psr/Log3/autoload.php',
        '%{_datadir}/php/Psr/Log2/autoload.php',
        '%{_datadir}/php/Psr/Log/autoload.php',
    ],
]);
EOF


%install
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}


%check
%if %{with tests}
: Generate autoloader
mkdir vendor
%{_bindir}/phpab \
    --output vendor/autoload.php \
    --template fedora \
    test_fixtures/src \
    test_fixtures/vendor/doctrine/foo

cat << 'EOF' | tee -a vendor/autoload.php
\Fedora\Autoloader\Dependencies::required([
    '%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php',
]);
EOF

ret=0
for cmd in "php %{phpunit}" "php82 %{_bindir}/phpunit11" "php83 %{_bindir}/phpunit12" "php84 %{_bindir}/phpunit12" "php85 %{_bindir}/phpunit13"; do
  if which $cmd; then
    set $cmd
    $1 -d auto_prepend_file=vendor/autoload.php \
      $2 \
        --filter '^((?!(testDeprecationTrackByEnv)).)*$' \
        || ret=1
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
%{_datadir}/php/%{ns_vendor}/%{ns_project}/


%changelog
* Mon Feb  9 2026 Remi Collet <remi@remirepo.net> - 1.1.6-1
- update to 1.1.6

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr  8 2025 Remi Collet <remi@remirepo.net> - 1.1.5-1
- update to 1.1.5 (no change)
- switch to phpunit12

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec  9 2024 Remi Collet <remi@remirepo.net> - 1.1.4-1
- update to 1.1.4
- re-license spec file to CECILL-2.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 31 2024 Remi Collet <remi@remirepo.net> - 1.1.3-1
- update to 1.1.3 (no change)
- Fix FTBFS #2261475

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 28 2023 Remi Collet <remi@remirepo.net> - 1.1.2-1
- update to 1.1.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun  5 2023 Remi Collet <remi@remirepo.net> - 1.1.1-1
- update to 1.1.1

* Tue May 30 2023 Remi Collet <remi@remirepo.net> - 1.1.0-1
- update to 1.1.0

* Thu Apr 20 2023 Remi Collet <remi@remirepo.net> - 1.0.0-4
- add upstream patch for test suite with PHP 8.2 #2171642

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May  3 2022 Remi Collet <remi@remirepo.net> - 1.0.0-1
- update to 1.0.0
- allow psr/log 2 and 3
- drop patch merged upstream

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 31 2021 Remi Collet <remi@remirepo.net> - 0.5.3-2
- add LICENSE file copy/pasted from other doctrine project,
  and from https://github.com/doctrine/deprecations/pull/27

* Tue Mar 30 2021 Remi Collet <remi@remirepo.net> - 0.5.3-1
- initial package
- open https://github.com/doctrine/deprecations/issues/26 missing License
