# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-pecl-rrd
#
# Copyright (c) 2011-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%global with_zts   0%{?__ztsphp:1}
%global pecl_name  rrd
%global ini_name   40-%{pecl_name}.ini
%global sources    %{pecl_name}-%{version}
%global _configure ../%{sources}/configure

Summary:      PHP Bindings for rrdtool
Name:         php-pecl-rrd
Version:      2.0.3
Release:      18%{?dist}
License:      BSD-2-Clause
URL:          https://pecl.php.net/package/rrd

Source0:      https://pecl.php.net/get/%{sources}.tgz

Patch0:       %{pecl_name}-build.patch

ExcludeArch:   %{ix86}

BuildRequires: make
BuildRequires: gcc
BuildRequires: php-devel >= 7.0
BuildRequires: rrdtool
BuildRequires: pkgconfig(librrd) >= 1.3.0
BuildRequires: php-pear

Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Conflicts:    rrdtool-php
Provides:     php-pecl(%{pecl_name})         = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:     php-%{pecl_name}               = %{version}%{?pre}
Provides:     php-%{pecl_name}%{?_isa}       = %{version}%{?pre}


%description
Procedural and simple OO wrapper for rrdtool - data logging and graphing
system for time series data.


%prep 
%setup -c -q

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    -e '/LICENSE/s/role="doc"/role="src"/' \
    -i package.xml

cd %{sources}
%patch -P0 -p1

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_RRD_VERSION/{s/.* "//;s/".*$//;p}' php_rrd.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif


%build
# See https://bugzilla.redhat.com/2264827
# only "const" issues
export CFLAGS="%{optflags} -Wno-incompatible-pointer-types"

cd %{sources}
%{__phpize}

cd ../NTS
%configure --with-php-config=%{__phpconfig}
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%configure --with-php-config=%{__ztsphpconfig}
make %{?_smp_mflags}
%endif


%install
make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 %{sources}/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'
%endif

%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

# See https://bugzilla.redhat.com/1224530 - segfault on ARM
%ifnarch %{arm} s390x
cd %{sources}

if pkg-config librrd --atleast-version=1.5.0
then
  : ignore test failed with rrdtool > 1.5
  rm tests/rrd_{016,017}.phpt
fi
if ! pkg-config librrd --atleast-version=1.4.0
then
  : ignore test failed with rrdtool < 1.4
  rm tests/rrd_{012,017}.phpt
fi

cp ../NTS/tests/data/Makefile   tests/data
cp ../NTS/tests/rrdtool-bin.inc tests
make -C tests/data clean
make -C tests/data all

TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php -q --show-diff
%endif


%files
%license %{sources}/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 14 2024 Remi Collet <remi@fedoraproject.org> - 2.0.3-16
- rebuild for https://fedoraproject.org/wiki/Changes/php84

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 16 2024 Remi Collet <remi@remirepo.net> - 2.0.3-14
- drop 32-bit support
  https://fedoraproject.org/wiki/Changes/php_no_32_bit

* Mon Feb 19 2024 Remi Collet <remi@remirepo.net> - 2.0.3-13
- ignore incompatible-pointer-types see #2264827

* Mon Jan 29 2024 Remi Collet <remi@remirepo.net> - 2.0.3-12
- fix incompatible pointer types using patch from
  https://github.com/php/pecl-processing-rrd/pull/4
- build out of sources tree

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 03 2023 Remi Collet <remi@remirepo.net> - 2.0.3-10
- rebuild for https://fedoraproject.org/wiki/Changes/php83

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 20 2023 Remi Collet <remi@remirepo.net> - 2.0.3-8
- use SPDX license ID

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 05 2022 Remi Collet <remi@remirepo.net> - 2.0.3-6
- rebuild for https://fedoraproject.org/wiki/Changes/php82

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 28 2021 Remi Collet <remi@remirepo.net> - 2.0.3-3
- rebuild for https://fedoraproject.org/wiki/Changes/php81

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Apr 28 2021 Remi Collet <remi@remirepo.net> - 2.0.3-1
- update to 2.0.3

* Mon Apr 19 2021 Remi Collet <remi@remirepo.net> - 2.0.2-1
- update to 2.0.2

* Fri Mar  5 2021 Remi Collet <remi@remirepo.net> - 2.0.1-17
- rebuild for https://fedoraproject.org/wiki/Changes/php80
- add upstream patch for PHP 8

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Remi Collet <remi@remirepo.net> - 2.0.1-13
- rebuild for https://fedoraproject.org/wiki/Changes/php74

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Remi Collet <remi@remirepo.net> - 2.0.1-10
- Rebuild for https://fedoraproject.org/wiki/Changes/php73

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Remi Collet <remi@remirepo.net> - 2.0.1-7
- undefine _strict_symbol_defs_build

* Tue Oct 03 2017 Remi Collet <remi@fedoraproject.org> - 2.0.1-6
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- rebuild for https://fedoraproject.org/wiki/Changes/php71

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Thu Apr 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-10
- rebuild for new rrdtool
- fix license management
- don't provide the test suite

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-9
- drop scriptlets (replaced by file triggers in php-pear)
- cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 24 2015 Remi Collet <remi@fedoraproject.org> - 1.1.3-6
- ignore failed tests with rrdtool 1.5
  FTBFS detected by Koschei, reported upstream
- skip test suite on arm

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.3-4
- rebuild for https://fedoraproject.org/wiki/Changes/Php56

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Remi Collet <rcollet@redhat.com> - 1.1.3-2
- add numerical prefix to extension configuration file

* Wed Jan 15 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3 (stable)
- drop merged patch

* Tue Jan 14 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 (stable)
- install doc in pecl doc_dir
- install tests in pecl test_dir
- add conditional build of ZTS extension

* Mon Sep 09 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-2
- patch for build warning
- patch to fix test result with recent rrdtool

* Mon Sep 09 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.1.0-3
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 12 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable), api 1.1.0 (stable)

* Tue Jul 31 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-4
- ignore test results (fails with rrdtool 1.4.7)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-3
- build against php 5.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Remi Collet <remi@fedoraproject.org> 1.0.5-1
- update to 1.0.5
- change license from PHP to BSD

* Tue Aug 16 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.4-1
- Version 1.0.4 (stable) - API 1.0.4 (stable)
- fix filters

* Fri Apr 29 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.3 (stable)
- no change in sources

* Wed Apr 20 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.2 (stable)
- no change in sources

* Sat Apr 16 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.1 (stable)
- no change in sources
- remove generated Changelog (only latest version, no real value)

* Tue Apr 12 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.0-1
- Version 1.0.0 (stable) - API 1.0.0 (stable)
- remove all patches merged by upstream

* Sat Mar 05 2011 Remi Collet <Fedora@FamilleCollet.com> 0.10.0-2
- improved patches
- implement rrd_strversion

* Fri Mar 04 2011 Remi Collet <Fedora@FamilleCollet.com> 0.10.0-1
- Version 0.10.0 (stable) - API 0.10.0 (beta)
- remove patches, merged upstream
- add links to 5 new upstream bugs

* Mon Jan 03 2011 Remi Collet <Fedora@FamilleCollet.com> 0.9.0-1
- Version 0.9.0 (beta) - API 0.9.0 (beta)
- initial RPM

