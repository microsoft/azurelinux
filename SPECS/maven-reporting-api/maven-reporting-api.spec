Summary:        API to manage report generation
Name:           maven-reporting-api
Version:        3.1.1
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://maven.apache.org/shared/maven-reporting-api
Source0:        https://archive.apache.org/dist/maven/reporting/%{name}-%{version}-source-release.zip
BuildArch:      noarch
BuildRequires:  gnupg2
BuildRequires:  maven-local
# BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  maven-parent
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)

%description
API to manage report generation.  Maven-reporting-api is included in the
Maven 2.x core distribution, but was moved to shared components to
achieve report decoupling from the Maven 3 core.

%prep
# %{gpgverify} --data=%{SOURCE0} --signature=%{SOURCE1} --keyring=%{SOURCE2}
%autosetup

# Fix end of line encoding
sed -i.orig 's/\\r//' README.md
touch -r README.md.orig README.md
rm README.md.orig

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE NOTICE

%changelog
* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1:3.1.1-6
- Rebuilt for java-21-openjdk as system jdk
