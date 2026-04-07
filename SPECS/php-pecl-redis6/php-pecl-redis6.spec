# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# RHEL/Fedora spec file for php-pecl-redis6
# without SCL compatibility from:
#
# remirepo spec file for php-pecl-redis6
#
# SPDX-FileCopyrightText:  Copyright 2012-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_without       tests
%if 0%{?fedora}
# optional compressors/serializers enabled by default
%bcond_without       igbinary
%bcond_without       msgpack
%bcond_without       liblzf
%else
# optional compressors/serializers disabled by default
%bcond_with          igbinary
%bcond_with          msgpack
%bcond_with          liblzf
%endif
%bcond_without       valkey

%global pie_vend     phpredis
%global pie_proj     phpredis
%global pecl_name    redis
# after 20-json, 40-igbinary and 40-msgpack
%global ini_name     50-%{pecl_name}.ini

%global upstream_version 6.3.0
#global upstream_prever  RC2
%global sources          %{pecl_name}-%{upstream_version}%{?upstream_prever}

Summary:       PHP extension for interfacing with key-value stores
Name:          php-pecl-redis6
Version:       %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:       1%{?dist}
License:       PHP-3.01
URL:           https://pecl.php.net/package/redis
Source0:       https://pecl.php.net/get/%{sources}.tgz

ExcludeArch:   %{ix86}

BuildRequires: make
BuildRequires: gcc
BuildRequires: php-devel >= 7.4
BuildRequires: php-pear
BuildRequires: php-json
%if %{with igbinary}
BuildRequires: php-pecl-igbinary-devel
%endif
%if %{with msgpack}
BuildRequires: php-pecl-msgpack-devel >= 2.0.3
%endif
%if %{with liblzf}
BuildRequires: pkgconfig(liblzf)
%endif
BuildRequires: pkgconfig(libzstd) >= 1.3.0
BuildRequires: pkgconfig(liblz4)
# to run Test suite
%if %{with tests}
%if %{with valkey}
BuildRequires: valkey
%else
BuildRequires: redis
%endif
%endif

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
Requires:      php-json%{?_isa}
%if %{with igbinary}
Requires:      php-igbinary%{?_isa}
%endif
%if %{with msgpack}
Requires:      php-msgpack%{?_isa}
%endif

Provides:      php-%{pecl_name}                 = %{version}
Provides:      php-%{pecl_name}%{?_isa}         = %{version}
Provides:      php-pecl(%{pecl_name})           = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa}   = %{version}
Provides:      php-pie(%{pie_vend}/%{pie_proj}) = %{version}
Provides:      php-%{pie_vend}-%{pie_proj}      = %{version}

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 10 || "%{php_version}" > "8.4"
Obsoletes:     php-pecl-%{pecl_name}          < 6
Provides:      php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:      php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
Obsoletes:     php-pecl-%{pecl_name}4         < 6
Provides:      php-pecl-%{pecl_name}4         = %{version}-%{release}
Provides:      php-pecl-%{pecl_name}4%{?_isa} = %{version}-%{release}
Obsoletes:     php-pecl-%{pecl_name}5         < 6
Provides:      php-pecl-%{pecl_name}5         = %{version}-%{release}
Provides:      php-pecl-%{pecl_name}5%{?_isa} = %{version}-%{release}
%else
# A single version can be installed
Conflicts:     php-pecl-%{pecl_name}  < 6
Conflicts:     php-pecl-%{pecl_name}4 < 6
Conflicts:     php-pecl-%{pecl_name}5 < 6
%endif


%description
This extension provides an API for communicating with RESP-based key-value
stores, such as Redis, Valkey, and KeyDB.

This client implements most of the latest API.
As method only works when also implemented on the server side,
some doesn't work with an old server version.


%prep
%setup -q -c

# Don't install/register tests, license, and bundled library
sed -e 's/role="test"/role="src"/' \
    -e '/LICENSE/s/role="doc"/role="src"/' \
    -e '/liblzf/d' \
    -i package.xml

cd %{sources}
# Use system library
rm -r liblzf

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_REDIS_VERSION/{s/.* "//;s/".*$//;p}' php_redis.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}.
   exit 1
fi
cd ..

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so

; phpredis can be used to store PHP sessions. 
; To do this, uncomment and configure below

; RPM note : save_handler and save_path are defined
; for mod_php, in /etc/httpd/conf.d/php.conf
; for php-fpm, in %{_sysconfdir}/php-fpm.d/*conf

;session.save_handler = %{pecl_name}
;session.save_path = "tcp://host1:6379?weight=1, tcp://host2:6379?weight=2&timeout=2.5, tcp://host3:6379?weight=2"

; Configuration
;redis.arrays.algorithm = ''
;redis.arrays.auth = ''
;redis.arrays.autorehash = 0
;redis.arrays.connecttimeout = 0
;redis.arrays.consistent = 0
;redis.arrays.distributor = ''
;redis.arrays.functions = ''
;redis.arrays.hosts = ''
;redis.arrays.index = 0
;redis.arrays.lazyconnect = 0
;redis.arrays.names = ''
;redis.arrays.pconnect = 0
;redis.arrays.previous = ''
;redis.arrays.readtimeout = 0
;redis.arrays.retryinterval = 0
;redis.clusters.auth = 0
;redis.clusters.cache_slots = 0
;redis.clusters.persistent = 0
;redis.clusters.read_timeout = 0
;redis.clusters.seeds = ''
;redis.clusters.timeout = 0
;redis.pconnect.pooling_enabled = 1
;redis.pconnect.connection_limit = 0
;redis.pconnect.echo_check_liveness = 1
;redis.pconnect.pool_detect_dirty = 0
;redis.pconnect.pool_poll_timeout = 0
;redis.pconnect.pool_pattern => ''
;redis.session.locking_enabled = 0
;redis.session.lock_expire = 0
;redis.session.lock_retries = 100
;redis.session.lock_wait_time = 20000
;redis.session.early_refresh = 0
;redis.session.compression = none
;redis.session.compression_level = 3
EOF


%build
peclconf() {
%configure \
    --enable-redis \
    --enable-redis-session \
%if %{with igbinary}
    --enable-redis-igbinary \
%endif
%if %{with msgpack}
    --enable-redis-msgpack \
%endif
%if %{with liblzf}
    --enable-redis-lzf \
    --with-liblzf \
%else
    --disable-redis-lzf \
%endif
    --enable-redis-zstd \
    --with-libzstd \
    --enable-redis-lz4 \
    --with-liblz4 \
    --with-php-config=$1
}

cd %{sources}
%{__phpize}
sed -e 's/INSTALL_ROOT/DESTDIR/' -i build/Makefile.global

peclconf %{__phpconfig}
%make_build


%install
# Install the configuration file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

cd %{sources}
%make_install

# Documentation
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
# simple module load test
DEPS="--no-php-ini"
for i in json igbinary msgpack
do  [ -f %{php_extdir}/${i}.so ] && DEPS="$DEPS --define extension=${i}.so"
done

%{__php} $DEPS \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with tests}
cd %{sources}/tests
: Ignore ONLINE test
sed -e 's/testConnectException/skipConnectException/' -i RedisTest.php

: Launch redis server
%if %{with valkey}
SRV=%{_bindir}/valkey-server
CLI=%{_bindir}/valkey-cli
%else
SRV=%{_bindir}/redis-server
CLI=%{_bindir}/redis-cli
%endif

mkdir -p data
pidfile=$PWD/server.pid
port=$(%{__php} -r 'echo 9000 + PHP_MAJOR_VERSION*100 + PHP_MINOR_VERSION*10 + PHP_INT_SIZE;')
$SRV   \
    --bind      127.0.0.1      \
    --port      $port          \
    --daemonize yes            \
    --logfile   $PWD/server.log \
    --dir       $PWD/data      \
    --pidfile   $pidfile


: Run the test Suite
sed -e "s/6379/$port/" -i *.php

ret=0
export TEST_PHP_EXECUTABLE=%{__php}
export TEST_PHP_ARGS="$DEPS \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so"
$TEST_PHP_EXECUTABLE $TEST_PHP_ARGS TestRedis.php || ret=1

: Cleanup
if [ -f $pidfile ]; then
   $CLI -p $port shutdown nosave
   sleep 2
fi
cat $PWD/server.log

exit $ret
%else
: Upstream test suite disabled
%endif

%files
%license %{sources}/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%{php_extdir}/%{pecl_name}.so
%config(noreplace) %{php_inidir}/%{ini_name}


%changelog
* Fri Nov  7 2025 Remi Collet <remi@remirepo.net> - 6.3.0-1
- update to 6.3.0

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Mar 25 2025 Remi Collet <remi@remirepo.net> - 6.2.0-1
- update to 6.2.0
- re-license spec file to CECILL-2.1
- add virtual provides for pie

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 20 2024 Remi Collet <rcollet@redhat.com> - 6.1.0-3
- ignore 1 ONLINE test

* Mon Oct 14 2024 Remi Collet <remi@fedoraproject.org> - 6.1.0-2
- rebuild for https://fedoraproject.org/wiki/Changes/php84

* Mon Oct  7 2024 Remi Collet <remi@remirepo.net> - 6.1.0-1
- update to 6.1.0

* Mon Sep 16 2024 Remi Collet <remi@remirepo.net> - 6.0.2-3
- cleanup and modernize spec file

* Thu Jul 11 2024 Remi Collet <remi@remirepo.net> - 6.0.2-2
- use valkey on Fedora 41
- add upstream patch for PHP 8.4

* Mon Oct 23 2023 Remi Collet <remi@remirepo.net> - 6.0.2-1
- update to 6.0.2

* Mon Sep 25 2023 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1

* Mon Sep 11 2023 Remi Collet <remi@remirepo.net> - 6.0.0-1
- cleanup SCL stuff for Fedora review

* Mon Sep 11 2023 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0

* Mon Aug 21 2023 Remi Collet <remi@remirepo.net> - 6.0.0~RC2-1
- update to 6.0.0RC2

* Wed Aug  2 2023 Remi Collet <remi@remirepo.net> - 6.0.0~RC1-1
- update to 6.0.0RC1
- rename to php-pecl-redis6 for new API
- disable test suite for SCL
- open https://github.com/phpredis/phpredis/pull/2367 PHP 7.2 required

* Wed Jul 12 2023 Remi Collet <remi@remirepo.net> - 5.3.7-4
- build out of sources tree

* Thu Mar 23 2023 Remi Collet <remi@remirepo.net> - 5.3.7-3
- add patch for test suite with redis 7.2 from
  https://github.com/phpredis/phpredis/pull/2335

* Fri Sep  9 2022 Remi Collet <remi@remirepo.net> - 5.3.7-2
- rebuild for PHP 8.2 with msgpack and igbinary

* Wed Feb 16 2022 Remi Collet <remi@remirepo.net> - 5.3.7-1
- update to 5.3.7

* Mon Feb 14 2022 Remi Collet <remi@remirepo.net> - 5.3.7~RC2-1
- update to 5.3.7RC2 (beta, no change)

* Wed Feb  2 2022 Remi Collet <remi@remirepo.net> - 5.3.7~RC1-1
- update to 5.3.7RC1 (alpha)

* Tue Jan 18 2022 Remi Collet <remi@remirepo.net> - 5.3.6-1
- update to 5.3.6

* Mon Dec 20 2021 Remi Collet <remi@remirepo.net> - 5.3.5-1
- update to 5.3.5

* Wed Dec  8 2021 Remi Collet <remi@remirepo.net> - 5.3.5-0
- test build for upcoming 5.3.5

* Wed Nov 17 2021 Remi Collet <remi@remirepo.net> - 5.3.5~RC1-1
- update to 5.3.5RC1

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 5.3.4-2
- rebuild for 8.1.0RC1

* Thu Mar 25 2021 Remi Collet <remi@remirepo.net> - 5.3.4-1
- update to 5.3.4

* Wed Feb  3 2021 Remi Collet <remi@remirepo.net> - 5.3.3-1
- update to 5.3.3

* Thu Oct 22 2020 Remi Collet <remi@remirepo.net> - 5.3.2-1
- update to 5.3.2

* Wed Oct 14 2020 Remi Collet <remi@remirepo.net> - 5.3.2~RC2-1
- update to 5.3.2RC2

* Wed Oct  7 2020 Remi Collet <remi@remirepo.net> - 5.3.2~RC1-1
- update to 5.3.2RC1
- drop patch merged upstream

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 5.3.1-4
- rebuild for PHP 8.0.0RC1

* Wed Sep 23 2020 Remi Collet <remi@remirepo.net> - 5.3.1-3
- enable msgpack serializer with PHP 8

* Fri Sep 11 2020 Remi Collet <remi@remirepo.net> - 5.3.1-2
- add patches for PHP 8 from upstream and
  https://github.com/phpredis/phpredis/pull/1845
- disable msgpack serializer with PHP 8

* Wed Jul  8 2020 Remi Collet <remi@remirepo.net> - 5.3.1-1
- update to 5.3.1

* Wed Jul  1 2020 Remi Collet <remi@remirepo.net> - 5.3.0-1
- update to 5.3.0

* Sat Jun 27 2020 Remi Collet <remi@remirepo.net> - 5.3.0~RC2-1
- update to 5.3.0RC2
- drop patch merged upstream

* Fri Jun 26 2020 Remi Collet <remi@remirepo.net> - 5.3.0~RC1-1
- update to 5.3.0RC1
- enable lz4 compression support
- drop patch merged upstream
- add upstream patch to fix lz4 library name
- add new option in provided configuration file

* Wed May  6 2020 Remi Collet <remi@remirepo.net> - 5.2.2-2
- test build for https://github.com/phpredis/phpredis/pull/1750

* Wed May  6 2020 Remi Collet <remi@remirepo.net> - 5.2.2-1
- update to 5.2.2
- refresh options in provided configuration file

* Fri Mar 20 2020 Remi Collet <remi@remirepo.net> - 5.2.1-1
- update to 5.2.1

* Mon Mar  2 2020 Remi Collet <remi@remirepo.net> - 5.2.0-1
- update to 5.2.0

* Fri Feb 21 2020 Remi Collet <remi@remirepo.net> - 5.2.0~RC2-1
- update to 5.2.0RC2

* Mon Feb 17 2020 Remi Collet <remi@remirepo.net> - 5.2.0~RC1-1
- update to 5.2.0RC1

* Mon Nov 11 2019 Remi Collet <remi@remirepo.net> - 5.1.1-1
- update to 5.1.1

* Fri Nov  1 2019 Remi Collet <remi@remirepo.net> - 5.1.0-1
- update to 5.1.0

* Mon Oct 21 2019 Remi Collet <remi@remirepo.net> - 5.1.0~RC2-1
- update to 5.1.0RC2
- drop patch merged upstream

* Wed Oct  9 2019 Remi Collet <remi@remirepo.net> - 5.1.0~RC1-1
- update to 5.1.0RC1
- enable ZSTD compression support
- open https://github.com/phpredis/phpredis/pull/1648

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 5.0.2-2
- rebuild for 7.4.0RC1

* Tue Jul 30 2019 Remi Collet <remi@remirepo.net> - 5.0.2-1
- update to 5.0.2

* Tue Jul 23 2019 Remi Collet <remi@remirepo.net> - 5.0.1-2
- rebuild for 7.4.0beta1

* Fri Jul 12 2019 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Tue Jul  2 2019 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0

* Wed Jun 26 2019 Remi Collet <remi@remirepo.net> - 5.0.0~RC2-1
- update to 5.0.0RC2

* Thu Jun 20 2019 Remi Collet <remi@remirepo.net> - 5.0.0~RC1-1
- update to 5.0.0RC1
- rename to php-pecl-redis5
- raise dependency on PHP 7
- enable msgpack support
- enable json support
- update configuration for new options
- open https://github.com/phpredis/phpredis/pull/1578
  fix extension dependencies and report about json serializer

* Wed May 29 2019 Remi Collet <remi@remirepo.net> - 4.3.0-3
- rebuild

* Wed May 22 2019 Remi Collet <remi@remirepo.net> - 4.3.0-2
- cleanup

* Thu Mar 14 2019 Remi Collet <remi@remirepo.net> - 4.3.0-1
- update to 4.3.0 (stable)

* Wed Mar  6 2019 Remi Collet <remi@remirepo.net> - 4.3.0~RC2-1
- update to 4.3.0RC2 (beta)

* Mon Feb 25 2019 Remi Collet <remi@remirepo.net> - 4.3.0~RC1-1
- update to 4.3.0RC1 (alpha)
  no change sincy 4.2.1RC1, only version change according to semver
  see https://github.com/phpredis/phpredis/issues/1517

* Mon Feb 25 2019 Remi Collet <remi@remirepo.net> - 4.2.1~RC1-1
- update to 4.2.1RC1 (alpha)
- update provided configuration with new runtime option

* Tue Dec 11 2018 Remi Collet <remi@remirepo.net> - 4.2.0-3
- test build for upstream patch

* Tue Dec  4 2018 Remi Collet <remi@remirepo.net> - 4.2.0-2
- open https://github.com/phpredis/phpredis/issues/1472
  tests failing with redis 5.0.2

* Sun Nov 18 2018 Remi Collet <remi@remirepo.net> - 4.2.0-1
- update to 4.2.0 (stable)

* Fri Nov  9 2018 Remi Collet <remi@remirepo.net> - 4.2.0~RC3-1
- update to 4.2.0RC3 (beta)

* Wed Nov  7 2018 Remi Collet <remi@remirepo.net> - 4.2.0~RC2-2
- test build for https://github.com/phpredis/phpredis/pull/1444

* Fri Oct 26 2018 Remi Collet <remi@remirepo.net> - 4.2.0~RC2-1
- update to 4.2.0RC2 (beta)
- open https://github.com/phpredis/phpredis/issues/1437 32-bit failed test

* Sun Oct 21 2018 Remi Collet <remi@remirepo.net> - 4.2.0~RC1-2
- test build with upstream patches

* Fri Oct 12 2018 Remi Collet <remi@remirepo.net> - 4.2.0~RC1-1
- update to 4.2.0RC1 (alpha)

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 4.1.1-2
- rebuild for 7.3.0beta2 new ABI

* Sun Aug  5 2018 Remi Collet <remi@remirepo.net> - 4.1.1-1
- update to 4.1.1

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 4.1.0-2
- rebuld for 7.3.0alpha4 new ABI

* Tue Jul 10 2018 Remi Collet <remi@remirepo.net> - 4.1.0-1
- update to 4.1.0 (stable)

* Fri Jun 22 2018 Remi Collet <remi@remirepo.net> - 4.1.0~RC3-1
- update to 4.1.0RC3 (beta, no change)
- drop patches merged upstream

* Fri Jun  8 2018 Remi Collet <remi@remirepo.net> - 4.1.0~RC1-2
- test build with 7.3
- open https://github.com/phpredis/phpredis/pull/1366
  Fix: Warning: time() expects exactly 0 parameters, 1 given ...

* Fri Jun  8 2018 Remi Collet <remi@remirepo.net> - 4.1.0~RC1-1
- update to 4.1.0RC1 (alpha)
- open https://github.com/phpredis/phpredis/pull/1365
  use PHP_BINARY instead of php and allow override
- report https://github.com/phpredis/phpredis/issues/1364
  missing files in pecl archive
- add new redis.session.lock* options in provided configuration

* Wed Apr 25 2018 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2

* Wed Apr 18 2018 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1

* Mon Mar 19 2018 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0 (stable)

* Sat Mar  3 2018 Remi Collet <remi@remirepo.net> - 4.0.0~RC2-1
- update to 4.0.0RC2

* Wed Feb  7 2018 Remi Collet <remi@remirepo.net> - 4.0.0~RC1-4
- re-enable s390x build (was a temporary failure)

* Wed Feb  7 2018 Remi Collet <remi@remirepo.net> - 4.0.0~RC1-3
- add patch to skip online test from
  https://github.com/phpredis/phpredis/pull/1304
- exclude s390x arch reported as
  https://github.com/phpredis/phpredis/issues/1305

* Wed Feb  7 2018 Remi Collet <remi@remirepo.net> - 4.0.0~RC1-1
- update to 4.0.0RC1
- rename to php-pecl-redis4
- enable lzf support
- update configuration for new options

* Wed Jan  3 2018 Remi Collet <remi@remirepo.net> - 3.1.6-1
- Update to 3.1.6

* Thu Dec 21 2017 Remi Collet <remi@remirepo.net> - 3.1.5-1
- update to 3.1.5 (stable)

* Mon Dec 11 2017 Remi Collet <remi@remirepo.net> - 3.1.5~RC2-1
- update to 3.1.5RC2 (beta)

* Fri Dec  1 2017 Remi Collet <remi@remirepo.net> - 3.1.5~RC1-1
- update to 3.1.5RC1 (beta)

* Sun Nov  5 2017 Remi Collet <remi@remirepo.net> - 3.1.4-3
- add upstream patch, fix segfault with PHP 5.x

* Tue Oct 17 2017 Remi Collet <remi@remirepo.net> - 3.1.4-2
- rebuild

* Wed Sep 27 2017 Remi Collet <remi@remirepo.net> - 3.1.4-1
- update to 3.1.4 (stable)

* Wed Sep 13 2017 Remi Collet <remi@remirepo.net> - 3.1.4~RC3-1
- update to 3.1.4RC3 (beta)

* Wed Sep 13 2017 Remi Collet <remi@remirepo.net> - 3.1.4~RC2-1
- update to 3.1.4RC2 (beta)
- open https://github.com/phpredis/phpredis/issues/1236
  unwanted noise (warning) not even using the extension

* Mon Sep  4 2017 Remi Collet <remi@remirepo.net> - 3.1.4~RC1-1
- update to 3.1.4RC1 (beta)

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 3.1.3-2
- rebuild for PHP 7.2.0beta1 new API

* Mon Jul 17 2017 Remi Collet <remi@remirepo.net> - 3.1.3-1
- update to 3.1.3 (stable)

* Tue Jun 27 2017 Remi Collet <remi@remirepo.net> - 3.1.3~RC2-1
- update to 3.1.3RC2 (beta)

* Wed Jun 21 2017 Remi Collet <remi@remirepo.net> - 3.1.3~RC1-2
- rebuild for 7.2.0alpha2

* Thu Jun  1 2017 Remi Collet <remi@remirepo.net> - 3.1.3~RC1-1
- update to 3.1.3RC1 (beta)

* Sat Mar 25 2017 Remi Collet <remi@remirepo.net> - 3.1.2-1
- Update to 3.1.2 (stable)

* Wed Feb  1 2017 Remi Collet <remi@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1 (stable)

* Tue Jan 17 2017 Remi Collet <remi@fedoraproject.org> - 3.1.1-0.2.RC2
- Update to 3.1.1RC2

* Thu Dec 22 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-0.1.RC1
- test build for open upcoming 3.1.1RC1

* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-0
- test build for open upcoming 3.1.1

* Thu Dec 15 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-2
- test build for open upcoming 3.1.1
- open https://github.com/phpredis/phpredis/issues/1060 broken impl
  with https://github.com/phpredis/phpredis/pull/1064
- reed https://github.com/phpredis/phpredis/issues/1062 session php 7.1
  with https://github.com/phpredis/phpredis/pull/1063

* Thu Dec 15 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- update to 3.1.0
- open https://github.com/phpredis/phpredis/issues/1052 max version
- open https://github.com/phpredis/phpredis/issues/1053 segfault
- open https://github.com/phpredis/phpredis/issues/1054 warnings
- open https://github.com/phpredis/phpredis/issues/1055 reflection
- open https://github.com/phpredis/phpredis/issues/1056 32bits tests

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-3
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-2
- rebuild for PHP 7.1 new API version

* Sat Jun 11 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0 (stable)

* Thu Jun  9 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.1.20160603git6447940
- refresh and bump version

* Thu May  5 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.6.20160504gitad3c116
- refresh

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.5.20160215git2887ad1
- enable igbinary support

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.4.20160215git2887ad1
- refresh

* Thu Feb 11 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.3.20160208git0d4b421
- refresh

* Tue Jan 26 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.2.20160125git7b36957
- refresh

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.2.20160106git4a37e47
- improve package.xml, set stability=devel

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 2.2.8-0.1.20160106git4a37e47
- update to 2.2.8-dev for PHP 7
- use git snapshot

* Sat Jun 20 2015 Remi Collet <remi@fedoraproject.org> - 2.2.7-2
- allow build against rh-php56 (as more-php56)

* Tue Mar 03 2015 Remi Collet <remi@fedoraproject.org> - 2.2.7-1
- Update to 2.2.7 (stable)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.2.5-5.1
- Fedora 21 SCL mass rebuild

* Fri Oct  3 2014 Remi Collet <rcollet@redhat.com> - 2.2.5-5
- fix segfault with igbinary serializer
  https://github.com/nicolasff/phpredis/issues/341

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 2.2.5-4
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 2.2.5-3
- add numerical prefix to extension configuration file (php 5.6)
- add comment about session configuration

* Thu Mar 20 2014 Remi Collet <rcollet@redhat.com> - 2.2.5-2
- fix memory corruption with PHP 5.6
  https://github.com/nicolasff/phpredis/pull/447

* Wed Mar 19 2014 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- Update to 2.2.5

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 2.2.4-3
- allow SCL build

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> - 2.2.4-2
- cleaups
- move doc in pecl_docdir

* Mon Sep 09 2013 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- Update to 2.2.4

* Tue Apr 30 2013 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- update to 2.2.3
- upstream moved to pecl, rename from php-redis to php-pecl-redis

* Tue Sep 11 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-5.git6f7087f
- more docs and improved description

* Sun Sep  2 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-4.git6f7087f
- latest snahot (without bundled igbinary)
- remove chmod (done upstream)

* Sat Sep  1 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-3.git5df5153
- run only test suite with redis > 2.4

* Fri Aug 31 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-2.git5df5153
- latest master
- run test suite

* Wed Aug 29 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2
- enable ZTS build

* Tue Aug 28 2012 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- initial package
