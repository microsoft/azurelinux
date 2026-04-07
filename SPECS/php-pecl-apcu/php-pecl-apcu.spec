# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Fedora spec file for php-pecl-apcu
#
# SPDX-FileCopyrightText:  Copyright 2013-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%global pie_vend   apcu
%global pie_proj   apcu
%global pecl_name  apcu
%global ini_name   40-%{pecl_name}.ini
%global sources    %{pecl_name}-%{version}

Name:           php-pecl-apcu
Summary:        APC User Cache
Version:        5.1.28
Release:        1%{?dist}
Source0:        https://pecl.php.net/get/%{sources}.tgz
Source1:        %{pecl_name}.ini
Source2:        %{pecl_name}-panel.conf
Source3:        %{pecl_name}.conf.php

License:        PHP-3.01
URL:            https://pecl.php.net/package/APCu

ExcludeArch:    %{ix86}

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  php-devel
BuildRequires:  php-pear

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-%{pecl_name}                 = %{version}
Provides:       php-%{pecl_name}%{?_isa}         = %{version}
Provides:       php-pecl(%{pecl_name})           = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa}   = %{version}
Provides:       php-pie(%{pie_vend}/%{pie_proj}) = %{version}
Provides:       php-%{pie_vend}-%{pie_proj}      = %{version}


%description
APCu is userland caching: APC stripped of opcode caching.

APCu only supports userland caching of variables.

The %{?sub_prefix}php-pecl-apcu-bc package provides a drop
in replacement for APC.


%package devel
Summary:       APCu developer files (header)
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}

%description devel
These are the files needed to compile programs using APCu.


%package -n apcu-panel
Summary:       APCu control panel
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}
Requires:      php(httpd)
Requires:      php-gd
Requires:      httpd

%description -n apcu-panel
This package provides the APCu control panel, with Apache
configuration, available on http://localhost/apcu-panel/


%prep
%setup -qc

sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml

cd %{sources}
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_APCU_VERSION/{s/.* "//;s/".*$//;p}' php_apc.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

# Fix path to configuration file
sed -e s:apc.conf.php:%{_sysconfdir}/apcu-panel/conf.php:g \
    -i  %{sources}/apc.php


%build
cd %{sources}
%{__phpize}
sed -e 's/INSTALL_ROOT/DESTDIR/' -i build/Makefile.global

%configure \
   --enable-apcu \
   --with-php-config=%{__phpconfig}

%make_build


%install
cd %{sources}

# Install extension and configuration
%make_install
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

# Install the package XML file
install -D -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the Control Panel
# Pages
install -D -m 644 -p apc.php  \
        %{buildroot}%{_datadir}/apcu-panel/index.php
# Apache config
install -D -m 644 -p %{SOURCE2} \
        %{buildroot}%{_sysconfdir}/httpd/conf.d/apcu-panel.conf
# Panel config
install -D -m 644 -p %{SOURCE3} \
        %{buildroot}%{_sysconfdir}/apcu-panel/conf.php

# Test & Documentation
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd %{sources}
%{__php} -n \
   -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
   -m | grep '^apcu$'

# Upstream test suite
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
%{__php} -n run-tests.php -q --show-diff


%files
%license %{sources}/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so


%files devel
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}


%files -n apcu-panel
# Need to restrict access, as it contains a clear password
%attr(550,apache,root) %dir %{_sysconfdir}/apcu-panel
%config(noreplace) %{_sysconfdir}/apcu-panel/conf.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/apcu-panel.conf
%{_datadir}/apcu-panel


%changelog
* Tue Dec  9 2025 Remi Collet <remi@remirepo.net> - 5.1.28-1
- update to 5.1.28

* Fri Aug 29 2025 Remi Collet <remi@remirepo.net> - 5.1.27-1
- update to 5.1.27

* Wed Aug  6 2025 Remi Collet <remi@remirepo.net> - 5.1.26-1
- update to 5.1.26

* Tue Jul 29 2025 Remi Collet <remi@remirepo.net> - 5.1.25-2
- cleanup spec file, remove ZTS stuff and very old Obsoletes
- add pie Provides
- refresh configuration for new option and new default values

* Tue Jul 29 2025 Remi Collet <remi@remirepo.net> - 5.1.25-1
- update to 5.1.25
- re-license spec file to CECILL-2.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 14 2024 Remi Collet <remi@fedoraproject.org> - 5.1.24-2
- rebuild for https://fedoraproject.org/wiki/Changes/php84

* Mon Sep 23 2024 Remi Collet <remi@remirepo.net> - 5.1.24-1
- update to 5.1.24

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 16 2024 Remi Collet <remi@remirepo.net> - 5.1.23-4
- drop 32-bit support
  https://fedoraproject.org/wiki/Changes/php_no_32_bit

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Remi Collet <remi@remirepo.net> - 5.1.23-1
- update to 5.1.23

* Tue Oct 03 2023 Remi Collet <remi@remirepo.net> - 5.1.22-6
- rebuild for https://fedoraproject.org/wiki/Changes/php83
- build out of sources tree

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 20 2023 Remi Collet <remi@remirepo.net> - 5.1.22-5
- use SPDX license ID

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 05 2022 Remi Collet <remi@remirepo.net> - 5.1.22-3
- rebuild for https://fedoraproject.org/wiki/Changes/php82

* Tue Sep 20 2022 Remi Collet <remi@remirepo.net> - 5.1.22-2
- drop unneeded build dependency on pcre #2128350

* Mon Sep 19 2022 Remi Collet <remi@remirepo.net> - 5.1.22-1
- update to 5.1.22

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 28 2021 Remi Collet <remi@remirepo.net> - 5.1.21-2
- rebuild for https://fedoraproject.org/wiki/Changes/php81

* Thu Oct  7 2021 Remi Collet <remi@remirepo.net> - 5.1.21-1
- update to 5.1.21

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar  4 2021 Remi Collet <remi@remirepo.net> - 5.1.20-1
- update to 5.1.20

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct  5 2020 Remi Collet <remi@remirepo.net> - 5.1.19-1
- update to 5.1.19

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 28 2019 Remi Collet <remi@remirepo.net> - 5.1.18-1
- update to 5.1.18

* Thu Oct 03 2019 Remi Collet <remi@remirepo.net> - 5.1.17-3
- rebuild for https://fedoraproject.org/wiki/Changes/php74
- add upstream patches for test suite

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb  8 2019 Remi Collet <remi@remirepo.net> - 5.1.17-1
- update to 5.1.17

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec  7 2018 Remi Collet <remi@remirepo.net> - 5.1.15-1
- update to 5.1.15

* Wed Nov 21 2018 Remi Collet <remi@remirepo.net> - 5.1.14-1
- update to 5.1.14 (stable)

* Mon Nov 19 2018 Remi Collet <remi@remirepo.net> - 5.1.13-1
- update to 5.1.13 (stable)

* Thu Oct 11 2018 Remi Collet <remi@remirepo.net> - 5.1.12-3
- Rebuild for https://fedoraproject.org/wiki/Changes/php73

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  9 2018 Remi Collet <remi@remirepo.net> - 5.1.12-1
- update to 5.1.12 (stable)

* Thu Mar  8 2018 Remi Collet <remi@remirepo.net> - 5.1.11-1
- update to 5.1.11 (stable)

* Fri Feb 16 2018 Remi Collet <remi@remirepo.net> - 5.1.10-1
- update to 5.1.10 (stable)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Remi Collet <remi@remirepo.net> - 5.1.9-2
- undefine _strict_symbol_defs_build

* Tue Jan  2 2018 Remi Collet <remi@fedoraproject.org> - 5.1.9-1
- Update to 5.1.9 (php 7, stable)

* Tue Oct 03 2017 Remi Collet <remi@fedoraproject.org> - 5.1.8-5
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Remi Collet <remi@fedoraproject.org> - 5.1.8-1
- Update to 5.1.8 (php 7, stable)

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 5.1.7-2
- rebuild for https://fedoraproject.org/wiki/Changes/php71

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 5.1.7-1
- Update to 5.1.7 (php 7, stable)

* Thu Oct  6 2016 Remi Collet <remi@fedoraproject.org> - 5.1.6-1
- Update to 5.1.6 (php 7, stable)

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 5.1.5-1
- Update to 5.1.5 (php 7, stable)

* Wed Apr 20 2016 Remi Collet <remi@fedoraproject.org> - 4.0.11-1
- Update to 4.0.11 (stable)
- fix license usage and spec cleanup

* Wed Apr 20 2016 Remi Collet <remi@fedoraproject.org> - 4.0.10-4
- add upstream patch, fix FTBFS with 5.6.21RC1, thanks Koschei

* Wed Feb 10 2016 Remi Collet <remi@fedoraproject.org> - 4.0.10-3
- drop scriptlets (replaced file triggers in php-pear)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 4.0.10-1
- Update to 4.0.10 (stable)

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 4.0.8-1
- Update to 4.0.8

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 27 2014 Remi Collet <remi@fedoraproject.org> - 4.0.7-1
- Update to 4.0.7

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 4.0.6-2
- rebuild for https://fedoraproject.org/wiki/Changes/Php56

* Thu Jun 12 2014 Remi Collet <remi@fedoraproject.org> - 4.0.6-1
- Update to 4.0.6 (beta)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 4.0.4-2
- add numerical prefix to extension configuration file

* Sat Mar 01 2014 Remi Collet <remi@fedoraproject.org> - 4.0.4-1
- Update to 4.0.4 (beta)

* Mon Jan 27 2014 Remi Collet <remi@fedoraproject.org> - 4.0.3-1
- Update to 4.0.3 (beta)
- install doc in pecl doc_dir
- install tests in pecl test_dir (in devel)
- cleanup SCL stuff

* Mon Jan 13 2014 Remi Collet <rcollet@redhat.com> - 4.0.2-3
- EPEL-7 build

* Mon Sep 16 2013 Remi Collet <rcollet@redhat.com> - 4.0.2-2
- fix perm on config dir
- improve SCL compatibility
- always provides php-pecl-apc-devel and apc-panel

* Mon Sep 16 2013 Remi Collet <remi@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2

* Sat Jul 27 2013 Remi Collet <remi@fedoraproject.org> - 4.0.1-3
- restore APC serializers ABI (patch merged upstream)

* Mon Jul 15 2013 Remi Collet <rcollet@redhat.com> - 4.0.1-2
- adapt for SCL

* Tue Apr 30 2013 Remi Collet <remi@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1
- add missing scriptlet
- fix Conflicts

* Thu Apr 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-2
- fix segfault when used from command line

* Wed Mar 27 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- first pecl release
- rename from php-apcu to php-pecl-apcu

* Tue Mar 26 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.4.git4322fad
- new snapshot (test before release)

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.3.git647cb2b
- new snapshot with our pull request
- allow to run test suite simultaneously on 32/64 arch
- build warning free

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.2.git6d20302
- new snapshot with full APC compatibility

* Sat Mar 23 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.1.git44e8dd4
- initial package, version 4.0.0
