Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package ed25519-java
#
# Copyright (c) 2025 SUSE LLC
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


%global artifactId eddsa
Name:           ed25519-java
Version:        0.3.0
Release:        1%{?dist}
Summary:        Implementation of EdDSA (Ed25519) in Java
License:        CC0-1.0
URL:            https://github.com/str4d/ed25519-java
Source0:        https://github.com/str4d/ed25519-java/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
Patch0:         0001-EdDSAEngine.initVerify-Handle-any-non-EdDSAPublicKey.patch
Patch1:         0002-Disable-test-that-relies-on-internal-sun-JDK-classes.patch
Patch2:         %{name}-CVE-2020-36843.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap >= 6
BuildRequires:  javapackages-tools
BuildArch:      noarch

%description
This is an implementation of EdDSA in Java. Structurally, it
is based on the ref10 implementation in SUPERCOP (see
http://ed25519.cr.yp.to/software.html).

There are two internal implementations:

* A port of the radix-2^51 operations in ref10
  - fast and constant-time, but only useful for Ed25519.
* A generic version using BigIntegers for calculation
  - a bit slower and not constant-time, but compatible
    with any EdDSA parameter specification.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
ant jar javadoc

%install

# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{artifactId}-%{version}.jar %{buildroot}%{_javadir}/%{artifactId}.jar
ln -sf %{_javadir}/%{artifactId}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{artifactId}.pom
%add_maven_depmap %{artifactId}.pom %{artifactId}.jar

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -r target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%{_javadir}/%{name}.jar
%doc README.md
%license LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}
%license LICENSE.txt

%changelog
* Tue Dec 16 2025 BinduSri Adabala <v-badabala@microsoft.com> - 0.3.0-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified

* Fri Mar 14 2025 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * ed25519-java-CVE-2020-36843.patch
    + backport commit https://github.com/i2p/i2p.i2p/commit/
    /d7d1dcb5399c61cf2916ccc45aa25b0209c88712
    + Fixes bsc#1239551, CVE-2020-36843: no check performed on
    scalar to avoid signature malleability
* Wed Oct 30 2024 Fridrich Strba <fstrba@suse.com>
- Rewrite the build using ant
* Wed Feb 21 2024 Gus Kenion <gus.kenion@suse.com>
- Use %%patch -P N instead of deprecated %%patchN.
* Mon Sep 11 2023 Fridrich Strba <fstrba@suse.com>
- Reproducible builds: use SOURCE_DATE_EPOCH for timestamp
* Tue Mar 22 2022 Fridrich Strba <fstrba@suse.com>
- Build with source and target levels 8
- Added patches:
  * 0001-EdDSAEngine.initVerify-Handle-any-non-EdDSAPublicKey.patch
  * 0002-Disable-test-that-relies-on-internal-sun-JDK-classes.patch
    + Remove use of internal sun JDK classes
* Mon Jun 29 2020 Fridrich Strba <fstrba@suse.com>
- Initial packaging of ed25519 0.3.0
