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
%doc NOTICE.txt

%files javadoc
%{_javadocdir}/%{name}
%license LICENSE.txt
%doc NOTICE.txt
%exclude /usr/share/doc/apache-commons-compress-javadoc/NOTICE.txt
%exclude /usr/share/doc/apache-commons-compress/NOTICE.txt

%changelog
* Fri Nov 21 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.26.1-1
- Initial Azure Linux import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified

* Tue May 14 2024 Fridrich Strba <fstrba@suse.com>
- Upgrade to 1.26.1
  * Fixed Bugs
    + COMPRESS-659: TarArchiveOutputStream should use Commons IO
    Charsets instead of Commons Codec Charsets.
    + COMPRESS-660: Add org.apache.commons.codec to OSGi imports.
    + COMPRESS-664 Return null value from getNextEntry() for empty
    file.
    + COMPRESS-664: Remove unused variables in tests.
    + COMPRESS-666: Multithreaded access to Tar archive throws
    java.util.zip.ZipException: Corrupt GZIP trailer.
    + COMPRESS-644: ArchiveStreamFactory.detect(InputStream) returns
    TAR for ICO file.
    + COMPRESS-661: ArchiveInputStream markSupported should always
    return false.
    + COMPRESS-662: Remove out of date jar and scripts.
* Tue Feb 20 2024 Dominique Leuenberger <dimstar@opensuse.org>
- Use %%patch -P N instead of deprecated %%patchN.
* Mon Feb 19 2024 Fridrich Strba <fstrba@suse.com>
- Upgrade to 1.26
  * Fixing several vulnerabilities
    + bsc#1220068, CVE-2024-26308
    + bsc#1220070, CVE-2024-25710
  * New Features
    + Add and use ZipFile.builder(), ZipFile.Builder, and deprecate
    constructors
    + Add and use SevenZFile.builder(), SevenZFile.Builder, and
    deprecate constructors
    + Add and use ArchiveInputStream.getCharset()
    + Add and use ArchiveEntry.resolveIn(Path)
    + Add Maven property project.build.outputTimestamp for build
    reproducibility
  * Fixed Bugs
    + COMPRESS-632: Check for invalid PAX values in TarArchiveEntry
    + COMPRESS-632: Fix for zero size headers in ArjInputStream
    + COMPRESS-632: Fixes and tests for ArInputStream
    + COMPRESS-632: Fixes for dump file parsing
    + COMPRESS-632: Improve CPIO exception detection and handling
    + Deprecate SkipShieldingInputStream without replacement (no
    longer used)
    + Reuse commons-codec, don't duplicate class PureJavaCrc32C
    (removed package-private class)
    + Reuse commons-codec, don't duplicate class XXHash32
    (deprecated class)
    + Reuse commons-io, don't duplicate class Charsets (deprecated
    class)
    + Reuse commons-io, don't duplicate class IOUtils (deprecated
    methods)
    + Reuse commons-io, don't duplicate class BoundedInputStream
    (deprecated class)
    + Reuse commons-io, don't duplicate class FileTimes (deprecated
    TimeUtils methods)
    + Reuse Arrays.equals(byte[], byte[]) and deprecate
    ArchiveUtils.isEqual(byte[], byte[])
    + Add a null-check for the class loader of OsgiUtils
    + Add a null-check in Pack200.newInstance(String, String)
    + Deprecate ChecksumCalculatingInputStream in favor of
    java.util.zip.CheckedInputStream
    + Deprecate CRC32VerifyingInputStream
    .CRC32VerifyingInputStream(InputStream, long, int)
    + COMPRESS-655: FramedSnappyCompressorOutputStream produces
    incorrect output when writing a large buffer
    + COMPRESS-657: Fix TAR directory entries being misinterpreted
    as files
    + Deprecate unused method FileNameUtils.getBaseName(String)
    + Deprecate unused method FileNameUtils.getExtension(String)
    + ArchiveInputStream.BoundedInputStream.read() incorrectly adds
    1 for EOF to the bytes read count
    + Deprecate IOUtils.read(File, byte[])
    + Deprecate IOUtils.copyRange(InputStream, long, OutputStream,
    int)
    + COMPRESS-653: ZipArchiveOutputStream multi archive updates
    metadata in incorrect file
    + Deprecate ByteUtils.InputStreamByteSupplier
    + Deprecate ByteUtils.fromLittleEndian(InputStream, int)
    + Deprecate ByteUtils.toLittleEndian(DataOutput, long, int)
    + Reduce duplication by having ArchiveInputStream extend
    FilterInputStream
    + Support preamble garbage in ZipArchiveInputStream
    + COMPRESS-658: Fix formatting the lowest expressable DOS time
    + Drop reflection from ExtraFieldUtils static initialization
    + Preserve exception causation in
    ExtraFieldUtils.register(Class)
- Upgrade to 1.25.0
  * New features:
    + Add GzipParameters.getFileName() and deprecate getFilename()
    + Add GzipParameters.setFileName(String) and deprecate
    setFilename(String)
    + Add FileNameUtil.getCompressedFileName(String) and deprecate
    getCompressedFilename(String)
    + Add FileNameUtil.getUncompressedFileName(String) and deprecate
    getUncompressedFilename(String)
    + Add FileNameUtil.isCompressedFileName(String) and deprecate
    isCompressedFilename(String)
    + Add BZip2Utils.getCompressedFileName(String) and deprecate
    getCompressedFilename(String)
    + Add BZip2Utils.getUncompressedFileName(String) and deprecate
    getUncompressedFilename(String)
    + Add BZip2Utils.isCompressedFileName(String) and deprecate
    isCompressedFilename(String)
    + Add LZMAUtils.getCompressedFileName(String) and deprecate
    getCompressedFilename(String)
    + Add LZMAUtils.getUncompressedFileName(String) and deprecate
    getUncompressedFilename(String)
    + Add LZMAUtils.isCompressedFileName(String) and deprecate
    isCompressedFilename(String)
    + Add XYUtils.getCompressedFileName(String) and deprecate
    getCompressedFilename(String)
    + Add XYUtils.getUncompressedFileName(String) and deprecate
    getUncompressedFilename(String)
    + Add XYUtils.isCompressedFileName(String) and deprecate
    isCompressedFilename(String)
    + Add GzipUtils.getCompressedFileName(String) and deprecate
    getCompressedFilename(String)
    + Add GzipUtils.getUncompressedFileName(String) and deprecate
    getUncompressedFilename(String)
    + Add GzipUtils.isCompressedFileName(String) and deprecate
    isCompressedFilename(String)
    + Add SevenZOutputFile.putArchiveEntry(SevenZArchiveEntry) and
    deprecate putArchiveEntry(ArchiveEntry)
    + Add generics to ChangeSet and ChangeSetPerformer
    + Add generics to ArchiveStreamProvider and friends
    + Add a generic type parameter to ArchiveOutputStream and avoid
    unchecked/unconfirmed type casts in subclasses
    + Add a generic type parameter to ArchiveInputStream and
    deprecate redundant get methods in subclasses
    + COMPRESS-648: Add ability to restrict autodetection in
    CompressorStreamFactory
  * Fixed Bugs:
    + Precompile regular expression in
    ArArchiveInputStream.isBSDLongName(String)
    + Precompile regular expression in
    ArArchiveInputStream.isGNULongName(String)
    + Precompile regular expression in
    TarArchiveEntry.parseInstantFromDecimalSeconds(String)
    + Precompile regular expression in
    ChangeSet.addDeletion(Change)
    + COMPRESS-649: Improve performance in
    BlockLZ4CompressorOutputStream
    + Null-guard Lister.main(String[]) for programmatic invocation
    + NPE in pack200.NewAttributeBands.Reference
    .addAttributeToBand(NewAttribute, InputStream)
    + Incorrect lazy initialization and update of static field in
    pack200.CodecEncoding.getSpecifier(Codec, Codec)
    + Incorrect string comparison in unpack200.AttributeLayout
    .numBackwardsCallables()
    + Inefficient use of keySet iterator instead of entrySet
    iterator in pack200.PackingOptions
    .addOrUpdateAttributeActions(List, Map, int)
    + Package private class pack200.IcBands.IcTuple should be a
    static inner class
    + Private class ZipFile.BoundedFileChannelInputStream should be
    a static inner class
    + Refactor internal SevenZ AES256SHA256Decoder InputStream into
    a named static inner class
    + Refactor internal SevenZ AES256SHA256Decoder OutputStream into
    a named static inner class
    + Use the root Locale for string conversion of command line
    options in org.apache.commons.compress.archivers.sevenz.CLI
    + Calling PackingUtils.config(PackingOptions) with null now
    closes the internal FileHandler
    + COMPRESS-650: LZ4 compressor throws IndexOutOfBoundsException
    + COMPRESS-632: LZWInputStream.initializeTables(int) should
    throw IllegalArgumentException instead of
    ArrayIndexOutOfBoundsException
    + COMPRESS-647: Throw IOException instead of
    ArrayIndexOutOfBoundsException when reading Zip with data
    descriptor entries
- Update to 1.24.0
  * New features:
    + Make ZipArchiveEntry.getLocalHeaderOffset() public
  * Fixed Bugs:
    + Use try-with-resources in ArchiveStreamFactory
    + Javadoc and code comments: Sanitize grammar issues and typos
    + Remove redundant (null) initializations
    + [StepSecurity] ci: Harden GitHub Actions
- Update to 1.23.0
  * New features:
    + COMPRESS-614: Use FileTime for time fields in
    SevenZipArchiveEntry
    + COMPRESS-621: Fix calculation the offset of the first ZIP
    central directory entry
    + COMPRESS-633:Add encryption support for SevenZ
    + COMPRESS-613: Support for extra time data in Zip archives
    + COMPRESS-621: Add org.apache.commons.compress.archivers.zip
    .DefaultBackingStoreSupplier to write to a custom folder
    instead of the default temporary folder.
    + COMPRESS-600: Add capability to configure Deflater strategy
    in GzipCompressorOutputStream:
    GzipParameters.setDeflateStrategy(int).
  * Fixed Bugs:
    + Implicit narrowing conversion in compound assignment
    + Avoid NPE in FileNameUtils.getBaseName(Path) for paths with
    zero elements like root paths
    + Avoid NPE in FileNameUtils.getExtension(Path) for paths with
    zero elements like root paths
    + LZMA2Decoder.decode() looses original exception
    + Extract conditions and avoid duplicate code.
    + Remove duplicate conditions. Use switch instead.
    + Replace JUnit 3 and 4 with JUnit 5
    + Make 'ZipFile.offsetComparator' static
    + COMPRESS-638: The GzipCompressorOutputStream#writeHeader()
    uses ISO_8859_1 to write the file name and comment. If the
    strings contains non-ISO_8859_1 characters, unknown characters
    are displayed after decompression. Use percent encoding for
    non ISO_8859_1 characters.
    + Port some code from IO to NIO APIs
    + pack200: Fix FileBands misusing InputStream#read(byte[])
    + COMPRESS-641: Add TarArchiveEntry.getLinkFlag()
    + COMPRESS-642: Integer overflow ArithmeticException in
    TarArchiveOutputStream
    + COMPRESS-642: org.apache.commons.compress.archivers.zip
    .ZipFile.finalize() should not write to std err.
  * Removed:
    + Remove BZip2CompressorOutputStream.finalize() which only wrote
    to std err
- Update to 1.22
  * New features:
    + COMPRESS-602: Migrate zip package to use NIO
    + Add APK file extension constants: ArchiveStreamFactory.APK,
    APKM, APKS, XAPK
    + ArchiveStreamFactory.createArchiveInputStream(String,
    InputStream, String) supports the "APK" format (it's a JAR)
    + Expander example now has NIO Path versions of IO File APIs
    + COMPRESS-612: Improve TAR support for file times
    + Add SevenZArchiveEntry.setContentMethods(SevenZMethodConfiguration...)
  * Fixed Bugs:
    + Fix some compiler warnings in pack200 packages
    + Close File input stream after unpacking in
    Pack200UnpackerAdapter.unpack(File, JarOutputStream)
    + Pack200UnpackerAdapter.unpack(InputStream, JarOutputStream)
    should not close its given input stream
    + COMPRESS-596: Fix minor problem in examples.
    + COMPRESS-584: Add a limit to the copy buffer in
    IOUtils.readRange() to avoid reading more from a channel than
    asked for
    + Documentation nits
    + Replace wrapper Collections.sort is with an instance method
    directly
    + Replace manual comparisons with Comparator.comparingInt()
    + Replace manual copy of array contents with System.arraycopy()
    + Fix thread safety issues when encoding 7z password
    + bzip2: calculate median-of-3 on unsigned values
    + Use Math.min and Math.max calculations.
    + COMPRESS-603: Expander should be able to work if an entry's
    name is "./".
    + COMPRESS-604: Ensure compatibility with Java 8
    + Use StringBuilder instead of StringBuffer.
    + Inline variable. Remove redundant local variable.
    + Use compare method
    + Remove Unnecessary interface modifiers
    + Avoid use C-style array declaration.
    + ChecksumVerifyingInputStream.read() does not always validate
    checksum at end-of-stream
    + Fix TarFileTest
    + COMPRESS-625: Update Wikipedia link in TarUtils.java:627.
    + COMPRESS-626: OutOfMemoryError on malformed pack200 input
    (attributes).
    + COMPRESS-628: OutOfMemoryError on malformed pack200 input
    (org.apache.commons.compress.harmony.pack200.NewAttributeBands
    .readNextUnionCase).
    + COMPRESS-628: OutOfMemoryError on malformed unpack200 input
    (org.apache.commons.compress.harmony.unpack200
    .NewAttributeBands.readNextUnionCase).
    + Some input streams are not closed in org.apache.commons
    .compress.harmony.pack200.PackingUtils
    + COMPRESS-627: Pack200 causes a 'archive.3E' error if it's not
    in the system class loader.
- Modified patches:
  * 0001-Remove-Brotli-compressor.patch
  * 0002-Remove-ZSTD-compressor.patch
  * 0003-Remove-Pack200-compressor.patch
    + rediff to changed context
- Removed patch:
  * fix_java_8_compatibility.patch
    + not needed, since we handle the compatibility differently
* Mon Mar 21 2022 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * 0003-Remove-Pack200-compressor.patch
    + Remove support for pack200 which depends on old asm3
* Tue Jul 20 2021 Fridrich Strba <fstrba@suse.com>
- Updated to 1.21
  * When reading a specially crafted 7Z archive, the construction of
    the list of codecs that decompress an entry can result in an
    infinite loop. This could be used to mount a denial of service
    attack against services that use Compress' sevenz package.
    (CVE-2021-35515, bsc#1188463)
  * When reading a specially crafted 7Z archive, Compress can be
    made to allocate large amounts of memory that finally leads to
    an out of memory error even for very small inputs. This could
    be used to mount a denial of service attack against services
    that use Compress' sevenz package. (CVE-2021-35516, bsc#1188464)
  * When reading a specially crafted TAR archive, Compress can be
    made to allocate large amounts of memory that finally leads to
    an out of memory error even for very small inputs. This could be
    used to mount a denial of service attack against services that
    use Compress' tar package. (CVE-2021-35517, bsc#1188465)
  * When reading a specially crafted ZIP archive, Compress can be
    made to allocate large amounts of memory that finally leads to
    an out of memory error even for very small inputs. This could
    be used to mount a denial of service attack against services
    that use Compress' zip package. (CVE-2021-36090, bsc#1188466)
- New dependency on asm3 for Pack200 compressor
- Rebased patch fix_java_8_compatibility.patch to a new context and
  added some new ocurrences
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
