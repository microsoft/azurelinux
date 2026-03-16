Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package apache-commons-codec
#
# Copyright (c) 2020 SUSE LLC
# Copyright (c) 2000-2010, JPackage Project
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


%define base_name  codec
%define short_name commons-%{base_name}
%bcond_with tests
Name:           apache-commons-codec
Version:        1.15
Release:        2%{?dist}
Summary:        Apache Commons Codec Package
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://commons.apache.org/codec/
Source0:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source2:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz.asc
Source1:        %{name}-build.xml
# Data in DoubleMetaphoneTest.java originally has an inadmissible license.
# The author gives MIT in e-mail communication.
Source100:      aspell-mail.txt
BuildRequires:  ant
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
Requires:       java >= 1.8
Provides:       jakarta-%{short_name} = %{version}
Obsoletes:      jakarta-%{short_name} < %{version}
Provides:       %{short_name} = %{version}
Obsoletes:      %{short_name} < %{version}
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit >= 1.7
BuildRequires:  apache-commons-lang3
BuildRequires:  hamcrest-core
BuildRequires:  junit
BuildRequires:  mozilla-nss
%endif

%description
Commons Codec is an attempt to provide definitive implementations of
commonly used encoders and decoders.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML
Provides:       jakarta-%{short_name}-javadoc = %{version}
Obsoletes:      jakarta-%{short_name}-javadoc < %{version}
Provides:       %{short_name}-javadoc = %{version}
Obsoletes:      %{short_name}-javadoc < %{version}

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE1} build.xml
cp %{SOURCE100} aspell-mail.txt

#fixes eof encoding
dos2unix RELEASE-NOTES*.txt LICENSE.txt NOTICE.txt

%pom_remove_parent .

%build
mkdir -p lib
%if %{with tests}
build-jar-repository -s lib junit4 hamcrest/core commons-lang3
%endif
ant \
%if %{without tests}
  -Dtest.skip=true \
%endif
  -Dcompiler.source=1.8 -Dcompiler.target=1.8 \
  jar javadoc

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}.jar
ln -sf %{short_name}.jar %{buildroot}%{_javadir}/%{name}.jar
# poms
# Install pom file
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 pom.xml %{buildroot}%{_mavenpomdir}/%{short_name}.pom
%add_maven_depmap %{short_name}.pom %{short_name}.jar -a "%{short_name}:%{short_name}"
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%pre javadoc
if [ -L %{_javadocdir}/%{name} ]; then
  rm -f %{_javadocdir}/%{name};
fi

%files -f .mfiles
%license LICENSE.txt
%doc RELEASE-NOTES.txt
%{_javadir}/%{name}.jar

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.15-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.15-1.2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Oct 27 2020 Pedro Monreal <pmonreal@suse.com>
- Update to 1.15
  * Fix: MurmurHash3: Ensure hash128 maintains the sign extension bug.
  * Update: Base32/Base64/BCodec: Added strict decoding property to
    control handling of trailing bits. Default lenient mode discards
    them without error. Strict mode raise an exception.
  * Update: Base32/Base64 Input/OutputStream: Added strict decoding
    property to control handling of trailing bits. Default lenient
    mode discards them without error. Strict mode raise an exception.
  * Update: Update tests from JUnit 4.12 to 4.13.
  * Add: Base16Codec and Base16Input/OutputStream.
  * Add: Hex encode/decode with existing arrays.
  * Update: Update actions/checkout from v1 to v2.3.2.
  * Update: Update actions/setup-java from v1.4.0 to v1.4.1.
- Remove timeout.patch
* Tue Jun  2 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Update to version 1.14
  * Release 1.14 - 2019-12-30
  - Fix: Hex: Allow encoding read-only ByteBuffer.
  - Fix: Hex: Only use an available ByteBuffer backing array if
    the length equals the remaining byte count.
  - Update: MurmurHash3: Deprecate hash64 methods and hash methods
    accepting a String that use the default encoding.
  - Fix: BaseNCodec to expand buffer using overflow conscious code.
  - Fix: Base32/64: Fixed decoding check that all the final trailing
    bits to discard are zero.
  - Add: Add MurmurHash3.hash128x64 methods to fix sign extension error
    during seeding in hash128 methods.
  - Add: Add MurmurHash3.hash32x86 methods and IncrementalHash32x86 to
    fix sign extension error in hash32 methods.
  - Fix: Allow repeat calls to MurmurHash3.IncrementalHash32.end() to
    generate the same value.
  - Add: Add RandomAccessFile digest methods #31.
  - Add: Add Path APIs to org.apache.commons.codec.digest.DigestUtils
    similar to File APIs.
  - Add: Add SHA-512/224 and SHA-512/256 to DigestUtils for Java 9 and up.
  - Add: Add missing note in javadoc when sign extension error is present #34.
  - Fix: Reliance on default encoding in MurmurHash2 and MurmurHash3.
  - Update: Don't reload standard Charsets in org.apache.commons.codec.Charsets.
  - Update: Deprecate Charset constants in org.apache.commons.codec.Charsets
    in favor of java.nio.charset.StandardCharsets.
  * Release 1.13 - 2019-07-20
  - Fix: ColognePhonetic handles x incorrectly.
  - Fix: ColognePhonetic does not treat the letter H correctly.
  - Fix: Reject any decode request for a value that is impossible to
    encode to for Base32/Base64 rather than blindly decoding.
  - Add: MurmurHash2 for 32-bit or 64-bit value.
  - Add: MurmurHash3 for 32-bit or 128-bit value.
  - Update: Broken direct java.nio.ByteBuffer support in
    org.apache.commons.codec.binary.Hex.
  * Release 1.12 - 2019-02-04
  - Fix: B64 salt generator: Random -> ThreadLocalRandom.
  - Fix: Wrong value calculated by Cologne Phonetic if a special character
    is placed between equal letters.
  - Update: Update from Java 6 to Java 7.
  - Add: Add Percent-Encoding Codec (described in RFC3986 and RFC7578).
  - Fix: ColognePhoneticTest.testIsEncodeEquals missing assertions.
  - Add: Add SHA-3 methods in DigestUtils.
* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
* Fri Feb 15 2019 Fridrich Strba <fstrba@suse.com>
- Update to version 1.11
  * New features:
    + Add Automatic-Module-Name manifest entry for Java 9.
    Fixes CODEC-242.
    + Add BaseNCodec.encode(byte[], int, int) input with offset and
    length parameters for Base64 and Base32. Fixes CODEC-202.
    + Add convenience API org.apache.commons.codec.binary.Hex.
    .encodeHexString(byte[]|ByteBuffer, boolean).
    Fixes CODEC-224.
    + Add convenience method decodeHex(String). Fixes CODEC-203.
    + Add DigestUtils.getDigest(String, MessageDigest).
    Fixes CODEC-210.
    + Add faster CRC32 implementation. Fixes CODEC-205.
    + Add HmacAlgorithms.HMAC_SHA_224 (Java 8 only).
    Fixes CODEC-217.
    + Add java.io.File APIs to MessageDigestAlgorithm.
    Fixes CODEC-206.
    + Add support for CRC32-C. Fixes CODEC-171.
    + Add support for XXHash32. Fixes CODEC-241.
    + BaseNCodecOutputStream only supports writing EOF on close().
    Fixes CODEC-183.
    + Create a minimal Digest command line utility:
    org.apache.commons.codec.digest.Digest. Fixes CODEC-212.
    + Fluent interface for DigestUtils. Fixes CODEC-220.
    + Fluent interface for HmacUtils. Fixes CODEC-222.
    + Make some DigestUtils APIs public. Fixes CODEC-208.
    + Support java.nio.ByteBuffer in DigestUtils. Fixes CODEC-193.
    + Support java.nio.ByteBuffer in
    org.apache.commons.codec.binary.Hex. Fixes CODEC-194.
    + Support JEP 287: SHA-3 Hash Algorithms. Fixes CODEC-213.
    + Support SHA-224 in DigestUtils on Java 8. Fixes CODEC-195.
  * Removed feature:
    + Drop obsolete Ant build. Fixes CODEC-223.
  * Changes:
    + Base32.decode should support lowercase letters.
  Fixes CODEC-234.
    + HmacUtils.updateHmac calls reset() unnecessarily.
  Fixes CODEC-221.
    + Soundex should support more algorithm variants.
  Fixes CODEC-233.
  * Fixed bugs:
    + Base32.HEX_DECODE_TABLE contains the wrong value 32.
  Fixes CODEC-200.
    + Base64.encodeBase64String could better use newStringUsAscii
  (ditto encodeBase64URLSafeString). Fixes CODEC-145.
    + BaseNCodec: encodeToString and encodeAsString methods are
  identical. Fixes CODEC-144.
    + Bug in HW rule in Soundex. Fixes CODEC-199.
    + Charsets Javadoc breaks build when using Java 8.
  Fixes CODEC-207.
    + Don't deprecate Charsets Charset constants in favor of
  Java 7's java.nio.charset.StandardCharsets. Fixes CODEC-219.
    + Fix minor resource leaks. Fixes CODEC-225.
    + Javadoc for SHA-224 DigestUtils methods should mention
  Java 1.8.0 restriction instead of 1.4.0. Fixes CODEC-209.
    + StringUtils.equals(CharSequence cs1, CharSequence cs2) can
  fail with String Index OBE. Fixes CODEC-231.
    + StringUtils.newStringxxx(null) should return null, not NPE.
  Fixes CODEC-229.
    + URLCodec is neither immutable nor threadsafe.
  Fixes CODEC-232.
    + URLCodec.WWW_FORM_URL should be private. Fixes CODEC-230.
- Generate the Ant build file and use it
- Add an option --with tests and don't run tests by default. This
  diminshes the number of dependencies and speeds-up the build.
* Tue Feb  5 2019 Fridrich Strba <fstrba@suse.com>
- Clean-up the spec file
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Run fdupes on documentation
* Fri Sep 29 2017 fstrba@suse.com
- Don't condition the maven defines on release version, but on
  _maven_repository being defined
* Thu Sep  7 2017 fstrba@suse.com
- Build with java source and target versions 1.6
  * fixes build with jdk9
* Fri May 19 2017 tchvatal@suse.com
- Fix build with new javapackages-tools
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Fri Dec  5 2014 p.drouand@gmail.com
- Update to version 1.10
  New features:
  + Add Daitch-Mokotoff Soundex
    Issue: CODEC-192.
  + QuotedPrintableCodec does not support soft line break per the
    'quoted-printable' example on Wikipedia
    Issue: CODEC-121.
  + Make possible to provide padding byte to BaseNCodec in constructor
    Issue: CODEC-181.
  Fixed Bugs:
  + Added clarification to Javadoc of Base64 concerning the use of the
    urlSafe parameter
    Issue: CODEC-185.
  + Added clarification to the Javadoc of Base[32|64]OutputStream that it
    is mandatory to call close()
    Issue: CODEC-191.
  + Add support for HMAC Message Authentication Code (MAC) digests
    Issue: CODEC-188.
  + Beider Morse Phonetic Matching producing incorrect tokens
    Issue: CODEC-187.
  + NullPointerException in DoubleMetaPhone.isDoubleMetaphoneEqual when
    using empty strings
    Issue: CODEC-184.
  + Fix Javadoc 1.8.0 errors
    Issue: CODEC-180.
  + Fix Java 8 build Javadoc errors
    Issue: CODEC-189.
  Changes:
  + Deprecate Charsets Charset constants in favor of Java 7's
    java.nio.charset.StandardCharsets
    Issue: CODEC-178.
  + Update from commons-parent 34 to 35
    Issue: CODEC-190.
- Use javapackages-tools instead of java-devel
- Remove gpg_verify usage; let obs handle it
* Mon Jul  7 2014 tchvatal@suse.com
- Set the bytecode properly on sle11
* Mon Jul  7 2014 tchvatal@suse.com
- Depend on junit not junit4.
* Sun Jun 22 2014 schwab@suse.de
- timeout.patch: avoid spurious timeout in BeiderMorse tests
* Thu May 15 2014 darin@darins.net
- disable bytecode check on sle_11
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Mon Aug 26 2013 mvyskocil@suse.com
- update to 1.8
  * Add DigestUtils.updateDigest(MessageDigest, InputStream). Thanks to Daniel Cassidy.
  * Add JUnit to test our decode with pad character in the middle.
  * Add Match Rating Approach (MRA) phonetic algorithm encoder. Thanks to crice.
  * ColognePhonetic encoder unnecessarily creates many char arrays on every loop run. Thanks to leo141.
  * Base64.encodeBase64URLSafeString doesn't add padding characters at the end.
- temporary add mozilla-nss to BR: to pass tests
- drop unecessary source files
- add signature verification
- use newer add_maven_depmap
- fix source urls
* Mon Apr  2 2012 mvyskocil@suse.cz
- add junit4 to fix a build fail
* Tue Feb 28 2012 mvyskocil@suse.cz
- update to 1.6, sync with Fedora
* Fri Sep 22 2006 skh@suse.de
- don't use icecream
- use target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Dec 19 2005 dbornkessel@suse.de
- Current version 1.3 from JPackage.org
