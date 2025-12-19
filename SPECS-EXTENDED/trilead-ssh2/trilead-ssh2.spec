Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package trilead-ssh2
#
# Copyright (c) 2024 SUSE LLC
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


%global buildver 217
%global patchlvl 371
%global githash  vc1d30dc5a_b_32

Name:           trilead-ssh2
Version:        %{buildver}.%{patchlvl}.%{githash}
Release:        1%{?dist}
Summary:        SSH-2 protocol implementation in pure Java
License:        BSD-3-Clause AND MIT
Group:          Development/Libraries/Java
URL:            https://github.com/jenkinsci/trilead-ssh2
Source0:        https://github.com/jenkinsci/%{name}/archive/refs/tags/build-%{buildver}-jenkins-%{patchlvl}.%{githash}.tar.gz
Source1:        %{name}-build.xml
Patch0:         0001-Remove-the-dependency-on-google-tink.patch
BuildRequires:  ant
BuildRequires:  ed25519-java
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.9
BuildRequires:  javapackages-local-bootstrap >= 6
BuildRequires:  javapackages-tools
BuildRequires:  jbcrypt
BuildArch:      noarch

%description
Trilead SSH-2 for Java is a library which implements the SSH-2 protocol in pure
Java (tested on J2SE 1.4.2 and 5.0). It allows one to connect to SSH servers
from within Java programs. It supports SSH sessions (remote command execution
and shell access), local and remote port forwarding, local stream forwarding,
X11 forwarding and SCP. There are no dependencies on any JCE provider, as all
crypto functionality is included.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%autosetup -n %{name}-build-%{buildver}-jenkins-%{patchlvl}.%{githash} -p1
cp %{SOURCE1} build.xml

%pom_remove_dep :tink
%pom_xpath_set pom:project/pom:version "build-%{buildver}-jenkins-%{patchlvl}.%{githash}"

%build
mkdir -p lib
build-jar-repository -s lib eddsa jbcrypt
%{ant} package javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-*.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a "org.tmatesoft.svnkit:trilead-ssh2","com.trilead:trilead-ssh2"

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -aL target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE.txt
%doc HISTORY.txt README.txt

%files javadoc
%license LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Fri Dec 19 2025 BinduSri Adabala <v-badabala@microsoft.com> - 217.371.vc1d30dc5a_b_32-1
- Upgrade to 217.371.vc1d30dc5a_b_32
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 217.8-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 217.8-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Set Xdoclint to none.

* Tue Apr 16 2019 Fridrich Strba <fstrba@suse.com>
- Fix the license tag and clean up the spec file a bit
* Wed Oct 24 2018 Fridrich Strba <fstrba@suse.com>
- Initial packaging built manually without maven. Spec file adapted
  from Fedora rpm.