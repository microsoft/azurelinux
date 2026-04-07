# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-comparator7
#
# SPDX-FileCopyrightText:  Copyright 2014-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    6a7de5df2e094f9a80b40a522391a7e6022df5f6
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   comparator
%global gh_date      2026-01-24
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global major        7
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   Comparator

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        7.1.4
Release:        1%{?dist}
Summary:        Compare PHP values for equality, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.3
BuildRequires:  php-bcmath
BuildRequires:  php-dom
BuildRequires:  php-mbstring
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^12.2"
BuildRequires:  phpunit12 >= 12.2
BuildRequires:  (php-composer(%{pk_vendor}/diff)     >= 7.0   with php-composer(%{pk_vendor}/diff)     < 8)
BuildRequires:  (php-composer(%{pk_vendor}/exporter) >= 7.0   with php-composer(%{pk_vendor}/exporter) < 8)
%endif

# from composer.json
#        "php": ">=8.3",
#        "sebastian/diff": "^7.0",
#        "sebastian/exporter": "^7.0"
#        "ext-dom": "*",
#        "ext-mbstring": "*"
Requires:       php(language) >= 8.3
Requires:       php-dom
Requires:       php-mbstring
Requires:       (php-composer(%{pk_vendor}/diff)     >= 7.0   with php-composer(%{pk_vendor}/diff)     < 8)
Requires:       (php-composer(%{pk_vendor}/exporter) >= 7.0   with php-composer(%{pk_vendor}/exporter) < 8)
# from phpcompatinfo report for version 6.3.0
#   Only core, date, spl (bcmath is optional)
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
This component provides the functionality to compare PHP values for equality.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --template fedora --output src/autoload.php src

# Rely on include_path as in PHPUnit dependencies
cat <<EOF | tee -a src/autoload.php

\Fedora\Autoloader\Dependencies::required([
    '%{php_home}/%{ns_vendor}/Diff7/autoload.php',
    '%{php_home}/%{ns_vendor}/Exporter7/autoload.php',
]);
EOF


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with tests}
mkdir vendor
%{_bindir}/phpab --template fedora --output vendor/autoload.php tests/_fixture

: Run upstream test suite
ret=0
for cmd in php php83 php84 php85; do
  if which $cmd; then
    $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
      %{_bindir}/phpunit12 --bootstrap vendor/autoload.php --no-coverage || ret=1
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
* Mon Jan 26 2026 Remi Collet <remi@remirepo.net> - 7.1.4-1
- update to 7.1.4

* Wed Aug 20 2025 Remi Collet <remi@remirepo.net> - 7.1.3-1
- update to 7.1.3

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jun 21 2025 Remi Collet <remi@remirepo.net> - 7.1.0-1
- update to 7.1.0

* Sat Mar  8 2025 Remi Collet <remi@remirepo.net> - 7.0.1-1
- update to 7.0.1

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 7.0.0-2
- enable test suite

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 7.0.0-1
- update to 7.0.0
- raise dependency on PHP 8.3
- raise dependency on sebastian/diff 7
- raise dependency on sebastian/exporter 7
- rename to php-sebastian-comparator7
- move to /usr/share/php/SebastianBergmann/Comparator7

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 6.3.0-2
- enable test suite

* Mon Jan  6 2025 Remi Collet <remi@remirepo.net> - 6.3.0-1
- update to 6.3.0

* Thu Oct 31 2024 Remi Collet <remi@remirepo.net> - 6.2.1-1
- update to 6.2.1

* Wed Oct 30 2024 Remi Collet <remi@remirepo.net> - 6.2.0-1
- update to 6.2.0

* Mon Oct 21 2024 Remi Collet <remi@remirepo.net> - 6.1.1-1
- update to 6.1.1

* Thu Sep 12 2024 Remi Collet <remi@remirepo.net> - 6.1.0-1
- update to 6.1.0

* Mon Aug 12 2024 Remi Collet <remi@remirepo.net> - 6.0.2-1
- update to 6.0.2

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.2
- raise dependency on sebastian/diff 6
- raise dependency on sebastian/exporter 6
- rename to php-sebastian-comparator6
- move to /usr/share/php/SebastianBergmann/Comparator6

* Tue Jan 30 2024 Remi Collet <remi@remirepo.net> - 5.0.1-4
- add upstream patch for phpunit >= 10.4 FTBFS #2261508

* Fri Aug 18 2023 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 8.1
- raise dependency on sebastian/diff 5
- raise dependency on sebastian/exporter 5
- rename to php-sebastian-comparator5
- move to /usr/share/php/SebastianBergmann/Comparator5
- add dependency on mbstring extension

* Wed Sep 14 2022 Remi Collet <remi@remirepo.net> - 4.0.8-1
- update to 4.0.8

* Wed Sep 14 2022 Remi Collet <remi@remirepo.net> - 4.0.7-1
- update to 4.0.7

* Tue Oct 27 2020 Remi Collet <remi@remirepo.net> - 4.0.6-1
- update to 4.0.6

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 4.0.5-1
- update to 4.0.5

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 4.0.4-1
- update to 4.0.4 (no change)

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 4.0.3-1
- update to 4.0.3

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2
- sources from git snapshot

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 7.3
- raise dependency on sebastian/diff 4
- raise dependency on sebastian/exporter 4
- rename to php-sebastian-comparator4
- move to /usr/share/php/SebastianBergmann/Comparator4

* Thu Jul 12 2018 Remi Collet <remi@remirepo.net> - 3.0.2-1
- update to 3.0.2

* Tue Jun 19 2018 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1

* Wed Apr 18 2018 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- rename to php-sebastian-comparator3
- raise dependency on PHP 7.1
- raise dependency on sebastian/diff 3.0
- use phpunit7

* Fri Feb  2 2018 Remi Collet <remi@remirepo.net> - 2.1.3-1
- Update to 2.1.3 (no change)
- allow sebastian/diff v3
- use range dependencies on F27+

* Fri Jan 12 2018 Remi Collet <remi@remirepo.net> - 2.1.2-1
- Update to 2.1.2

* Sat Dec 23 2017 Remi Collet <remi@remirepo.net> - 2.1.1-1
- Update to 2.1.1

* Fri Nov  3 2017 Remi Collet <remi@remirepo.net> - 2.1.0-1
- Update to 2.1.0
- raise dependency on sebastian/exporter 3.1

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 2.0.2-1
- Update to 2.0.2
- raise dependency on sebastian/diff 2.0
- raise various dependencies on latest minor version

* Wed Jul 12 2017 Remi Collet <remi@remirepo.net> - 2.0.1-1
- Update to 2.0.1

* Fri Mar  3 2017 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 3.0.0
- rename to php-sebastian-comparator2
- raise dependency on PHP 7
- raise dependency on sebastian/exporter 3

* Sun Jan 29 2017 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- update to 1.2.4

* Sun Jan 29 2017 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- update to 1.2.3

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2 (no change)
- allow sebastian/exporter 2.0

* Thu Nov 17 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1
- switch to fedora/autoloader

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-3
- manage dependencies in autoloader

* Fri Jan 30 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1
- raise dependency on sebastian/diff >= 1.2
- raise dependency on sebastian/exporter >= 1.2

* Thu Dec  4 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- enable test suite

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add composer dependencies

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
