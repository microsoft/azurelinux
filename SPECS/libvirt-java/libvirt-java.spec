# The "ant-junit" package is currently unavailable in CBL-Mariner but is only needed to run the "%check" section.
%bcond_with junit

Summary:        Java bindings for the libvirt virtualization API
Name:           libvirt-java
Version:        0.5.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://libvirt.org/
Source:         https://libvirt.org/sources/java/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  java-devel >= 1.5.0
BuildRequires:  jna
BuildRequires:  jpackage-utils
%if 0%{with_check} && 0%{with junit}
BuildRequires:  ant-junit
%endif

Requires:       jna
Requires:       jpackage-utils
Requires:       libvirt-client >= 0.9.12
Requires:       msopenjdk-11

%description
Libvirt-java is a base framework allowing to use libvirt, the virtualization
API though the Java programming language.
It requires libvirt-client >= 0.9.12

%prep
%autosetup -p1

%build
ant build jar

%install
install -d -m0755 %{buildroot}%{_javadir}
install -d -m0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp target/libvirt-%{version}.jar %{buildroot}%{_javadir}/libvirt.jar

%check
%if 0%{with junit}
ant test
%endif

%files
%license LICENSE
%doc AUTHORS NEWS README INSTALL
%{_javadir}/libvirt.jar

%changelog
* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.5.3-1
- Auto-upgrade to 0.5.3 - Azure Linux 3.0 - package upgrades

* Wed Jan 05 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.2-1
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.
- Updated version to 0.5.2.
- Removed the documentation and "devel" subpackages.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 0.4.9-17
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Cole Robinson <crobinso@redhat.com> - 0.4.9-6
- Require java-headless (bz #1068369)

* Mon Jan 06 2014 Cole Robinson <crobinso@redhat.com> - 0.4.9-5
- Remove versioned jars from javadir (bz #1022139)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Cole Robinson <crobinso@redhat.com> - 0.4.9-3
- Fix FTBFS issue (bz #914153)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 14 2012 Daniel Veillard <veillard@redhat.com> - 0.4.9-1
- Change Licence to MIT and release 0.4.9
- Fix IndexOutOfBoundsException for unknown error codes
- Fix javadoc warnings
- Fix typo in Domain.java

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 6 2012 Daniel Veillard <veillard@redhat.com> - 0.4.8-1
- Add flags to StoragePoolRefresh
- use byte[] array for secretGetValue
- Fix for the jna parameter passing issue
- Added domain flags and error constants for libvirt 0.9.12

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 3 2011 Bryan Kearney <bkearney@redhat.com) - 0.4.7-1
- Only throw errors on real errors.
- Remote non thread safe error reporting
- BZ 600819 Incorrect scheduler parameter value passed to native API.

* Mon Jul 6 2010 Bryan Kearney <bkearney@redhat.com) - 0.4.6-1
- Added libvirt support up to 0.8.2 API

* Mon May 24 2010 Bryan Kearney <bkearney@redhat.com) - 0.4.5-1
- Added libvirt support up to 0.8.1 API

* Fri May 14 2010 Bryan Kearney <bkearney@redhat.com> - 0.4.3-1
- Added libvirt API support for up to 0.7.1
- Reduce java dependencies to 1.5
- Improved packaging for javadocs
- Better Free/Close handling

* Fri Jan 29 2010 Bryan Kearney <bkearney@redhat.com> - 0.4.2-1
- Changed Scheduled Parameters to be a Union instead of a Struct.
- Better Pointer mappings in the error callback

* Mon Jan 18 2010 Bryan Kearney <bkearney@redhat.com> - 0.4.1-1
- Better null checking around Scheduled Parameters
- Added error function callback

* Tue Dec 1 2009 Bryan Kearney <bkearney@redhat.com> - 0.4.0-2
- Modified the dependency to be libvirt-client instead of libvirt.

* Tue Nov 24 2009 Bryan Kearney <bkearney@redhat.com> - 0.4.0-1
- Added libvirt APIs up through 0.7.0

* Tue Nov 24 2009 Bryan Kearney <bkearney@redhat.com> - 0.3.2-1
- Added libvirt APIs up through 0.6.1

* Thu Oct 29 2009 Bryan Kearney <bkearney@redhat.com> - 0.3.1-1
- Added maven building tools.
- Fixed connection and domain bugs found by Thomas Treutner

* Wed Jul 29 2009 Bryan Kearney <bkearney@redhat.com> - 0.3.0-1
- refactored the code to use jna (https://jna.dev.java.net/)

* Fri Jul 18 2008 Daniel Veillard <veillard@redhat.com> - 0.2.0-1
- new release 0.2.0
- finished cleanup of APIs

* Thu Jul  3 2008 Daniel Veillard <veillard@redhat.com> - 0.1.2-1
- new release 0.1.2

* Tue Jul  1 2008 Daniel Veillard <veillard@redhat.com> - 0.1.1-1
- new release 0.1.1

* Tue Jun 24 2008 Daniel Veillard <veillard@redhat.com> - 0.1.0-1
- created
