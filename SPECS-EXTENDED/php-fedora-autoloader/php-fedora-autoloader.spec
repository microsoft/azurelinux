Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# Fedora spec file for php-fedora-autoloader
#
# Copyright (c) 2016-2020 Shawn Iwinski <shawn@iwin.ski>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     php-fedora
%global github_name      autoloader
%global github_version   1.0.1
%global github_commit    7cd61b5a927c8f446df8e820aa288434e18a7f0c

%global composer_vendor  fedora
%global composer_project autoloader

# "php": ">= 5.3.3"
%global php_min_ver 5.3.3
# "theseer/autoload": "^1.22"
%global phpab_min_ver 1.22
%global phpab_max_ver 2.0

%{!?phpdir:  %global phpdir  %{_datadir}/php}
%global  phpab_template_dir  %{phpdir}/TheSeer/Autoload/templates/ci

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       3%{?dist}
Summary:       Fedora Autoloader

License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_check}
BuildRequires: php-cli
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
%if 0%{?fedora} >= 26 || 0%{?rhel} >= 8
%global phpunit %{_bindir}/phpunit6
%else
%global phpunit %{_bindir}/phpunit
%endif
BuildRequires: %{phpunit}
BuildRequires: php-composer(theseer/autoload) >= %{phpab_min_ver}
BuildRequires: php-pear
## phpcompatinfo (computed from version 1.0.1)
BuildRequires: php-ctype
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.0.1)
Requires:      php-ctype
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Static PSR-4 [1], PSR-0 [2], and classmap autoloader.  Includes loader for
required and optional dependencies.

[1] http://www.php-fig.org/psr/psr-4/
[2] http://www.php-fig.org/psr/psr-0/

# ------------------------------------------------------------------------------


%package devel

Summary: %{name} devel

Requires: %{name} = %{version}-%{release}
Requires: php-composer(theseer/autoload) >= %{phpab_min_ver}
Requires: php-composer(theseer/autoload) <  %{phpab_max_ver}

%description devel
Provides needed tools to build other packages:
- phpab fedora template


# ------------------------------------------------------------------------------


%prep
%setup -qn %{github_name}-%{github_commit}

: Set autoload path in phpab templates
sed "s#___AUTOLOAD_PATH___#'Fedora/Autoloader'#" \
    res/phpab/fedora.php.tpl >res/phpab/fedora2.php.tpl
sed "s#___AUTOLOAD_PATH___#'%{phpdir}/Fedora/Autoloader'#" \
    -i res/phpab/fedora.php.tpl


%build
# Empty build section, nothing to build


%install
: Main
mkdir -p %{buildroot}%{phpdir}/Fedora/Autoloader
cp -rp src/* %{buildroot}%{phpdir}/Fedora/Autoloader/

: Devel
mkdir -p %{buildroot}%{phpab_template_dir}
cp -p res/phpab/fedora*.php.tpl %{buildroot}%{phpab_template_dir}/


%check
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require '%{buildroot}%{phpdir}/Fedora/Autoloader/autoload.php';

if (!class_exists('PHPUnit\\Framework\\TestCase')) {
  class_alias('PHPUnit_Framework_TestCase', 'PHPUnit\\Framework\\TestCase');
}
BOOTSTRAP

: Upstream tests
RETURN_CODE=0
for PHP_EXEC in "php %{phpunit}" %{?rhel:php54 php55 php56} php70 "php71 %{_bindir}/phpunit6" "php72 %{_bindir}/phpunit6" "php73 %{_bindir}/phpunit6" "php74 %{_bindir}/phpunit6"; do
    set $PHP_EXEC
    if [ "php" == "$1" ] || which $PHP_EXEC; then
        $1 -d include_path=.:%{buildroot}%{phpdir}:%{phpdir}:%{_datadir}/pear \
            ${2:-%{_bindir}/phpunit} \
                --bootstrap bootstrap.php \
                --verbose
    fi
done
exit $RETURN_CODE


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%dir %{phpdir}/Fedora
     %{phpdir}/Fedora/Autoloader

%files devel
%doc *.md
%doc composer.json
%{phpab_template_dir}/fedora*.php.tpl


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Feb 12 2020 Shawn Iwinski <shawn@iwin.ski> - 1.0.1-2
- Add tests bootstrap to fix EPEL6 build

* Wed Feb 12 2020 Shawn Iwinski <shawn@iwin.ski> - 1.0.1-1
- Update to 1.0.1 (RHBZ #1802372)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec  4 2018 Remi Collet <remi@remirepo.net> - 1.0.0-5
- cleanup for EL-8

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 04 2017 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-1
- Update to 1.0.0

* Tue Mar 28 2017 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-0.1.rc1
- Update to 1.0.0-rc1
- Test with SCLs if available
- Add fedora2 template relying on include_path

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 28 2016 Shawn Iwinski <shawn@iwin.ski> - 0.2.1-2
- Do not install tests into buildroot

* Fri Oct 28 2016 Shawn Iwinski <shawn@iwin.ski> - 0.2.1-1
- Update to 0.2.1
- Remove applied patches that are included in 0.2.1
- Re-add custom include_path and bootstrap for tests
- Add php-cli build dependency

* Thu Oct 27 2016 Shawn Iwinski <shawn@iwin.ski> - 0.2.0-5
- Add upstream patch "Remove self-autoload constant and prepend
  self-autoload PSR-4 register"
- Remove custom include_path and bootstrap for tests

* Thu Oct 27 2016 Remi Collet <remi@fedoraproject.org> - 0.2.0-4
- workaround when not in global autoloader

* Wed Oct 26 2016 Shawn Iwinski <shawn@iwin.ski> - 0.2.0-3
- Update to 0.2.0
- Remove applied patches that are included in 0.2.0

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 0.1.2-3
- rename 1 method to avoid conflicts with symfony

* Sat Oct 22 2016 Remi Collet <remi@fedoraproject.org> - 0.1.2-2
- ensure we use newly installed autoloader in buildroot

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 0.1.2-1
- update to 0.1.2

* Wed Oct 19 2016 Shawn Iwinski <shawn@iwin.ski> - 0.1.1-1
- Update to 0.1.1
- Fix phpab template
- Move docs to devel subpackage

* Wed Oct 19 2016 Shawn Iwinski <shawn@iwin.ski> - 0.1.0-1
- Initial package
