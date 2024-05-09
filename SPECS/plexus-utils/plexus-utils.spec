Summary:        Plexus Common Utilities
#
# spec file for package plexus-utils
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
Name:           plexus-utils
Version:        3.3.0
Release:        4%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://codehaus-plexus.github.io/plexus-utils/
Source0:        https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}.tar.gz
Source1:        https://apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  javapackages-bootstrap
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
Plexus contains end-to-end developer tools for writing applications.
At the core is the container, which can be embedded or for an
application server. There are many reusable components for hibernate,
form processing, jndi, i18n, velocity, etc. Plexus also includes an
application server which is like a J2EE application server.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp %{SOURCE1} .

%pom_remove_parent .
%pom_xpath_inject "pom:project" "<groupId>org.codehaus.plexus</groupId>" .

	
%mvn_file : plexus/utils
%mvn_alias : plexus:plexus-utils
 
%build
%mvn_build -f -- -Dmaven.compiler.source=17 -Dmaven.compiler.target=17 -Dmaven.javadoc.source=17 -Dmaven.compiler.release=17
 
%install
%mvn_install

%files -f .mfiles
%doc NOTICE.txt LICENSE-2.0.txt

%files javadoc
%doc NOTICE.txt LICENSE-2.0.txt
%{_javadocdir}/%{name}

%changelog
* Fri Feb 23 2024 Riken Maharjan <rmaharjan@microsoft.com> - 3.3.0-4
- Rebuilt with msopenjdk-17 and maven
- change source, target

* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.3.0-3
- Moved from extended to core
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.3.0-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 3.3.0
- Removed patch:
  * 0001-Follow-symlinks-in-NioFiles.copy.patch
    + not needed with this version

* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent pom since we are not building
  using Maven.

* Sun Mar  3 2019 Jan Engelhardt <jengelh@inai.de>
- Describe package, not project.

* Sat Mar  2 2019 Fridrich Strba <fstrba@suse.com>
- Initial package for plexus-utils 3.1.1
- Generate and customize ant build file
