# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-myclabs-deep-copy
#
# SPDX-FileCopyrightText:  Copyright 2015-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#
%bcond_without       tests

%global gh_commit    07d290f0c47959fd5eed98c95ee5602db07e0b6a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     myclabs
%global gh_project   DeepCopy
%global c_project    deep-copy
%global major        %nil
%global php_home     %{_datadir}/php

Name:           php-myclabs-deep-copy%{major}
Version:        1.13.4
Release:        1%{?dist}

Summary:        Create deep copies (clones) of your objects

License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snashop to get upstream test suite
Source0:        php-myclabs-deep-copy-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
%if %{with tests}
# For tests
BuildRequires:  php(language) >= 7.1
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "doctrine/collections": "^1.6.8",
#        "doctrine/common": "^2.13.3 || ^3.2.2",
#        "phpspec/prophecy": "^1.10",
#        "phpunit/phpunit": "^7.5.20 || ^8.5.23 || ^9.5.13"
BuildRequires: (php-composer(phpspec/prophecy)     >= 1.10  with php-composer(phpspec/prophecy)     < 2)
BuildRequires:  phpunit9 >= 9.5.13
%endif
# For autoloader
BuildRequires:  php-fedora-autoloader-devel

# From composer.json, "require": {
#        "php": "^7.1 || ^8.0"
Requires:       php(language) >= 7.1
# From phpcompatinfo report for version 1.8.0
Requires:       php-reflection
Requires:       php-date
Requires:       php-spl
# Required by autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{gh_owner}/%{c_project}) = %{version}


%description
DeepCopy helps you create deep copies (clones) of your objects.
It is designed to handle cycles in the association graph.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
phpab --template fedora --output src/%{gh_project}/autoload.php src/%{gh_project}
cat << 'EOF' | tee -a src/%{gh_project}/autoload.php
require_once __DIR__ . '/deep_copy.php';
EOF


%install
: Library
mkdir -p %{buildroot}%{php_home}
cp -pr src/%{gh_project} %{buildroot}%{php_home}/%{gh_project}%{major}


%check
%if %{with tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{php_home}/%{gh_project}%{major}/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('DeepCopy\\', dirname(__DIR__).'/fixtures/');
\Fedora\Autoloader\Autoload::addPsr4('DeepCopyTest\\', dirname(__DIR__).'/tests/DeepCopyTest/');
\Fedora\Autoloader\Dependencies::required([
    '%{php_home}/Prophecy/autoload.php',
]);
EOF

# disable doctrine related tests
rm -r tests/DeepCopyTest/Matcher/Doctrine \
      tests/DeepCopyTest/Filter/Doctrine

ret=0
for cmd in php php81 php82 php83 php84 php85; do
  if which $cmd; then
    $cmd -d auto_prepend_file=vendor/autoload.php \
       %{_bindir}/phpunit9 \
         --filter '^((?!(test_it_can_apply_two_filters_with_chainable_filter|test_it_can_copy_property_after_applying_doctrine_proxy_filter_with_chainable_filter)).)*$' \
         --verbose || ret=1
  fi
done
exit $ret
%else
: Test suite disabled
%endif


%files
%license LICENSE
%doc composer.json
%doc README.md
%{php_home}/%{gh_project}%{major}


%changelog
* Fri Aug  1 2025 Remi Collet <remi@remirepo.net> - 1.13.4-1
- update to 1.13.4

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul  7 2025 Remi Collet <remi@remirepo.net> - 1.13.3-1
- update to 1.13.3

* Sun May  4 2025 Remi Collet <remi@remirepo.net> - 1.13.1-1
- update to 1.13.1

* Wed Feb 12 2025 Remi Collet <remi@remirepo.net> - 1.13.0-1
- update to 1.13.0
- re-license spec file to CECILL-2.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 12 2024 Remi Collet <remi@remirepo.net> - 1.12.1-1
- update to 1.12.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 13 2024 Remi Collet <remi@remirepo.net> - 1.12.0-2
- update to 1.12.0
- disable test suite
- use classmap autoloader

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar  8 2023 Remi Collet <remi@remirepo.net> - 1.11.1-1
- update to 1.11.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar  3 2022 Remi Collet <remi@remirepo.net> - 1.11.0-1
- update to 1.11.0

* Thu Mar  3 2022 Remi Collet <remi@remirepo.net> - 1.10.3-1
- update to 1.10.3
- switch to phpunit9 and doctrine/common v3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Nov 14 2020 Remi Collet <remi@remirepo.net> - 1.10.2-1
- update to 1.10.2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Remi Collet <remi@remirepo.net> - 1.10.1-1
- update to 1.10.1

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 1.10.0-2
- update to 1.10.0 (no change)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Remi Collet <remi@remirepo.net> - 1.9.5-1
- update to 1.9.5

* Mon Dec 16 2019 Remi Collet <remi@remirepo.net> - 1.9.4-1
- update to 1.9.4

* Mon Aug 12 2019 Remi Collet <remi@remirepo.net> - 1.9.3-1
- update to 1.9.3 (no change)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 15 2019 Remi Collet <remi@remirepo.net> - 1.9.1-1
- update to 1.9.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Remi Collet <remi@remirepo.net> - 1.8.1-1
- update to 1.8.1

* Wed May 30 2018 Remi Collet <remi@remirepo.net> - 1.8.0-1
- update to 1.8.0 (no change)
- raise dependency on PHP 7.1
- use phpunit7

* Wed May 30 2018 Remi Collet <remi@remirepo.net> - 1.8.0-0
- update to 1.8.0 (no change)
- boostrap build using phpunit6 (rely on include_path)
- fix autoloader to avoid duplicate definition

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 20 2017 Remi Collet <remi@remirepo.net> - 1.7.0-1
- Update to 1.7.0
- raise dependency on PHP 5.6

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 13 2017 Remi Collet <remi@remirepo.net> - 1.6.1-1
- Update to 1.6.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0

* Tue Nov  1 2016 Remi Collet <remi@fedoraproject.org> - 1.5.5-1
- update to 1.5.5
- switch to fedora/autoloader

* Mon Sep 19 2016 Remi Collet <remi@fedoraproject.org> - 1.5.4-1
- update to 1.5.4

* Tue Sep 13 2016 Remi Collet <remi@fedoraproject.org> - 1.5.3-1
- update to 1.5.3

* Wed Sep  7 2016 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- update to 1.5.2

* Mon May  2 2016 Remi Collet <remi@fedoraproject.org> - 1.5.1-1
- update to 1.5.1
- run test suite with both PHP 5 and 7 when available

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov  8 2015 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Mon Oct  5 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Mon Jul 20 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1 (no change, pr #14 merged)

* Sat Jul  4 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- initial package, version 1.3.0
- open https://github.com/myclabs/DeepCopy/pull/14 - fix perms
