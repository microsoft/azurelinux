Summary:        Database servers made by the original developers of MySQL.
Name:           mariadb
Version:        10.11.6
Release:        1%{?dist}
License:        GPLv2 WITH exceptions AND LGPLv2 AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Databases

# A buildable mariadb environment needs functioning submodules that do not work from the archive download
# To generate run CBL-Mariner/SPECS/mariadb/generate_source_tarball.sh script
URL:            https://mariadb.org/
Source0:        https://github.com/MariaDB/server/archive/mariadb-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  fmt-devel
BuildRequires:  krb5-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  pcre2-devel
BuildRequires:  pkgconf
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
Requires:       %{name}-connector-c
Conflicts:      mysql
%if %{with_check}
BuildRequires:  perl(Test::More)
%endif

%description
MariaDB Server is one of the most popular database servers in the world. It’s made by the original developers of MySQL and guaranteed to stay open source. Notable users include Wikipedia, WordPress.com and Google.

MariaDB turns data into structured information in a wide array of applications, ranging from banking to websites. It is an enhanced, drop-in replacement for MySQL. MariaDB is used because it is fast, scalable and robust, with a rich ecosystem of storage engines, plugins and many other tools make it very versatile for a wide variety of use cases.

%package          server
Summary:        MariaDB server
Requires:       %{name}-errmsg = %{version}-%{release}
Requires:       mariadb-connector-c-config
Requires(postun): shadow-utils
Requires(pre):  shadow-utils

%description      server
The MariaDB server and related files

%package          server-galera
Summary:        MariaDB Galera Cluster is a synchronous multi-master cluster for MariaDB
Group:          Applications/Databases
Requires:       %{name}-server = %{version}-%{release}

%description      server-galera
MariaDB Galera Cluster is a synchronous multi-master cluster for MariaDB. It is available on Linux only, and only supports the XtraDB/InnoDB storage engines (although there is experimental support for MyISAM - see the wsrep_replicate_myisam system variable).

%package          devel
Summary:        Development headers for mariadb
Requires:       %{name} = %{version}-%{release}
Requires:       mariadb-connector-c-devel

%description devel
Development headers for developing applications linking to maridb

%package          errmsg
Summary:        errmsg for mariadb

%description      errmsg
errmsg for maridb

%prep
%autosetup -p1
# Remove PerconaFT from here because of AGPL licence
rm -rf storage/tokudb/PerconaFT
# Disable "embedded" directory which only contains "test-connect" test
sed -i '/ADD_SUBDIRECTORY(unittest\/embedded)/d' ./CMakeLists.txt

%build
# Disable symbol generation
export CFLAGS="`echo " %{build_cflags} " | sed 's/ -g//'`"
export CXXFLAGS="`echo " %{build_cxxflags} " | sed 's/ -g//'`"

mkdir build && cd build

cmake -DCMAKE_BUILD_TYPE=Release                        \
      -DCMAKE_INSTALL_PREFIX=%{_prefix}                       \
      -DINSTALL_DOCDIR=share/doc/mariadb-%{version}         \
      -DINSTALL_DOCREADMEDIR=share/doc/mariadb-%{version}   \
      -DINSTALL_MANDIR=share/man                        \
      -DINSTALL_MYSQLSHAREDIR="share/mysql"           \
      -DINSTALL_SYSCONFDIR="%{_sysconfdir}"             \
      -DINSTALL_SYSCONF2DIR="%{_sysconfdir}/my.cnf.d"   \
      -DINSTALL_MYSQLTESTDIR=share/mysql/test           \
      -DINSTALL_PLUGINDIR=lib/mysql/plugin              \
      -DINSTALL_SBINDIR=sbin                            \
      -DINSTALL_SCRIPTDIR=bin                           \
      -DINSTALL_SQLBENCHDIR=share/mysql/bench           \
      -DINSTALL_SUPPORTFILESDIR=share                   \
      -DMYSQL_DATADIR="%{_sharedstatedir}/mysql"               \
      -DMYSQL_UNIX_ADDR="%{_sharedstatedir}/mysql/mysqld.sock" \
      -DWITH_EXTRA_CHARSETS=complex                     \
      -DWITH_EMBEDDED_SERVER=ON                         \
      -DWITH_PCRE=system                                \
      -DWITH_SSL=system                                 \
      -DWITH_ZLIB=system                                \
      -DWITH_LIBFMT=system                              \
      -DSKIP_TESTS=ON                                   \
      -DTOKUDB_OK=0                                     \
      -DUPDATE_SUBMODULES=OFF                           \
      ..

make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/%{_libdir}/systemd/system

# Remove files that overlap with mariadb-connector-c packages
rm %{buildroot}%{_bindir}/{mariadb_config,mariadb-config,mysql_config}
rm %{buildroot}%{_sysconfdir}/my.cnf
rm %{buildroot}%{_sysconfdir}/my.cnf.d/client.cnf
rm %{buildroot}%{_libdir}/libmariadb.so.*
rm %{buildroot}%{_libdir}/libmysqlclient.so
rm %{buildroot}%{_libdir}/libmysqlclient_r.so
rm %{buildroot}%{_libdir}/libmariadb.so
rm %{buildroot}%{_libdir}/mysql/plugin/{auth_gssapi_client.so,caching_sha2_password.so,client_ed25519.so,dialog.so,mysql_clear_password.so,sha256_password.so}
rm %{buildroot}%{_libdir}/pkgconfig/libmariadb.pc
rm %{buildroot}%{_includedir}/mysql/{errmsg.h,ma_list.h,ma_pvio.h,ma_tls.h,mysql_version.h,mysqld_error.h,mariadb_com.h,mariadb_ctype.h,mariadb_dyncol.h,mariadb_rpl.h,mariadb_stmt.h,mariadb_version.h,mysql.h}
rm %{buildroot}%{_includedir}/mysql/mariadb/ma_io.h
rm %{buildroot}%{_includedir}/mysql/mysql/{client_plugin.h,plugin_auth.h,plugin_auth_common.h}

mv  %{buildroot}%{_datadir}/systemd/mariadb.service %{buildroot}/%{_libdir}/systemd/system/mariadb.service
mv  %{buildroot}%{_datadir}/systemd/mariadb@.service %{buildroot}/%{_libdir}/systemd/system/mariadb@.service
mv  %{buildroot}%{_datadir}/systemd/mariadb-extra@.socket %{buildroot}/%{_libdir}/systemd/system/mariadb-extra@.socket
mv  %{buildroot}%{_datadir}/systemd/mariadb@.socket %{buildroot}/%{_libdir}/systemd/system/mariadb@.socket
mv  %{buildroot}%{_datadir}/systemd/mysql.service %{buildroot}/%{_libdir}/systemd/system/mysql.service
mv  %{buildroot}%{_datadir}/systemd/mysqld.service %{buildroot}/%{_libdir}/systemd/system/mysqld.service
rm %{buildroot}/%{_sbindir}/rcmysql
rm %{buildroot}/%{_libdir}/*.a
mkdir -p %{buildroot}/%{_sharedstatedir}/mysql
install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable mariadb.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-mariadb.preset

%check
cd build
make test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%pre server
if [ $1 -eq 1 ] ; then
    getent group  mysql  >/dev/null || groupadd -r mysql
    getent passwd mysql  >/dev/null || useradd  -c "mysql" -s /bin/false -g mysql -M -r mysql
fi

%post server
/sbin/ldconfig
chown  mysql:mysql %{_sharedstatedir}/mysql || :
mysql_install_db --datadir="%{_sharedstatedir}/mysql" --user="mysql" --basedir="%{_prefix}" >/dev/null || :
%systemd_post  mariadb.service

%postun server
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    if getent passwd mysql >/dev/null; then
        userdel mysql
    fi
    if getent group mysql >/dev/null; then
        groupdel mysql
    fi
fi
%systemd_postun_with_restart mariadb.service

%preun server
%systemd_preun mariadb.service

%files
%defattr(-,root,root)
%{_libdir}/libmariadbd.so.*
%{_bindir}/aria_s3_copy
%{_bindir}/mariadb
%{_bindir}/mariadb-access
%{_bindir}/mariadb-admin
%{_bindir}/mariadb-backup
%{_bindir}/mariadb-binlog
%{_bindir}/mariadb-check
%{_bindir}/mariadb-client-test
%{_bindir}/mariadb-client-test-embedded
%{_bindir}/mariadb-conv
%{_bindir}/mariadb-convert-table-format
%{_bindir}/mariadb-dump
%{_bindir}/mariadb-dumpslow
%{_bindir}/mariadb-embedded
%{_bindir}/mariadb-find-rows
%{_bindir}/mariadb-fix-extensions
%{_bindir}/mariadb-hotcopy
%{_bindir}/mariadb-import
%{_bindir}/mariadb-install-db
%{_bindir}/mariadb-ldb
%{_bindir}/mariadb-plugin
%{_bindir}/mariadb-secure-installation
%{_bindir}/mariadb-setpermission
%{_bindir}/mariadb-show
%{_bindir}/mariadb-slap
%{_bindir}/mariadb-test
%{_bindir}/mariadb-test-embedded
%{_bindir}/mariadb-tzinfo-to-sql
%{_bindir}/mariadb-upgrade
%{_bindir}/mariadb-waitpid
%{_bindir}/mariadbd-multi
%{_bindir}/mariadbd-safe
%{_bindir}/mariadbd-safe-helper
%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_plugin
%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/mysql_client_test
%{_bindir}/mysql_client_test_embedded
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_embedded
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_ldb
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_upgrade
%{_bindir}/mysqltest
%{_bindir}/mysqltest_embedded
%{_bindir}/mytop
%{_bindir}/perror
%{_bindir}/sst_dump
%{_bindir}/myrocks_hotbackup
%{_mandir}/man1/msql2mysql.1.gz
%{_mandir}/man1/mysql.1.gz
%{_mandir}/man1/mysqlaccess.1.gz
%{_mandir}/man1/mysqladmin.1.gz
%{_mandir}/man1/mysqlbinlog.1.gz
%{_mandir}/man1/mysqlcheck.1.gz
%{_mandir}/man1/mysql_client_test.1.gz
%{_mandir}/man1/mysql_client_test_embedded.1.gz
%{_mandir}/man1/mysql_config.1.gz
%{_mandir}/man1/mysql_convert_table_format.1.gz
%{_mandir}/man1/mysqldump.1.gz
%{_mandir}/man1/mysqldumpslow.1.gz
%{_mandir}/man1/mysql_find_rows.1.gz
%{_mandir}/man1/mysql_fix_extensions.1.gz
%{_mandir}/man1/mysql_plugin.1.gz
%{_mandir}/man1/mysql_secure_installation.1.gz
%{_mandir}/man1/mysql_setpermission.1.gz
%{_mandir}/man1/mysqlshow.1.gz
%{_mandir}/man1/mysqlslap.1.gz
%{_mandir}/man1/mysql-stress-test.pl.1.gz
%{_mandir}/man1/mysqltest.1.gz
%{_mandir}/man1/mysqltest_embedded.1.gz
%{_mandir}/man1/mysql-test-run.pl.1.gz
%{_mandir}/man1/mysql_tzinfo_to_sql.1.gz
%{_mandir}/man1/mysql_upgrade.1.gz
%{_mandir}/man1/mysql_waitpid.1.gz
%{_mandir}/man1/perror.1.gz
%{_datadir}/mysql/charsets/*
%{_datadir}/magic
%{_datadir}/pam_user_map.so
%{_datadir}/user_map.conf
%config(noreplace) /etc/my.cnf.d/s3.cnf
%config(noreplace) /etc/my.cnf.d/spider.cnf
%license COPYING
%doc CREDITS

%exclude %{_datadir}/mysql/bench
%exclude %{_datadir}/mysql/test
%exclude %{_docdir}/mariadb-%{version}/*

%files server
%config(noreplace) %{_sysconfdir}/logrotate.d/mariadb
%config(noreplace) %{_sysconfdir}/my.cnf.d/enable_encryption.preset
%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/server.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/hashicorp_key_management.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/provider_bzip2.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/provider_lzma.cnf
%dir %attr(0750,mysql,mysql) %{_sharedstatedir}/mysql
%{_libdir}/mysql/plugin*
%{_bindir}/aria_chk
%{_bindir}/aria_dump_log
%{_bindir}/aria_ftdump
%{_bindir}/aria_pack
%{_bindir}/aria_read_log
%{_bindir}/innochecksum
%{_bindir}/mariabackup
%{_bindir}/mariadb-service-convert
%{_bindir}/mbstream
%{_bindir}/myisam_ftdump
%{_bindir}/myisamchk
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_install_db
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysqld_safe
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe_helper
%{_bindir}/mysqldumpslow
%{_bindir}/mysqlhotcopy
%{_bindir}/my_print_defaults
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip
%{_bindir}/wsrep_sst_backup
%{_bindir}/wsrep_sst_common
%{_bindir}/wsrep_sst_mariabackup
%{_bindir}/wsrep_sst_mysqldump
%{_bindir}/wsrep_sst_rsync
%{_bindir}/wsrep_sst_rsync_wan
%{_sbindir}/*
%{_unitdir}/*.service
%{_unitdir}/*.socket
%{_libdir}/systemd/system-preset/50-mariadb.preset
%{_datadir}/binary-configure
%{_datadir}/mariadb.logrotate
%{_datadir}/mini-benchmark
%{_datadir}/mysql.server
%{_datadir}/mysqld_multi.server
%{_datadir}/policy/apparmor/README
%{_datadir}/policy/apparmor/usr.sbin.mysqld
%{_datadir}/policy/apparmor/usr.sbin.mysqld.local
%{_datadir}/policy/selinux/README
%{_datadir}/policy/selinux/mariadb-server.fc
%{_datadir}/policy/selinux/mariadb-server.te
%{_datadir}/policy/selinux/mariadb.te
%{_datadir}/wsrep.cnf
%{_datadir}/wsrep_notify
%{_mandir}/man1/aria_chk.1.gz
%{_mandir}/man1/aria_dump_log.1.gz
%{_mandir}/man1/aria_ftdump.1.gz
%{_mandir}/man1/aria_pack.1.gz
%{_mandir}/man1/aria_read_log.1.gz
%{_mandir}/man1/aria_s3_copy.1.gz
%{_mandir}/man1/innochecksum.1.gz
%{_mandir}/man1/mariadb-service-convert.1.gz
%{_mandir}/man1/myisamchk.1.gz
%{_mandir}/man1/myisam_ftdump.1.gz
%{_mandir}/man1/myisamlog.1.gz
%{_mandir}/man1/myisampack.1.gz
%{_mandir}/man1/my_print_defaults.1.gz
%{_mandir}/man1/my_safe_process.1.gz
%{_mandir}/man1/mysqld_multi.1.gz
%{_mandir}/man1/mysqld_safe.1.gz
%{_mandir}/man1/mysqld_safe_helper.1.gz
%{_mandir}/man1/mysqlhotcopy.1.gz
%{_mandir}/man1/mysqlimport.1.gz
%{_mandir}/man1/mysql_install_db.1.gz
%{_mandir}/man1/mysql.server.1.gz
%{_mandir}/man1/replace.1.gz
%{_mandir}/man1/resolveip.1.gz
%{_mandir}/man1/resolve_stack_dump.1.gz
%{_mandir}/man1/wsrep_sst_common.1.gz
%{_mandir}/man1/wsrep_sst_mysqldump.1.gz
%{_mandir}/man1/wsrep_sst_rsync.1.gz
%{_mandir}/man1/mariabackup.1.gz
%{_mandir}/man1/mbstream.1.gz
%{_mandir}/man1/mysql_embedded.1.gz
%{_mandir}/man1/mysql_ldb.1.gz
%{_mandir}/man1/wsrep_sst_mariabackup.1.gz
%{_mandir}/man1/wsrep_sst_rsync_wan.1.gz
%{_mandir}/man1/mariadb-access.1.gz
%{_mandir}/man1/mariadb-admin.1.gz
%{_mandir}/man1/mariadb-backup.1.gz
%{_mandir}/man1/mariadb-binlog.1.gz
%{_mandir}/man1/mariadb-check.1.gz
%{_mandir}/man1/mariadb-client-test-embedded.1.gz
%{_mandir}/man1/mariadb-client-test.1.gz
%{_mandir}/man1/mariadb-conv.1.gz
%{_mandir}/man1/mariadb-convert-table-format.1.gz
%{_mandir}/man1/mariadb-dump.1.gz
%{_mandir}/man1/mariadb-dumpslow.1.gz
%{_mandir}/man1/mariadb-embedded.1.gz
%{_mandir}/man1/mariadb-find-rows.1.gz
%{_mandir}/man1/mariadb-fix-extensions.1.gz
%{_mandir}/man1/mariadb-hotcopy.1.gz
%{_mandir}/man1/mariadb-import.1.gz
%{_mandir}/man1/mariadb-install-db.1.gz
%{_mandir}/man1/mariadb-ldb.1.gz
%{_mandir}/man1/mariadb-plugin.1.gz
%{_mandir}/man1/mariadb-secure-installation.1.gz
%{_mandir}/man1/mariadb-setpermission.1.gz
%{_mandir}/man1/mariadb-show.1.gz
%{_mandir}/man1/mariadb-slap.1.gz
%{_mandir}/man1/mariadb-test-embedded.1.gz
%{_mandir}/man1/mariadb-test.1.gz
%{_mandir}/man1/mariadb-tzinfo-to-sql.1.gz
%{_mandir}/man1/mariadb-upgrade.1.gz
%{_mandir}/man1/mariadb-waitpid.1.gz
%{_mandir}/man1/mariadb.1.gz
%{_mandir}/man1/mariadb_config.1.gz
%{_mandir}/man1/mariadbd-multi.1.gz
%{_mandir}/man1/mariadbd-safe-helper.1.gz
%{_mandir}/man1/mariadbd-safe.1.gz
%{_mandir}/man1/myrocks_hotbackup.1.gz
%{_mandir}/man1/mytop.1.gz
%{_mandir}/man8/*
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/maria_add_gis_sp.sql
%{_datadir}/mysql/maria_add_gis_sp_bootstrap.sql
%{_datadir}/mysql/mroonga/install.sql
%{_datadir}/mysql/mroonga/uninstall.sql
%{_datadir}/mysql/mysql_performance_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/mysql_test_db.sql
%{_datadir}/mysql/mysql_sys_schema.sql
%license %{_datadir}/mysql/mroonga/AUTHORS
%license %{_datadir}/mysql/mroonga/COPYING
%license %{_datadir}/groonga-normalizer-mysql/lgpl-2.0.txt
%license %{_datadir}/groonga/COPYING
%doc %{_datadir}/groonga-normalizer-mysql/README.md
%doc %{_datadir}/groonga/README.md

%files server-galera
%{_bindir}/galera_new_cluster
%{_bindir}/galera_recovery
%{_datadir}/systemd/use_galera_new_cluster.conf
%{_mandir}/man1/galera_new_cluster.1.gz
%{_mandir}/man1/galera_recovery.1.gz

%files devel
%{_includedir}/mysql/*
%{_datadir}/aclocal/mysql.m4
%{_libdir}/libmariadbd.so
%{_libdir}/libmysqld.so
%{_libdir}/pkgconfig/mariadb.pc
%{_mandir}/man3/*.3.gz

%files errmsg
%{_datadir}/mysql/bulgarian/errmsg.sys
%{_datadir}/mysql/chinese/errmsg.sys
%{_datadir}/mysql/czech/errmsg.sys
%{_datadir}/mysql/danish/errmsg.sys
%{_datadir}/mysql/dutch/errmsg.sys
%{_datadir}/mysql/english/errmsg.sys
%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/estonian/errmsg.sys
%{_datadir}/mysql/french/errmsg.sys
%{_datadir}/mysql/georgian/errmsg.sys
%{_datadir}/mysql/german/errmsg.sys
%{_datadir}/mysql/greek/errmsg.sys
%{_datadir}/mysql/hungarian/errmsg.sys
%{_datadir}/mysql/italian/errmsg.sys
%{_datadir}/mysql/japanese/errmsg.sys
%{_datadir}/mysql/korean/errmsg.sys
%{_datadir}/mysql/norwegian-ny/errmsg.sys
%{_datadir}/mysql/norwegian/errmsg.sys
%{_datadir}/mysql/polish/errmsg.sys
%{_datadir}/mysql/portuguese/errmsg.sys
%{_datadir}/mysql/romanian/errmsg.sys
%{_datadir}/mysql/russian/errmsg.sys
%{_datadir}/mysql/serbian/errmsg.sys
%{_datadir}/mysql/slovak/errmsg.sys
%{_datadir}/mysql/spanish/errmsg.sys
%{_datadir}/mysql/swedish/errmsg.sys
%{_datadir}/mysql/ukrainian/errmsg.sys
%{_datadir}/mysql/hindi/errmsg.sys

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 10.6.9-5
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Jul 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.6.9-4
- Explicitly using the system versions of PCRE2, openSSL, and zlib.

* Thu Feb 09 2023 Rachel Menge <rachelmenge@microsoft.com> - 10.6.9-3
- Add patch for CVE-2022-47015

* Wed Sep 07 2022 Andrew Phelps <anphel@microsoft.com> - 10.6.9-2
- Add shadow-utils pre/postun requirements

* Tue Aug 30 2022 Henry Beberman <henry.beberman@microsoft.com> - 10.6.9-1
- Upgrade to v10.6.9 to address CVE-2022-32091, CVE-2022-32081

* Fri May 20 2022 Chris Co <chrco@microsoft.com> - 10.6.8-1
- Upgrade to v10.6.8 to address CVE-2022-27448, CVE-2022-27449,
  CVE-2022-27451, CVE-2022-27457, CVE-2022-27458
- Add new files bulgarian errmsg.sys, chinese errmsg.sys, wsrep_sst_backup

* Fri Apr 29 2022 Olivia Crain <oliviacrain@microsoft.com> - 10.6.7-2
- Fix conflicts with mariadb-connector-c

* Tue Feb 15 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 10.6.7-1
- Upgrading to v10.6.7.
- Adding reference to new unpackaged man files.
- Adding comment and script to help with submodule tarball creation.
- Adding with_check perl(Test::More) BR for "dbug" ptest failure.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.3.28-3
- Removing the explicit %%clean stage.

* Fri Nov 19 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.3.28-2
- Adding a fix to work with newer version of cmake.

* Fri Apr 02 2021 Nicolas Ontiveros <niontive@microsoft.com> - 10.3.28-1
- Upgrade to version 10.3.28, which resolves CVE-2021-27928

*   Thu Jan 14 2021 Andrew Phelps <anphel@microsoft.com> 10.3.17-4
-   Disable failing "test-connect" test and binary "test-connect-t"

*   Fri Jun 12 2020 Henry Beberman <henry.beberman@microsoft.com> 10.3.17-3
-   Temporarily disable generation of debug symbols.

*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 10.3.17-2
-   Renaming Linux-PAM to pam

*   Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> 10.3.17-1
-   Update to version 10.3.17. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 10.3.11-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Jan 23 2019 Ajay Kaher <akaher@vmware.com> 10.3.11-2
-   Remove PerconaFT from mariadb pkg because of AGPL licence

*   Wed Jan 02 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 10.3.11-1
-   Upgrade to version 10.3.11

*   Mon Nov 19 2018 Ajay Kaher <akaher@vmware.com> 10.3.9-3
-   Enabling for aarch64

*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 10.3.9-2
-   Adding BuildArch

*   Thu Sep 06 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 10.3.9-1
-   Update to version 10.3.9

*   Tue Nov 07 2017 Xiaolin Li <xiaolinl@vmware.com> 10.2.10-1
-   Update to verion 10.2.10 to address CVE-2017-10378, CVE-2017-10268

*   Wed Sep 06 2017 Xiaolin Li <xiaolinl@vmware.com> 10.2.8-1
-   Update to 10.2.8 and enable build server.

*   Thu Aug 31 2017 Xiaolin Li <xiaolinl@vmware.com> 10.1.24-3
-   Fixed make check issue.

*   Fri Aug 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 10.1.24-2
-   Specify MariaDB conflicts with MySQL

*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 10.1.24-1
-   Initial packaging for Photon
