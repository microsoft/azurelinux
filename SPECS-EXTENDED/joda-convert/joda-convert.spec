Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           joda-convert
Version:        1.9.2
Release:        7%{?dist}
Summary:        Java library for conversion to and from standard string formats
License:        ASL 2.0
URL:            https://github.com/JodaOrg/joda-convert/
BuildArch:      noarch

Source0:        https://github.com/JodaOrg/joda-convert/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)

%description
Java library to enable conversion to and from standard string formats.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains the %{summary}.

%prep
%setup -q
%mvn_file : %{name}
sed -i s/\r// *.txt

%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.2-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 18 2017 Michael Simacek <msimacek@redhat.com> - 1.9.2-1
- Update to upstream version 1.9.2

* Tue Aug 22 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.3-1
- Update to upstream version 1.8.3

* Mon Aug 14 2017 Michael Simacek <msimacek@redhat.com> - 1.8.2-1
- Update to upstream version 1.8.2

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.1-5
- Remove unneeded maven-javadoc-plugin invocation

* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 1.8.1-4
- Remove useless plugins

* Tue May 31 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.1-3
- Disable maven-checkstyle-plugin

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 20 2015 Michael Simacek <msimacek@redhat.com> - 1.8.1-1
- Update to upstream version 1.8.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Aug  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-1
- Update to upstream version 1.7

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-1
- Update to upstream version 1.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 14 2013 Mat Booth <fedora@matbooth.co.uk> - 1.3.1-1
- Update to latest upstream, fixes rhbz #919539
- Use XMvn macros

* Tue May 28 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3-2
- Install NOTICE file with javadoc as well
- Use full URL for Source0

* Fri Feb 22 2013 Andy Grimm <agrimm@gmail.com> - 1.3-1
- Update to 1.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Andy Grimm <agrimm@gmail.com> - 1.2-1
- update to 1.2 and pull source tarball correctly

* Tue Oct 18 2011 Andy Grimm <agrimm@gmail.com> - 1.1-1
- Initial package
