# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sphinx_user sphinx
%global sphinx_group sphinx
%global sphinx_home %{_localstatedir}/lib/sphinx

# rpmbuild < 4.6 support
%if ! 0%{?__isa_bits}
%ifarch x86_64 ia64 ppc64 sparc64 s390x alpha ppc64le aarch64
%global __isa_bits 64
%else
%global __isa_bits 32
%endif
%endif

%if 0%{?fedora} >= 37 || 0%{?rhel} >= 10
%bcond_with java
%else
%bcond_without java
%endif


Name:		sphinx
Version:	2.2.11
Release:	34%{?dist}
Summary:	Free open-source SQL full-text search engine
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:	GPL-2.0-or-later
URL:		http://sphinxsearch.com

Source0:	http://sphinxsearch.com/files/%{name}-%{version}-release.tar.gz
Source1:	searchd.service
Patch0:		%{name}-2.0.3-fix_static.patch
Patch1:		listen_local.patch
Patch2:		sphinx-configure-c99.patch
Patch3:		sphinx-c99.patch

BuildRequires: make
BuildRequires:  gcc gcc-c++
BuildRequires:	expat-devel
BuildRequires:	mariadb-connector-c-devel openssl-devel
BuildRequires:	libpq-devel
BuildRequires:	systemd

Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

# Users and groups
       

%description
Sphinx is a full-text search engine, distributed under GPL version 2.
Commercial licensing (e.g. for embedded use) is also available upon request.

Generally, it's a standalone search engine, meant to provide fast,
size-efficient and relevant full-text search functions to other
applications. Sphinx was specially designed to integrate well with SQL
databases and scripting languages.

Currently built-in data source drivers support fetching data either via
direct connection to MySQL, or PostgreSQL, or from a pipe in a custom XML
format. Adding new drivers (e.g. native support other DBMSes) is
designed to be as easy as possible.

Search API native ported to PHP, Python, Perl, Ruby, Java, and also
available as a plug-gable MySQL storage engine. API is very lightweight so
porting it to new language is known to take a few hours.

As for the name, Sphinx is an acronym which is officially decoded as SQL
Phrase Index.
For the Sphinx documentation generator, see python-sphinx instead.


%package -n libsphinxclient
Summary:	Pure C search-d client API library


%description -n libsphinxclient
Pure C search-d client API library
Sphinx search engine, http://sphinxsearch.com/


%package -n libsphinxclient-devel
Summary:	Development libraries and header files for libsphinxclient
Requires:	libsphinxclient = %{version}-%{release}


%description -n libsphinxclient-devel
Pure C search-d client API library
Sphinx search engine, http://sphinxsearch.com/


%if %{with java}
%package java
Summary:		Java API for Sphinx
BuildRequires:	java-devel
Requires:		java-headless
Requires:		jpackage-utils


%description java
This package provides the Java API for Sphinx,
the free, open-source full-text search engine,
designed with indexing database content in mind.
%endif

%package php
Summary:	PHP API for Sphinx
Requires:	php-common >= 5.1.6


%description php
This package provides the PHP API for Sphinx,
the free, open-source full-text search engine,
designed with indexing database content in mind.


%prep
%setup -qn %{name}-%{version}-release
%patch -P0 -p1 -b .fix_static
%patch -P1 -p1 -b .default_listen
%patch -P2 -p1
%patch -P3 -p1

# Fix wrong-file-end-of-line-encoding
for f in \
	api/java/mk.cmd \
	api/ruby/test.rb \
	api/ruby/spec/%{name}/%{name}_test.sql \
	api/ruby/spec/%{name}/%{name}_test.sql \
; do
	sed -i 's/\r$//' ${f};
done

# Fix file not UTF8
iconv -f iso8859-1 -t utf-8 doc/%{name}.txt > doc/%{name}.txt.conv && mv -f doc/%{name}.txt.conv doc/%{name}.txt

# Create a sysusers.d config file
cat >sphinx.sysusers.conf <<EOF
g sphinx -
u sphinx - 'Sphinx Search' %{sphinx_home} /bin/bash
EOF

%build
%if %{__isa_bits} == 64
%configure --sysconfdir=%{_sysconfdir}/%{name} --with-mysql --with-pgsql --enable-id64
%else
%configure --sysconfdir=%{_sysconfdir}/%{name} --with-mysql --with-pgsql
%endif

make %{?_smp_mflags}

# Build libsphinxclient
pushd api/libsphinxclient
    %configure
    make #%{?_smp_mflags}
popd


%if %{with java}
# make the java api
make -C api/java 
%endif


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p -c"

install -p -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/searchd.service

# Create /var/log/sphinx
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}

# Create /var/run/sphinx
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/%{name}

# Create /var/lib/sphinx
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}

# Create sphinx.conf
cp $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}-min.conf.dist \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf
    
# Modify sphinx.conf
sed -i 's|/var/log/searchd.log|%{_localstatedir}/log/%{name}/searchd.log|g' \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf

sed -i 's|/var/log/query.log|%{_localstatedir}/log/%{name}/query.log|g' \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf

sed -i 's|/var/log/searchd.pid|%{_localstatedir}/run/%{name}/searchd.pid|g' \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf

sed -i 's|/var/data|%{_localstatedir}/lib/sphinx|g' \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf

# Create /etc/logrotate.d/sphinx
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name} << EOF
%{_localstatedir}/log/%{name}/*.log {
       weekly
       rotate 10
       copytruncate
       delaycompress
       compress
       notifempty
       missingok
}
EOF

# Create tmpfile run configuration
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
cat > $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf << EOF
d /run/%{name} 755 %{name} root -
EOF

# Install libsphinxclient
pushd api/libsphinxclient/
    make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p -c"
popd

%if %{with java}
# install the java api
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -m 0644 api/java/%{name}api.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{_javadir}/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}api.jar
%endif

# install the php api
# "Non-PEAR PHP extensions should put their Class files in /usr/share/php."
# - http://fedoraproject.org/wiki/Packaging:PHP
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/php
install -m 0644 api/%{name}api.php $RPM_BUILD_ROOT%{_datadir}/php

# clean-up .la archives
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# clean-up .a archives
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

install -m0644 -D sphinx.sysusers.conf %{buildroot}%{_sysusersdir}/sphinx.conf



%post
%systemd_post searchd.service

%preun
%systemd_preun searchd.service

%ldconfig_scriptlets -n libsphinxclient

%postun
%systemd_postun_with_restart searchd.service

%posttrans
chown -R %{sphinx_user}:root %{_localstatedir}/log/%{name}/
chown -R %{sphinx_user}:root %{_localstatedir}/run/%{name}/
chown -R %{sphinx_user}:root %{_localstatedir}/lib/%{name}/

%triggerun -- sphinx < 2.0.3-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save searchd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del searchd >/dev/null 2>&1 || :
/bin/systemctl try-restart searchd.service >/dev/null 2>&1 || :


%files
%doc COPYING doc/sphinx.txt sphinx-min.conf.dist sphinx.conf.dist example.sql
%dir %{_sysconfdir}/sphinx
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%exclude %{_sysconfdir}/%{name}/*.conf.dist
%exclude %{_sysconfdir}/%{name}/example.sql
%{_unitdir}/searchd.service
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_bindir}/*
%dir %attr(0755, %{sphinx_user}, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, %{sphinx_user}, root) %{_localstatedir}/run/%{name}
%dir %attr(0755, %{sphinx_user}, root) %{_localstatedir}/lib/%{name}
%{_mandir}/man1/*
%{_sysusersdir}/sphinx.conf

%files -n libsphinxclient
%doc COPYING %{?with_java: api/java} api/ruby api/*.php api/*.py api/libsphinxclient/README
%{_libdir}/libsphinxclient-0*.so

%files -n libsphinxclient-devel
%{_libdir}/libsphinxclient.so
%{_includedir}/*

%if %{with java}
%files java
%doc api/java/README COPYING
%{_javadir}/*
%endif

%files php
%doc COPYING
%{_datadir}/php/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2.11-33
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 2.2.11-31
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 19 2023 Florian Weimer <fweimer@redhat.com> - 2.2.11-28
- Additional C compatibility fixes

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Florian Weimer <fweimer@redhat.com> - 2.2.11-25
- C99 compatibility fixes

* Tue Aug 16 2022 Michal Schorm <mschorm@redhat.com> - 2.2.11-24
- Remove the Java binding
  Resolves: #2104104, #2113735

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.2.11-22
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2.11-19
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 2.2.11-18
- rebuild for libpq ABI fix rhbz#1908268

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 2.2.11-15
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 05 2019 Ben Cotton <bcotton@fedoraproject.org> - 2.2.11-13
- Listen only on localhost (CVE-2019-14511, rhbz#1749190)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 2.2.11-11
- Revert incorrect use of _tmpfiledir rhbx#1551735

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Ben Cotton <bcotton@fedoraproject.org> - 2.2.11-9
- Fix FTBFS rhbz#1606397

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 20 2017 Ben Cotton <bcotton@fedoraproject.org> - 2.2.11-6
- Change MariaDB interface package dependency rhbz#1493696
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Aug 11 2016 Gerald Cox <gbcox@fedoraproject.org> 2.2.11-2
- Correct tmpfile.d sphinx.conf rhbz#1366414

* Tue Jul 26 2016 Gerald Cox <gbcox@fedoraproject.org> 2.2.11-1
- Upstream 2.2.11; remove mysqld.service rhbz#1288815

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Sep 6 2015 Gerald Cox <gbcox@fedoraproject.org> - 2.2.10-1
- Upstream 2.2.10 rhbz#1260452

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Gerald Cox <gbcox@fedoraproject.org> - 2.2.9-1
- Upstream 2.2.9 rhbz#1201311

* Sun Mar 29 2015 Gerald Cox <gbcox@fedoraproject.org> - 2.2.8-1
- Upstream 2.2.8 rhbz#1201311

* Wed Jan 21 2015 Gerald Cox <gbcox@fedoraproject.org> - 2.2.7-1
- Upstream 2.2.7

* Sat Nov 15 2014 Gerald Cox <gbcox@fedoraproject.org> - 2.2.6-1
- Upstream 2.2.6

* Mon Nov 10 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.2.5-2
- Drop ExclusiveArch as armv7hl issue is fixed and aarch64/ppc64/s390 never had issues

* Tue Oct 28 2014 Gerald Cox <gbcox@fedoraproject.org> - 2.2.5-1
- Upstream 2.2.5
- ExclusiveArch: %%{ix86} x86_64 rhbz#1107361

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.5-2
- Move to java-headless
- Resolves: rhbz#1068545

* Tue Mar 25 2014 Michael Simacek <msimacek@redhat.com> - 2.1.5-2
- Remove version from JAR name

* Sun Jan 26 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.5-1
- upstream 2.1.5

* Sun Jan 26 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.2-2
- Fix build with systemd
- Cleanup and modernise spec

* Sat Nov  2 2013 Christof Damian <christof@damian.net> - 2.1.2-1
- upstream 2.1.2

* Fri Jul 26 2013 Christof Damian <christof@damian.net> - 2.0.8-2
- --enable-id64 flag for 64-bit builds

* Sat May 11 2013 Christof Damian <christof@damian.net> - 2.0.8-1
- upstream 2.0.8

* Sat Apr 20 2013 Christof Damian <christof@damian.net> - 2.0.7-1
- upstream 2.0.7
- use tmpfiles.d to create pid directory
- move default log file location to /var/log/sphinx
- use systemd macros BZ 850323

* Wed Mar  6 2013 Michel Salim <salimma@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6
- Remove obsoleted patches

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Jon Ciesla <limburgher@gmail.com> - 2.0.3-1
- New upstream, migrate to systemd, BZ 692157.
- Patched for gcc47.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 0.9.9-6
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 11 2010 Christof Damian <christof@damian.net> - 0.9.9-4
- add java and php subpackages ( bug 566787 )

* Sat Dec 11 2010 Christof Damian <christof@damian.net> - 0.9.9-3
- change default listen address to localhost ( bug 566792 )
- add ghost for files in /var/run/ ( bug 656694 )

* Wed Jul 14 2010 Christof Damian <christof@damian.net> - 0.9.9-2
- add COPYING file to lib package

* Thu Feb 11 2010 Allisson Azevedo <allisson@gmail.com> 0.9.9-1
- Update to 0.9.9 (#556997).
- Added sphinx-0.9.9-fix_static.patch to fix FTBS.
- Run sphinx searchd as non-root user (#541464).

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8.1-4
- Rebuild with new openssl

* Wed Aug 12 2009 Allisson Azevedo <allisson@gmail.com> 0.9.8.1-3
- Fixed macros consistency.
- Modified make install to keep timestamps.
- Added libsphinxclient package.

* Fri Aug  7 2009 Allisson Azevedo <allisson@gmail.com> 0.9.8.1-2
- Added sysv init.
- Added logrotate.d entry.

* Thu Jul 30 2009 Allisson Azevedo <allisson@gmail.com> 0.9.8.1-1
- Initial rpm release.
