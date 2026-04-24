# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-object-enumerator3
#
# Copyright (c) 2015-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    ac5b293dba925751b808e02923399fb44ff0d541
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   object-enumerator
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
%global major        3
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   ObjectEnumerator
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

# NOTICE: used by phpunit 6, 7 and 8

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        3.0.5
Release: 5%{?dist}
Summary:        Traverses array and object to enumerate all referenced objects, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 7.0
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
BuildRequires:  (php-composer(%{pk_vendor}/object-reflector) >= 1.1.1 with php-composer(%{pk_vendor}/object-reflector) < 2)
BuildRequires:  (php-composer(sebastian/recursion-context)   >= 3.0   with php-composer(sebastian/recursion-context)   < 4)
# From composer.json"require-dev": {
#        "phpunit/phpunit": "^6.0"
BuildRequires:  phpunit8
%endif

# from composer.json
#        "php": ">=7.0",
#        "sebastian/object-reflector": "^1.1.1",
#        "sebastian/recursion-context": "^3.0"
Requires:       php(language) >= 7.0
Requires:       (php-composer(%{pk_vendor}/object-reflector) >= 1.1.1 with php-composer(%{pk_vendor}/object-reflector) < 2)
Requires:       (php-composer(sebastian/recursion-context)   >= 3.0   with php-composer(sebastian/recursion-context)   < 4)
# from phpcompatinfo report for version 3.0.1:
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Traverses array structures and object graphs to enumerate all
referenced objects.

This package provides the version %{major} of the library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader, from composer.json "autoload": {
#        "classmap": [
#            "src/"
%{_bindir}/phpab --template fedora --output src/autoload.php src
cat << 'EOF' | tee -a src/autoload.php
// Dependencies
require_once '%{php_home}/%{ns_vendor}/ObjectReflector/autoload.php';
require_once '%{php_home}/%{ns_vendor}/RecursionContext3/autoload.php';
EOF


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with_tests}
mkdir vendor
%{_bindir}/phpab --template fedora --output vendor/autoload.php tests/_fixture

: Fix for phpunit8
find tests/ -name \*php -exec sed -e 's/setUp()/setUp():void/'  -i {} \;

: Run upstream test suite
ret=0
for cmd in php php81 php82 php83; do
  if which $cmd; then
    %{_bindir}/php -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
    %{_bindir}/phpunit8	  --verbose || ret=1
  fi
done
exit $ret
%else
: bootstrap build with test suite disabled
%endif


%files
%license LICENSE
%doc README.md composer.json
%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar  1 2024 Remi Collet <remi@remirepo.net> - 3.0.5-1
- update to 3.0.5 (no change)
- sources from git snapshot

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 21 2023 Remi Collet <remi@remirepo.net> - 3.0.4-9
- use SPDX License id

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 10 2021 Remi Collet <remi@remirepo.net> - 3.0.4-4
- switch to phpunit8

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Remi Collet <remi@remirepo.net> - 3.0.4-1
- update to 3.0.4 (no change)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec  6 2018 Remi Collet <remi@remirepo.net> - 3.0.3-3
- cleanup for EL-8

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb  6 2018 Remi Collet <remi@remirepo.net> - 3.0.3-2
- use range dependencies on F27+

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 3.0.3-1
- Update to 3.0.3 - no change
- raise dependency on sebastian/object-reflector 1.1.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 12 2017 Remi Collet <remi@remirepo.net> - 3.0.2-1
- Update to 3.0.2
- add dependency on sebastian/object-reflector

* Sun Mar 12 2017 Remi Collet <remi@remirepo.net> - 3.0.1-1
- Update to 3.0.1

* Fri Mar  3 2017 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0
- rename to php-sebastian-object-enumerator3
- raise dependency on PHP 7
- raise dependency on recursion-context 3

* Sat Feb 18 2017 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 (no change)
- raise dependency on sebastian/recursion-context 2.0

* Wed Nov 16 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- raise dependency on sebastian/recursion-context 1.0.4

* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- switch to fedora/autoloader

* Wed Mar 23 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

