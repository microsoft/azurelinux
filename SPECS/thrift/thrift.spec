%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
 
%{?perl_default_filter}
%global __provides_exclude_from ^(%{python3_sitearch}/.*\\.so|%{php_extdir}/.*\\.so)$
 
%global have_mongrel 0
 
# erlang-jsx is available in F19 but orphaned in F22
%global have_jsx 0
 
# We should be able to enable this in the future
%global want_d 0
 
# Can't do anything with java with all the build deps in modules
%global want_java 0
 
%if 0%{?want_java} == 0
%global java_configure --without-java
%else
%global java_configure --with-java
%endif
 
# Thrift's Ruby support depends on Mongrel.  Since Mongrel is
# deprecated in Fedora, we can't support Ruby bindings for Thrift
# unless and until Thrift is patched to use a different HTTP server.
%if 0%{?have_mongrel} == 0
%global ruby_configure --without-ruby
%global with_ruby 0
%else
%global ruby_configure --with-ruby
%global want_ruby 1
%endif
 
# Thrift's Erlang support depends on the JSX library, which is not
# currently available in Fedora.
 
%if 0%{?have_jsx} == 0
%global erlang_configure --without-erlang
%global want_erlang 0
%else
%global erlang_configure --with-erlang
%global want_erlang 1
%endif
 
# PHP appears broken in Thrift 0.9.1
%global want_php 0
 
%if 0%{?want_php} == 0
%global php_langname %{nil}
%global php_configure --without-php
%else
%global php_langname PHP,\ 
%global php_configure --with-php
%endif
 
# Thrift's GO support doesn't build under Fedora
%global want_golang 0
%global golang_configure --without-go
 
# Thrift's Lua support has not yet been worked on
%global want_lua 0
%global lua_configure --without-lua
 
# NOTE: thrift versions their libraries by package version, so each version
# change is a SONAME change and dependencies need to be rebuilt
Summary: Software framework for cross-language services development
Name:    thrift
Version: 0.15.0
Release: 6%{?dist}

# Parts of the source are used under the BSD and zlib licenses, but
# these are OK for inclusion in an Apache 2.0-licensed whole:
# https://www.apache.org/legal/3party.html
 
# Here's the breakdown:
# ./lib/py/compat/win32/stdint.h is 2-clause BSD
# ./compiler/cpp/src/md5.[ch] are zlib
License: Apache-2.0 AND BSD-3-Clause AND Zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:     https://thrift.apache.org/
 
Source0: https://archive.apache.org/dist/%{name}/%{version}/%{name}-%{version}.tar.gz
 
Source1: https://repo1.maven.org/maven2/org/apache/thrift/lib%{name}/%{version}/lib%{name}-%{version}.pom
Source2: https://raw.github.com/apache/%{name}/%{version}/bootstrap.sh
 
# fix configure.ac insistence on using /usr/local/lib for JAVA_PREFIX
Patch1: configure-java-prefix.patch
 
 
# BuildRequires for language-specific bindings are listed under these
# subpackages, to facilitate enabling or disabling individual language
# bindings in the future

BuildRequires: pkgconfig(libcrypto)
BuildRequires: python3-six
%if 0%{?want_java} > 0
BuildRequires: ant >= 1.7
%endif
BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: boost-devel
BuildRequires: boost-static
BuildRequires: flex
BuildRequires: gcc-c++
BuildRequires: glib2-devel
BuildRequires: libevent-devel
BuildRequires: libstdc++-devel
BuildRequires: libtool
BuildRequires: openssl-devel
BuildRequires: openssl-libs
BuildRequires: zlib-devel
 
%if 0%{?want_golang} > 0
BuildRequires: golang
Requires: golang
%endif
 
%description
 
The Apache Thrift software framework for cross-language services
development combines a software stack with a code generation engine to
build services that work efficiently and seamlessly between C++, Java,
Python, %{?php_langname}and other languages.
 
%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: boost-devel
 
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
 
%package -n python3-%{name}
Summary: Python 3 support for %{name}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python3
Obsoletes: python-%{name} < 0.10.0-1%{?dist}
Obsoletes: python2-%{name} < 0.10.0-14%{?dist}
 
%description -n python3-%{name}
The python3-%{name} package contains Python bindings for %{name}.
 
%package -n perl-%{name}
Summary: Perl support for %{name}
Provides: perl(Thrift) = %{version}-%{release}
BuildRequires: perl-Bit-Vector
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-generators
Requires: perl-Bit-Vector
Requires: perl(Encode)
Requires: perl(HTTP::Request)
Requires: perl(IO::Select)
Requires: perl(IO::Socket::INET)
Requires: perl(LWP::UserAgent)
Requires: perl(POSIX)
Requires: perl(base)
Requires: perl(constant)
Requires: perl(strict)
Requires: perl(utf8)
Requires: perl(warnings)
# thrift improperly packages some components in files with names different
# than the package they contain
Provides: perl(Thrift::Exception)
Provides: perl(Thrift::MessageType)
Provides: perl(Thrift::Type)
BuildArch: noarch
 
%description -n perl-%{name}
The perl-%{name} package contains Perl bindings for %{name}.
 
%if %{?want_d}
%package -n d-%{name}
Summary: D support for %{name}
BuildRequires: ldc
 
%description -n d-%{name}
The d-%{name} package contains D bindings for %{name}.
%endif
 
%if 0%{?want_php} != 0
%package -n php-%{name}
Summary: PHP support for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
Requires: php(language) >= 5.3.0
Requires: php-date
Requires: php-json
BuildRequires: php-devel
 
%description -n php-%{name}
The php-%{name} package contains PHP bindings for %{name}.
%endif
 
%if 0%{?want_java} > 0
%package -n lib%{name}-javadoc
Summary: API documentation for java-%{name}
Requires: lib%{name}-java = %{version}-%{release}
BuildArch: noarch
 
%description -n lib%{name}-javadoc 
The lib%{name}-javadoc package contains API documentation for the
Java bindings for %{name}.
 
%package -n lib%{name}-java
Summary: Java support for %{name}
 
BuildRequires: apache-commons-codec
BuildRequires: apache-commons-lang
BuildRequires: apache-commons-logging
BuildRequires: httpcomponents-client
BuildRequires: httpcomponents-core
BuildRequires: java-devel
BuildRequires: javapackages-tools
BuildRequires: javapackages-local
BuildRequires: junit
BuildRequires: log4j
BuildRequires: slf4j
# javax.servlet-api 3.1.0 is provided by glassfish-servlet-api
BuildRequires: mvn(javax.servlet:javax.servlet-api) = 3.1.0
 
Requires: java-headless >= 1:1.6.0
Requires: javapackages-tools
Requires: mvn(org.slf4j:slf4j-api)
Requires: mvn(commons-lang:commons-lang)
Requires: mvn(org.apache.httpcomponents:httpclient)
Requires: mvn(org.apache.httpcomponents:httpcore)
BuildArch: noarch
 
%description -n lib%{name}-java
The lib%{name}-java package contains Java bindings for %{name}.
%endif
 
%if 0%{?want_ruby} > 0
%package -n ruby-%{name}
Summary: Ruby support for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: ruby(release)
BuildRequires: ruby-devel
 
%description -n ruby-%{name}
The ruby-%{name} package contains Ruby bindings for %{name}.
%endif
 
%if 0%{?want_erlang} > 0
%package -n erlang-%{name}
Summary: Erlang support for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: erlang
Requires: erlang-jsx
BuildRequires: erlang
BuildRequires: erlang-rebar
 
%description -n erlang-%{name}
The erlang-%{name} package contains Erlang bindings for %{name}.
%endif
 
 
%prep
%autosetup -p1
 
%{?!el5:sed -i -e 's/^AC_PROG_LIBTOOL/LT_INIT/g' configure.ac}
 
# avoid spurious executable permissions in debuginfo package
find . -name \*.cpp -or -name \*.cc -or -name \*.h | xargs -r chmod 644
 
cp -p %{SOURCE2} bootstrap.sh
 
# work around linking issues
echo 'libthriftz_la_LIBADD = $(ZLIB_LIBS) -lthrift -L.libs' >> lib/cpp/Makefile.am
echo 'EXTRA_libthriftz_la_DEPENDENCIES = libthrift.la' >> lib/cpp/Makefile.am
 
# fix broken upstream check for ant version; we enforce this with BuildRequires, so no need to check here
sed -i 's|ANT_VALID=.*|ANT_VALID=1|' aclocal/ax_javac_and_java.m4
 
# explicitly set python3
shopt -s globstar
sed -i -E 's@^(#!.*/env) *python *$@\1 python3@' **/*.py
 
%build
export PY_PREFIX=%{_prefix}
export PERL_PREFIX=%{_prefix}
export PHP_PREFIX=%{php_extdir}
export JAVA_PREFIX=%{_javadir}
export RUBY_PREFIX=%{_prefix}
export GOBJECT_LIBS=$(pkg-config --libs gobject-2.0)
export GOBJECT_CFLAGS=$(pkg-config --cflags gobject-2.0)

find %{_builddir} -name rebar -exec rm -f '{}' \;
find . -name Makefile\* -exec sed -i -e 's/[.][/]rebar/rebar/g' {} \;
 
# install javadocs in proper places
sed -i 's|-Dinstall.javadoc.path=$(DESTDIR)$(docdir)/java|-Dinstall.javadoc.path=$(DESTDIR)%{_javadocdir}/%{name}|' lib/java/Makefile.*
 
# build a jar without a version number
#sed -i 's|${thrift.artifactid}-${version}|${thrift.artifactid}|' lib/java/build.xml
 
# Proper permissions for Erlang files
sed -i 's|$(INSTALL) $$p|$(INSTALL) --mode 644 $$p|g' lib/erl/Makefile.am
 
sh ./bootstrap.sh
 
# use unversioned doc dirs where appropriate (via _pkgdocdir macro)
export PYTHON=%{_bindir}/python3
%configure --disable-dependency-tracking --disable-static --with-boost=/usr \
  --docdir=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}} \
  %{java_configure} %{ruby_configure} %{erlang_configure} %{golang_configure} %{php_configure} %{lua_configure}
 
# eliminate unused direct shlib dependencies
sed -i -e 's/ -shared / -Wl,--as-needed\0/g' libtool
 
%make_build
 
%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name fastbinary.so | xargs -r chmod 755
find %{buildroot} -name \*.erl -or -name \*.hrl -or -name \*.app | xargs -r chmod 644
 
# Remove javadocs jar
%if 0%{?want_java} > 0
find %{buildroot}/%{_javadir} -name lib%{name}-javadoc.jar -exec rm -f '{}' \;
# Add POM file and depmap
mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-libthrift.pom
%add_maven_depmap JPP-libthrift.pom libthrift.jar
%endif
 
# Remove bundled jar files
find %{buildroot} -name \*.jar -a \! -name \*thrift\* -exec rm -f '{}' \;
 
# Move perl files into appropriate places
find %{buildroot} -name \*.pod -exec rm -f '{}' \;
find %{buildroot} -name .packlist -exec rm -f '{}' \;

 
%if 0%{?want_php} != 0
 
# Move arch-independent php files into the appropriate place
mkdir -p %{buildroot}/%{_datadir}/php/
mv %{buildroot}/%{php_extdir}/Thrift %{buildroot}/%{_datadir}/php/
%endif
 
# Fix permissions on Thread.h
find %{buildroot} -name Thread.h -exec chmod a-x '{}' \;
 
# Ensure all python scripts are executable
find %{buildroot} -name \*.py -exec grep -q /usr/bin/env {} \; -print | xargs -r chmod 755
%ldconfig_scriptlets


%files
%doc LICENSE NOTICE
%{_bindir}/thrift
%{_libdir}/libthrift-%{version}.so
%{_libdir}/libthriftz-%{version}.so
%{_libdir}/libthriftnb-%{version}.so
  
%files devel
%{_includedir}/thrift
%{_libdir}/*.so
%{_libdir}/*.so.0
%{_libdir}/*.so.0.0.0
%exclude %{_libdir}/lib*-%{version}.so
%{_libdir}/pkgconfig/thrift-z.pc
%{_libdir}/pkgconfig/thrift-nb.pc
%{_libdir}/pkgconfig/thrift.pc
%{_libdir}/pkgconfig/thrift_c_glib.pc
%doc LICENSE NOTICE

 
%if 0%{?want_php} != 0
%files -n php-%{name}
%config(noreplace) /etc/php.d/thrift_protocol.ini
%{_datadir}/php/Thrift/
%{php_extdir}/thrift_protocol.so
%doc LICENSE NOTICE
%endif
 
%if %{?want_erlang} > 0
%files -n erlang-%{name}
%{_libdir}/erlang/lib/%{name}-%{version}/
%doc LICENSE NOTICE
%endif
 
%files -n python3-%{name}
%{python3_sitearch}/%{name}
%{python3_sitearch}/%{name}-%{version}-py%{python3_version}.egg-info
%doc LICENSE NOTICE
 
%if 0%{?want_java} > 0
%files -n lib%{name}-javadoc
%{_javadocdir}/%{name}
%doc LICENSE NOTICE
 
%files -n lib%{name}-java -f .mfiles
%doc LICENSE NOTICE
%endif
 
%changelog
* Thu May 09 2024 Henry Beberman <henry.beberman@microsoft.com> - 0.15.0-6
- Backport from AzureLinux 3.0

* Tue Mar 19 2024 Himaja Kesari <himajakesari@microsoft.com> - 0.15.0-5
- Initial CBL-Mariner import from Fedora 40 (license: MIT).
- License verified.

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Fri Jun 16 2023 Orion Poplawski <orion@nwra.com> - 0.15.0-2
- Re-enable LTO, seems to be working again
 
* Thu Jun 15 2023 Orion Poplawski <orion@nwra.com> - 0.15.0-1
- Update to 0.15.0
 
* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.14.0-14
- Rebuilt for Python 3.12
 
* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Fri Nov 18 2022 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.14.0-12
- Convert license tags to SPDX
 
* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.14.0-10
- Rebuilt for Python 3.11
 
* Tue Jun 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.14.0-9
- Work around GCC 12 error by disabling LTO (close RHBZ#2046213)
 
* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.14.0-8
- Perl 5.36 rebuild
 
* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.14.0-6
- Rebuilt with OpenSSL 3.0.0
 
* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.14.0-4
- Rebuilt for Python 3.10
 
* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.14.0-3
- Perl 5.34 rebuild
 
* Thu Feb 18 2021 Orion Poplawski <orion@nwra.com> - 0.14.0-2
- Add patch to fix compilation on non-x86
 
* Mon Feb 15 2021 Orion Poplawski <orion@nwra.com> - 0.14.0-1
- Update to 0.14.0 (bz#1928172) CVE-2020-13949
 
* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Mon Oct 05 2020 Orion Poplawski <orion@nwra.com> - 0.13.0-9
- Add BR python3-setuptools
 
* Wed Sep 23 2020 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.13.0-8
- rebuilt for side tag f34-build-side-30069
 
* Thu Sep 17  2020 Orion Poplawski <orion@nwra.com> - 0.13.0-7
- Drop unneeded BR on flex-devel (bz#1871095)
 
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.13.0-5
- Perl 5.32 rebuild
 
* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-4
- Rebuilt for Python 3.9
 
* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Wed Dec 4 2019 Orion Poplawski <orion@nwra.com> - 0.13.0-2
- Fix perl dependencies
- Explicitly disable lua
 
* Sun Dec 1 2019 Orion Poplawski <orion@nwra.com> - 0.13.0-1
- Update to 0.13.0 (bz#1778343)
- Drops fb303 package
- Switch to Qt5
 
* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-20
- Rebuilt for Python 3.8.0rc1 (#1748018)
 
* Tue Aug 20 2019 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.10.0-19
- Fix FTBFS (by removing Java support) and fix Python3 issues (rhbz#1738810 and rhbz#1533306)
 
* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.10.0-17
- Perl 5.30 rebuild
 
* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Wed Jul 18 2018 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.10.0-15
- Rebuild to address transient error
 
* Wed Jul 18 2018 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.10.0-14
- Migrate to python3; rhbz#1533306
 
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.10.0-12
- Perl 5.28 rebuild
 
* Wed May 30 2018 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.10.0-11
- Fix FTBFS; update servlet-api dependency (rhbz#1581175)
 
* Thu Mar 08 2018 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.10.0-10
- Add gcc-c++ BuildRequires
 
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Fri Dec 22 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.10.0-8
- Fix for rhbz#1507518
 
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild
 
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Thu Jul 06 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.10.0-5
- Fix FTBFS in rawhide: add BR javapackages-local
 
* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.10.0-4
- Perl 5.26 rebuild
 
* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild
 
* Mon Mar 13 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.10.0-2
- Build TNonblockingServer, remove useless man page, and use java-headless
 
* Tue Mar 07 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.10.0-1
- Update to thrift 0.10.0
 
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-17.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-17.5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages
 
* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.9.1-17.4
- Perl 5.24 rebuild
 
* Wed Mar 30 2016 Petr Pisar <ppisar@redhat.com> - 0.9.1-17.3
- Adapt to GCC 6 (bug #1306671)
 
* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-17.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Sat Jan 16 2016 Jonathan Wakely <jwakely@redhat.com> - 0.9.1-17.1
- Rebuilt for Boost 1.60
 
* Mon Nov 23 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.1-17
- Fix release
 
* Wed Oct 21 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.9.1-16.6
- Backport THRIFT-2214 fix to get package built on aarch64.
 
* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.9.1-16.5
- Rebuilt for Boost 1.59
 
* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-16.4
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159
 
* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.9.1-16.3
- rebuild for Boost 1.58
 
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-16.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.9.1-16.1
- Perl 5.22 rebuild
 
* Fri Apr 24 2015 Michal Srb <msrb@redhat.com> - 0.9.1-16
- Fix FTBFS (Resolves: rhbz#1195364)
 
* Mon Apr 20 2015 Will Benton <willb@redhat.com> - 0.9.1-15
- Dropped Erlang support for F22 and above, since erlang-jsx is orphaned
 
* Wed Apr  8 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.1-14
- Split Qt4/GLib runtimes into separate subpackages
- Drop mono support, it's broken and not even shipped (and it pulls mono-core)
 
* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 0.9.1-13.3
- Rebuild for boost 1.57.0
* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.9.1-13.2
- Perl 5.20 rebuild
 
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-13.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
 
* Fri Jun 27 2014 Petr Pisar <ppisar@redhat.com> - 0.9.1-13
- Use add_maven_depmap-generated file lists (bug #1107448)
 
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-12.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.9.1-12.1
- Rebuild for boost 1.55.0
 
* Mon May 05 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.9.1-12
- Fix EPEL build
 
* Fri Feb 21 2014 willb <willb@redhat> - 0.9.1-11
- fix BZ 1068561
 
* Fri Dec 20 2013 willb <willb@redhat> - 0.9.1-10
- fix BZ 1045544
 
* Wed Oct 16 2013 willb <willb@redhat> - 0.9.1-9
- Remove spurious dependencies
- Move some versioned shared libraries from -devel
 
* Wed Oct 16 2013 Dan Horák <dan[at]danny.cz> - 0.9.1-8
- Mono available only on selected arches
 
* Sun Oct 13 2013 willb <willb@redhat> - 0.9.1-7
- minor specfile cleanups
 
* Fri Oct 11 2013 willb <willb@redhat> - 0.9.1-6
- added thrift man page
- integrated fb303
- fixed many fb303 library dependency problems
 
* Tue Oct 1 2013 willb <willb@redhat> - 0.9.1-5
- fixed extension library linking when an older thrift package is not
  already installed
- fixed extension library dependencies in Makefile
 
* Tue Oct 1 2013 willb <willb@redhat> - 0.9.1-4
- addresses rpmlint warnings and errors
- properly links glib, qt, and z extension libraries
 
* Mon Sep 30 2013 willb <willb@redhat> - 0.9.1-3
- adds QT support
- clarified multiple licensing
- uses parallel make
- removes obsolete M4 macros
- specifies canonical location for source archive
 
* Tue Sep 24 2013 willb <willb@redhat> - 0.9.1-2
- fixes for i686
- fixes bogus requires for Java package
 
* Fri Sep 20 2013 willb <willb@redhat> - 0.9.1-1
- updated to upstream version 0.9.1
- disables PHP support, which FTBFS in this version
 
* Fri Sep 20 2013 willb <willb@redhat> - 0.9.0-5
- patch build xml to generate unversioned jars instead of moving after the fact
- unversioned doc dirs on Fedora versions where this is appropriate
- replaced some stray hardcoded paths with macros
- thanks to Gil for the above observations and suggestions for fixes
 
* Thu Aug 22 2013 willb <willb@redhat> - 0.9.0-4
- removed version number from jar name (obs pmackinn)
 
* Thu Aug 22 2013 willb <willb@redhat> - 0.9.0-3
- Fixes for F19 and Erlang support
 
* Thu Aug 15 2013 willb <willb@redhat> - 0.9.0-2
- Incorporates feedback from comments on review request
 
* Mon Jul 1 2013 willb <willb@redhat> - 0.9.0-1
- Initial package

