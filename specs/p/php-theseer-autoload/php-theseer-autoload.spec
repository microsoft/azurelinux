# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-theseer-autoload
#
# SPDX-FileCopyrightText:  Copyright 2014-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%global gh_commit    c3a22a88ae6bdadbe0c8274a51d29998eb152983
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     theseer
%global gh_project   Autoload
%global php_home     %{_datadir}/php/TheSeer
%global pear_name    Autoload
%global pear_channel pear.netpirates.net

%if 0%{?fedora}
%bcond_without  tests
%else
%bcond_with     tests
%endif

Name:           php-theseer-autoload
Version:        1.29.4
Release: 2%{?dist}
Summary:        A tool and library to generate autoload code

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{?gh_short}.tar.gz

# Autoloader path
Patch0:         %{gh_project}-rpm.patch

BuildArch:      noarch
BuildRequires:  php(language) >= 7.4
BuildRequires:  php-cli
BuildRequires:  php-date
BuildRequires:  php-json
BuildRequires:  php-openssl
BuildRequires:  php-phar
BuildRequires:  php-spl
BuildRequires:  php-tokenizer
BuildRequires: (php-composer(theseer/directoryscanner)     >= 1.3.2 with php-composer(theseer/directoryscanner)     < 2)
BuildRequires: (php-composer(zetacomponents/console-tools) >= 1.7   with php-composer(zetacomponents/console-tools) < 2)
%if %{with tests}
%global phpunit %{_bindir}/phpunit9
BuildRequires:  %{phpunit}
%endif

# From composer.json, "require": {
#        "php": ">=5.3",
#        "ext-openssl": "*",
#        "theseer/directoryscanner": "^1.3.3",
#        "zetacomponents/console-tools": "^1.7.2"
Requires:       php(language) >= 5.3.1
Requires:       php-openssl
Requires:      (php-composer(theseer/directoryscanner)     >= 1.3.2 with php-composer(theseer/directoryscanner)     < 2)
Requires:      (php-composer(zetacomponents/console-tools) >= 1.7   with php-composer(zetacomponents/console-tools) < 2)
# From phpcompatinfo report for version 1.25.0
Requires:       php-cli
Requires:       php-date
Requires:       php-json
Requires:       php-phar
Requires:       php-spl
Requires:       php-tokenizer
# Optional xdebug

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(theseer/autoload) = %{version}


%description
The PHP AutoloadBuilder CLI tool phpab is a command line application
to automate the process of generating an autoload require file with
the option of creating static require lists as well as phar archives.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch -P0 -p0 -b .rpm

: drop composer dependencies
sed -e '\:../vendor/:d'    -i src/autoload.php

: add package dependencies
cat <<EOF | tee            -a src/autoload.php
// Dependencies
require '/usr/share/php/TheSeer/DirectoryScanner/autoload.php';
require '/usr/share/php/ezc/Base/base.php';
spl_autoload_register(array('\\ezcBase','autoload'));
EOF

# set version
sed -e 's/@VERSION@/%{version}/' -i phpab.php


%build
# Empty build section, most likely nothing required.


%install
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/%{gh_project}

install -Dpm 0755 phpab.php %{buildroot}%{_bindir}/phpab


%check
: Check version
sed -e 's:%{php_home}:%{buildroot}%{php_home}:' phpab.php >t.php
php t.php --version | grep %{version}
php t.php --output foo.php src

%if %{with tests}
: Fix test suite to use installed library
cat <<EOF | tee tests/init.php
<?php
require '%{buildroot}%{_datadir}/php/TheSeer/Autoload/autoload.php';
EOF

ret=0
for cmd in "php %{phpunit}" php81 php82 php83 php84 php85; do
  if which $cmd; then
    set $cmd
    $1 ${2:-%{_bindir}/phpunit9} --verbose || ret=1
  fi
done
exit $ret
%endif


%pre
if [ -x %{_bindir}/pear ]; then
  %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%license LICENSE
%doc README.md composer.json
%{php_home}/%{gh_project}
%{_bindir}/phpab


%changelog
* Tue Dec  9 2025 Remi Collet <remi@remirepo.net> - 1.29.4-1
- update to 1.29.4
- re-license spec file to CECILL-2.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec  3 2024 Remi Collet <remi@remirepo.net> - 1.29.3-1
- update to 1.29.3 (no change)

* Mon Oct  7 2024 Remi Collet <remi@remirepo.net> - 1.29.2-1
- update to 1.29.2

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May  2 2024 Remi Collet <remi@remirepo.net> - 1.29.1-1
- update to 1.29.1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 19 2023 Remi Collet <remi@remirepo.net> - 1.29.0-1
- update to 1.29.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Remi Collet <remi@remirepo.net> - 1.28.0-1
- update to 1.28.0

* Fri Feb 17 2023 Remi Collet <remi@remirepo.net> - 1.27.2-1
- update to 1.27.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Remi Collet <remi@remirepo.net> - 1.27.1-1
- update to 1.27.1

* Mon Jan 24 2022 Remi Collet <remi@remirepo.net> - 1.27.0-1
- update to 1.27.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec  6 2021 Remi Collet <remi@remirepo.net> - 1.26.3-2
- disable test suite on EL

* Mon Jul 26 2021 Remi Collet <remi@remirepo.net> - 1.26.3-1
- update to 1.26.3 (no change)
- raise dependency on theseer/directoryscanner 1.3.3
- raise dependency on zetacomponents/console-tools 1.7.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Remi Collet <remi@remirepo.net> - 1.26.1-1
- update to 1.26.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Remi Collet <remi@remirepo.net> - 1.26.0-1
- update to 1.26.0
- drop patch merged upstream

* Tue Oct 27 2020 Remi Collet <remi@remirepo.net> - 1.25.9-3
- add upstream patch for PHP 8
- add patch for Xdebug 3 from
  https://github.com/theseer/Autoload/pull/97

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar 20 2020 Remi Collet <remi@remirepo.net> - 1.25.9-1
- update to 1.25.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Remi Collet <remi@remirepo.net> - 1.25.8-1
- update to 1.25.8

* Fri Nov 15 2019 Remi Collet <remi@remirepo.net> - 1.25.7-1
- update to 1.25.7

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Remi Collet <remi@remirepo.net> - 1.25.6-1
- update to 1.25.6

* Thu Apr 25 2019 Remi Collet <remi@remirepo.net> - 1.25.5-1
- update to 1.25.5

* Fri Apr 19 2019 Remi Collet <remi@remirepo.net> - 1.25.4-1
- update to 1.25.4

* Mon Feb 11 2019 Remi Collet <remi@remirepo.net> - 1.25.3-1
- update to 1.25.3

* Mon Feb  4 2019 Remi Collet <remi@remirepo.net> - 1.25.2-1
- update to 1.25.2

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Remi Collet <remi@remirepo.net> - 1.25.1-1
- update to 1.25.1
- drop patch merged upstream

* Mon Oct 15 2018 Remi Collet <remi@remirepo.net> - 1.25.0-3
- add upstream patch for PHP 7.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  2 2018 Remi Collet <remi@remirepo.net> - 1.25.0-1
- update to 1.25.0
- use range dependencies

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Remi Collet <remi@remirepo.net> - 1.24.1-1
- Update to 1.24.1
- drop patch merged upstream

* Mon Jun 26 2017 Remi Collet <remi@remirepo.net> - 1.24.0-1
- Update to 1.24.0
- use phpunit6 on F26+
- add patch for PHP 5.3 in EL-6 from
  https://github.com/theseer/Autoload/pull/78

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 1.23.0-1
- update to 1.23.0

* Sat Aug 13 2016 Remi Collet <remi@fedoraproject.org> - 1.22.0-1
- update to 1.22.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Remi Collet <remi@fedoraproject.org> - 1.21.0-1
- update to 1.21.0

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.20.3-1
- update to 1.20.3

* Sat Jul 25 2015 Remi Collet <remi@fedoraproject.org> - 1.20.0-1
- update to 1.20.0

* Thu Jul 16 2015 Remi Collet <remi@fedoraproject.org> - 1.19.2-2
- swicth from eZ to Zeta Components

* Tue Jul 14 2015 Remi Collet <remi@fedoraproject.org> - 1.19.2-1
- update to 1.19.2

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 1.19.0-1
- update to 1.19.0

* Wed Jul  1 2015 Remi Collet <remi@fedoraproject.org> - 1.18.0-1
- update to 1.18.0
- load dependencies in the autoloader (not in the command)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 15 2015 Remi Collet <remi@fedoraproject.org> - 1.17.0-1
- Update to 1.17.0

* Tue Nov 25 2014 Remi Collet <remi@fedoraproject.org> - 1.16.2-1
- Update to 1.16.2
- switch from pear to github sources

* Wed Nov 12 2014 Remi Collet <remi@fedoraproject.org> - 1.16.0-2
- define date.timezone in phpab command to avoid warning

* Tue Sep 02 2014 Remi Collet <remi@fedoraproject.org> - 1.16.0-1
- Update to 1.16.0

* Thu Aug 14 2014 Remi Collet <remi@fedoraproject.org> - 1.15.1-1
- Update to 1.15.1

* Tue Aug 12 2014 Remi Collet <remi@fedoraproject.org> - 1.15.0-1
- Update to 1.15.0

* Thu Apr 24 2014 Remi Collet <remi@fedoraproject.org> - 1.14.2-1
- Update to 1.14.2

* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 1.14.1-1
- initial package, version 1.14.1
