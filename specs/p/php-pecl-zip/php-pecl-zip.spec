# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Fedora spec file for php-pecl-zip
#
# SPDX-FileCopyrightText:  Copyright 2013-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%global pecl_name        zip
%global pie_vend         pecl
%global pie_proj         zip
%global ini_name         40-%{pecl_name}.ini
%global upstream_version 1.22.7
#global upstream_prever  RC6
%global sources          %{pecl_name}-%{upstream_version}%{?upstream_prever}

Summary:      A ZIP archive management extension
Name:         php-pecl-zip
Version:      %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release: 2%{?dist}
License:      PHP-3.01
URL:          https://pecl.php.net/package/zip

Source0:      https://pecl.php.net/get/%{sources}.tgz

ExcludeArch:   %{ix86}

BuildRequires: make
BuildRequires: gcc
BuildRequires: php-devel
BuildRequires: pkgconfig(libzip) >= 1.0.0
BuildRequires: zlib-devel
BuildRequires: php-pear

Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

# Extension
Provides:     php-%{pecl_name} = %{version}-%{release}
Provides:     php-%{pecl_name}%{?_isa} = %{version}-%{release}
# PECL
Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}
# PIE
Provides:     php-pie(%{pie_vend}/%{pie_proj}) = %{version}


%description
Zip is an extension to create and read zip files.


%prep 
%setup -c -q

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    -e '/LICENSE/s/role="doc"/role="src"/' \
    -i package.xml

cd %{sources}
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_ZIP_VERSION/{s/.* "//;s/".*$//;p}' php8/php_zip.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}.
   exit 1
fi

cd ..
: Create the configuration file
cat >%{ini_name} << 'EOF'
; Enable ZIP extension module
extension=%{pecl_name}.so
EOF


%build
cd %{sources}
%{__phpize}
sed -e 's/INSTALL_ROOT/DESTDIR/' -i build/Makefile.global

%configure \
  --with-libzip \
  --with-libdir=%{_lib} \
  --with-php-config=%{__phpconfig}

%make_build


%install
: Install the configuration file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

: Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

cd %{sources}
: Install the extension
%make_install

: Install the Documentation
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd %{sources}
: minimal load test of the extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

: upstream test suite
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
TEST_PHP_EXECUTABLE=%{__php} \
%{__php} -n run-tests.php -q --show-diff


%files
%license %{sources}/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so


%changelog
* Thu Sep 25 2025 Remi Collet <remi@remirepo.net> - 1.22.7-1
- update to 1.22.7

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed May  7 2025 Remi Collet <remi@remirepo.net> - 1.22.6-1
- update to 1.22.6

* Thu Feb 20 2025 Remi Collet <remi@remirepo.net> - 1.22.5-1
- update to 1.22.5
- re-license spec file to CECILL-2.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 14 2024 Remi Collet <remi@fedoraproject.org> - 1.22.4-2
- rebuild for https://fedoraproject.org/wiki/Changes/php84

* Thu Sep 26 2024 Remi Collet <remi@remirepo.net> - 1.23.4-1
- update to 1.22.4
- modernize spec file

* Thu Aug 22 2024 Remi Collet <remi@remirepo.net> - 1.22.3-6
- rebuild for broken ABI in 8.3.10, fixed in 8.3.11RC2

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 16 2024 Remi Collet <remi@remirepo.net> - 1.22.3-4
- drop 32-bit support
  https://fedoraproject.org/wiki/Changes/php_no_32_bit

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 14 2023 Remi Collet <remi@remirepo.net> - 1.22.3-1
- update to 1.22.3
- build out of sources tree

* Tue Oct 03 2023 Remi Collet <remi@remirepo.net> - 1.22.2-2
- rebuild for https://fedoraproject.org/wiki/Changes/php83

* Thu Aug 24 2023 Remi Collet <remi@remirepo.net> - 1.22.2-1
- update to 1.22.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Remi Collet <remi@remirepo.net> - 1.22.1-1
- update to 1.22.1

* Thu Apr 20 2023 Remi Collet <remi@remirepo.net> - 1.21.1-3
- use SPDX license ID

* Wed Oct 05 2022 Remi Collet <remi@remirepo.net> - 1.21.1-2
- rebuild for https://fedoraproject.org/wiki/Changes/php82

* Fri Sep 16 2022 Remi Collet <remi@remirepo.net> - 1.21.1-1
- update to 1.21.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Remi Collet <remi@remirepo.net> - 1.21.0-1
- update to 1.21.0

* Mon May  2 2022 Remi Collet <remi@remirepo.net> - 1.20.1-1
- update to 1.20.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 28 2021 Remi Collet <remi@remirepo.net> - 1.20.0-2
- rebuild for https://fedoraproject.org/wiki/Changes/php81

* Tue Oct 12 2021 Remi Collet <remi@remirepo.net> - 1.20.0-1
- update to 1.20.0
- run test suite in parallel

* Wed Sep  1 2021 Remi Collet <remi@remirepo.net> - 1.19.4-1
- update to 1.19.4

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun  7 2021 Remi Collet <remi@remirepo.net> - 1.19.3-1
- update to 1.19.3

* Thu Mar  4 2021 Remi Collet <remi@remirepo.net> - 1.19.2-3
- rebuild for https://fedoraproject.org/wiki/Changes/php80

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Remi Collet <remi@remirepo.net> - 1.19.2-1
- update to 1.19.2

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 1.19.1-1
- update to 1.19.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun  8 2020 Remi Collet <remi@remirepo.net> - 1.19.0-1
- update to 1.19.0

* Fri Mar 20 2020 Remi Collet <remi@remirepo.net> - 1.18.2-1
- update to 1.18.2

* Thu Mar 19 2020 Remi Collet <remi@remirepo.net> - 1.18.1-1
- update to 1.18.1

* Mon Mar 16 2020 Remi Collet <remi@remirepo.net> - 1.18.0-1
- update to 1.18.0

* Mon Mar  9 2020 Remi Collet <remi@remirepo.net> - 1.18.0~RC6-1
- update to 1.18.0RC6

* Fri Feb 28 2020 Remi Collet <remi@remirepo.net> - 1.17.2-1
- Update to 1.17.2

* Mon Feb  3 2020 Remi Collet <remi@remirepo.net> - 1.17.1-1
- Update to 1.17.1

* Fri Jan 31 2020 Remi Collet <remi@remirepo.net> - 1.17.0-1
- Update to 1.17.0

* Wed Jan 29 2020 Remi Collet <remi@remirepo.net> - 1.16.1-1
- Update to 1.16.1

* Tue Jan 28 2020 Remi Collet <remi@remirepo.net> - 1.16.0-1
- Update to 1.16.0

* Thu Oct 03 2019 Remi Collet <remi@remirepo.net> - 1.15.5-2
- rebuild for https://fedoraproject.org/wiki/Changes/php74

* Tue Sep 10 2019 Remi Collet <remi@remirepo.net> - 1.15.5-1
- Update to 1.15.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Remi Collet <remi@remirepo.net> - 1.15.4-2
- Rebuild for https://fedoraproject.org/wiki/Changes/php73

* Wed Oct  3 2018 Remi Collet <remi@remirepo.net> - 1.15.4-1
- Update to 1.15.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Remi Collet <remi@remirepo.net> - 1.15.3-1
- Update to 1.15.3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Remi Collet <remi@remirepo.net> - 1.15.2-2
- undefine _strict_symbol_defs_build

* Tue Dec 19 2017 Remi Collet <remi@fedoraproject.org> - 1.15.2-1
- Update to 1.15.2

* Tue Oct 03 2017 Remi Collet <remi@fedoraproject.org> - 1.15.1-4
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 11 2017 Remi Collet <remi@remirepo.net> - 1.15.1-1
- Update to 1.15.1

* Mon Jul 10 2017 Remi Collet <remi@remirepo.net> - 1.15.0-1
- Update to 1.15.0

* Wed Apr  5 2017 Remi Collet <remi@remirepo.net> - 1.14.0-1
- Update to 1.14.0

* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> - 1.13.5-4
- rebuild for new libzip

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 1.13.5-2
- rebuild for https://fedoraproject.org/wiki/Changes/php71

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.13.5-1
- Update to 1.13.5

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 1.13.4-1
- Update to 1.13.4

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 1.13.3-2
- rebuild for https://fedoraproject.org/wiki/Changes/php70

* Thu Jun 23 2016 Remi Collet <remi@fedoraproject.org> - 1.13.3-1
- Update to 1.13.3

* Tue Mar  1 2016 Remi Collet <remi@fedoraproject.org> - 1.13.2-1
- Update to 1.13.2
- fix license management

* Wed Feb 10 2016 Remi Collet <remi@fedoraproject.org> - 1.13.1-3
- drop scriptlets (replaced file triggers in php-pear)
- ignore 1 test (change in php, FTBFS detected by Koschei)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 10 2015 Remi Collet <remi@fedoraproject.org> - 1.13.1-1
- Update to 1.13.1 (no change)

* Mon Sep  7 2015 Remi Collet <remi@fedoraproject.org> - 1.13.0-1
- Update to 1.13.0
- raise dependency on libzip 1.0.0
- don't install/register tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 1.12.5-2
- rebuild for new libzip

* Thu Apr 16 2015 Remi Collet <remi@fedoraproject.org> - 1.12.5-1
- Update to 1.12.5 (stable)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 1.12.4-4
- rebuild for https://fedoraproject.org/wiki/Changes/Php56

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Remi Collet <rcollet@redhat.com> - 1.12.4-2
- add numerical prefix to extension configuration file

* Wed Jan 29 2014 Remi Collet <remi@fedoraproject.org> - 1.12.4-1
- Update to 1.12.4 (stable) for libzip 0.11.2

* Thu Dec 12 2013 Remi Collet <remi@fedoraproject.org> - 1.12.3-1
- Update to 1.12.3 (stable)
- drop merged patch

* Thu Oct 24 2013 Remi Collet <remi@fedoraproject.org> 1.12.2-2
- upstream patch, don't use any libzip private struct
- drop LICENSE_libzip when system version is used
- always build ZTS extension

* Wed Oct 23 2013 Remi Collet <remi@fedoraproject.org> 1.12.2-1
- update to 1.12.2 (beta)
- drop merged patches
- install doc in pecl doc_dir
- install tests in pecl test_dir

* Thu Aug 22 2013 Remi Collet <rcollet@redhat.com> 1.12.1-5
- really really fix all spurious-executable-perm

* Thu Aug 22 2013 Remi Collet <rcollet@redhat.com> 1.12.1-4
- really fix all spurious-executable-perm

* Thu Aug 22 2013 Remi Collet <rcollet@redhat.com> 1.12.1-3
- fixes from review comments #999313: clarify License
- drop execution right from sources
- BR libzip-devel always needed

* Tue Aug 20 2013 Remi Collet <rcollet@redhat.com> 1.12.1-2
- refresh our merged patches from upstream git

* Thu Aug 08 2013 Remi Collet <rcollet@redhat.com> 1.12.1-1
- New spec for version 1.12.1 (beta)
