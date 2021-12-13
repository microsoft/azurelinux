Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-cipher
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


Name:           plexus-cipher
Version:        1.7
Release:        2%{?dist}
Summary:        Plexus Cipher: encryption/decryption Component
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-cipher
# git clone https://github.com/sonatype/plexus-cipher.git
# cd plexus-cipher/
# note this is version 1.7 + our patches which were incorporated by upstream maintainer
# git archive --format tar --prefix=plexus-cipher-1.7/ 0cff29e6b2e | gzip -9 > plexus-cipher-1.7.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  atinject
BuildRequires:  cdi-api
BuildRequires:  fdupes
BuildRequires:  javapackages-local
BuildRequires:  sisu-inject
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildArch:      noarch

%description
Plexus Cipher: encryption/decryption Component

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
API documentation for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml

# replace %{version}-SNAPSHOT with %{version}
%pom_xpath_replace pom:project/pom:version "<version>%{version}</version>"

# fedora moved from sonatype sisu to eclipse sisu. sisu-inject-bean artifact
# doesn't exist in eclipse sisu. this artifact contains nothing but
# bundled classes from atinject, cdi-api, aopalliance and maybe others.
%pom_remove_dep org.sonatype.sisu:sisu-inject-bean
%pom_add_dep javax.inject:javax.inject:1:provided
%pom_add_dep javax.enterprise:cdi-api:1.0:provided
%pom_remove_dep junit:junit
%pom_add_dep junit:junit:3.8.2:test

%pom_remove_parent .

%mvn_file : plexus/%{name}

%build
mkdir -p lib
build-jar-repository -s lib cdi-api atinject org.eclipse.sisu.inject

%ant compile
%ant jar javadoc

%mvn_artifact pom.xml target/%{name}-%{version}.jar

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Mar 20 2019 Fridrich Strba <fstrba@suse.com>
- Generate the javax.inject.Named running sisu-inject at compile
  time.
* Fri Mar  8 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-cipher 1.7
- Generate and customize the ant build.xml file
- Generate the javax.inject.Named by grepping source files that
  have the @Named annotation
