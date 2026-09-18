# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           xmvn-connector-ivy
Version:        4.0.0
Release:        8%{?dist}
Summary:        XMvn Connector for Apache Ivy
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://fedora-java.github.io/xmvn/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/fedora-java/xmvn-connector-ivy/releases/download/%{version}/xmvn-connector-ivy-%{version}.tar.xz

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.apache.ivy:ivy)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(org.fedoraproject.xmvn:xmvn-api)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)

%description
This package provides XMvn Connector for Apache Ivy, which provides
integration of Apache Ivy with XMvn.  It provides an adapter which
allows XMvn resolver to be used as Ivy resolver.

%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
This package provides %{summary}.

%prep
%setup -q

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 4.0.0-8
- Rebuilt for java-25-openjdk as preffered jdk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 4.0.0-5
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 4.0.0-3
- Rebuilt for java-21-openjdk as system jdk

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jul 25 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0-1
- Update to upstream version 4.0.0

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0~20210707.d300ce6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0~20210707.d300ce6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0~20210707.d300ce6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 4.0.0~20210707.d300ce6-5
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.0.0~20210707.d300ce6-4
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0~20210707.d300ce6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0~20210707.d300ce6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.0~20210707.d300ce6-1
- Initial packaging

