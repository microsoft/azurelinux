# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Build -python subpackage
%bcond_without python
# Build -python subpackage with C++. This significantly improves performance
# compared to the pure-Python implementation.
%if v"0%{?python3_version}" >= v"3.14"
# TypeError: Metaclasses with custom tp_new are not supported
# https://bugzilla.redhat.com/show_bug.cgi?id=2343969
%bcond_with python_cpp
%else
%bcond_without python_cpp
%endif
# Build -java subpackage
%if %{defined rhel}
%bcond_with java
%else
%bcond_without java
%endif

#global rcver rc2

Summary:        Protocol Buffers - Google's data interchange format
Name:           protobuf
# NOTE: perl-Alien-ProtoBuf has an exact-version dependency on the version of
# protobuf with which it was built; it therefore needs to be rebuilt even for
# “patch” updates of protobuf.
Version:        3.19.6
%global so_version 30
Release:        19%{?dist}

# The entire source is BSD-3-Clause, except the following files, which belong
# to the build system; are unpackaged maintainer utility scripts; or are used
# only for building tests that are not packaged—and so they do not affect the
# licenses of the binary RPMs:
#
# FSFAP:
#   m4/ax_cxx_compile_stdcxx.m4
#   m4/ax_prog_cc_for_build.m4
#   m4/ax_prog_cxx_for_build.m4
# Apache-2.0:
#   python/mox.py
#   python/stubout.py
#   third_party/googletest/
#     except the following, which are BSD-3-Clause:
#       third_party/googletest/googletest/test/gtest_pred_impl_unittest.cc
#       third_party/googletest/googletest/include/gtest/gtest-param-test.h
#       third_party/googletest/googletest/include/gtest/gtest-param-test.h.pump
#       third_party/googletest/googletest/include/gtest/internal/gtest-param-util-generated.h
#       third_party/googletest/googletest/include/gtest/internal/gtest-param-util-generated.h.pump
#       third_party/googletest/googletest/include/gtest/internal/gtest-type-util.h
#       third_party/googletest/googletest/include/gtest/internal/gtest-type-util.h.pump
# MIT:
#   conformance/third_party/jsoncpp/json.h
#   conformance/third_party/jsoncpp/jsoncpp.cpp
License:        BSD-3-Clause
URL:            https://github.com/protocolbuffers/protobuf
Source0:        %{url}/archive/v%{version}%{?rcver}/protobuf-%{version}%{?rcver}-all.tar.gz

Source1:        ftdetect-proto.vim
Source2:        protobuf-init.el

# We bundle a copy of the exact version of gtest that is used by upstream in
# the source RPM rather than using the system copy. This is to be discouraged,
# but necessary in this case.  It is not treated as a bundled library because
# it is used only at build time, and contributes nothing to the installed
# files.  We take measures to verify this in %%check. See
# https://github.com/protocolbuffers/protobuf/tree/v%%{version}/third_party to
# check the correct commit hash.
%global gtest_url https://github.com/google/googletest
%global gtest_commit 5ec7f0c4a113e2f18ac2c6cc7df51ad6afc24081
%global gtest_dir googletest-%{gtest_commit}
# For tests (using exactly the same version as the release)
Source3:        %{gtest_url}/archive/%{gtest_commit}/%{gtest_dir}.tar.gz

# Man page hand-written for Fedora in groff_man(7) format based on “protoc
# --help” output.
Source4:        protoc.1

# https://github.com/protocolbuffers/protobuf/issues/8082
Patch1:         protobuf-3.14-disable-IoTest.LargeOutput.patch
# Disable tests that are failing on 32bit systems
Patch2:         disable-tests-on-32-bit-systems.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2051202
# java.lang.ClassLoader.defineClass(java.lang.String,byte[],int,int,java.security.ProtectionDomain)
# throws java.lang.ClassFormatError accessible: module java.base does not "opens java.lang" to unnamed module @12d5624a
#	at com.google.protobuf.ServiceTest.testGetPrototype(ServiceTest.java:107)
Patch3:         protobuf-3.19.4-jre17-add-opens.patch
# Backport upstream commit da973aff2adab60a9e516d3202c111dbdde1a50f:
#   Fix build with Python 3.11
#
#   The PyFrameObject structure members have been removed from the public C API.
Patch4:         protobuf-3.19.4-python3.11.patch
# Backport upstream commit 9252b64ef3887e869999752010d553f068338a60:
#   Automated rollback of commit 0ee34de
Patch5:         protobuf-3.19.6-jre21.patch
# Fix build with GCC 15 on s390x and i686
# From https://bugzilla.redhat.com/show_bug.cgi?id=2343969#c16
#  and https://github.com/protocolbuffers/protobuf/commit/47c1998e4e7f21175bc1e3840907d4219a11b25a
#  and https://github.com/protocolbuffers/protobuf/commit/a2859cc2ce25711613002104022186c0c37d9f1f
Patch6:         protobuf-3.19.6-gcc15.patch

# A bundled copy of jsoncpp is included in the conformance tests, but the
# result is not packaged, so we do not treat it as a formal bundled
# dependency—thus the virtual Provides below is commented out. The bundling is
# removed in a later release:
#   Make jsoncpp a formal dependency
#   https://github.com/protocolbuffers/protobuf/pull/10739
# The bundled version number is obtained from JSONCPP_VERSION_STRING in
# conformance/third_party/jsoncpp/json.h.
# Provides:       bundled(jsoncpp) = 1.6.5

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

BuildRequires:  make
BuildRequires:  gcc-c++

BuildRequires:  emacs
BuildRequires:  zlib-devel

%if %{with java}
%ifnarch %{java_arches}
Obsoletes:      protobuf-java-util < 3.19.4-4
Obsoletes:      protobuf-javadoc < 3.19.4-4
Obsoletes:      protobuf-parent < 3.19.4-4
Obsoletes:      protobuf-bom < 3.19.4-4
Obsoletes:      protobuf-javalite < 3.19.4-4
%endif
%endif

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package compiler
Summary:        Protocol Buffers compiler
Requires:       protobuf = %{version}-%{release}

%description compiler
This package contains Protocol Buffers compiler for all programming
languages

%package devel
Summary:        Protocol Buffers C++ headers and libraries
Requires:       protobuf = %{version}-%{release}
Requires:       protobuf-compiler = %{version}-%{release}
Requires:       zlib-devel

Obsoletes:      protobuf-static < 3.19.6-4

%description devel
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries

%package lite
Summary:        Protocol Buffers LITE_RUNTIME libraries

%description lite
Protocol Buffers built with optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-devel
Summary:        Protocol Buffers LITE_RUNTIME development libraries
Requires:       protobuf-devel = %{version}-%{release}
Requires:       protobuf-lite = %{version}-%{release}

Obsoletes:      protobuf-lite-static < 3.19.6-4

%description lite-devel
This package contains development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%if %{with python}
%package -n python3-protobuf
Summary:        Python bindings for Google Protocol Buffers
BuildRequires:  python3-devel
%if %{with python_cpp}
Requires:       protobuf%{?_isa} = %{version}-%{release}
%else
BuildArch:      noarch
%endif
Conflicts:      protobuf-compiler > %{version}
Conflicts:      protobuf-compiler < %{version}
Provides:       protobuf-python3 = %{version}-%{release}

%description -n python3-protobuf
This package contains Python libraries for Google Protocol Buffers
%endif

%package vim
Summary:        Vim syntax highlighting for Google Protocol Buffers descriptions
BuildArch:      noarch
# We don’t really need vim or vim-enhanced to be already installed in order to
# install a plugin for it. We do need to depend on vim-filesystem, which
# provides the necessary directory structure.
Requires:       vim-filesystem

%description vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor


%if %{with java}
%ifarch %{java_arches}

%package java
Summary:        Java Protocol Buffers runtime library
BuildArch:      noarch
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.google.code.gson:gson)
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(com.google.guava:guava-testlib)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.easymock:easymock)
Conflicts:      protobuf-compiler > %{version}
Conflicts:      protobuf-compiler < %{version}
Obsoletes:      protobuf-javanano < 3.6.0

%description java
This package contains Java Protocol Buffers runtime library.

%package javalite
Summary:        Java Protocol Buffers lite runtime library
BuildArch:      noarch

%description javalite
This package contains Java Protocol Buffers lite runtime library.

%package java-util
Summary:        Utilities for Protocol Buffers
BuildArch:      noarch

%description java-util
Utilities to work with protos. It contains JSON support
as well as utilities to work with proto3 well-known types.

%package javadoc
Summary:        Javadoc for protobuf-java
BuildArch:      noarch

%description javadoc
This package contains the API documentation for protobuf-java.

%package parent
Summary:        Protocol Buffer Parent POM
BuildArch:      noarch

%description parent
Protocol Buffer Parent POM.

%package bom
Summary:        Protocol Buffer BOM POM
BuildArch:      noarch

%description bom
Protocol Buffer BOM POM.

%endif
%endif

%package emacs
Summary:        Emacs mode for Google Protocol Buffers descriptions
BuildArch:      noarch
Requires:       emacs-filesystem >= %{_emacs_version}
Obsoletes:      protobuf-emacs-el < 3.6.1-4

%description emacs
This package contains syntax highlighting for Google Protocol Buffers
descriptions in the Emacs editor.

%prep
%setup -q -n protobuf-%{version}%{?rcver} -a 3
%ifarch %{ix86}
# IoTest.LargeOutput fails on 32bit arches
# https://github.com/protocolbuffers/protobuf/issues/8082
%patch 1 -p1
# Need to disable more tests that fail on 32bit arches only
%patch 2 -p0
%endif
%patch 3 -p1 -b .jre17
%patch 4 -p1 -b .python311
%patch 5 -p1 -b .jre21
%patch 6 -p1 -b .gcc15

# Copy in the needed gtest/gmock implementations.
%setup -q -T -D -b 3 -n protobuf-%{version}%{?rcver}
rm -rvf 'third_party/googletest'
mv '../%{gtest_dir}' 'third_party/googletest'

find -name \*.cc -o -name \*.h | xargs chmod -x
chmod 644 examples/*
%if %{with java}
%ifarch %{java_arches}
%pom_remove_dep com.google.errorprone:error_prone_annotations java/util/pom.xml
%pom_remove_dep com.google.j2objc:j2objc-annotations java/util/pom.xml
%pom_remove_dep com.google.truth:truth java/pom.xml java/{core,lite,util}/pom.xml

# Remove annotation libraries we don't have
annotations=$(
    find -name '*.java' |
      xargs grep -h -e '^import com\.google\.errorprone\.annotation' \
                    -e '^import com\.google\.j2objc\.annotations' |
      sort -u | sed 's/.*\.\([^.]*\);/\1/' | paste -sd\|
)
find -name '*.java' | xargs sed -ri \
    "s/^import .*\.($annotations);//;s/@($annotations)"'\>\s*(\((("[^"]*")|([^)]*))\))?//g'

# Make OSGi dependency on sun.misc package optional
%pom_xpath_inject "pom:configuration/pom:instructions" "<Import-Package>sun.misc;resolution:=optional,*</Import-Package>" java/core

# Backward compatibility symlink
%mvn_file :protobuf-java:jar: protobuf/protobuf-java protobuf
%endif
%endif

rm -f src/solaris/libstdc++.la

%generate_buildrequires
cd python
%pyproject_buildrequires

%build
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"
./autogen.sh
%configure --disable-static

# -Wno-error=type-limits:
#     https://bugzilla.redhat.com/show_bug.cgi?id=1838470
#     https://github.com/protocolbuffers/protobuf/issues/7514
#     https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95148
#  (also set in %%check)
%make_build CXXFLAGS="%{build_cxxflags} -Wno-error=type-limits"

%if %{with python}
pushd python
%pyproject_wheel %{?with_python_cpp:-C--global-option=--cpp_implementation}
popd
%endif

%if %{with java}
%ifarch %{java_arches}
%ifarch %{ix86} s390x
export MAVEN_OPTS=-Xmx1024m
%endif
%pom_disable_module kotlin java/pom.xml
%pom_disable_module kotlin-lite java/pom.xml
# tests require com.google.truth:truth even to build
%mvn_build -s -- -f java/pom.xml -Dmaven.test.skip=true
%endif
%endif

%{_emacs_bytecompile} editors/protobuf-mode.el


%check
%make_build check CXXFLAGS="%{build_cxxflags} -Wno-error=type-limits"
%if %{with python_cpp}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%endif
%pyproject_check_import -e '*json_format_proto3_pb2' %{!?with_python_cpp:-e '*.pyext*'}


%install
%make_install %{?_smp_mflags} STRIPBINARIES=no INSTALL="%{__install} -p" CPPROG="cp -p"
find %{buildroot} -type f -name "*.la" -exec rm -f {} +

# protoc.1 man page
install -p -m 0644 -D -t '%{buildroot}%{_mandir}/man1' '%{SOURCE4}'

%if %{with python}
pushd python
%pyproject_install
%pyproject_save_files -L google
%if %{without python_cpp}
find %{buildroot}%{python3_sitelib} -name \*.py -exec sed -i -e '1{\@^#!@d}' {} +
%endif
popd
%endif
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with java}
%ifarch %{java_arches}
%mvn_install
%endif
%endif

mkdir -p %{buildroot}%{_emacs_sitelispdir}/protobuf
install -p -m 0644 editors/protobuf-mode.el %{buildroot}%{_emacs_sitelispdir}/protobuf
install -p -m 0644 editors/protobuf-mode.elc %{buildroot}%{_emacs_sitelispdir}/protobuf
mkdir -p %{buildroot}%{_emacs_sitestartdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_emacs_sitestartdir}

%files
%doc CHANGES.txt CONTRIBUTORS.txt README.md
%license LICENSE
%{_libdir}/libprotobuf.so.%{so_version}{,.*}

%files compiler
%doc README.md
%license LICENSE
%{_bindir}/protoc
%{_mandir}/man1/protoc.1*
%{_libdir}/libprotoc.so.%{so_version}{,.*}

%files devel
%dir %{_includedir}/google
%{_includedir}/google/protobuf/
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc
%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/Makefile examples/README.md

%files emacs
%license LICENSE
%{_emacs_sitelispdir}/protobuf/
%{_emacs_sitestartdir}/protobuf-init.el

%files lite
%license LICENSE
%{_libdir}/libprotobuf-lite.so.%{so_version}{,.*}

%files lite-devel
%{_libdir}/libprotobuf-lite.so
%{_libdir}/pkgconfig/protobuf-lite.pc

%if %{with python}
%files -n python3-protobuf -f %{pyproject_files}
%if %{with python_cpp}
%{python3_sitearch}/protobuf-%{version}%{?rcver}-py3.*-nspkg.pth
%else
%{python3_sitelib}/protobuf-%{version}%{?rcver}-py3.*-nspkg.pth
%endif
%license LICENSE
%doc python/README.md
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%endif

%files vim
%license LICENSE
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with java}
%ifarch %{java_arches}

%files java -f .mfiles-protobuf-java
%doc examples/AddPerson.java examples/ListPeople.java
%doc java/README.md
%license LICENSE

%files java-util -f .mfiles-protobuf-java-util
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%files parent -f .mfiles-protobuf-parent
%license LICENSE

%files bom -f .mfiles-protobuf-bom
%license LICENSE

%files javalite -f .mfiles-protobuf-javalite
%license LICENSE

%endif
%endif


%changelog
* Sun Sep 28 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 3.19.6-19
- Rebuilt for java-25-openjdk as system jdk

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.19.6-18
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.19.6-17
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Jul 29 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 3.19.6-16
- Convert to pyproject macros

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 17 2025 Miro Hrončok <mhroncok@redhat.com> - 3.19.6-14
- Build with recent GCC

* Tue Jun 17 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.19.6-13
- Temporarily use GCC 14 to workaround FTBFS on i686 and s390x
- Don’t build Python extension with C++ on Python 3.14+

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.19.6-12
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.19.6-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.19.6-5
- Rebuilt for Python 3.12

* Wed Apr 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 3.19.6-4
- Stop packaging static libraries
- Stop using deprecated %%patchN syntax

* Tue Apr 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 3.19.6-3
- Remove unnecessary explicit pkgconfig dependencies
- Remove an obsolete workaround for failing Java tests
- Remove conditionals for retired 32-bit ARM architecture
- Remove a slow-test workaround on s390x
- Reduce macro indirection in the spec file

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.19.6-1
- Update to 3.19.6; fix CVE-2022-3171

* Wed Dec 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.19.5-1
- Update to 3.19.5; fix CVE-2022-1941

* Sun Dec 04 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.19.4-7
- Update License to SPDX
- Improved handling of gtest sources
- Update/correct gtest commit hash to match upstream
- Simplify the Source0 URL with a macro
- Drop manual dependency on python3-six, no longer needed
- Drop obsolete python_provide macro
- Drop python3_pkgversion macro
- Update summary and description to refer to “Python” instead of “Python 3”
- Re-enable compiled Python extension on Python 3.11
- Ensure all subpackages always have LICENSE, or depend on something that does
- Remove obsolete ldconfig_scriptlets macros
- The -vim subpackage now depends on vim-filesystem, no longer on vim-enhanced
- Add a man page for protoc
- Use a macro to avoid repeating the .so version, and improve .so globs

* Sun Aug 14 2022 Orion Poplawski <orion@nwra.com> - 3.19.4-6
- Build python support with C++ (bz#2107921)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.19.4-4
- Exclude java subpackages on non-java arches (fix RHBZ#2104092)
- Obsolete java subpackages on non-java arches

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.19.4-3
- Rebuilt for Python 3.11

* Sun Feb 13 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.19.4-2
- Add some --add-opens option for java17
- Restrict heap usage for mvn also on %%ix86

* Mon Feb 07 2022 Orion Poplawski <orion@nwra.com> - 3.19.4-1
- Update to 3.19.4

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 3.19.0-4
- Rebuilt for java-17-openjdk as system jdk

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 10 2021 Orion Poplawski <orion@nwra.com> - 3.19.0-2
- Re-enable java

* Wed Oct 27 2021 Major Hayden <major@mhtx.net> - 3.19.0-1
- Update to 3.19.1

* Fri Oct 22 2021 Adrian Reber <adrian@lisas.de> - 3.18.1-2
- Disable tests that fail on 32bit arches

* Thu Oct 14 2021 Orion Poplawski <orion@nwra.com> - 3.18.1-1
- Update to 3.18.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.14.0-5
- Rebuilt for Python 3.10

* Thu May 06 2021 Adrian Reber <adrian@lisas.de> - 3.14.0-4
- Reintroduce the emacs subpackage to avoid file conflicts between
  protobuf-compiler.x86_64 and protobuf-compiler.i686

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 3.14.0-3
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Adrian Reber <adrian@lisas.de> - 3.14.0-1
- Update to 3.14.0

* Wed Aug 26 2020 Charalampos Stratakis <cstratak@redhat.com> - 3.13.0-1
- Update to 3.13.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.3-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 3.12.3-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jun 19 2020 Adrian Reber <adrian@lisas.de> - 3.12.3-2
- Update to 3.12.3

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.11.4-2
- Rebuilt for Python 3.9

* Tue Mar 31 2020 Adrian Reber <adrian@lisas.de> - 3.11.4-1
- Update to 3.11.4

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 Adrian Reber <adrian@lisas.de> - 3.11.2-1
- Update to 3.11.2

* Tue Nov 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-9
- Drop python2-protobuf (#1765879)

* Sat Oct 26 2019 Orion Poplawski <orion@nwra.com> - 3.6.1-8
- Drop obsolete BR on python-google-apputils

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 8 2019 Orion Poplawski <orion@nwra.com> - 3.6.1-4
- Update emacs packaging to comply with guidelines

* Wed Feb 27 2019 Orion Poplawski <orion@nwra.com> - 3.6.1-3
- Update googletest to 1.8.1 to re-enable tests

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 23 2018 Felix Kaechele <heffer@fedoraproject.org> - 3.6.1-1
- update to 3.6.1
- obsolete javanano subpackage; discontinued upstream

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.0-8
- Rebuild for new binutils

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-6
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.5.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.0-4
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.0-2
- Switch to %%ldconfig_scriptlets

* Thu Nov 23 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.0-1
- Update to 3.5.0

* Mon Nov 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.4.1-1
- Update to 3.4.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Mat Booth <mat.booth@redhat.com> - 3.3.1-2
- Make OSGi dependency on sun.misc package optional. This package is not
  available in all execution environments and will not be available in Java 9.

* Mon Jun 12 2017 Orion Poplawski <orion@cora.nwra.com> - 3.3.1-1
- Update to 3.3.1

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Orion Poplawski <orion@cora.nwra.com> - 3.2.0-1
- Update to 3.2.0 final

* Mon Jan 23 2017 Orion Poplawski <orion@cora.nwra.com> - 3.2.0-0.1.rc2
- Update to 3.2.0rc2

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-6
- Rebuild for Python 3.6

* Sat Nov 19 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-5
- Disable slow test on arm

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-4
- Ship python 3 module

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-3
- Fix jar file compat symlink

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-2
- Add needed python requirement

* Fri Nov 04 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-2
- Make various sub-packages noarch

* Fri Nov 04 2016 gil cattaneo <puntogil@libero.it> 3.1.0-2
- enable javanano
- minor changes to adapt to current guidelines

* Fri Nov 04 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-1
- Update to 3.1.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-3
- Tests no longer segfaulting on arm

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 6 2015 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-1
- Update to 2.6.1
- New URL
- Cleanup spec
- Add patch to fix emacs compilation with emacs 24.4
- Drop java-fixes patch, use pom macros instead
- Add BR on python-google-apputils and mvn(org.easymock:easymock)
- Run make check
- Make -static require -devel (bug #1067475)

* Thu Mar 26 2015 Kalev Lember <kalevlember@gmail.com> - 2.6.0-4
- Rebuilt for GCC 5 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.6.0-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Dec 17 2014 Peter Lemenkov <lemenkov@gmail.com> - 2.6.0-2
- Added missing Requires zlib-devel to protobuf-devel (see rhbz #1173343). See
  also rhbz #732087.

* Sun Oct 19 2014 Conrad Meyer <cemeyer@uw.edu> - 2.6.0-1
- Bump to upstream release 2.6.0 (rh# 1154474).
- Rebase 'java fixes' patch on 2.6.0 pom.xml.
- Drop patch #3 (fall back to generic GCC atomics if no specialized atomics
  exist, e.g. AArch64 GCC); this has been upstreamed.

* Sun Oct 19 2014 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-11
- protobuf-emacs requires emacs(bin), not emacs (rh# 1154456)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.0-9
- Update to current Java packaging guidelines

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5.0-7
- Use Requires: java-headless rebuild (#1067528)

* Thu Dec 12 2013 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-6
- BR python-setuptools-devel -> python-setuptools

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Dan Horák <dan[at]danny.cz> - 2.5.0-4
- export the new generic atomics header (rh #926374)

* Mon May 6 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5.0-3
- Add support for generic gcc atomic operations (rh #926374)

* Sat Apr 27 2013 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-2
- Remove changelog history from before 2010
- This spec already runs autoreconf -fi during %%build, but bump build for
  rhbz #926374

* Sat Mar 9 2013 Conrad Meyer <cemeyer@uw.edu> - 2.5.0-1
- Bump to latest upstream (#883822)
- Rebase gtest, maven patches on 2.5.0

* Tue Feb 26 2013 Conrad Meyer <cemeyer@uw.edu> - 2.4.1-12
- Nuke BR on maven-doxia, maven-doxia-sitetools (#915620)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.4.1-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jan 20 2013 Conrad Meyer <konrad@tylerc.org> - 2.4.1-9
- Fix packaging bug, -emacs-el subpackage should depend on -emacs subpackage of
  the same version (%%version), not the emacs version number...

* Thu Jan 17 2013 Tim Niemueller <tim@niemueller.de> - 2.4.1-8
- Added sub-package for Emacs editing mode

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012 Dan Horák <dan[at]danny.cz> - 2.4.1-6
- disable test-suite until g++ 4.7 issues are resolved

* Mon Mar 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4.1-5
- Update to latest java packaging guidelines

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.4.1-2
- Adding zlib-devel as BR (rhbz: #732087)

* Thu Jun 09 2011 BJ Dierkes <wdierkes@rackspace.com> - 2.4.1-1
- Latest sources from upstream.
- Rewrote Patch2 as protobuf-2.4.1-java-fixes.patch

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.0-6
- Fix java subpackage bugs #669345 and #669346
- Use new maven plugin names
- Use mavenpomdir macro for pom installation

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 2.3.0-5
- generalize hardcoded reference to 2.6 in python subpackage %%files manifest

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 15 2010 James Laska <jlaska@redhat.com> - 2.3.0-3
- Correct use of %%bcond macros

* Wed Jul 14 2010 James Laska <jlaska@redhat.com> - 2.3.0-2
- Enable python and java sub-packages

* Tue May 4 2010 Conrad Meyer <konrad@tylerc.org> - 2.3.0-1
- bump to 2.3.0
