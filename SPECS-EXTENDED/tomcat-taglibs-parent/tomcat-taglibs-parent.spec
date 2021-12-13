Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           tomcat-taglibs-parent
Version:        3
Release:        13%{?dist}
Summary:        Apache Taglibs Parent

License:        ASL 2.0
URL:            http://tomcat.apache.org/taglibs/
Source0:        http://svn.apache.org/repos/asf/tomcat/taglibs/taglibs-parent/tags/taglibs-parent-3/pom.xml
Source1:        %{name}-LICENSE.txt
BuildArch: noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

%description
Apache Taglibs Parent pom used for building purposes.

%prep
%setup -q -c -T
cp -p %{SOURCE0} .
cp %{SOURCE1} ./LICENSE.txt

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%dir %{_mavenpomdir}/%{name}

%changelog
* Fri Dec 10 2021 Thomas Crain <thcrain@microsoft.com> - 3-13
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 4 2015 Alexander Kurtakov <akurtako@redhat.com> 3-2
- Fix review issues.

* Wed Mar 4 2015 Alexander Kurtakov <akurtako@redhat.com> 3-1
- Initial package.
