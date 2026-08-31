# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global bits %{__isa_bits}
%global debug_package %{nil}

# jansi-native-1.8 tag is missing from git
# https://github.com/fusesource/jansi-native/commit/5015ad0
%global commit 5015ad023a55785dbe6ad19cc786c0533387feff

Name:           jansi-native
Version:        1.8
Release:        23%{?dist}
Summary:        Jansi Native implements the JNI Libraries used by the Jansi project
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            http://jansi.fusesource.org/
Source0:        https://github.com/fusesource/jansi-native/archive/%{commit}/jansi-native-%{version}.tar.gz

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.fusesource:fusesource-pom:pom:)
# jansi-native is embedded in jansi 2.x
BuildRequires:  mvn(org.fusesource.jansi:jansi)
BuildRequires:  mvn(org.fusesource.hawtjni:hawtjni-runtime) >= 1.9-2
# jansi-native provides JNI libraries for use by the JAVA Jansi project,
# so it is only necessary on java_arches
ExclusiveArch:  %{java_arches}

%description
Jansi is a small java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it like Windows and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences.

%package javadoc
Summary:          Javadocs for %{name}
BuildArch:        noarch

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jansi-native-%{commit}

%mvn_alias :jansi-linux%{bits} :jansi-linux
%mvn_file :jansi-linux%{bits} %{name}/jansi-linux%{bits} %{name}/jansi-linux

# use more modern source and target settings
%pom_xpath_set //pom:source 1.8
%pom_xpath_set //pom:target 1.8

# fix javadoc generation for java 11
%pom_remove_plugin :maven-javadoc-plugin
%pom_xpath_inject pom:pluginManagement/pom:plugins "<plugin>
<artifactId>maven-javadoc-plugin</artifactId>
<configuration>
<source>1.8</source>
<detectJavaApiLink>false</detectJavaApiLink>
</configuration>
</plugin>"

%pom_xpath_remove "pom:plugin[pom:artifactId='hawtjni-maven-plugin']"

%build
%mvn_build

# copy libjansi.so
so_dir=target/generated-sources/hawtjni/lib/META-INF/native/linux%{bits}/
mkdir -p $so_dir
cp -a %{_prefix}/lib/jansi/libjansi.so $so_dir

%mvn_build -- -Dplatform=linux%{bits}

%install
%mvn_install

%files -f .mfiles
%doc readme.md changelog.md
%license license.txt

%files javadoc -f .mfiles-javadoc
%license license.txt

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.8-23
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.8-20
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.8-18
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug 01 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.8-15
- rebuilt w/ no changes

* Tue Aug 01 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.8-14
- Copy libjansi.so from jansi 2.x (jansi package)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 16 2022 Hans de Goede <hdegoede@redhat.com> - 1.8-10
- jansi-native provides JNI libraries for use by the JAVA Jansi project and
  the JDK is no longer build on i686, disable i686 builds (rhbz#2104052)

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.8-9
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug  2 2021 Jerry James <loganjerry@gmail.com> - 1.8-7
- Fix maven-compiler-plugin settings (bz 1987588)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.8-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jun 26 2020 Mat Booth <mat.booth@redhat.com> - 1.8-3
- Allow building against Java 11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 05 2019 Fabio Valentini <decathorpe@gmail.com> - 1.8-1
- Update to version 1.8.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 Michael Simacek <msimacek@redhat.com> - 1.7-7
- Build missing native lib

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.7-5
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Michael Simacek <msimacek@redhat.com> - 1.7-1
- Update to upstream version 1.7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug 03 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.5-7
- Fix FTBFS due to XMvn changes in F21 (#1106820)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5-5
- Cleanup BuildRequires

* Thu Mar  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5-4
- Require hawtjni >= 1.9-2

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-4
- Use Requires: java-headless rebuild (#1067528)

* Fri Jan 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5-4
- Install attached artifacts
- Resolves: rhbz#1028550

* Tue Nov 26 2013 Marek Goldmann <mgoldman@redhat.com> - 1.5-3
- Mark javadoc subpackage as noarch

* Mon Nov 25 2013 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.5-2
- Use %%__isa_bits macro to support all architectures

* Wed Sep 11 2013 Marek Goldmann <mgoldman@redhat.com> - 1.5-1
- Upstream release 1.5

* Tue Aug 06 2013 Marek Goldmann <mgoldman@redhat.com> - 1.4-7
- New guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Dec 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-3
- revbump after jnidir change

* Wed Dec 12 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-2
- Move normal jar from javajnidir to javadir

* Wed Sep 19 2012 Marek Goldmann <mgoldman@redhat.com> - 1.4-1
- Upstream release 1.4
- Fixing "archiver requires 'AM_PROG_AR' in 'configure.ac'" error
- FTBFS: config.status: error: cannot find input file: `Makefile.in' RHBZ#858377

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Dan Horák <dan[at]danny.cz> 1.2-2
- fix build on non-x86 64-bit arches

* Thu Jul 28 2011 Marek Goldmann <mgoldman@redhat.com> 1.2-1
- Upstream release 1.2
- Using new jnidir

* Tue May 31 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-2
- Updated summary
- Removed debuginfo package
- Added license to javadoc package
- Fixed dependency on maven-hawtjni-plugin

* Fri May 27 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-1
- Initial packaging

