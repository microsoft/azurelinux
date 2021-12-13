Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven2
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


Name:           maven2
Version:        2.2.1
Release:        2%{?dist}
Summary:        Java project management and project comprehension tool
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org
# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source1:        generate-tarball.sh
Source2:        %{name}-build.tar.xz
Patch2:         %{name}-%{version}-update-tests.patch
Patch4:         %{name}-%{version}-unshade.patch
Patch5:         %{name}-%{version}-default-resolver-pool-size.patch
Patch6:         %{name}-%{version}-strip-jackrabbit-dep.patch
Patch8:         %{name}-%{version}-migrate-to-plexus-containers-container-default.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local
BuildRequires:  maven-lib
BuildRequires:  maven-wagon-provider-api
BuildRequires:  modello
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-interpolation
BuildRequires:  plexus-utils
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildArch:      noarch

%description
Apache Maven is a software project management and comprehension tool.
Based on the concept of a project object model (POM), Maven can manage
a project's build, reporting and documentation from a central piece of
information.

%package -n maven-artifact
Summary:        Compatibility Maven artifact artifact
Group:          Development/Libraries/Java

%description -n maven-artifact
Maven artifact manager artifact

%package -n maven-artifact-manager
Summary:        Compatibility Maven artifact manager artifact
Group:          Development/Libraries/Java

%description -n maven-artifact-manager
Maven artifact manager artifact

%package -n maven-model
Summary:        Compatibility Maven model artifact
Group:          Development/Libraries/Java

%description -n maven-model
Maven model artifact

%package -n maven-monitor
Summary:        Compatibility Maven monitor artifact
Group:          Development/Libraries/Java

%description -n maven-monitor
Maven monitor artifact

%package -n maven-plugin-registry
Summary:        Compatibility Maven plugin registry artifact
Group:          Development/Libraries/Java

%description -n maven-plugin-registry
Maven plugin registry artifact

%package -n maven-profile
Summary:        Compatibility Maven profile artifact
Group:          Development/Libraries/Java

%description -n maven-profile
Maven profile artifact

%package -n maven-project
Summary:        Compatibility Maven project artifact
Group:          Development/Libraries/Java

%description -n maven-project
Maven project artifact

%package -n maven-settings
Summary:        Compatibility Maven settings artifact
Group:          Development/Libraries/Java

%description -n maven-settings
Maven settings artifact

%package -n maven-toolchain
Summary:        Compatibility Maven toolchain artifact
Group:          Development/Libraries/Java

%description -n maven-toolchain
Maven toolchain artifact

%package -n maven-plugin-descriptor
Summary:        Maven Plugin Description Model
Group:          Development/Libraries/Java

%description -n maven-plugin-descriptor
Maven plugin descriptor artifact

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -a2

%patch2 -b .update-tests

%patch4 -b .unshade

# disable parallel artifact resolution
%patch5 -p1 -b .parallel-artifacts-resolution

# remove unneeded jackrabbit dependency
%patch6 -p1 -b .strip-jackrabbit-dep

%patch8 -p1 -b .plexus-container

for nobuild in apache-maven maven-artifact-test \
               maven-compat maven-core maven-plugin-api \
               maven-plugin-parameter-documenter maven-reporting \
               maven-repository-metadata maven-script \
               maven-error-diagnostics; do
    %pom_disable_module $nobuild
done

# Don't install parent POM
%{mvn_package} :maven __noinstall

%{mvn_package} :{*} @1

# Install all artifacts in Maven 3 directory.
%{mvn_file} ":{*}" maven/@1

# these parts are compatibility versions which are available in
# maven-3.x as well. We default to maven-3, but if someone asks for
# 2.x we provide few compat versions
%{mvn_compat_version} ":maven-{artifact,model,settings}" \
                    2.0.2 2.0.6 2.0.7 2.0.8 2.2.1

# Don't depend on backport-util-concurrent
%pom_remove_dep :backport-util-concurrent
%pom_remove_dep :backport-util-concurrent maven-artifact-manager
sed -i s/edu.emory.mathcs.backport.// `find -name DefaultArtifactResolver.java`

# Tests are skipped, so remove dependencies with scope 'test'.
for pom in $(grep -l ">test<" $(find -name pom.xml | grep -v /test/)); do
    %pom_xpath_remove "pom:dependency[pom:scope[text()='test']]" $pom
done

# Enforces that java is at least 1.5.0, which is always true for us
%pom_remove_plugin :maven-enforcer-plugin

%build
mkdir -p lib
build-jar-repository -s lib \
	maven/maven-core \
	maven/maven-plugin-api \
	maven/maven-repository-metadata \
	maven-wagon/provider-api \
	plexus-classworlds \
	plexus-containers/plexus-component-annotations \
	plexus-containers/plexus-container-default \
	plexus/interpolation \
	plexus/utils

for module in \
    maven-artifact \
    maven-artifact-manager \
    maven-model \
    maven-monitor \
    maven-plugin-descriptor \
    maven-plugin-registry \
    maven-profile \
    maven-settings \
    maven-project \
    maven-toolchain; do
  pushd $module
    %{ant} -Dtest.skip=true jar javadoc
  popd
  %{mvn_artifact} ${module}/pom.xml ${module}/target/${module}-%{version}.jar
  mkdir -p target/site/apidocs
  cp -r ${module}/target/site/apidocs target/site/apidocs/${module}
done

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%if 0
for i in maven-{artifact,model,settings}; do
  %pom_xpath_set "ns0:dependency[ns0:artifactId[text()='${i}']]/ns0:requestedVersion" "%{version}" .xmvn-reactor
done
%endif

%files -n maven-artifact -f .mfiles-maven-artifact
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files -n maven-artifact-manager -f .mfiles-maven-artifact-manager
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files -n maven-model -f .mfiles-maven-model
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files -n maven-monitor -f .mfiles-maven-monitor
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files -n maven-plugin-registry -f .mfiles-maven-plugin-registry
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files -n maven-profile -f .mfiles-maven-profile
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files -n maven-project -f .mfiles-maven-project
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files -n maven-settings -f .mfiles-maven-settings
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files -n maven-toolchain -f .mfiles-maven-toolchain
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files -n maven-plugin-descriptor -f .mfiles-maven-plugin-descriptor
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%files javadoc -f .mfiles-javadoc
%license apache-maven/LICENSE.txt apache-maven/NOTICE.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.1-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven2 2.2.1 compatibility libraries
- Generate and customize the ant build files
