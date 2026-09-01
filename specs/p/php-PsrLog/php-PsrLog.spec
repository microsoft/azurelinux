# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Fedora spec file for php-PsrLog
#
# Copyright (c) 2013-2021 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#

%global github_owner     php-fig
%global github_name      log
%global github_version   1.1.4
%global github_commit    d49695b909c3b7628b6289db5479a1c204601f11

%global composer_vendor  psr
%global composer_project log

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:      php-PsrLog
Version:   %{github_version}
Release:   11%{?dist}
Summary:   Common interface for logging libraries

License:   MIT
URL:       https://www.php-fig.org/psr/psr-3/
Source0:   https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch: noarch
# For tests
BuildRequires:  php-cli
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)

Requires:  php(language) >= 5.3.0
# phpcompatinfo requires (computed from version 1.1.0)
Requires:  php-date
Requires:  php-pcre
Requires:  php-spl
# Autoloader
Requires:  php-composer(fedora/autoloader)

# php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}
Provides:  php-%{composer_vendor}-%{composer_project}           = %{version}-%{release}
# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
This package holds all interfaces/classes/traits related to PSR-3 [1].

Note that this is not a logger of its own. It is merely an interface that
describes a logger. See the specification for more details.

[1] https://www.php-fig.org/psr/psr-3/


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee Psr/Log/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!class_exists('Fedora\\Autoloader\\Autoload', false)) {
    require_once '%{phpdir}/Fedora/Autoloader/autoload.php';
}

\Fedora\Autoloader\Autoload::addPsr4('Psr\\Log\\', __DIR__);
AUTOLOAD


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -rp Psr %{buildroot}%{_datadir}/php/


%check
: Check if our autoloader works
php -r '
require "%{buildroot}%{_datadir}/php/Psr/Log/autoload.php";
$a = new Psr\Log\NullLogger();
echo "Ok\n";
exit(0);
'


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{_datadir}/php/Psr
     %{_datadir}/php/Psr/Log


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May  3 2021 Remi Collet <remi@remirepo.net> - 1.1.4-1
- update to 1.1.4

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 24 2020 Remi Collet <remi@remirepo.net> - 1.1.3-1
- update to 1.1.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov  4 2019 Remi Collet <remi@remirepo.net> - 1.1.2-1
- update to 1.1.2

* Fri Oct 25 2019 Remi Collet <remi@remirepo.net> - 1.1.1-1
- update to 1.1.1

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 22 2018 Remi Collet <remi@remirepo.net> - 1.1.0-1
- update to 1.1.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- update to 1.0.2
- switch from symfony/class-loader to fedora/autoloader
- add minimal %%check for autoloader

* Sun Sep 25 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-1
- Updated to 1.0.1 (RHBZ #1377513)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-9
- Added php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT} ("php-psr-log") virtual provide
- %%license usage

* Mon Nov 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-8
- Added autoloader

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-6
- Replaced single-use %%composer_vendor and %%composer_project

* Fri Jun 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-5
- Updated URL
- Requires php-common => php(language)
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-2
- Updated URL
- Added php-date require

* Thu Jan 10 2013 Shawn Iwinski <shawn.iwiinski@gmail.com> - 1.0.0-1
- Initial package
