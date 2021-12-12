Vendor:         Microsoft Corporation
Distribution:   Mariner
%global base_name       antunit

Name:             ant-%{base_name}
Version:          1.3
Release:          14%{?dist}
Summary:          Provide antunit ant task
License:          ASL 2.0
URL:              http://ant.apache.org/antlibs/%{base_name}/
Source0:          http://www.apache.org/dist/ant/antlibs/%{base_name}/source/apache-%{name}-%{version}-src.tar.bz2
BuildArch:        noarch

BuildRequires:    javapackages-local
BuildRequires:    ant
BuildRequires:    ant-junit
BuildRequires:    ant-testutil


%description
The <antunit> task drives the tests much like <junit> does for JUnit tests.

When called on a build file, the task will start a new Ant project for that
build file and scan for targets with names that start with "test". For each
such target it then will:

   1. Execute the target named setUp, if there is one.
   2. Execute the target itself - if this target depends on other targets the
      normal Ant rules apply and the dependent targets are executed first.
   3. Execute the target names tearDown, if there is one.


%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n apache-%{name}-%{version}
mv CONTRIBUTORS CONTRIBUTORS.orig
iconv -f ISO-8859-1 -t UTF-8 CONTRIBUTORS.orig > CONTRIBUTORS
touch -r CONTRIBUTORS.orig CONTRIBUTORS


%build
ant package


%install
%mvn_artifact %{name}-%{version}.pom build/lib/%{name}-%{version}.jar
%mvn_file ":ant-antunit" ant/ant-antunit
%mvn_install -J docs/

# OPT_JAR_LIST fragments
mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "ant/%{name}" > %{buildroot}%{_sysconfdir}/ant.d/%{base_name}


%files -f .mfiles
%license LICENSE NOTICE
%doc CONTRIBUTORS README README.html WHATSNEW
%config(noreplace) %{_sysconfdir}/ant.d/%{base_name}

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 23 2017 Mat Booth <mat.booth@redhat.com> - 1.3-8
- Fix failure to build from source

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 28 2017 Orion Poplawski <orion@cora.nwra.com> 1.3-6
- BR ant

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Orion Poplawski <orion@cora.nwra.com> 1.3-1
- Update to 1.3

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2-13
- Use Requires: java-headless rebuild (#1067528)

* Thu Aug 15 2013 Orion Poplawski <orion@cora.nwra.com> 1.2-12
- Another attempt at fixing the install

* Thu Aug 15 2013 Orion Poplawski <orion@cora.nwra.com> 1.2-11
- Fix install locations (bug 988561)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-9
- Update to current packaging guidelines

* Wed Jun 12 2013 Orion Poplawski <orion@cora.nwra.com> 1.2-7
- Update spec for new Java guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-5
- Remove ppc64 ExcludeArch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 6 2012 Orion Poplawski <orion@cora.nwra.com> 1.2-3
- Drop junit4 references

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan 4 2012 Orion Poplawski <orion@cora.nwra.com> 1.2-1
- Update to 1.2

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Orion Poplawski <orion@cora.nwra.com> 1.1-4
- ExcludeArch ppc64 - no java >= 1:1.6.0 on ppc64

* Mon Dec 6 2010 Orion Poplawski <orion@cora.nwra.com> 1.1-3
- Rename to ant-antunit
- Drop BuildRoot and %%clean
- Drop unneeded Provides

* Fri Oct 29 2010 Orion Poplawski <orion@cora.nwra.com> 1.1-2
- Add /etc/ant.d/antunit
- Add Requires: ant

* Thu Oct 28 2010 Orion Poplawski <orion@cora.nwra.com> 1.1-1
- Initial package
