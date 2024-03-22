#
# spec file for package plexus-interpolation
#
# Copyright (c) 2019 SUSE LLC
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
%bcond_with tests
Summary:        Plexus Interpolation API
Name:           plexus-interpolation
Version:        1.26
Release:        5%{?dist}
License:        Apache-2.0 AND Apache-1.1 AND MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/%{name}
Source0:        https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch


Patch0:         0001-Use-PATH-env-variable-instead-of-JAVA_HOME.patch

%description
Plexus interpolator is the outgrowth of multiple iterations of development
focused on providing a more modular, flexible interpolation framework for
the expression language style commonly seen in Maven, Plexus, and other
related projects.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}	
%patch 0 -p1
	
%pom_add_dep junit:junit:4.13.1:test
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-scm-publish-plugin
	
%build
%mvn_file : plexus/interpolation
%mvn_build -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Mar 21 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.26-5
- Add patch using Fedora 40 (License: MIT)

* Fri Feb 23 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.26-4
- Rebuilt with msopenjdk-17, and maven

* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.26-3
- Moved from extended to core
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.26-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 20 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.26-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 1.26

* Wed Mar  6 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-interpolation 1.22
- Generate and customize ant build.xml file to be able to build
  outside maven
