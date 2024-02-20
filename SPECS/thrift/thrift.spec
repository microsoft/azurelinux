# thrift: FTBFS in Fedora 36: /usr/include/c++/12/bits/new_allocator.h:158:33:
# error: 'operator delete' called on pointer '_605' with nonzero offset [1,
# 9223372036854775800] [-Werror=free-nonheap-object]
# https://bugzilla.redhat.com/show_bug.cgi?id=2046213
#
 
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
Name:    thrift
Version: 0.15.0
Release: 0%{?dist}
Summary: Software framework for cross-language services development
 
# Parts of the source are used under the BSD and zlib licenses, but
# these are OK for inclusion in an Apache 2.0-licensed whole:
# https://www.apache.org/legal/3party.html
 
# Here's the breakdown:
# ./lib/py/compat/win32/stdint.h is 2-clause BSD
# ./compiler/cpp/src/md5.[ch] are zlib
License: Apache-2.0 AND BSD-3-Clause AND Zlib
URL:     https://thrift.apache.org/
 
Source0: https://archive.apache.org/dist/%{name}/%{version}/%{name}-%{version}.tar.gz
 
Source1: https://repo1.maven.org/maven2/org/apache/thrift/lib%{name}/%{version}/lib%{name}-%{version}.pom
Source2: https://raw.github.com/apache/%{name}/%{version}/bootstrap.sh
 
# fix configure.ac insistence on using /usr/local/lib for JAVA_PREFIX
Patch2: configure-java-prefix.patch
 
 
# BuildRequires for language-specific bindings are listed under these
# subpackages, to facilitate enabling or disabling individual language
# bindings in the future

BuildRequires:  pkgconfig(libcrypto)
BuildRequires:python3-six
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
BuildRequires: qt5-qtbase-devel
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
 
%package        qt
Summary:        Qt support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    qt
The %{name}-qt package contains Qt bindings for %{name}.
 
%package        glib
Summary:        GLib support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    glib
The %{name}-qt package contains GLib bindings for %{name}.
 
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
BuildRequires: perl(Bit::Vector)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl-generators
Requires: perl(Bit::Vector)
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
echo 'libthrift_c_glib_la_LIBADD = $(GLIB_LIBS) $(GOBJECT_LIBS) -L../cpp/.libs ' >> lib/c_glib/Makefile.am
echo 'libthriftqt5_la_LIBADD = $(QT_LIBS) -lthrift -L.libs' >> lib/cpp/Makefile.am
echo 'libthriftz_la_LIBADD = $(ZLIB_LIBS) -lthrift -L.libs' >> lib/cpp/Makefile.am
echo 'EXTRA_libthriftqt5_la_DEPENDENCIES = libthrift.la' >> lib/cpp/Makefile.am
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
export GLIB_LIBS=$(pkg-config --libs glib-2.0)
export GLIB_CFLAGS=$(pkg-config --cflags glib-2.0)
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

%check
# Running the test parallely is flaky and hangs the pipeline sometimes. Avoid using `-j` flags
make -k check

%files
%doc LICENSE NOTICE
%{_bindir}/thrift
%{_libdir}/libthrift-%{version}.so
%{_libdir}/libthriftz-%{version}.so
%{_libdir}/libthriftnb-%{version}.so
 
%files glib
%{_libdir}/libthrift_c_glib.so
%{_libdir}/libthrift_c_glib.so.*
 
%files qt
%{_libdir}/libthriftqt5.so
%{_libdir}/libthriftqt5-%{version}.so
 
%files devel
%{_includedir}/thrift
%{_libdir}/*.so
%{_libdir}/*.so.0
%{_libdir}/*.so.0.0.0
%exclude %{_libdir}/lib*-%{version}.so
%{_libdir}/pkgconfig/thrift-z.pc
%{_libdir}/pkgconfig/thrift-qt5.pc
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