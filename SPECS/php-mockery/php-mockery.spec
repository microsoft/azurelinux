# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Fedora spec file for php-deepend-Mockery
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%bcond_without       tests

%global gh_commit    1f4efdd7d3beafe9807b08156dfcb176d18f1699
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     mockery
%global gh_project   mockery
%global ns_project   Mockery
%global major        1

Name:           php-mockery
Version:        1.6.12
Release:        4%{?dist}
Summary:        Mockery is a simple but flexible PHP mock object framework

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

# Use our autoloader
Patch0:         %{gh_project}-tests.patch

BuildArch:      noarch
%if %{with tests}
BuildRequires:  php(language) >= 7.3
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^8.5 || ^9.6.17",
#        "symplify/easy-coding-standard": "^12.1.4"
%global phpunit %{_bindir}/phpunit9
BuildRequires: phpunit9 >= 9.6.17
BuildRequires: (php-composer(hamcrest/hamcrest-php) >= 2.0.1 with php-composer(hamcrest/hamcrest-php) < 3)
BuildRequires:  php-pdo
# Autoloader
%endif
BuildRequires:  php-fedora-autoloader-devel

# From composer.json, "require": {
#        "php": ">=7.3",
#        "lib-pcre": ">=7.0",
#        "hamcrest/hamcrest-php": "~2.0"
Requires:       php(language) >= 7.3
Requires:      (php-composer(hamcrest/hamcrest-php) >= 2.0.1 with php-composer(hamcrest/hamcrest-php) < 3)
# From phpcompatinfo report for version 1.4.2
Requires:       php-pcre
Requires:       php-spl
Requires:       php-reflection
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(mockery/mockery) = %{version}


%description
Mockery is a simple but flexible PHP mock object framework for use in unit 
testing. It is inspired by Ruby's flexmock and Java's Mockito, borrowing 
elements from both of their APIs.

Autoloader: %{_datadir}/php/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv library/*.php library/%{ns_project}/
phpab --template fedora --output library/%{ns_project}/autoload.php library

cat << 'EOF' | tee -a library/%{ns_project}/autoload.php

\Fedora\Autoloader\Dependencies::required([
    '/usr/share/php/Hamcrest2/autoload.php',
    __DIR__ . '/helpers.php',
]);
EOF

%patch -P0 -p0 -b .rpm

rm -f docs/.gitignore


%build
# Empty build section, most likely nothing required.


%install
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp library/%{ns_project} %{buildroot}/%{_datadir}/php/%{ns_project}%{major}


%check
%if %{with tests}
: Use installed tree and our autoloader
export COMPOSER_VENDOR_DIR=%{buildroot}%{_datadir}/php/%{ns_project}%{major}

phpab --output tests/classmap.php --exclude */SemiReservedWordsAsMethods.php tests/Mockery tests/Fixture

: Run upstream test suite
ret=0

# need investigation
rm tests/Mockery/MockeryCanMockClassesWithSemiReservedWordsTest.php

for cmd in php php81 php82 php83; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit9 \
      --no-coverage \
      --verbose || ret=1
  fi
done
exit $ret
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md docs
%doc composer.json
%{_datadir}/php/%{ns_project}%{major}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 16 2024 Remi Collet <remi@remirepo.net> - 1.6.12-1
- update to 1.6.12

* Fri Mar 22 2024 Remi Collet <remi@remirepo.net> - 1.6.11-1
- update to 1.6.11

* Wed Mar 20 2024 Remi Collet <remi@remirepo.net> - 1.6.10-1
- update to 1.6.10

* Wed Mar 13 2024 Remi Collet <remi@remirepo.net> - 1.6.9-1
- update to 1.6.9 (revert to 1.6.7 code)

* Tue Mar 12 2024 Remi Collet <remi@remirepo.net> - 1.6.8-1
- update to 1.6.8

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Remi Collet <remi@remirepo.net> - 1.6.7-1
- update to 1.6.7

* Thu Aug 24 2023 Remi Collet <remi@remirepo.net> - 1.6.6-1
- update to 1.6.6

* Thu Jul 20 2023 Remi Collet <remi@remirepo.net> - 1.6.4-1
- update to 1.6.4

* Wed Jul 19 2023 Remi Collet <remi@remirepo.net> - 1.6.3-1
- update to 1.6.3

* Thu Jun  8 2023 Remi Collet <remi@remirepo.net> - 1.6.2-1
- update to 1.6.2

* Tue Jun  6 2023 Remi Collet <remi@remirepo.net> - 1.6.1-1
- update to 1.6.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 12 2022 Remi Collet <remi@remirepo.net> - 1.5.1-1
- update to 1.5.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Remi Collet <remi@remirepo.net> - 1.5.0-1
- update to 1.5.0

* Tue Sep 14 2021 Remi Collet <remi@remirepo.net> - 1.4.4-1
- update to 1.4.4

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 24 2021 Remi Collet <remi@remirepo.net> - 1.4.3-1
- update to 1.4.3

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 12 2020 Remi Collet <remi@remirepo.net> - 1.4.2-1
- update to 1.4.2
- raise dependency on PHP 7.3
- drop compatibility with old phpunit 5, 6 and 7
- run test suite with both phpunit 8 and 9

* Mon Aug 17 2020 Remi Collet <remi@remirepo.net> - 1.3.3-1
- update to 1.3.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Remi Collet <remi@remirepo.net> - 1.3.2-1
- update to 1.3.2
- switch to phpunit9
- raise dependency on hamcrest/hamcrest-php 2.0.1
- sources from git snapshot

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan  3 2020 Remi Collet <remi@remirepo.net> - 1.3.1-1
- update to 1.3.1

* Mon Nov 25 2019 Remi Collet <remi@remirepo.net> - 1.3.0-1
- update to 1.3.0
- use phpunit8

* Mon Sep 30 2019 Remi Collet <remi@remirepo.net> - 1.2.4-1
- update to 1.2.4
- drop patch merged upstream

* Mon Aug 19 2019 Remi Collet <remi@remirepo.net> - 1.2.3-1
- update to 1.2.3
- add patch for PHP 7.4 from
  https://github.com/mockery/mockery/pull/993

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 13 2019 Remi Collet <remi@remirepo.net> - 1.2.2-1
- update to 1.2.2

* Mon Feb 11 2019 Remi Collet <remi@remirepo.net> - 1.2.1-1
- update to 1.2.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct  3 2018 Remi Collet <remi@remirepo.net> - 1.2.0-1
- update to 1.2.0
- switch to phpunit7

* Sun May 13 2018 Remi Collet <remi@remirepo.net> - 1.1.0-1
- update to 1.1.0

* Mon Jan 22 2018 Remi Collet <remi@remirepo.net> - 1.0-1
- Update to 1.0
- rename to php-mockery and move to /usr/share/php/Mockery1
- raise dependency on PHP 5.6
- raise dependency on hamcrest/hamcrest-php 2.0
- use phpunit6 on F26+

* Fri Oct  6 2017 Remi Collet <remi@remirepo.net> - 0.9.9-4
- add patches for PHP 7.2

* Tue Feb 28 2017 Remi Collet <remi@remirepo.net> - 0.9.9-1
- Update to 0.9.9

* Fri Feb 10 2017 Remi Collet <remi@remirepo.net> - 0.9.8-1
- Update to 0.9.8

* Fri Dec 23 2016 Remi Collet <remi@fedoraproject.org> - 0.9.7-1
- Update to 0.9.7

* Sat Nov 26 2016 Remi Collet <remi@fedoraproject.org> - 0.9.6-1
- Update to 0.9.6
- switch to fedora/autoloader

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 0.9.5-1
- Update to 0.9.5

* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 0.9.3-1
- downgrade to 0.9.3

* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 0.9.4-1
- Update to 0.9.4
- add autoloader using symfony/class-loader
- add dependency on hamcrest/hamcrest-php
- run test suite
- use github archive from commit reference

* Wed Jul 16 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.1-2
- fixed requires (Remi)
- add script which will delete older pear package if installed (Remi)
- fix provides/obsoletes (Remi)

* Tue Jul 15 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.1-1
- update to 0.9.1 (RHBZ #1119451)

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Fri Apr 19 2013 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0 (backport)

* Thu Apr 18 2013 Christof Damian <christof@damian.net> - 0.8.0-1
- upstream 0.8.0

* Sun Mar 04 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.7.2-1
- upstream 0.7.2, rebuild for remi repository

* Sun Mar  4 2012 Christof Damian <christof@damian.net> - 0.7.2-1
- upstream 0.7.2

* Tue Jul 27 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.6.3-2
- rebuild for remi repository

* Tue Jul 27 2010 Christof Damian <christof@damian.net> - 0.6.3-2
- add license and readme file from github

* Fri May 28 2010 Christof Damian <christof@damian.net> - 0.6.0-1
- initial packaging


