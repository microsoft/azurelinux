Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package objectweb-anttask
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
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


Name:           objectweb-anttask
Version:        1.2
Release:        267%{?dist}
Summary:        ObjectWeb Ant task
License:        LGPLv2+
Group:          Development/Languages/Java
Url:            https://forge.objectweb.org/projects/monolog/
Source0:        %{_distro_sources_url}/ow_util_ant_tasks_1.2.zip
Source1:        %{name}-LICENSE.txt
Patch1:         objectweb-anttask-ant17.patch
Patch2:         objectweb-anttask-java5.patch
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  unzip
BuildRequires:  xalan-j2
BuildRequires:  xml-commons-apis
Provides:       owanttask
BuildArch:      noarch

%description
ObjectWeb Ant task

%prep
%setup -q -c -n %{name}
%patch 1
%patch 2 -p1
find . -name "*.class" -exec rm {} \;
find . -name "*.jar" -exec rm {} \;

cp %{SOURCE1} ./LICENSE.txt

%build
export CLASSPATH=$(build-classpath xalan-j2)
ant \
    -Dbuild.compiler=modern \
    -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 \
    jar

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 output/lib/ow_util_ant_tasks.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir}
  ln -sf %{name}-%{version}.jar %{name}.jar
popd

%files
%license LICENSE.txt
%{_javadir}/*

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-267
- Updating naming for 3.0 version of Azure Linux.

* Tue Apr 26 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.2-266
- Updated source URL.

* Fri Dec 10 2021 Thomas Crain <thcrain@microsoft.com> - 1.2-265
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-264
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Oct  4 2017 fstrba@suse.com
- Specify java source and target level 1.6 in order to allow
  building with jdk9
- Removed patch:
  * objectweb-anttask-java14compat.patch
    + Do not hardcode java source and target levels; we specify
    them on command-line
  * objectweb-anttask-java5.patch
    + Rename enum -> emun, since "enum" is a keyword in java5+
  + Fix "no suitable method found for put(String,String) ...
    argument mismatch; String cannot be converted to String[]"
    with java5+
* Thu Sep 26 2013 mvyskocil@suse.com
- Build with gcc-java as openjdk7 (1.7.0_40) fails to build it
* Tue Sep 18 2007 ro@suse.de
- hack to build with ant-1.7 (MultipleCopy works only for FileSets
  not for real ResourceCollection yet)
* Thu Mar 29 2007 ro@suse.de
- added unzip to buildreq
* Thu Sep 21 2006 skh@suse.de
- don't use icecream
- fix BuildRequires: add xalan-j2
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Oct 17 2005 jsmeix@suse.de
- Current version 1.2 from JPackage.org
