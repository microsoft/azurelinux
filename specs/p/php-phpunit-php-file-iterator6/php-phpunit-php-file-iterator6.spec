# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-phpunit-php-file-iterator6
#
# Copyright (c) 2009-2025 Christof Damian, Remi Collet
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#

%bcond_without       tests

%global gh_commit    3d1cd096ef6bea4bf2762ba586e35dbd317cbfd5
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-file-iterator
%global gh_date      2026-02-02
%global php_home     %{_datadir}/php
# Packagist
%global pk_vendor    phpunit
%global pk_project   %{gh_project}
%global major        6
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   FileIterator


Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        6.0.1
Release:        1%{?dist}
Summary:        FilterIterator implementation based on a list of suffixes, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.3
%if %{with tests}
# From composer.json, "require-dev"
#        "phpunit/phpunit": "^12.0"
BuildRequires:  phpunit12
%endif
BuildRequires:  php-fedora-autoloader-devel

# From composer.json, "require"
#        "php": ">=8.3"
Requires:       php(language) >= 8.3
# From phpcompatinfo report for 4.0.0
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
%if %{with tests}
mkdir vendor
touch vendor/autoload.php

: Run upstream test suite
ret=0
for cmd in php php83 php84 php85; do
  if which $cmd; then
    $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
      %{_bindir}/phpunit12 || ret=1
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
* Tue Feb  3 2026 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 6.0.0-2
- enable test suite

* Fri Feb  7 2025 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0
- raise dependency on PHP 8.3
- rename to php-phpunit-php-file-iterator6
- move to /usr/share/php/SebastianBergmann/FileIterator6

* Tue Feb  4 2025 Remi Collet <remi@remirepo.net> - 5.1.0-2
- enable test suite

* Tue Aug 27 2024 Remi Collet <remi@remirepo.net> - 5.1.0-1
- update to 5.1.0

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Mon Feb  5 2024 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- raise dependency on PHP 8.2
- rename to php-phpunit-php-file-iterator5
- move to /usr/share/php/SebastianBergmann/FileIterator5

* Thu Aug 31 2023 Remi Collet <remi@remirepo.net> - 4.1.0-1
- update to 4.1.0

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 4.0.2-3
- Enable test suite

* Tue May  9 2023 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2

* Mon Feb 13 2023 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- raise dependency on PHP 8.1
- rename to php-phpunit-php-file-iterator4
- move to /usr/share/php/SebastianBergmann/FileIterator4

* Thu Dec  2 2021 Remi Collet <remi@remirepo.net> - 3.0.6-1
- update to 3.0.6

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 3.0.5-1
- update to 3.0.5 (no change)

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
