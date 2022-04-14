Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package hsqldb
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


#Compat macro for new _fillupdir macro introduced in Nov 2017
%if ! %{defined _fillupdir}
  %define _fillupdir /var/adm/fillup-templates
%endif

Name:           hsqldb
Version:        2.4.1
Release:        3%{?dist}
Summary:        HyperSQL Database Engine
License:        BSD
Group:          Productivity/Databases/Servers
Url:            http://hsqldb.sourceforge.net/
Source0:        http://downloads.sourceforge.net/hsqldb/%{name}-%{version}.zip
Source1:        hsqldb-1.8.0-standard.cfg
Source2:        hsqldb-1.8.0-standard-server.properties
Source3:        hsqldb-1.8.0-standard-webserver.properties
Source4:        hsqldb-1.8.0-standard-sqltool.rc
Source5:        http://www.hsqldb.org/repos/org/hsqldb/hsqldb/%{version}/hsqldb-%{version}.pom
# Custom systemd files - talking with upstream about incorporating them, see
# http://sourceforge.net/projects/hsqldb/forums/forum/73673/topic/5367103
Source6:        hsqldb.systemd
Source7:        hsqldb-wrapper
Source8:        hsqldb-post
Source9:        hsqldb-stop
# Javadoc fails to create since apidocs folder is deleted and not recreated
Patch0:         %{name}-apidocs.patch
# Package org.hsqldb.cmdline was only compiled with java 1.5
Patch1:         %{name}-cmdline.patch
# Jdk10's javadoc ends up in error when a remote url cannot be reached
Patch2:         hsqldb-2.4.1-javadoc10.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
# Needed for maven conversions
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  javapackages-tools
BuildRequires:  junit
BuildRequires:  servletapi5
BuildRequires:  pkgconfig(systemd)
BuildRequires:  unzip
Requires:       java >= 1.8
Requires:       servletapi5
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Requires(pre):  shadow-utils
Requires(post): systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%description
HSQLdb is a relational database engine written in JavaTM , with a JDBC
driver, supporting a subset of ANSI-92 SQL. It offers a small (about
100k), fast database engine which offers both in memory and disk based
tables. Embedded and server modes are available. Additionally, it
includes tools such as a minimal web server, in-memory query and
management tools (can be run as applets or servlets, too) and a number
of demonstration examples.

Downloaded code should be regarded as being of production quality. The
product is currently being used as a database and persistence engine in
many Open Source Software projects and even in commercial projects and
products! In it's current version it is extremely stable and reliable.
It is best known for its small size, ability to execute completely in
memory and its speed. Yet it is a completely functional relational
database management system that is completely free under the Modified
BSD License. Yes, that's right, completely free of cost or
restrictions!

%package manual
Summary:        Manual for %{name}
Group:          Documentation/Other

%description manual
Manual for %{name}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demo for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n %{name}-%{version}/%{name}

# set right permissions
find . -name "*.sh" -exec chmod 755 {} +

# remove all _notes directories
find . -name _notes -exec rm -rf {} +

# remove all binary libs
find . -name "*.jar" -exec rm -f {} +
find . -name "*.class" -exec rm -f {} +
find . -name "*.war" -exec rm -f {} +

# correct silly permissions
chmod -R go=u-w *

# Fix doc location
sed -i -e 's/doc-src/doc/g' build/build.xml
sed -i -e 's|doc/apidocs|%{_javadocdir}/%{name}|g' index.html

%patch0 -p1
%patch1 -p1
%patch2 -p2

%build
export CLASSPATH=$(build-classpath servletapi5 junit)

pushd build
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF8 -Dant.build.javac.source=1.7 -Dant.build.javac.target=1.7"
ant hsqldb javadoc
popd

%install
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 lib/%{name}.jar %{buildroot}%{_javadir}/%{name}.jar

# systemd
install -d -m 755 %{buildroot}%{_unitdir}
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}
install -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/%{name}.service
install -m 755 %{SOURCE7} %{buildroot}%{_libexecdir}/%{name}/%{name}-wrapper
install -m 755 %{SOURCE8} %{buildroot}%{_libexecdir}/%{name}/%{name}-post
install -m 755 %{SOURCE9} %{buildroot}%{_libexecdir}/%{name}/%{name}-stop

# rchsqldb link
install -d -m 0755 %{buildroot}/%{_sbindir}/
ln -sf service %{buildroot}/%{_sbindir}/rc%{name}

# sysconfig
#install -d -m 0755 %{buildroot}%{_fillupdir}
#install -m 700 %{SOURCE1} %{buildroot}%{_fillupdir}/sysconfig.%{name}
install -d -m 0755 %{buildroot}/%{_sysconfdir}
install -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/%{name}.conf

# serverconfig
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -m 644 %{SOURCE2} %{buildroot}%{_localstatedir}/lib/%{name}/server.properties
install -m 644 %{SOURCE3} %{buildroot}%{_localstatedir}/lib/%{name}/webserver.properties
install -m 600 %{SOURCE4} %{buildroot}%{_localstatedir}/lib/%{name}/sqltool.rc

# lib
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/lib

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -r doc/apidocs/* %{buildroot}%{_javadocdir}/%{name}

# data
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/data

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/sample
rm -f sample/%{name}.init
install -m 644 sample/* %{buildroot}%{_datadir}/%{name}/sample

# manual
install -d -m 755 %{buildroot}%{_docdir}/%{name}-%{version}
cp -pr doc/* %{buildroot}%{_docdir}/%{name}-%{version}
cp -p index.html %{buildroot}%{_docdir}/%{name}-%{version}

cd ..
# Maven metadata
install -pD -T -m 644 %{SOURCE5} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

pushd %{buildroot}%{_localstatedir}/lib/%{name}/lib
    # build-classpath can not be used as the jar is not
    # yet present during the build
    ln -s %{_javadir}/hsqldb.jar hsqldb.jar
    ln -s $(build-classpath servletapi5) servletapi5.jar
popd

%fdupes -s %{buildroot}

%pre
# Add the "hsqldb" user and group
# we need a shell to be able to use su - later
if [ `getent group %{name}` ]; then
    : OK group hsqldb already present
else
    %{_sbindir}/groupadd -r %{name} 2> /dev/null || :
fi
if [ `getent passwd %{name}` ]; then
    : OK user hsqldb already present
else
    %{_sbindir}/useradd -r -g %{name} -c "Hsqldb" -s /bin/sh \
    -d %{_localstatedir}/lib/%{name} %{name} 2> /dev/null || :
fi

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(0644,root,root,0755)
%license hsqldb/doc/hsqldb_lic.txt
%dir %{_docdir}/%{name}-%{version}
%{_javadir}/*
%{_sbindir}/rc%{name}
%{_unitdir}/%{name}.service
%dir %{_libexecdir}/%{name}/
%attr(0755,root,root) %{_libexecdir}/%{name}/%{name}-post
%attr(0755,root,root) %{_libexecdir}/%{name}/%{name}-stop
%attr(0755,root,root) %{_libexecdir}/%{name}/%{name}-wrapper
%{_localstatedir}/lib/%{name}/lib
%attr(0700,hsqldb,hsqldb) %{_localstatedir}/lib/%{name}/data
%attr(0644,root,root) %{_localstatedir}/lib/%{name}/server.properties
%attr(0644,root,root) %{_localstatedir}/lib/%{name}/webserver.properties
%attr(0600,hsqldb,hsqldb) %{_localstatedir}/lib/%{name}/sqltool.rc
%dir %{_localstatedir}/lib/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %{_mavenpomdir}
%{_mavenpomdir}/*
%{_datadir}/maven-metadata/%{name}.xml

%files manual
%defattr(0644,root,root,0755)
%license hsqldb/doc/hsqldb_lic.txt
%doc %{_docdir}/%{name}-%{version}

%files javadoc
%defattr(0644,root,root,0755)
%license hsqldb/doc/hsqldb_lic.txt
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,0755)
%{_datadir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.1-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 27 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.4.1-2.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Update systemd macros.

* Wed Jun 12 2019 Dominique Leuenberger <dimstar@opensuse.org>
- BuildRequire pkgconfig(systemd) instead of systemd: allow OBS to
  shortcut the build queues by allowing usage of systemd-mini
* Thu Jul 12 2018 fstrba@suse.com
- Version bump to 2.4.1
  * Require java 8 or higher
- Changed patch:
  * hsqldb-2.3.3-javadoc10.patch -> hsqldb-2.4.1-javadoc10.patch
    + rediff to changed context
* Mon Dec 18 2017 fstrba@suse.com
- Added patch:
  * hsqldb-2.3.3-javadoc10.patch
    + Fix build with jdk10's javadoc that ends in error when a
    link cannot be downloaded
* Thu Nov 23 2017 rbrown@suse.com
- Replace references to /var/adm/fillup-templates with new
  %%_fillupdir macro (boo#1069468)
* Fri Sep 29 2017 fstrba@suse.com
- Mofified patch:
  * hsqldb-apidocs.patch
    + Don't force -Xdoclint:none, since we switched the default
    doclint run off in all our java-devel providers and this
    option does not work with java < 1.8
* Fri Sep  8 2017 fstrba@suse.com
- Specify java source and target version 1.7 in order to allow
  build with jdk9
* Fri May 19 2017 mpluskal@suse.com
- Update dependencies
* Wed Jul 29 2015 tchvatal@suse.com
- Version bump to 2.3.3:
  * Various serveral minor issues
  * No obvious detailed changelog
- Fix build with jdk8 by tweaking doclint:
  * hsqldb-apidocs.patch
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Sun Jan 18 2015 p.drouand@gmail.com
- Update to version 2.3.2
  * fixed several minor issues
  * fixed bug with incomplete rollback of MVCC transaction that
    inserts and updates the same row
  * fixed issue with parsing of long BIT strings in SQL
  * fixed issue with SQL triggers when columns were added or dropped
    from a table with SQL triggers
  * fixed issue with an index added to a TEMP table with ON COMMIT
    PRESERVE ROWS and containing data
  * added URL property hsqldb.digest which can be used with alternative
    secure hash algorithms for passwords
  * changed the class used for offline backup and restore to
    org.hsqldb.lib.tar.DbBackupMain
  * extended the scope of SET DATABASE SQL REFERENCES TRUE to catch
    ambiguity with identical table aliases
  * extended support for the DEFAULT keyword used in INSERT and UPDATE
    to apply to columns with no default
  * improved support for recursive queries
  * improved ORA and MYS syntax compatibility modes
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Wed Sep  4 2013 mvyskocil@suse.com
- Update to 2.2.9
  * new core fully multithreaded core supports 2PL (two-phased locking)
    and MVCC (multiversion concurrency control), plus a hybrid 2PL+MVCC
    transaction control mode
  * Massive high performance LOB store for BLOBs and CLOBs up to multi-gigabyte
    size, with total storage capacity of 64 terabytes.
  * Increased default storage space of 16GB for ordinary data, with fast
    startup and shutdown. Storage space can be extended to 2TB.
  * Large result sets, views and subqueries can now be stored on disk (on the
    server side) while being generated and accessed. The threshold to store
    a result on disk, as well as the actual fetch size in client-server
    configurations can be specified per connection.
  * All query conditions, whether in a JOIN or WHERE clause, are now
    allocated to an index if possible.
  * HyperSQL supports schema-based stored procedures and functions written
    entirely in SQL and JAVA.
  * Support for BIT, BIT VARYING, CLOB, BLOB, INTERVAL according to the
    SQL Standards
  * and many more - see http://hsqldb.sourceforge.net/web/features200.html
- Dropped patches
  * hsqldb-1.8.0-scripts.patch
  * hsqldb-1.8.0.10-suse-initscript.patch (systemd service is used)
  * hsqldb-jdbc-4.1.patch
  * hsqldb-tmp.patch (hsqldb-wrapper is used)
- New patches
  * hsqldb-apidocs.patch
  * hsqldb-cmdline.patch
- systemd integration and drop init script
* Mon May 21 2012 mvyskocil@suse.cz
- Update to 1.8.1.3
  * adds support for fast closing of huge database files
  * better query optimisation.
  * bugfixes
- add maven pom
- fix build with jdk7
- run su with -s /bin/sh in initscript
* Mon Dec 19 2011 dmueller@suse.de
- fix hsqldb_lic.txt packaged in hsqldb-manual and hsqldb
* Fri Jan 14 2011 mvyskocil@suse.cz
- fix bnc#664425 - error in init script of hsqldb
  * init PATH on the begining
  * use absolute names
- change default shell from /bin/false to /bin/sh to make su command
  (and server start) possible
- change hsqldb jar location to /usr/share/java/hsqldb.jar
* Wed May 13 2009 mvyskocil@suse.cz
- Initial SUSE packaging od hsqldb 1.8.0.10 from jpackage.org
