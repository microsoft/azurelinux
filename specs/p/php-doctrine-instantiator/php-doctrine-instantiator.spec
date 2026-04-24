# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-doctrine-instantiator
#
# Copyright (c) 2014-2023 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# bootstrap needed when rebuilding PHPUnit for new major version
%global bootstrap    0
%global gh_commit    0a0fa9780f5d4e507415a065172d26a98d02047b
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     doctrine
%global gh_project   instantiator
%global major        %nil
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-doctrine-instantiator
Version:        1.5.0
Release: 9%{?dist}
Summary:        Instantiate objects in PHP without invoking their constructors

License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        php-%{gh_owner}-%{gh_project}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
BuildRequires:  php(language) >= 7.1
BuildRequires:  php-phar
BuildRequires:  php-pdo
BuildRequires:  php-reflection
BuildRequires:  php-spl
%global phpunit %{_bindir}/phpunit9
BuildRequires:  %{phpunit}
%endif

# From composer.json
#        "php": "^7.1 || ^8.0"
Requires:       php(language) >= 7.1
# From phpcompatinfo report for version 1.1.0
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Obsoletes:      php-doctrine-instantiator11 < %{version}-%{release}
Provides:       php-doctrine-instantiator11 = %{version}-%{release}
Provides:       php-composer(doctrine/instantiator) = %{version}


%description
This library provides a way of avoiding usage of constructors when
instantiating PHP classes.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a simple autoloader
%{_bindir}/phpab \
    --output src/Doctrine/Instantiator/autoload.php \
    --template fedora \
    src/Doctrine/Instantiator


%install
mkdir -p                         %{buildroot}%{_datadir}/php/Doctrine
cp -pr src/Doctrine/Instantiator %{buildroot}%{_datadir}/php/Doctrine/Instantiator%{major}


%check
%if %{with_tests}
: Generate autoloader
mkdir vendor
%{_bindir}/phpab \
    --output vendor/autoload.php \
    --template fedora \
    tests
cat << 'EOF' | tee -a vendor/autoload.php
require "%{buildroot}%{_datadir}/php/Doctrine/Instantiator/autoload.php";
Fedora\Autoloader\Autoload::addPsr0('DoctrineTest\\InstantiatorPerformance\\', dirname(__DIR__).'/tests');
Fedora\Autoloader\Autoload::addPsr0('DoctrineTest\\InstantiatorTest\\', dirname(__DIR__).'/tests');
Fedora\Autoloader\Autoload::addPsr0('DoctrineTest\\InstantiatorTestAsset\\', dirname(__DIR__).'/tests');
EOF

: Run test suite
ret=0
for cmdarg in "php %{phpunit}" php80 php81 php82; do
  if which $cmdarg; then
    set $cmdarg
    $1 -d auto_prepend_file=vendor/autoload.php \
      ${2:-%{_bindir}/phpunit9} \
        --verbose || ret=1
  fi
done
exit $ret
%else
: Test suite disabled
%endif


%files
%license LICENSE
%doc *.md composer.json
%dir %{_datadir}/php/Doctrine
     %{_datadir}/php/Doctrine/Instantiator%{major}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan  3 2023 Remi Collet <remi@remirepo.net> - 1.5.0-1
- update to 1.5.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar  3 2022 Remi Collet <remi@remirepo.net> - 1.4.1-1
- update to 1.4.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Remi Collet <remi@remirepo.net> - 1.4.0-1
- update to 1.4.0 (no change)
- switch to phpunit9

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun  2 2020 Remi Collet <remi@remirepo.net> - 1.3.1-1
- update to 1.3.1 (no change)
- switch to phpunit8

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 13 2019 Remi Collet <remi@remirepo.net> - 1.3.0-1
- update to 1.3.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 25 2019 Remi Collet <remi@remirepo.net> - 1.2.0-1
- update to 1.2.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 1.1.0-1
- Update to 1.1.0
- raise dependency on PHP 7.1
- switch to phpunit6
- use git snapshot for sources

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- update to 1.0.5
- improve test suite during the build

* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4 (no change)
- add autoloader

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3

* Mon Aug 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- initial package, version 1.0.2
