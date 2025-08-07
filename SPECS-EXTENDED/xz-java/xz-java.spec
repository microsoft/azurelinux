Vendor:         Microsoft Corporation
Distribution:   Azure Linux

#
# spec file for package xz-java
#
# Copyright (c) 2024 SUSE LLC
# Copyright (c) 2013 Peter Conrad
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

Name:           xz-java
Version:        1.10
Release:        1%{?dist}
Summary:        Pure Java implementation of XZ compression
License:        0BSD
Group:          Development/Libraries/Java
URL:            https://tukaani.org/xz/java.html
Source:         https://tukaani.org/xz/xz-java-%{version}.zip
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap >= 6
BuildRequires:  unzip

Obsoletes:      java-xz < %{version}
Provides:       java-xz = %{version}

BuildArch:      noarch

%description
This is an implementation of XZ data compression in pure Java.
Single-threaded streamed compression and decompression and random access
decompression have been implemented.

%package javadoc
Summary:        API documentation of Java XZ compression library
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation of xz-java.

%prep
%setup -q -c -n %{name}

%build
sed -i 's/linkoffline="[^"]*"//;/extdoc_/d' build.xml
ant  -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 clean jar doc maven

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 build/maven/xz-%{version}.jar  %{buildroot}%{_javadir}/%{name}.jar
(cd %{buildroot}%{_javadir} && ln -s %{name}.jar xz.jar)
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 build/maven/xz-%{version}.pom %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/doc/* %{buildroot}%{_javadocdir}/%{name}
# remove duplicated license files from javadoc
rm -f %{buildroot}%{_javadocdir}/%{name}/legal/LICENSE
rm -f %{buildroot}%{_javadocdir}/%{name}/legal/ADDITIONAL_LICENSE_INFO

%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license COPYING
%doc NEWS.md README.md THANKS.md
%{_javadir}/xz.jar

%files javadoc
%exclude %{_javadocdir}/%{name}/legal/LICENSE
%exclude %{_javadocdir}/%{name}/legal/ADDITIONAL_LICENSE_INFO
%{_javadocdir}/%{name}

%changelog
* Tue May 20 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.10-1
- Initial Azure Linux import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified

-------------------------------------------------------------------
Fri Aug  2 15:55:10 UTC 2024 - Anton Shvetz <shvetz.anton@gmail.com>

- Update to version 1.10
  * Licensing change: From version 1.10 onwards, XZ for Java is
    under the BSD Zero Clause License (0BSD). 1.9 and older are in
    the public domain and obviously remain so; the change only
    affects the new releases.
    0BSD is an extremely permissive license which doesn't require
    retaining or reproducing copyright or license notices when
    distributing the code, thus in practice there is extremely
    little difference to public domain.
  * Mark copyright and license information in the source package so
    that it is compliant to the REUSE Specification version 3.2.
  * Improve LZMAInputStream.enableRelaxedEndCondition():
    + Error detection is slightly better.
    + The input position will always be at the end of the stream
      after successful decompression.
  * Support .lzma files that have both a known uncompressed size
    and the end marker. Such files are uncommon but valid. The same
    issue was fixed in XZ Utils 5.2.6 in 2022.
  * Add ARM64 and RISC-V BCJ filters.
  * Speed optimizations:
    + Delta filter
    + LZMA/LZMA2 decoder
    + LZMA/LZMA2 encoder (partially Java >= 9 only)
    + CRC64 (Java >= 9 only)
  * Changes that affect API/ABI compatibility:
    + Change XZOutputStream constructors to not call the method
      public void updateFilters(FilterOptions[] filterOptions).
    + In SeekableXZInputStream, change the method public void
      seekToBlock(int blockNumber) to not call the method public
      long getBlockPos(int blockNumber).
    + Make the filter options classes final:
      ~ ARM64Options
      ~ ARMOptions
      ~ ARMThumbOptions
      ~ DeltaOptions
      ~ IA64Options
      ~ LZMA2Options
      ~ PowerPCOptions
      ~ RISCVOptions
      ~ SPARCOptions
      ~ X86Options
  * Add new system properties:
    + org.tukaani.xz.ArrayCache sets the default ArrayCache: Dummy
      (default) or Basic. See the documentation of ArrayCache and
      BasicArrayCache.
    + org.tukaani.xz.MatchLengthFinder (Java >= 9 only) sets the
      byte array comparison method used for finding match lengths
      in LZMA/LZMA2 encoder: UnalignedLongLE (default on x86-64 and
      ARM64) or Basic (default on other systems). The former could
      be worth testing on other 64-bit little endian systems that
      support fast unaligned memory access.
  * Build system (Apache Ant):
    + Building the documentation no longer downloads element-list
      or package-list file; the build is now fully offline. Such
      files aren't needed with OpenJDK >= 16 whose javadoc can
      auto-link to platform documentation on docs.oracle.com. With
      older OpenJDK versions, links to platform documentation
      aren't generated anymore.
    + Don't require editing of build.properties to build with
      OpenJDK 8. Now it's enough to use ant -Djava8only=true. Older
      OpenJDK versions are no longer supported because the main
      source tree uses Java 8 features.
    + Support reproducible builds. See the notes in README.md.
    + Add a new Ant target pom that only creates xz.pom.
    + Change ant dist to use git archive to create a .zip file.
  * Convert the plain text documentation in the source tree to
    Markdown (CommonMark).
  * The binaries of 1.10 in the Maven Central require Java 8 and
    contain optimized classes for Java >= 9 as multi-release JAR.
    They were built with OpenJDK 21.0.4 on GNU/Linux using the
    following command:
    SOURCE_DATE_EPOCH=1722262226 TZ=UTC0 ant maven

-------------------------------------------------------------------
Thu Sep 21 06:43:05 UTC 2023 - Fridrich Strba <fstrba@suse.com>

- Build with java source/target levels 8

-------------------------------------------------------------------
Mon Dec 12 19:32:21 UTC 2022 - Anton Shvetz <shvetz.anton@gmail.com>

- Update to version 1.9
  * Release notes at /usr/share/doc/packages/xz-java/NEWS
- Remove obsolete patch:
  * xz-java-source-version.patch

-------------------------------------------------------------------
Wed Feb 13 12:27:36 UTC 2019 - Klaus Kämpf <kkaempf@suse.com>

- add provides/obsoletes for xz-java (boo#1125298)

-------------------------------------------------------------------
Sat Jan 26 12:01:16 UTC 2019 - Jan Engelhardt <jengelh@inai.de>

- Trim future goals from description.

-------------------------------------------------------------------
Wed Jan  9 08:43:32 UTC 2019 - Fridrich Strba <fstrba@suse.com>

- Modified patch:
  * java-3d_source_version.patch -> xz-java-source-version.patch
    + change name to correspond to reality

-------------------------------------------------------------------
Sat Oct 27 19:12:19 UTC 2018 - Fridrich Strba <fstrba@suse.com>

- renamed package to xz-java

-------------------------------------------------------------------
Tue Oct 23 19:26:13 UTC 2018 - Fridrich Strba <fstrba@suse.com>

- Update to 1.8
- Modified patch:
  * java-3d_source_version.patch
    - Rediff to changed context

-------------------------------------------------------------------
Mon Oct 22 12:45:47 UTC 2018 - Fridrich Strba <fstrba@suse.com>

- Generate the maven pom files and install them

-------------------------------------------------------------------
Sat May  3 00:05:11 UTC 2014 - ecsos@opensuse.org

- update to 1.5

-------------------------------------------------------------------
Mon Nov 11 15:52:00 UTC 2013 - robertherb@arcor.de.de
- Update to 1.4
- renamed package to java-xz

-------------------------------------------------------------------
Sat Aug 31 15:52:00 UTC 2013 - conrad@quisquis.de
- Fixed Source header

-------------------------------------------------------------------
Sat Aug 31 10:24:00 UTC 2013 - conrad@quisquis.de
- Upgrade to 1.3

-------------------------------------------------------------------
Fri Apr  5 17:15:00 UTC 2013 - conrad@quisquis.de
- Fixed fedora build deps
- Fixed license string

-------------------------------------------------------------------
Thu Mar 28 13:51:00 UTC 2013 - conrad@quisquis.de
- Disabled external links in javadoc

-------------------------------------------------------------------
Thu Mar 28 13:28:00 UTC 2013 - conrad@quisquis.de
- Disabled download_files service - upstream server hangs

-------------------------------------------------------------------
Thu Mar 28 13:01:00 UTC 2013 - conrad@quisquis.de
- Initial project creation
