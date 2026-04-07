# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-version4
#
# Copyright (c) 2013-2023 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    c51fa83a5d8f43f1402e3f32a005e6262244ef17
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   version
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace (fake ns_project as not PSR-4 compliant)
%global ns_vendor    SebastianBergmann
%global ns_project   Version
%global ver_major    4
%global php_home     %{_datadir}/php


Name:           php-%{pk_vendor}-%{pk_project}%{ver_major}
Version:        4.0.1
Release:        7%{?dist}
Summary:        Managing the version number of Git-hosted PHP projects, version %{ver_major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.1
BuildRequires:  php-cli
BuildRequires:  php-fedora-autoloader-devel

# From composer.json, "require": {
#        "php": ">=8.1"
Requires:       php(language) >= 8.1
Requires:       git
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Library that helps with managing the version number
of Git-hosted PHP projects.

This package provides version %{ver_major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate the Autoloader
%{_bindir}/phpab --template fedora --output src/autoload.php src


%install
# Not PSR-4 compliant, but ok as we use a classmap
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}


%check
: check autoloader
php -r '
require "%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}/autoload.php";
exit (class_exists("%{ns_vendor}\\%{ns_project}") ? 0 : 1);
'


%files
%license LICENSE
%doc *.md
%doc composer.json
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}%{ver_major}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun  6 2023 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1 (no change)

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 8.1
- rename to php-sebastian-version4
- move to /usr/share/php/SebastianBergmann/Version4

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 3.0.2-1
- update to 3.0.2 (no change)

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1 (no change)
- sources from git snapshot

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- raise dependency on PHP 7.3
- rename to php-sebastian-version3
- move to /usr/share/php/SebastianBergmann/Version3

* Sat Nov 26 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 (no change)
- switch to fedora/autoloader

* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- raise minimal php version to 5.6

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6
- generate autoloader
- fix PSR-0 layout

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Sun Jan  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4
- fix scriptlet
- drop pear compatibility provides
- fix license usage

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-3
- composer dependencies

* Sat Mar  8 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3
- move from pear channel to github sources because of
  https://github.com/sebastianbergmann/phpunit/wiki/Release-Announcement-for-PHPUnit-4.0.0
- add %%check
- add missing dependency on git

* Thu Feb 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Thu Apr  4 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
