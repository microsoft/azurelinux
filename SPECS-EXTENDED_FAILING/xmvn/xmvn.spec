Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package xmvn
#
# Copyright (c) 2020 SUSE LLC
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


Name:           xmvn
Version:        3.1.0
Release:        3%{?dist}
Summary:        Local Extensions for Apache Maven
License:        Apache-2.0
Group:          Development/Tools/Building
URL:            https://fedora-java.github.io/xmvn/
BuildRequires:  %{name}-api = %{version}
BuildRequires:  %{name}-connector-aether = %{version}
BuildRequires:  %{name}-core = %{version}
BuildRequires:  %{name}-subst
BuildRequires:  javapackages-tools
BuildRequires:  maven
BuildRequires:  maven-lib
Requires:       %{name}-minimal = %{version}-%{release}

%description
This package provides extensions for Apache Maven that can be used to
manage system artifact repository and use it to resolve Maven
artifacts in offline mode, as well as Maven plugins to help with
creating RPM packages containing Maven artifacts.

%package        minimal
Summary:        Dependency-reduced version of XMvn
Group:          Development/Tools/Building
Requires:       %{name}-api = %{version}
Requires:       %{name}-connector-aether = %{version}
Requires:       %{name}-core = %{version}
Requires:       maven-lib >= 3.4.0

%description    minimal
This package provides minimal version of XMvn, incapable of using
remote repositories.

%prep

%build

%install
maven_home=$(realpath $(dirname $(realpath $(which mvn)))/..)

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -aL ${maven_home}/* %{buildroot}%{_datadir}/%{name}/

for i in api core connector-aether; do
    ln -s $(build-classpath %{name}/%{name}-${i}) %{buildroot}%{_datadir}/%{name}/lib/ext/
done

# Irrelevant Maven launcher scripts
rm -f %{buildroot}%{_datadir}/%{name}/bin/*

for cmd in mvn mvnDebug; do
    cat <<EOF >%{buildroot}%{_datadir}/%{name}/bin/$cmd
#!/bin/sh -e
export _FEDORA_MAVEN_HOME="%{_datadir}/%{name}"
exec ${maven_home}/bin/$cmd "\${@}"
EOF
    chmod 755 %{buildroot}%{_datadir}/%{name}/bin/$cmd
done

# possibly recreate symlinks that can be automated with xmvn-subst
%{name}-subst -s -R %{buildroot} %{buildroot}%{_datadir}/%{name}/

# /usr/bin/xmvn
install -dm 0755 %{buildroot}%{_bindir}
ln -sf %{_datadir}/%{name}/bin/mvn %{buildroot}%{_bindir}/%{name}

# mvn-local symlink
ln -s %{name} %{buildroot}%{_bindir}/mvn-local

# make sure our conf is identical to maven so yum won't freak out
install -d -m 755 %{buildroot}%{_datadir}/%{name}/conf/
cp -P ${maven_home}/conf/settings.xml %{buildroot}%{_datadir}/%{name}/conf/
cp -P ${maven_home}/bin/m2.conf %{buildroot}%{_datadir}/%{name}/bin/

%pre minimal
if [ -L %{_datadir}/%{name}/conf/logging ]; then
    rm -f %{_datadir}/%{name}/conf/logging
fi

%files
%{_bindir}/mvn-local

%files minimal
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/bin
%dir %{_datadir}/%{name}/lib
%{_datadir}/%{name}/lib/*.jar
%{_datadir}/%{name}/lib/ext
%{_datadir}/%{name}/lib/jansi-native
%{_datadir}/%{name}/bin/m2.conf
%{_datadir}/%{name}/bin/mvn
%{_datadir}/%{name}/bin/mvnDebug
%{_datadir}/%{name}/boot
%{_datadir}/%{name}/conf

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.0-3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon May 11 2020 Fridrich Strba <fstrba@suse.com>
- Do not use %%%%pretrans
* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 3.1.0
* Wed Mar 27 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of xmvn 3.0.0
