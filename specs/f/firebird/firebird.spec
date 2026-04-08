# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         upversion 4.0.6.3221
%global         pkgversion Firebird-%{upversion}-0

%global         major 4.0
%global         _hardened_build 1
# firebird is mis-compiled when LTO is enabled. A root
# cause analysis has not yet been completed. Reported upstream.
# Disable LTO for now
%global         _lto_cflags %nil

Name:           firebird
Version:        %{upversion}
Release:        1%{?dist}

Summary:        SQL relational database management system
# Automatically converted from old format: Interbase - review is highly recommended.
License:        Interbase-1.0
URL:            http://www.firebirdsql.org/

Source0:        https://github.com/FirebirdSQL/firebird/releases/download/v4.0.6/%{pkgversion}.tar.xz
Source1:        firebird-logrotate
Source2:        README.Fedora
Source3:        firebird.service
Source4:        fb_config

# from OpenSuse
Patch101:       add-pkgconfig-files.patch

# from Debian to be sent upstream
Patch203:       no-copy-from-icu.patch
Patch205:       cloop-honour-build-flags.patch

# from upstream
Patch301:       c++17.patch
Patch302:       noexcept.patch
Patch401:       btyacc-honour-build-flags.patch

# not yet upstream
Patch501:       examples-honour-build-flags.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtommath-devel
BuildRequires: libtool
BuildRequires: ncurses-devel
BuildRequires: libicu-devel
BuildRequires: libedit-devel
BuildRequires: gcc-c++
BuildRequires: libstdc++-static
BuildRequires: systemd-rpm-macros
BuildRequires: chrpath
BuildRequires: zlib-devel
BuildRequires: procmail
BuildRequires: make
BuildRequires: libtomcrypt-devel
BuildRequires: unzip
BuildRequires: sed

Requires(postun): /usr/sbin/userdel
Requires(postun): /usr/sbin/groupdel
Recommends:     logrotate
Requires:       libfbclient2 = %{version}-%{release}
Requires:       libib-util = %{version}-%{release}
Requires:       %{name}-utils = %{version}-%{release}

Obsoletes:      firebird-arch < 4.0
Obsoletes:      firebird-filesystem < 4.0
Obsoletes:      firebird-classic-common < 4.0
Obsoletes:      firebird-classic < 4.0
Obsoletes:      firebird-superclassic < 4.0
Obsoletes:      firebird-superserver < 4.0
Conflicts:      firebird-arch < 4.0
Conflicts:      firebird-filesystem < 4.0
Conflicts:      firebird-classic-common < 4.0
Conflicts:      firebird-classic < 4.0
Conflicts:      firebird-superclassic < 4.0
Conflicts:      firebird-superserver < 4.0


%description
Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.


%package devel
Requires:       %{name} = %{version}-%{release}
Requires:       libfbclient2-devel = %{version}-%{release}
Summary:        UDF support library for Firebird SQL server

%description devel
This package is needed for development of client applications and user
defined functions (UDF) for Firebird SQL server.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.


%package -n libib-util
Summary:        Firebird SQL UDF support library

%description -n libib-util
libib_util contains utility functions used by
User-Defined Functions (UDF) for memory management etc.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.


%package -n libfbclient2
Summary:        Firebird SQL server client library
Obsoletes:      firebird-libfbclient < 4.0
Conflicts:      firebird-libfbclient < 4.0
Obsoletes:      firebird-libfbembed < 4.0

%description -n libfbclient2
Shared client library for Firebird SQL server.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.


%package -n libfbclient2-devel
Summary:        Development libraries and headers for Firebird SQL server
Requires:       %{name}-devel = %{version}-%{release}
Requires:       libfbclient2 = %{version}-%{release}
Requires:       pkgconfig

%description -n libfbclient2-devel
Development files for Firebird SQL server client library.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.


%package doc
Requires:       %{name} = %{version}-%{release}
Summary:        Documentation for Firebird SQL server
BuildArch:      noarch

%description doc
Documentation for Firebird SQL server.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.


%package utils
Requires:       libfbclient2 = %{version}-%{release}
Summary:        Firebird SQL user utilities

%description utils
Firebird SQL user utilities.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.


%package examples
Requires:       %{name}-doc = %{version}-%{release}
Summary:        Examples for Firebird SQL server
BuildArch:      noarch

%description examples
Examples for Firebird SQL server.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.


%prep
%setup -q -n %{pkgversion}
%patch -P101 -p1
%patch -P203 -p1
%patch -P205 -p1
%patch -P301 -p1
%patch -P302 -p1
%patch -P401 -p1
%patch -P501 -p1

# Create a sysusers.d config file
cat >firebird.sysusers.conf <<EOF
u firebird - - - -
EOF


%build
%ifarch s390x
%global _lto_cflags %{nil}
%endif
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="${CFLAGS} -fno-delete-null-pointer-checks"
NOCONFIGURE=1 ./autogen.sh
%configure --disable-rpath --prefix=%{_prefix} \
  --with-system-editline \
  --with-fbbin=%{_bindir} --with-fbsbin=%{_sbindir} \
  --with-fbconf=%{_sysconfdir}/%{name} \
  --with-fblib=%{_libdir} --with-fbinclude=%{_includedir} \
  --with-fbdoc=%{_defaultdocdir}/%{name} \
  --with-fbsample=%{_defaultdocdir}/%{name}/sample \
  --with-fbsample-db=%{_localstatedir}/lib/%{name}/data \
  --with-fbhelp=%{_localstatedir}/lib/%{name}/system \
  --with-fbintl=%{_libdir}/%{name}/intl \
  --with-fbmisc=%{_datadir}/%{name}/misc \
  --with-fbsecure-db=%{_localstatedir}/lib/%{name}/secdb \
  --with-fbmsg=%{_localstatedir}/lib/%{name}/system \
  --with-fblog=%{_localstatedir}/log/%{name} \
  --with-fbglock=%{_rundir}/%{name} \
  --with-fbplugins=%{_libdir}/%{name}/plugins \
  --with-fbtzdata=%{_localstatedir}/lib/%{name}/tzdata 

make %{?_smp_mflags}
cd gen
sed -i '/linkFiles "/d' ./install/makeInstallImage.sh
./install/makeInstallImage.sh
chmod -R u+w buildroot%{_docdir}/%{name}

%install
chmod u+rw,a+rx gen/buildroot/%{_includedir}/firebird/impl
cp -r gen/buildroot/* ${RPM_BUILD_ROOT}/
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp -v gen/install/misc/*.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/
install -m0644 -D firebird.sysusers.conf %{buildroot}%{_sysusersdir}/firebird.conf

cd ${RPM_BUILD_ROOT}
rm -vf .%{_sbindir}/*.sh
mv -v .%{_sbindir}/fb_config .%{_libdir}/
install -p -m 0755 %{SOURCE4} %{buildroot}%{_sbindir}/fb_config
rm -vf .%{_includedir}/perf.h
rm -vf .%{_libdir}/libicu*.so
chmod -R u+w .%{_docdir}/%{name}
mv -v .%{_datadir}/%{name}/misc/upgrade/udf/* .%{_docdir}/%{name}/
rm -rvf .%{_datadir}/%{name}/misc
mv -v .%{_sysconfdir}/%{name}/README.md .%{_sysconfdir}/%{name}/CHANGELOG.md \
  .%{_docdir}/%{name}/
mv -v .%{_sysconfdir}/%{name}/IDPLicense.txt .%{_docdir}/%{name}/
mv -v .%{_sysconfdir}/%{name}/IPLicense.txt .%{_docdir}/%{name}/
install -p -m 0644 -D %{SOURCE2} .%{_docdir}/%{name}/README.Fedora
mv -v .%{_bindir}/gstat .%{_bindir}/gstat-fb
mv -v .%{_bindir}/isql .%{_bindir}/isql-fb
rm -rvf .%{_defaultdocdir}/%{name}/sample/prebuilt

mkdir -p .%{_localstatedir}/log/%{name}
mkdir -p .%{_sysconfdir}/logrotate.d
echo 1 > .%{_localstatedir}/log/%{name}/%{name}.log
sed "s@%{name}.log@%{_localstatedir}/log/%{name}/%{name}.log@g" %{SOURCE1} > .%{_sysconfdir}/logrotate.d/%{name}

mkdir -p .%{_unitdir}
cp -f %{SOURCE3} .%{_unitdir}/%{name}.service


%pre 
# Add gds_db to /etc/services if needed
FileName=/etc/services
newLine="gds_db 3050/tcp  # Firebird SQL Database Remote Protocol"
oldLine=`grep "^gds_db" $FileName`
if [ -z "$oldLine" ]; then
 echo $newLine >> $FileName
fi


%post 
%systemd_post firebird.service


%postun 
%systemd_postun_with_restart firebird.service


%preun 
%systemd_preun firebird.service


%files
%{_docdir}/%{name}/
%{_bindir}/fbtracemgr
%{_sbindir}/firebird
%{_sbindir}/fbguard
%{_sbindir}/fb_lock_print
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/databases.conf
%config(noreplace) %{_sysconfdir}/%{name}/fbtrace.conf
%config(noreplace) %{_sysconfdir}/%{name}/firebird.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins.conf
%config(noreplace) %{_sysconfdir}/%{name}/replication.conf
%dir %{_libdir}/%{name}
%dir %{_datadir}/%{name}
%{_libdir}/%{name}/intl
%{_libdir}/%{name}/plugins

%dir %{_localstatedir}/lib/%{name}
%dir %attr(0700,%{name},%{name}) %{_localstatedir}/lib/%{name}/secdb
%dir %attr(0700,%{name},%{name}) %{_localstatedir}/lib/%{name}/data
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/lib/%{name}/system
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/lib/%{name}/tzdata
%attr(0600,firebird,firebird) %config(noreplace) %{_localstatedir}/lib/%{name}/secdb/security4.fdb
%attr(0644,firebird,firebird) %{_localstatedir}/lib/%{name}/system/help.fdb
%attr(0644,firebird,firebird) %{_localstatedir}/lib/%{name}/system/firebird.msg
%attr(0644,firebird,firebird) %{_localstatedir}/lib/%{name}/tzdata/*.res
%ghost %dir %attr(0775,%{name},%{name}) /run/%{name}
%ghost %attr(0644,%{name},%{name}) /run/%{name}/fb_guard
%dir %{_localstatedir}/log/%{name}
%config(noreplace) %attr(0664,%{name},%{name})  %{_localstatedir}/log/%{name}/%{name}.log
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}

%attr(0644,root,root) %{_unitdir}/%{name}.service
%{_sysusersdir}/firebird.conf


%files devel
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/fb_config
%{_sbindir}/fb_config


%files -n libfbclient2
%{_libdir}/libfbclient.so.*


%files -n libfbclient2-devel
%{_libdir}/libfbclient.so
%{_libdir}/pkgconfig/fbclient.pc


%files -n libib-util
%{_libdir}/libib_util.so


%files doc
%{_docdir}/%{name}/
%exclude %{_docdir}/%{name}/sample
%exclude %{_docdir}/%{name}/IDPLicense.txt
%exclude %{_docdir}/%{name}/IPLicense.txt


%files utils
%{_bindir}/gstat-fb
%{_bindir}/fbsvcmgr
%{_bindir}/gbak
%{_bindir}/gfix
%{_bindir}/gpre
%{_bindir}/gsec
%{_bindir}/isql-fb
%{_bindir}/nbackup
%{_bindir}/qli
%{_bindir}/gsplit


%files examples
%{_docdir}/%{name}/sample
%attr(0600,firebird,firebird) %{_localstatedir}/lib/%{name}/data/employee.fdb


%changelog
* Thu Sep 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 4.0.6.3221-1
- 4.0.6.3221

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4.3010-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.0.4.3010-7
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4.3010-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 4.0.4.3010-5
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4.3010-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4.3010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4.3010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 09 2023 Philippe Makowski <makowski@fedoraproject.org> - 4.0.4.3010-0
- Update to 4.0.4 (#2247832)

* Tue Aug 08 2023 Philippe Makowski <makowski@fedoraproject.org> - 4.0.3.2975-0
- Update to 4.0.3 (#2228171)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2.2816-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2.2816-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec  1 2022 Florian Weimer <fweimer@redhat.com> - 4.0.2.2816-3
- Port configure script to C99

* Thu Nov 24 2022 Philippe Makowski <makowski@fedoraproject.org> - 4.0.2.2816-2
- Patch for autoconf 2.72 (#2144802)

* Fri Aug 12 2022 Philippe Makowski <makowski@fedoraproject.org> - 4.0.2.2816-1
- Update to 4.0.2 (#2033945)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0.2496-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 13 2022 Philippe Makowski <makowski@fedoraproject.org> - 4.0.0.2496-7
- Remove Standard output type syslog (#2035798)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0.2496-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Oct 10 2021 Kalev Lember <klember@redhat.com> - 4.0.0.2496-5
- Recommend logrotate rather than hard requiring

* Fri Oct 08 2021 Kalev Lember <klember@redhat.com> - 4.0.0.2496-4
- BuildRequire systemd-rpm-macros instead of systemd-units
- Remove requires on systemd-units as per updated guidelines

* Fri Aug 20 2021 Philippe Makowski <makowski@fedoraproject.org> - 4.0.0.2496-3
- Fix build on s390x (#1969393)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0.2496-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Philippe Makowski <makowski@fedoraproject.org> - 4.0.0.2496-1
- Update to 4.0.0 (#1963311)

* Mon May 10 2021 Jeff Law <law@tachyum.com> - 3.0.7.33374-5
- Re-enable LTO

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.7.33374-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7.33374-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 27 2020 Jeff Law <law@redhat.com> - 3.0.7.33374-2
- Force C++14 as this code is not C++17 ready

* Fri Oct 23 2020 Philippe Makowski <makowski@fedoraproject.org> - 3.0.7.33374-1
- new upstream release fix #1887991

* Mon Aug 10 2020 Jeff Law <law@fedoraproject.org> - 3.0.6.33328-4
- Disable LTO on s390x for now

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6.33328-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6.33328-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Philippe Makowski <makowski@fedoraproject.org> - 3.0.6.33328-1
- new upstream release fix #1850675

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5.33220-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Philippe Makowski <makowski@fedoraproject.org> - 3.0.5.33220-1
- new upstream release fix #1786885

* Mon Nov 4 2019 Philippe Makowski <makowski@fedoraproject.org> - 3.0.4.33054-5
- Change firebird-superserver.service file permissions, fix #1768091
- Set login shell to /sbin/nologin, fix #1764128
- Remove BR libtermcap-devel

* Wed Aug 21 2019 Philippe Makowski <makowski@fedoraproject.org> - 3.0.4.33054-4
- Remove tmpfile, fix #1687058

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4.33054-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4.33054-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 22 2018 Philippe Makowski <makowski@fedoraproject.org> - 3.0.4.33054-1
- new upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3.32900-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 18 2018 Richard W.M. Jones <rjones@redhat.com> - 3.0.3.32900-2
- Add support for riscv64.

* Tue Feb 20 2018 Philippe Makowski <makowski@fedoraproject.org> - 3.0.3.32900-1
- new upstream release.
- Drop obsolete ldconfig scriptlets.
- Fix tmpfiles path

* Tue Feb 13 2018 Remi Collet <remi@fedoraproject.org> - 3.0.2.32703-5
- add shebang in fb_config, fix #1544837

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2.32703-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2.32703-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2.32703-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 27 2017 Philippe Makowski <makowski@fedoraproject.org> - 3.0.2.32703-1
- new upstream release

* Tue Feb 21 2017 Philippe Makowski <makowski@fedoraproject.org> - 3.0.1.32609-5
- security fix (#1425333)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1.32609-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 15 2016 Philippe Makowski <makowski@fedoraproject.org> - 3.0.1.32609-3
- add requires on libfbclient2-devel for firebird-devel #1394750

* Mon Oct 31 2016 Philippe Makowski <makowski@fedoraproject.org> - 3.0.1.32609-2
- obsolete firebird-libfbembed #1388648
 
* Wed Oct 12 2016 Philippe Makowski <makowski@fedoraproject.org> - 3.0.1.32609-1
- new upstream release

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 2.5.5.26952.0-7
- rebuild for ICU 57.1

* Wed Mar 30 2016 Philippe Makowski <makowski@fedoraproject.org> - 2.5.5.26952.0-6
- use _tmpfilesdir macro

* Wed Mar 09 2016 Philippe Makowski <makowski@fedoraproject.org> - 2.5.5.26952.0-5
- Resolves: rbhz#1307503 building with gcc6

* Sat Feb 20 2016 David Tardon <dtardon@redhat.com> - 2.5.5.26952.0-4
- Resolves: rbhz#1309223 restore /usr/sbin/fb_config

* Fri Feb 05 2016 Philippe Makowski <makowski@fedoraproject.org> - 2.5.5.26952.0-3
- move fb_config (#1297506)
- fixe CVE-2016-1569 (#1297447 #1297450 #1297451) 

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5.26952.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 19 2015 Philippe Makowski <makowski@fedoraproject.org> 2.5.5.26952.0-1
- update to 2.5.5

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 2.5.4.26856.0-4
- rebuild for ICU 56.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4.26856.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.5.4.26856.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Thu Apr 2 2015 Philippe Makowski <makowski@fedoraproject.org> 2.5.4.26856.0-1
- update to 2.5.4 

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 2.5.3.26778.0-6
- rebuild for ICU 54.1

* Sun Dec 7 2014 Philippe Makowski <makowski@fedoraproject.org> 2.5.3.26778.0-5
- security fix firebird CORE-4630

* Thu Oct 30 2014 Philippe Makowski <makowski@fedoraproject.org>  2.5.3.26778.0-4
- Remove lib64 rpaths (#1154706)

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 2.5.3.26778.0-3
- rebuild for ICU 53.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3.26778.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 26 2014 Philippe Makowski <makowski@fedoraproject.org>  - 2.5.3.26778.0-1
- update from upstream 2.5.3
- update arm64 patch

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2.26539.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 2.5.2.26539.0-10
- rebuild (libicu)

* Sat Dec 07 2013 Philippe Makowski <makowski@fedoraproject.org>  2.5.2.26539.0-9
- fix FTBFS if "-Werror=format-security" flag is used   (bug #1037062)

* Thu Aug 08 2013 Philippe Makowski <makowski@fedoraproject.org>  2.5.2.26539.0-8
- add BR libatomic_ops-static  (bug #993439)

* Tue Jul 23 2013 Philippe Makowski <makowski@fedoraproject.org>  2.5.2.26539.0-7
- make fb_config executable  (bug #985335)

* Tue Jul 23 2013 Philippe Makowski <makowski@fedoraproject.org>  2.5.2.26539.0-6
- Provide fb_config in firebird-devel  (bug #985335)

* Mon Jun 03 2013 Philippe Makowski <makowski@fedoraproject.org>  2.5.2.26539.0-5
- Firebird fails to build for aarch64  (bug #969851)

* Thu Apr 25 2013 Philippe Makowski <makowski@fedoraproject.org>  2.5.2.26539.0-4
- set PIE compiler flags (bug #955274)

* Sun Mar 10 2013 Philippe Makowski <makowski@fedoraproject.org>  2.5.2.26539.0-3
- added patch from upstream to fix Firebird CORE-4058 CVE-2013-2492

* Sat Jan 26 2013 Rex Dieter <rdieter@fedoraproject.org> 2.5.2.26539.0-2
- rebuild (icu)

* Fri Nov 09 2012 Philippe Makowski <makowski@fedoraproject.org>  2.5.2.26539.0-1
- new upstream (bug fix release)
- added patch from upstream to fix Firebird CORE-3946

* Sat Aug 25 2012 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26351.0-4
- Modernize systemd scriptlets (bug #850109)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1.26351.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26351.0-2
- rebuild for icu 4.8

* Thu Jan 19 2012 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26351.0-1
- Fix non-fatal POSTIN fix rh #781691
- new upstream

* Fri Jan 06 2012 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26349.0-4
- Rebuild for GCC-4.7

* Mon Nov 28 2011 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26349.O-3
- Better systemd support fix rh #757624

* Sun Oct 02 2011 Karsten Hopp <karsten@redhat.com> 2.5.1.26349.O-2
- drop ppc64 configure script hack, not required anymore

* Thu Sep 29 2011 Philippe Makowski <makowski@fedoraproject.org>  2.5.1.26349.0-1
- new upstream (bug fix release)
- added patch from upstream to fix Firebird CORE-3610

* Thu Sep 22 2011 Philippe Makowski <makowski@fedoraproject.org>  2.5.0.26074.0-10
- Add support for systemd (rh #737281)

* Fri Apr 22 2011 Philippe Makowski <makowski@fedoraproject.org>  2.5.0.26074.0-8
- added patch from upstream to fix rh #697313

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 2.5.0.26074.0-7
- rebuild for icu 4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0.26074.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Philippe Makowski <makowski[at]fedoraproject.org>  2.5.0.26074.0-5
- services must not be enabled by default

* Tue Jan 25 2011 Karsten Hopp <karsten@redhat.com> 2.5.0.26074.0-4
- firebird got miscompiled on ppc and had an empty libfbclient.so.2.5.0
  bump release and rebuild

* Wed Dec 22 2010 Philippe Makowski <makowski[at]fedoraproject.org>  2.5.0.26074.0-3
- Fix wrong assign file for classic and classic common

* Thu Dec 16 2010 Dan Horák <dan[at]danny.cz>  2.5.0.26074.0-2
- sync the s390(x) utilities list with other arches
- add libatomic_ops-devel as BR: on non-x86 arches

* Sat Dec 04 2010 Philippe Makowski <makowski@fedoraproject.org>  2.5.0.26074.0-1
- Fix rh #656587 /var/run mounted as tempfs

* Mon Nov 22 2010 Philippe Makowski <makowski@fedoraproject.org>  2.5.0.26074.0-0
- build with last upstream

* Tue Jun 29 2010 Dan Horák <dan[at]danny.cz>  2.1.3.18185.0-9
- update the s390(x) patch to match upstream

* Fri Jun 04 2010 Philippe Makowski <makowski@fedoraproject.org>  2.1.3.18185.0-8
 - conditional BuildRequires libstdc++-static

* Fri Jun 04 2010 Philippe Makowski <makowski@fedoraproject.org>  2.1.3.18185.0-7
- build with last upstream
- Fix rh #563461 with backport mainstream patch CORE-2928


* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> 2.1.3.18185.0-6
- rebuild for icu 4.4

* Sat Sep 05 2009 Karsten Hopp <karsten@redhat.com> 2.1.3.18185.0-5
- fix build on s390x for F-12 mass rebuild (Dan Horák)

* Tue Aug 11 2009  Philippe Makowski <makowski at fedoraproject.org> 2.1.3.18185.0-4
- build it against system edit lib
- set correct setuid for Classic lock manager
- set correct permission for /var/run/firebird

* Wed Aug 05 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.3.18185.0-2
- rename /usr/bin/gstat to /usr/bin/gstat-fb  to avoid conflict with ganglia-gmond (rh #515510)
- remove stupid rm -rf in postun

* Thu Jul 30 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.3.18185.0-1
- Update to 2.1.3.18185
- Fix rh #514463
- Remove doc patch 
- Apply backport initscript patch

* Sat Jul 11 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-11
- change xinetd script (rh #506528)
- add missing library (and header files) for build php4-interbase module (rh #506728)
- update README.fedora
- automatically created user now have /bin/nologin as shell to make things a little more secure

* Tue May 12 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-8
- patch to fix gcc 4.4.0 and icu 4.2 build error

* Tue May 12 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-7
- patch to change lock files location and avoid %%{fbroot} owned by firebird user (rh #500219)
- add README.fedora
- add symlinks in /usr/bin
- change xinetd reload (rh #500219)

* Sat May 02 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-6
- add filesystem-subpackage
- remove common subpackage and use the main instead
- add logrotate config

* Thu Apr 30 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-5
- fix directories owning

* Thu Apr 23 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-4
- major cleaning install process to take care of the two architectures (Classic and Superserver) the right way

* Wed Apr 22 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-3
- fix group creation

* Sun Apr 19 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-2
- fix autogen issue for f11
- patch init script
- fix ppc64 lib destination issue

* Sun Apr 19 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-1
- backport doc patch
- update to 2.1.2.18118
- cleanup macros
- specifie libdir
- change firebird user login

* Sat Mar 28 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.1.17910.0-5
- Major packaging restructuring
 
* Sat Mar 21 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.1.17190.0-4
- Create a doc package
- major cleaning to avoid rpmlint errors
- revert to 2.1.1 (last stable build published)

* Mon Mar 09 2009  Jonathan MERCIER <bioinfornatics at gmail.com> 2.1.2.18116.0-3
- Perform %%configure with option --with-system-icu
- Add libicu-devel in BuildRequires
- Use iconv for convert files to UTF-8

* Thu Mar 05 2009  Jonathan MERCIER <bioinfornatics at gmail.com> 2.1.2.18116.0-2
- Update to 2.1.2
- Use %%global instead of %%define
- Change ${SOURCE1} to %%{SOURCE1}
- Change Group Database to Applications/Databases
- Change License IPL to Interbase
- Perform %%configure section's with some module
- Cconvert cyrillic character to UTF-8

* Thu Jul 17 2008 Arkady L. Shane <ashejn@yandex-team.ru> 2.1.1.17910.0-1
- Update to 2.1.1

* Fri Apr 18 2008 Arkady L. Shane <ashejn@yandex-team.ru> 2.1.0.17798.0-1
- Update to 2.1.0

* Thu Sep 27 2007 Arkady L. Shane <ashejn@yandex-team.ru> 2.0.3.12981.1-1
- Update to 2.0.3

* Thu Sep 13 2007 Arkady L. Shane <ashejn@yandex-team.ru> 2.0.1.12855.0-1
- Initial build for Fedora
- cleanup Mandriva spec
