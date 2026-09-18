# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-phpunit-php-file-iterator3
#
# Copyright (c) 2009-2023 Christof Damian, Remi Collet
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    cf1c2e7c203ac650e352f4cc675a7021e7d1b3cf
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-file-iterator
%global php_home     %{_datadir}/php
# Packagist
%global pk_vendor    phpunit
%global pk_project   %{gh_project}
%global major        3
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   FileIterator
%if %{bootstrap}
%bcond_with          tests
%else
%bcond_without       tests
%endif


Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        3.0.6
Release:        11%{?dist}
Summary:        FilterIterator implementation that filters files based on a list of suffixes, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
%if %{with tests}
# From composer.json, "require-dev"
#        "phpunit/phpunit": "^9.3"
BuildRequires:  phpunit9 >= 9.3
BuildRequires:  php(language) >= 7.3
BuildRequires:  php-pcre
BuildRequires:  php-spl
%endif
BuildRequires:  php-fedora-autoloader-devel

# From composer.json, "require"
#        "php": ">=7.3"
Requires:       php(language) >= 7.3
# From phpcompatinfo report for 3.0.0
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
FilterIterator implementation that filters files based on a list of suffixes.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
%{_bindir}/phpab \
   --template fedora \
   --output   src/autoload.php \
   src


%install
mkdir -p    %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src  %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%check
%if %{with_tests}
mkdir vendor
touch vendor/autoload.php

: Run upstream test suite
ret=0
for cmd in php php80 php81 php82; do
  if which $cmd; then
    $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
      %{_bindir}/phpunit9  --verbose || ret=1
  fi
done
exit $ret
%else
: bootstrap build with test suite disabled
%endif


%files
%license LICENSE
%doc ChangeLog.md README.md composer.json
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 21 2023 Remi Collet <remi@remirepo.net> - 1.1.4-7
- use SPDX License id

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec  2 2021 Remi Collet <remi@remirepo.net> - 3.0.6-1
- update to 3.0.6

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 3.0.5-1
- update to 3.0.5 (no change)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Remi Collet <remi@remirepo.net> - 3.0.4-1
- update to 3.0.4

* Mon Jun 29 2020 Remi Collet <remi@remirepo.net> - 3.0.3-1
- update to 3.0.3

* Tue Jun 16 2020 Remi Collet <remi@remirepo.net> - 3.0.2-1
- update to 3.0.2
- sources from git snapshot

* Sat Apr 18 2020 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- raise dependency on PHP 7.3
- rename to php-phpunit-php-file-iterator3
- move to /usr/share/php/SebastianBergmann/FileIterator3

* Fri Sep 14 2018 Remi Collet <remi@remirepo.net> - 2.0.2-1
- update to 2.0.2
- run upstream test suite

* Mon Jun 11 2018 Remi Collet <remi@remirepo.net> - 2.0.1-1
- update to 2.0.1

* Tue May 29 2018 Remi Collet <remi@remirepo.net> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP 7.1
- rename to php-phpunit-php-file-iterator2
- move to /usr/share/php/SebastianBergmann/FileIterator2

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 1.4.5-1
- Update to 1.4.5

* Mon Nov 27 2017 Remi Collet <remi@remirepo.net> - 1.4.3-1
- Update to 1.4.3

* Sat Nov 26 2016 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- update to 1.4.2 (no change)
- switch to fedora/autoloader

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1 (only CS)

* Thu Apr  2 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0
- fix license handling

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-5
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-3
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-2
- get sources from github

* Fri Oct 11 2013 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4
- raise dependencies: php 5.3.3, pear 1.9.4

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- upstream 1.3.3

* Sun Sep 23 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- upstream 1.3.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 17 2012 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Version 1.3.1 (stable) - API 1.3.0 (stable)
- unmacro current command
- remove pear version hack

* Mon Jan 16 2012 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- upstream 1.3.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  2 2011 Christof Damian <christof@damian.net> - 1.3.0-1
- upstream 1.3.0

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- upstream 1.3.0

* Fri Mar  4 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.6-1
- upstream 1.2.6
- rebuild for remi repository

* Fri Mar  4 2011 Christof Damian <christof@damian.net> - 1.2.6-1
- upstream 1.2.6

* Mon Feb 28 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.4-1
- upstream 1.2.4
- rebuild for remi repository

* Mon Feb 28 2011 Christof Damian <cdamian@robin.gotham.krass.com> - 1.2.4-1
- upstream 1.2.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 18 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.2.3-1
- upstream 1.2.3
- rebuild for remi repository

* Fri Sep 17 2010 Christof Damian <christof@damian.net> - 1.2.3-1
- upstream 1.2.3

* Thu Jul 22 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.2.2-2
- rebuild for remi repository

* Thu Jul 22 2010 Christof Damian <christof@damian.net> - 1.2.2-2
- fix minimum pear requirement

* Thu Jul 22 2010 Christof Damian <christof@damian.net> - 1.2.2-1
- upstream 1.2.2, bugfix

* Sun May  9 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.2.1-1
- rebuild for remi repository

* Sat May  8 2010 Christof Damian <christof@damian.net> - 1.2.1-1
- upstream 1.2.1

* Wed Feb 10 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- rebuild for remi repository

* Tue Feb  9 2010 Christof Damian <christof@damian.net> - 1.2.0-1
- upstream 1.2.0
- increased php-common requirements to 5.2.7
- increased php-pear requirement
- use global instead of define
- use channel macro in postun

* Fri Dec 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-2
- rebuild for remi repository

* Thu Dec 17 2009 Christof Damian <christof@damian.net> 1.1.1-2
- version 1.1.1 lowered the php requirement

* Thu Dec 17 2009 Christof Damian <christof@damian.net> 1.1.1-1
- upstream 1.1.1

* Thu Dec 17 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-4
- rebuild for remi repository

* Mon Nov 30 2009 Christof Damian <christof@damian.net> 1.1.0-4
- own pear directories

* Sat Nov 28 2009 Christof Damian <christof@damian.net> 1.1.0-3
- fixed php-pear buildrequire
- just require php-common

* Thu Nov 26 2009 Christof Damian <christof@damian.net> 1.1.0-2
- fix package.xml to work with older pear versions

* Wed Nov 25 2009 Christof Damian <christof@damian.net> 1.1.0-1
- Initial packaging
