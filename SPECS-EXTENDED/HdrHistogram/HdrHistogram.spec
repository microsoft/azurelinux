Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          HdrHistogram
Version:       2.1.11
Release:       3%{?dist}
Summary:       A High Dynamic Range (HDR) Histogram
License:       BSD and CC0
URL:           http://hdrhistogram.github.io/%{name}/
Source0:       https://github.com/%{name}/%{name}/archive/%{name}-%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(com.google.code.maven-replacer-plugin:replacer)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)
# fedora 25
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
# Explicit requires for javapackages-tools since HistogramLogProcessor script
# uses /usr/share/java-utils/java-functions
Requires:      javapackages-tools

BuildArch:     noarch

%description
HdrHistogram supports the recording and analyzing sampled data value
counts across a configurable integer value range with configurable value
precision within the range. Value precision is expressed as the number of
significant digits in the value recording, and provides control over value
quantization behavior across the value range and the subsequent value
resolution at any given level.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}
find  -name "*.class"  -print -delete
find  -name "*.jar"  -print -delete

%pom_remove_plugin :maven-dependency-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :nexus-staging-maven-plugin

%pom_xpath_set "pom:plugin[pom:groupId = 'com.google.code.maven-replacer-plugin' ]/pom:artifactId" replacer

%mvn_file :%{name} %{name}

%build
%mvn_build

%install
%mvn_install

%jpackage_script org.%{name}.HistogramLogProcessor "" "" %{name} HistogramLogProcessor true

%files -f .mfiles
%{_bindir}/HistogramLogProcessor
%doc README.md
%license COPYING.txt LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license COPYING.txt LICENSE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.11-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 10 2019 Jie Kang <jkang@redhat.com> - 2.1.11-1
- Update to 2.1.11

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 31 2018 Severin Gehwolf <sgehwolf@redhat.com> - 2.1.9-6
- Add explicit requirement on javapackages-tools for script which
  uses java-functions. See RHBZ#1600426.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 21 2016 Tomas Repik <trepik@redhat.com> - 2.1.9-1
- Update to 2.1.9

* Mon Mar 07 2016 Tomas Repik <trepik@redhat.com> - 2.1.8-1
- launcher HistogramLogProcessor installation
- Update to 2.1.8

* Thu Oct 22 2015 gil cattaneo <puntogil@libero.it> 2.1.7-1
- initial rpm
