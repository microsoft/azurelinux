Vendor:         Microsoft Corporation
Distribution:   Azure Linux

#
# spec file for package apache-commons-compress
#
# Copyright (c) 2024 SUSE LLC
#

%global base_name       compress
%global short_name      commons-%{base_name}
Name:           apache-%{short_name}
Version:        1.26.1
Release:        1%{?dist}
Summary:        Java API for working with compressed files and archivers
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-compress/
Source0:        https://archive.apache.org/dist/commons/compress/source/%{short_name}-%{version}-src.tar.gz
Source1:        %{name}-build.xml
Patch0:         0001-Remove-Brotli-compressor.patch
Patch1:         0002-Remove-ZSTD-compressor.patch
Patch2:         0003-Remove-Pack200-compressor.patch
BuildRequires:  ant
BuildRequires:  commons-codec
BuildRequires:  commons-io >= 2.14
BuildRequires:  commons-lang3
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap >= 6
BuildRequires:  xz-java
BuildRequires:  xml-commons-apis
BuildRequires:  javapackages-tools

Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}-%{release}
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
BuildArch:      noarch

%description
The Apache Commons Compress library defines an API for working with
ar, cpio, Unix dump, tar, zip, gzip, XZ, Pack200 and bzip2 files.
In version 1.14 read-only support for Brotli decompression has been added,
but it has been removed from this package.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE1} build.xml

# Unavailable Google Brotli library (org.brotli.dec)
%patch -P 0 -p1
%pom_remove_dep org.brotli:dec
rm -r src/{main,test}/java/org/apache/commons/compress/compressors/brotli

# Unavailable ZSTD JNI library
%patch -P 1 -p1
%pom_remove_dep :zstd-jni
rm -r src/{main,test}/java/org/apache/commons/compress/compressors/zstandard

# Remove support for pack200 which depends on ancient asm:asm:3.2
%patch -P 2 -p1
rm -r src/{main,test}/java/org/apache/commons/compress/harmony
rm -r src/main/java/org/apache/commons/compress/compressors/pack200
rm src/main/java/org/apache/commons/compress/java/util/jar/Pack200.java
rm -r src/test/java/org/apache/commons/compress/compressors/pack200
rm src/test/java/org/apache/commons/compress/java/util/jar/Pack200Test.java

# NPE with jdk10
%pom_remove_plugin :maven-javadoc-plugin

%pom_xpath_remove "pom:profiles/pom:profile[pom:id[text()='java9+']]"

%build
mkdir -p lib
build-jar-repository -s lib xz-java commons-io commons-codec commons-lang3
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
# Remove LICENSE from javadoc directory to avoid duplicate license warning
mv %{buildroot}%{_javadocdir}/%{name}/legal/ADDITIONAL_LICENSE_INFO .
mv %{buildroot}%{_javadocdir}/%{name}/legal/LICENSE .

%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%{_javadir}/%{name}.jar
%license LICENSE.txt
%license ADDITIONAL_LICENSE_INFO
%license NOTICE.txt

%files javadoc
%{_javadocdir}/%{name}
%license LICENSE.txt
%license NOTICE.txt
%exclude /usr/share/doc/apache-commons-compress-javadoc/NOTICE.txt
%exclude /usr/share/doc/apache-commons-compress/NOTICE.txt

%changelog
* Fri Nov 21 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.26.1-1
- Upgrade from openSUSE Tumbleweed.
- License verified

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
