Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package trilead-ssh2
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


%global buildver 217
%global patchlvl 8
Name:           trilead-ssh2
Version:        %{buildver}.%{patchlvl}
Release:        2%{?dist}
Summary:        SSH-2 protocol implementation in pure Java
License:        BSD-3-Clause AND MIT
Group:          Development/Libraries/Java
URL:            https://github.com/jenkinsci/trilead-ssh2
Source0:        https://github.com/jenkinsci/%{name}/archive/%{name}-build%{buildver}-jenkins-%{patchlvl}.tar.gz
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
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
%setup -q -n %{name}-%{name}-build%{buildver}-jenkins-%{patchlvl}

%build
mkdir -p build/classes
javac -d build/classes -source 6 -target 6 $(find src -name \*.java | xargs)
(cd build/classes && jar cf ../%{name}-%{version}.jar  $(find . -name \*.class))
mkdir -p build/docs
javadoc -d build/docs -source 6  $(find src -name \*.java | xargs) -Xdoclint:none

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 build/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a "org.tmatesoft.svnkit:trilead-ssh2","com.trilead:trilead-ssh2"

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -aL build/docs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE.txt
%doc HISTORY.txt README.txt

%files javadoc
%license LICENSE.txt
%{_javadocdir}/%{name}

%changelog
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
