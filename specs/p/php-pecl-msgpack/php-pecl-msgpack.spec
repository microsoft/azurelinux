# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Fedora spec file for php-pecl-msgpack
#
# Copyright (c) 2012-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# system library is outdated, and bundled library includes not yet released changes
# BTW, only pack_template.h and unpack_template.h headers are used
%bcond_with              msgpack

# to disable test suite
%bcond_without           tests

%global upstream_version 3.0.0
#global upstream_prever  RC2
#global upstream_lower   RC2
%global sources          %{pecl_name}-%{upstream_version}%{?upstream_prever}
%global _configure       ../%{sources}/configure

%global pecl_name        msgpack
%global ini_name         40-%{pecl_name}.ini

Summary:       API for communicating with MessagePack serialization
Name:          php-pecl-msgpack
Version:       %{upstream_version}%{?upstream_lower:~%{upstream_lower}}
Release:       4%{?dist}
Source:        https://pecl.php.net/get/%{pecl_name}-%{upstream_version}%{?upstream_prever}.tgz
License:       BSD-3-Clause
URL:           https://pecl.php.net/package/msgpack

ExcludeArch:   %{ix86}

BuildRequires: php-devel >= 7.0
BuildRequires: php-pear
BuildRequires: php-pecl-apcu-devel
%if %{with msgpack}
BuildRequires: msgpack-devel
%else
Provides:      bundled(msgpack) = 3.2.0
%endif

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

Provides:      php-%{pecl_name} = %{version}
Provides:      php-%{pecl_name}%{?_isa} = %{version}
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}


%description
This extension provide API for communicating with MessagePack serialization.

MessagePack is an efficient binary serialization format. It lets you exchange
data among multiple languages like JSON but it's faster and smaller.
For example, small integers (like flags or error code) are encoded into a
single byte, and typical short strings only require an extra byte in addition
to the strings themselves.

If you ever wished to use JSON for convenience (storing an image with metadata)
but could not for technical reasons (encoding, size, speed...), MessagePack is
a perfect replacement.


%package devel
Summary:       MessagePack developer files (header)
Requires:      php-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}

%description devel
These are the files needed to compile programs using MessagePack serializer.


%prep
%setup -qc

sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml

cd %{sources}
%if %{with msgpack}
# use system library
rm -rf msgpack
%endif

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_MSGPACK_VERSION/{s/.* "//;s/".*$//;p}' php_msgpack.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}%{?gh_date:-dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}%{?gh_date:-dev}.
   exit 1
fi
cd ..

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable MessagePack extension module
extension = %{pecl_name}.so

; Configuration options

;msgpack.error_display = On
;msgpack.php_only = On
;msgpack.assoc = On
;msgpack.illegal_key_insert = Off
;msgpack.use_str8_serialization = On
EOF


%build
cd %{sources}
%{__phpize}
sed -e 's/INSTALL_ROOT/DESTDIR/' -i build/Makefile.global

%configure --with-php-config=%{__phpconfig}
%make_build



%install
: Install the configuration file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

: Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

cd %{sources}
: Install the extension
%make_install

: Install Test and Documentation
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f tests/$i ] && install -Dpm 644 tests/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/tests/$i
   [ -f $i ]       && install -Dpm 644 $i       %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd %{sources}
# Erratic results
rm tests/034.phpt
# too slow
rm tests/035.phpt

: Minimal load test for the extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with tests}
: Upstream test suite
TEST_PHP_ARGS="-n -d extension=apcu.so -d extension=$PWD/modules/%{pecl_name}.so" \
%{__php} -n run-tests.php -q --show-diff %{?_smp_mflags}
%endif


%files
%license %{sources}/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so


%files devel
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 14 2024 Remi Collet <remi@fedoraproject.org> - 3.0.0-2
- rebuild for https://fedoraproject.org/wiki/Changes/php84

* Thu Sep 26 2024 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- modernize spec file
- add APCu support

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 16 2024 Remi Collet <remi@remirepo.net> - 2.2.0-6
- drop 32-bit support
  https://fedoraproject.org/wiki/Changes/php_no_32_bit

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 03 2023 Remi Collet <remi@remirepo.net> - 2.2.0-3
- rebuild for https://fedoraproject.org/wiki/Changes/php83

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun  2 2023 Remi Collet <remi@remirepo.net> - 2.2.0-1
- update to 2.2.0
- build out of sources tree
- use parallel execution for test suite

* Thu Apr 20 2023 Remi Collet <remi@remirepo.net> - 2.2.0~RC2-2
- use SPDX license ID

* Fri Oct  7 2022 Remi Collet <remi@remirepo.net> - 2.2.0~RC2-1
- update to 2.2.0RC2

* Wed Oct 05 2022 Remi Collet <remi@remirepo.net> - 2.2.0~RC1-4
- rebuild for https://fedoraproject.org/wiki/Changes/php82

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0~RC1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0~RC1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 28 2021 Remi Collet <remi@remirepo.net> - 2.2.0~RC1-1
- update to 2.2.0RC1
- rebuild for https://fedoraproject.org/wiki/Changes/php81

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar  4 2021 Remi Collet <remi@remirepo.net> - 2.1.2-2
- rebuild for https://fedoraproject.org/wiki/Changes/php80

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Remi Collet <remi@remirepo.net> - 2.1.2-1
- update to 2.1.2

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 2.1.1-1
- update to 2.1.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar  2 2020 Remi Collet <remi@remirepo.net> - 2.1.0-1
- update to 2.1.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0~beta1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Remi Collet <remi@remirepo.net> - 2.1.0~beta1-1
- update to 2.1.0beta1

* Thu Oct 03 2019 Remi Collet <remi@remirepo.net> - 2.0.3-4
- rebuild for https://fedoraproject.org/wiki/Changes/php74

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 20 2018 Remi Collet <remi@remirepo.net> - 2.0.3-1
- update to 2.0.3

* Thu Oct 11 2018 Remi Collet <remi@remirepo.net> - 2.0.3-0.1.20171026.943d272
- update to 2.0.3-dev for PHP 7.3 with patches from
  https://github.com/msgpack/msgpack-php/pull/124
  https://github.com/msgpack/msgpack-php/pull/127
- ignore test suite result for now

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Remi Collet <remi@remirepo.net> - 2.0.2-6
- undefine _strict_symbol_defs_build

* Tue Oct 03 2017 Remi Collet <remi@fedoraproject.org> - 2.0.2-5
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec  7 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- rebuild for https://fedoraproject.org/wiki/Changes/php71
- add patch for PHP 7.1

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 (php 7, beta)
- add patch for PHP 7.1
  open https://github.com/msgpack/msgpack-php/pull/87

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 0.5.7-3
- drop scriptlets (replaced by file triggers in php-pear)
- cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug 30 2015 Remi Collet <remi@fedoraproject.org> - 0.5.7-1
- Update to 0.5.7 (beta)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 0.5.5-8
- rebuild for https://fedoraproject.org/wiki/Changes/Php56

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Remi Collet <rcollet@redhat.com> - 0.5.5-6
- add numerical prefix to extension configuration file

* Tue Mar 11 2014 Remi Collet <remi@fedoraproject.org> - 0.5.5-5
- cleanups
- move doc in pecl_docdir
- move tests in pecl_testdir (devel)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  2 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-3
- use system msgpack library headers

* Tue Mar 26 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-2
- cleanups

* Wed Feb 20 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-1
- Update to 0.5.5

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 0.5.3-1.1
- also provides php-msgpack

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 0.5.3-1
- update to 0.5.3 (beta)

* Sat Sep 15 2012 Remi Collet <remi@fedoraproject.org> - 0.5.2-1
- initial package, version 0.5.2 (beta)

