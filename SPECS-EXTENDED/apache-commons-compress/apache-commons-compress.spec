Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package apache
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global base_name       compress
%global short_name      commons-%{base_name}
Name:           apache-%{short_name}
Version:        1.19
Release:        3%{?dist}
Summary:        Java API for working with compressed files and archivers
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://commons.apache.org/proper/commons-compress/
Source0:        http://archive.apache.org/dist/commons/compress/source/%{short_name}-%{version}-src.tar.gz
Source1:        http://archive.apache.org/dist/commons/compress/source/%{short_name}-%{version}-src.tar.gz.asc
Source2:        %{name}-build.xml
Patch0:         0001-Remove-Brotli-compressor.patch
Patch1:         0002-Remove-ZSTD-compressor.patch
Patch2:         fix_java_8_compatibility.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.7
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xz-java
Requires:       xz
Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}-%{release}
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
BuildArch:      noarch

%description
The Apache Commons Compress library defines an API for working with
ar, cpio, Unix dump, tar, zip, gzip, XZ, Pack200 and bzip2 files.
In version 1.14 read-only support for Brotli decompression has been added,
but it has been removed form this package.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE2} build.xml

# Unavailable Google Brotli library (org.brotli.dec)
%patch 0 -p1
%pom_remove_dep org.brotli:dec
rm -r src/{main,test}/java/org/apache/commons/compress/compressors/brotli

# Unavailable ZSTD JNI library
%patch 1 -p1
%pom_remove_dep :zstd-jni
rm -r src/{main,test}/java/org/apache/commons/compress/compressors/zstandard
rm src/test/java/org/apache/commons/compress/compressors/DetectCompressorTestCase.java

# Restore Java 8 compatibility
%patch 2 -p1

# remove osgi tests, we don't have deps for them
%pom_remove_dep org.ops4j.pax.exam:::test
%pom_remove_dep :org.apache.felix.framework::test
%pom_remove_dep :javax.inject::test
%pom_remove_dep :slf4j-api::test
rm src/test/java/org/apache/commons/compress/OsgiITest.java

# NPE with jdk10
%pom_remove_plugin :maven-javadoc-plugin

%pom_xpath_remove "pom:profiles/pom:profile[pom:id[text()='java9+']]"

%pom_remove_parent .
%pom_xpath_inject "pom:project" "<groupId>org.apache.commons</groupId>" .

%build
mkdir -p lib
build-jar-repository -s lib xz-java
%{ant} package javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}.jar
ln -sf %{short_name}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{short_name}.pom
%add_maven_depmap %{short_name}.pom %{short_name}.jar -a commons:commons-compress,commons-compress:commons-compress
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%{_javadir}/%{name}.jar
%license LICENSE.txt
%doc NOTICE.txt

%files javadoc
%{_javadocdir}/%{name}
%license LICENSE.txt
%doc NOTICE.txt

%changelog
* Mon Nov 14 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.19-3
- Add Requires on xz instead of mvn(org.tukaani:xz) to fix package install failure
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.19-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.19-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Aug 28 2019 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Updated to 1.19 [bsc#1148475, CVE-2019-12402]
  * ZipFile could get stuck in an infinite loop when parsing ZIP archives
    with certain strong encryption headers (CVE-2019-12402).
  * ZipArchiveInputStream and ZipFile will no longer throw an exception if
    an extra field generally understood by Commons Compress is malformed
    but rather turn them into UnrecognizedExtraField instances.  You can
    influence the way extra fields are parsed in more detail by using the
    new getExtraFields(ExtraFieldParsingBehavior) method of ZipArchiveEntry now.
  * Some of the ZIP extra fields related to strong encryption will now
    throw ZipExceptions rather than ArrayIndexOutOfBoundsExceptions in
    certain cases when used directly. There is no practical difference
    when they are read via ZipArchiveInputStream or ZipFile.
  * ParallelScatterZipCreator now writes entries in the same order they have
    been added to the archive.
  * ZipArchiveInputStream and ZipFile are more forgiving when parsing extra
    fields by default now.
  * TarArchiveInputStream has a new lenient mode that may allow it to read
    certain broken archives.
- Rebased patch fix_java_8_compatibility.patch
* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
* Sun Jan 27 2019 Jan Engelhardt <jengelh@inai.de>
- Add missing RPM group for %%name-javadoc.
* Fri Jan 25 2019 Fridrich Strba <fstrba@suse.com>
- Rename package to apache-commons-compress
  * Upgrade to version 1.18
  * Use build.xml file generated ba mvn ant:ant and simplified
    manually after
    + Allows building with ant and considerably shortens build
    cycle
- Added patches
  * 0001-Remove-Brotli-compressor.patch
    + do not build Brotli compressor, since we don't have its
    dependencies
  * 0002-Remove-ZSTD-compressor.patch
    + do not build ZSTD compressor, since we don't have its
    dependencies
  * fix_java_8_compatibility.patch
    + restore Java 8 compatibility in java.nio.ByteBuffer use
* Mon Sep 18 2017 fstrba@suse.com
- Fix build with jdk9: specify java source and target 1.6
- Build also the javadoc package
* Fri May 19 2017 tchvatal@suse.com
- Fix build under new javapackage-tools
* Thu Nov 29 2012 mvyskocil@suse.com
- use saxon and saxon-scripts only when using maven
* Thu May 14 2009 mvyskocil@suse.cz
- 'Initial SUSE packaging from jpackage.org 5.0'
