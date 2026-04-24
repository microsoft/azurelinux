# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          ed25519-java
Version:       0.3.0
Release: 27%{?dist}
Summary:       Implementation of EdDSA (Ed25519) in Java
# Automatically converted from old format: CC0 - review is highly recommended.
License:       CC0-1.0
URL:           https://github.com/str4d/ed25519-java
Source0:       https://github.com/str4d/ed25519-java/archive/v%{version}/%{name}-%{version}.tar.gz

# https://github.com/str4d/ed25519-java/commit/e0ac35769db8553fb714b09f0d3f3d2b001fd033
Patch0: 0001-EdDSAEngine.initVerify-Handle-any-non-EdDSAPublicKey.patch

Patch1: 0002-Disable-test-that-relies-on-internal-sun-JDK-classes.patch

BuildRequires: maven-local-openjdk25
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.hamcrest:hamcrest-all)

BuildArch:     noarch
ExclusiveArch:  %{java_arches} noarch

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
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch -P0 -p1
%patch -P1 -p1

# Unwanted tasks
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-source-plugin
# Unavailable plugin
%pom_remove_plugin :nexus-staging-maven-plugin

%mvn_file net.i2p.crypto:eddsa %{name} eddsa

# Remove hard-coded source/target
%pom_xpath_remove pom:plugin/pom:configuration/pom:target
%pom_xpath_remove pom:plugin/pom:configuration/pom:source

%build
%mvn_build -- -Dmaven.compiler.release=11

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 0.3.0-26
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 0.3.0-23
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 0.3.0-21
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 0.3.0-15
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0.3.0-14
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 01 2021 Mat Booth <mat.booth@gmail.com> - 0.3.0-12
- Add patches to fix dep on internal sun JDK class and fix test
  execution on Java 17

* Mon Nov 29 2021 Mat Booth <mat.booth@gmail.com> - 0.3.0-11
- Remove hard-coded source/target

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0.3.0-7
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jun 26 2020 Roland Grunberg <rgrunber@redhat.com> - 0.3.0-6
- Set maven-javadoc-plugin source to 1.8 for Java 11 build.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 07 2018 Mat Booth <mat.booth@redhat.com> - 0.3.0-2
- Make dep on sun.security.x509 optional

* Thu Nov 29 2018 Mat Booth <mat.booth@redhat.com> - 0.3.0-1
- Update to latest upstream release

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar 18 2016 gil cattaneo <puntogil@libero.it> 0.1.0-1
- update to 0.1.0

* Sat Dec 05 2015 gil cattaneo <puntogil@libero.it> 0.0.1-0.1.SNAPSHOT
- initial rpm
