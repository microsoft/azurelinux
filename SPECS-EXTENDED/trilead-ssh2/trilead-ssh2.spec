%global buildver 217
%global patchlvl 21

Name:           trilead-ssh2
Version:        %{buildver}.%{patchlvl}
Release:        14%{?dist}
Summary:        SSH-2 protocol implementation in pure Java

# Project is under BSD, but some parts are MIT licensed
# see LICENSE.txt for more information
# One file is ISC licensed: The bundled implementation of BCrypt.java
# One file is RSA licensed: src/com/trilead/ssh2/crypto/digest/MD5.java
License:        BSD and MIT and ISC and RSA

# Jenkins fork is used because the original sources of this library,
# "ganymed" and then "trilead" are both defunct and the original
# project sites are unavailable. However Jenkins project continues
# to maintain it
URL:            https://github.com/jenkinsci/trilead-ssh2
Source0:        https://github.com/jenkinsci/trilead-ssh2/archive/%{name}-build-%{buildver}-jenkins-%{patchlvl}.tar.gz

# Source of bundled BCrypt implementation, taken from:
# https://mvnrepository.com/artifact/org.connectbot.jbcrypt/jbcrypt/1.0.0
Source1:  BCrypt.java
Provides: bundled(jbcrypt) = 1.0.0

BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(net.i2p.crypto:eddsa)

BuildArch:      noarch
#ExclusiveArch:  %{java_arches} noarch

%description
Trilead SSH-2 for Java is a library which implements the SSH-2 protocol in pure
Java (tested on J2SE 1.4.2 and 5.0). It allows one to connect to SSH servers
from within Java programs. It supports SSH sessions (remote command execution
and shell access), local and remote port forwarding, local stream forwarding,
X11 forwarding and SCP. There are no dependencies on any JCE provider, as all
crypto functionality is included.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-build-%{buildver}-jenkins-%{patchlvl}

# jbcrypt is not available in Fedora, it is bundled instead
mkdir -p src/org/mindrot/jbcrypt
cp -p %{SOURCE1} src/org/mindrot/jbcrypt
%pom_remove_dep "org.connectbot.jbcrypt:jbcrypt"

# test dependency not available in Fedora
%pom_remove_dep "org.testcontainers:testcontainers"

# compat symlink/alias
%mvn_file  : %{name}/%{name} %{name}
%mvn_alias : "org.tmatesoft.svnkit:trilead-ssh2" "com.trilead:trilead-ssh2"

%build
# Skip tests due to unavailability of test deps
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%doc HISTORY.txt README.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 217.21-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 217.21-13
- Rebuilt for java-21-openjdk as system jdk

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 217.21-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 217.21-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 217.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 217.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 217.21-8
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 217.21-7
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 217.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 217.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 217.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 217.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Mat Booth <mat.booth@redhat.com> - 217.21-2
- Fix release number and license tag

* Tue Jul 14 2020 Mat Booth <mat.booth@redhat.com> - 217.21-1
- Update to latest upstream release

* Mon Jul 13 2020 Mat Booth <mat.booth@redhat.com> - 217-13.jenkins8
- Adopt license macro

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 217-12.jenkins8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 217-11.jenkins8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 217-10.jenkins8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 217-9.jenkins8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 217-8.jenkins8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 217-7.jenkins8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 01 2015 Michal Srb <msrb@redhat.com> - 217-6.jenkins8
- Update to 217-jenkins8

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 217-5.jenkins4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 217-4.jenkins4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 02 2014 Michal Srb <msrb@redhat.com> - 217-3.jenkins4
- Build version 217 from Jenkins sources

* Mon Jan 06 2014 Michal Srb <msrb@redhat.com> - 217-2
- Remove unneeded files
- Add POM file to sources

* Mon Jan 06 2014 Michal Srb <msrb@redhat.com> - 217-1
- Adapt to current packaging guidelines
- Build with XMvn
- Update to upstream version 217
- Add alias (Resolves: rhbz#1048829)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 215-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Tom Callaway <spot@fedoraproject.org> - 215-1
- update to 215

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 213-7
- Add maven metadata
- Drop gcj support
- Changes according to new guidelines (no clean section/buildroot)
- Versionless jars & javadocs

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 30 2009 Robert Marcano <robert@marcanoonline.com> - 213-5
- Fix Bug 492759, bad javadoc package group

* Tue Feb 16 2009 Robert Marcano <robert@marcanoonline.com> - 213-4
- Renaming package because main project moved, based on ganymed-ssh2
