Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package apache-commons-parent
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


%define base_name       parent
%define short_name      commons-%{base_name}
Name:           apache-%{short_name}
Version:        52
Release:        2%{?dist}
Summary:        Apache Commons Parent Pom
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/commons-parent-pom.html
Source0:        https://archive.apache.org/dist/commons/%{short_name}/%{short_name}-%{version}-src.tar.gz
BuildRequires:  javapackages-local
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-compiler-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-surefire-plugin)
BuildRequires:  mvn(org.apache:apache:pom:)
# Not generated automatically
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
Requires:       mvn(org.apache:apache:pom:)
Requires:       mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildArch:      noarch

%description
The Project Object Model files for the apache-commons packages.

%prep
%setup -q -n %{short_name}-%{version}-src

# Plugin is not in suse
%pom_remove_plugin org.apache.commons:commons-build-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-scm-publish-plugin

# Plugins useless in package builds
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :buildnumber-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-source-plugin

# Remove profiles for plugins that are useless in package builds
for profile in animal-sniffer japicmp jacoco cobertura clirr; do
    %pom_xpath_remove "pom:profile[pom:id='$profile']"
done

%build

%install
# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{short_name}.pom
%add_maven_depmap %{name}/%{short_name}.pom

%files -f .mfiles
%doc RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 52-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Oct 27 2020 Pedro Monreal <pmonreal@suse.com>
- Upgrade to version 52
- Full changelog:
  * github.com/apache/commons-parent/blob/master/RELEASE-NOTES.txt
* Fri Apr  5 2019 Fridrich Strba <fstrba@suse.com>
- Make the package suitable for building with maven. Do not patch
  out useful plugins.
* Tue Oct 23 2018 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 47 and cleanup the pom file installation
* Fri May 19 2017 tchvatal@suse.com
- Do not require java-devel for build
* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
- Fixed requires
- Spec file cleaned
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Mon Apr 14 2014 darin@darins.net
- add xz buildrequires for sles
- add buildroot for sles
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Tue Aug 27 2013 mvyskocil@suse.com
- update to 32
  * sync versions of various components in pom.xml
- use add_maven_depmap from last javapackages-tools
- dropped:
  * apache-commons-parent-remove-build-plugin.patch
* Tue Feb 28 2012 mvyskocil@suse.cz
- add missing provides/obsoletes to package
  now provides jakarta-commons-parent and commons-parent
* Wed Feb  8 2012 mvyskocil@suse.cz
- rename to apache-commons-parent to be sync with jpp and Fedora
- update to release 23
  * java-1.7 profile
  * ssh/scp support to maven-site-plugin in Maven3
* Fri Jan 29 2010 mvyskocil@suse.cz
- fixed bnc#575115 - corrected license tag
* Wed Jan 27 2010 mvyskocil@suse.cz
- initial SUSE packaging (jakarta-commons-parent-11-1.jpp5.src.rpm)
