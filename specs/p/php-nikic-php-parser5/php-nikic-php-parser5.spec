# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-nikic-php-parser5
#
# SPDX-FileCopyrightText:  Copyright 2016-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%if 0%{?fedora}
%bcond_without tests
%else
# disabled by default as phpunit is not available
%bcond_with    tests
%endif

%global gh_commit    dca41cd15c2ac9d055ad70dbfd011130757d1f82
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nikic
%global gh_project   PHP-Parser
%global pk_project   php-parser
%global php_home     %{_datadir}/php
%global ns_project   PhpParser
%global major        5

%global upstream_version 5.7.0
#global upstream_prever  rc1

Name:           php-%{gh_owner}-%{pk_project}%{major}
Version:        %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release: 2%{?dist}
Summary:        A PHP parser written in PHP - version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{upstream_version}%{?upstream_prever}-%{gh_short}.tgz
Source1:        makesrc.sh

# Autoloader
Patch0:         %{name}-rpm.patch

BuildArch:      noarch
%if %{with tests}
# For tests
BuildRequires:  php(language) >= 7.4
BuildRequires:  php-tokenizer
BuildRequires:  php-ctype
BuildRequires:  php-json
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^9.0",
#        "ircmaxell/php-yacc": "0.0.7"
%global phpunit %{_bindir}/phpunit9
BuildRequires:  phpunit9
# Autoloader
%endif
BuildRequires:  php-fedora-autoloader-devel

# From composer.json, "require": {
#        "php": ">=7.4",
#        "ext-tokenizer": "*",
#        "ext-json": "*",
#        "ext-ctype": "*"
Requires:       php(language) >= 7.4
Requires:       php-tokenizer
Requires:       php-json
Requires:       php-ctype
# From phpcompatinfo report for version 5.0.0
Requires:       php-cli
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{gh_owner}/%{pk_project}) = %{version}


%description
This is a PHP parser written in PHP.
Its purpose is to simplify static code analysis and manipulation.

This package provides the library version %{major} and the php-parse%{major} command.

Documentation: https://github.com/nikic/PHP-Parser/tree/master/doc

Autoloader: %{php_home}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch -P0 -p1 -b .rpm


%build
: Generate an simple classmap autoloader
phpab --template fedora \
      --tolerant \
      --output lib/%{ns_project}/autoload.php \
      lib/%{ns_project}


%install
: Library
mkdir -p                 %{buildroot}%{php_home}
cp -pr lib/%{ns_project} %{buildroot}%{php_home}/%{ns_project}%{major}

: Command
install -Dpm 0755 bin/php-parse %{buildroot}%{_bindir}/php-parse%{major}


%check
%if %{with tests}
: Test the command
sed -e 's:%{php_home}:%{buildroot}%{php_home}:' \
    bin/php-parse > bin/php-parse-test
php bin/php-parse-test --help

: Test suite autoloader
mkdir vendor
cat << 'AUTOLOAD' | tee vendor/autoload.php
<?php
\Fedora\Autoloader\Autoload::addPsr4('%{ns_project}\\', dirname(__DIR__).'/test/PhpParser/');
AUTOLOAD

: Upstream test suite
ret=0
for cmdarg in "php %{phpunit}" php81 php82 php83 php84 php85; do
  if which $cmdarg; then
    set $cmdarg
    $1 -d include_path=%{php_home} \
       -d auto_prepend_file=%{buildroot}/%{php_home}/%{ns_project}%{major}/autoload.php \
      ${2:-%{_bindir}/phpunit9} --verbose || ret=1
  fi
done
exit $ret
%else
: Test suite disabled
%endif


%files
%license LICENSE
%doc composer.json
%doc *.md
%{_bindir}/php-parse%{major}
%{php_home}/%{ns_project}%{major}


%changelog
* Tue Dec  9 2025 Remi Collet <remi@remirepo.net> - 5.7.0-1
- update to 5.7.0

* Wed Oct 22 2025 Remi Collet <remi@remirepo.net> - 5.6.2-1
- update to 5.6.2

* Thu Aug 14 2025 Remi Collet <remi@remirepo.net> - 5.6.1-1
- update to 5.6.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Remi Collet <remi@remirepo.net> - 5.5.0-1
- update to 5.5.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 31 2024 Remi Collet <remi@remirepo.net> - 5.4.0-1
- update to 5.4.0
- re-license spec file to CECILL-2.1

* Wed Oct  9 2024 Remi Collet <remi@remirepo.net> - 5.3.1-1
- update to 5.3.1

* Mon Sep 30 2024 Remi Collet <remi@remirepo.net> - 5.3.0-1
- update to 5.3.0

* Mon Sep 16 2024 Remi Collet <remi@remirepo.net> - 5.2.0-1
- update to 5.2.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 5.1.0-1
- update to 5.1.0

* Wed Mar  6 2024 Remi Collet <remi@remirepo.net> - 5.0.2-1
- update to 5.0.2

* Thu Feb 22 2024 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Mon Jan  8 2024 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0

* Thu Dec 21 2023 Remi Collet <remi@remirepo.net> - 5.0.0~rc1-1
- update to 5.0.0rc1

* Mon Sep 18 2023 Remi Collet <remi@remirepo.net> - 5.0.0~beta1-1
- update to 5.0.0beta1

* Tue Jun 27 2023 Remi Collet <remi@remirepo.net> - 5.0.0~alpha3-1
- update to 5.0.0alpha3
- rename to php-nikic-php-parser5
- install in /usr/share/php/PhpParser5
- raise dependency on PHP 7.1

* Mon Jun 26 2023 Remi Collet <remi@remirepo.net> - 4.16.0-1
- update to 4.16.0

* Wed May 24 2023 Remi Collet <remi@remirepo.net> - 4.15.5-1
- update to 4.15.5

* Mon Mar  6 2023 Remi Collet <remi@remirepo.net> - 4.15.4-1
- update to 4.15.4

* Tue Jan 17 2023 Remi Collet <remi@remirepo.net> - 4.15.3-1
- update to 4.15.3

* Mon Nov 14 2022 Remi Collet <remi@remirepo.net> - 4.15.2-1
- update to 4.15.2

* Thu Sep  8 2022 Remi Collet <remi@remirepo.net> - 4.15.1-1
- update to 4.15.1

* Mon Jun 13 2022 Remi Collet <remi@remirepo.net> - 4.14.0-2
- only run test suite on Fedora, not on EL

* Wed Jun  1 2022 Remi Collet <remi@remirepo.net> - 4.14.0-1
- update to 4.14.0

* Wed Dec  1 2021 Remi Collet <remi@remirepo.net> - 4.13.2-1
- update to 4.13.2

* Thu Nov  4 2021 Remi Collet <remi@remirepo.net> - 4.13.1-1
- update to 4.13.1

* Tue Sep 21 2021 Remi Collet <remi@remirepo.net> - 4.13.0-1
- update to 4.13.0

* Wed Jul 21 2021 Remi Collet <remi@remirepo.net> - 4.12.0-1
- update to 4.12.0

* Wed Jul 21 2021 Remi Collet <remi@remirepo.net> - 4.11.0-2
- add upstream patches for PHP 8.1

* Mon Jul  5 2021 Remi Collet <remi@remirepo.net> - 4.11.0-1
- update to 4.11.0
- switch to phpunit9

* Tue May  4 2021 Remi Collet <remi@remirepo.net> - 4.10.5-1
- update to 4.10.5

* Mon Dec 21 2020 Remi Collet <remi@remirepo.net> - 4.10.4-1
- update to 4.10.4

* Fri Dec  4 2020 Remi Collet <remi@remirepo.net> - 4.10.3-1
- update to 4.10.3

* Mon Sep 28 2020 Remi Collet <remi@remirepo.net> - 4.10.2-1
- update to 4.10.2

* Thu Sep 24 2020 Remi Collet <remi@remirepo.net> - 4.10.1-1
- update to 4.10.1

* Sun Sep 20 2020 Remi Collet <remi@remirepo.net> - 4.10.0-1
- update to 4.10.0

* Mon Aug 31 2020 Remi Collet <remi@remirepo.net> - 4.9.1-1
- update to 4.9.1

* Wed Aug 19 2020 Remi Collet <remi@remirepo.net> - 4.9.0-1
- update to 4.9.0

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 4.8.0-1
- update to 4.8.0

* Sun Jul 26 2020 Remi Collet <remi@remirepo.net> - 4.7.0-1
- update to 4.7.0

* Fri Jul  3 2020 Remi Collet <remi@remirepo.net> - 4.6.0-1
- update to 4.6.0

* Thu Jun 25 2020 Remi Collet <remi@remirepo.net> - 4.5.0-2
- switch to classmap autoloader
- add missing dependency on fedora/autoloader

* Wed Jun  3 2020 Remi Collet <remi@remirepo.net> - 4.5.0-1
- update to 4.5.0

* Mon Apr 13 2020 Remi Collet <remi@remirepo.net> - 4.4.0-1
- update to 4.4.0

* Tue Nov 12 2019 Remi Collet <remi@remirepo.net> - 4.3.0-1
- update to 4.3.0

* Mon Oct 28 2019 Remi Collet <remi@remirepo.net> - 4.2.5-1
- update to 4.2.5
- sources from git snapshot

* Mon Sep  2 2019 Remi Collet <remi@remirepo.net> - 4.2.4-1
- update to 4.2.4

* Mon Aug 19 2019 Remi Collet <remi@remirepo.net> - 4.2.3-1
- update to 4.2.3
- use phpunit8

* Mon May 27 2019 Remi Collet <remi@remirepo.net> - 4.2.2-1
- update to 4.2.2

* Mon Feb 18 2019 Remi Collet <remi@remirepo.net> - 4.2.1-1
- update to 4.2.1

* Sun Jan 13 2019 Remi Collet <remi@remirepo.net> - 4.2.0-1
- update to 4.2.0

* Thu Dec 27 2018 Remi Collet <remi@remirepo.net> - 4.1.1-1
- update to 4.1.1

* Wed Oct 10 2018 Remi Collet <remi@remirepo.net> - 4.1.0-1
- update to 4.1.0
- https://github.com/nikic/PHP-Parser/issues/539 - PHP 7.3

* Tue Sep 18 2018 Remi Collet <remi@remirepo.net> - 4.0.4-1
- update to 4.0.4

* Mon Jul 16 2018 Remi Collet <remi@remirepo.net> - 4.0.3-1
- update to 4.0.3

* Mon Jun  4 2018 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2

* Mon Mar 26 2018 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1

* Thu Mar 22 2018 Remi Collet <remi@remirepo.net> - 4.0.0-1
- Update to 4.0.0
- rename to php-nikic-php-parser4 and move to /usr/share/php/PhpParser4
- raise dependency on PHP 7
- use phpunit6 or phpunit7 (F28+)

* Thu Mar  1 2018 Remi Collet <remi@remirepo.net> - 3.1.5-1
- Update to 3.1.5

* Fri Jan 26 2018 Remi Collet <remi@remirepo.net> - 3.1.4-1
- Update to 3.1.4

* Wed Dec 27 2017 Remi Collet <remi@remirepo.net> - 3.1.3-1
- Update to 3.1.3

* Mon Nov  6 2017 Remi Collet <remi@remirepo.net> - 3.1.2-1
- Update to 3.1.2

* Mon Sep  4 2017 Remi Collet <remi@remirepo.net> - 3.1.1-1
- Update to 3.1.1

* Sat Aug  5 2017 Remi Collet <remi@remirepo.net> - 3.1.0-1
- Update to 3.1.0

* Thu Jun 29 2017 Remi Collet <remi@remirepo.net> - 3.0.6-1
- Update to 3.0.6

* Mon Mar  6 2017 Remi Collet <remi@remirepo.net> - 3.0.5-1
- Update to 3.0.5
- always provide the command, with version suffix

* Sat Feb 11 2017 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- update to 3.0.4

* Sat Feb  4 2017 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- update to 3.0.3

* Wed Dec 7  2016 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- new package for library version 3

