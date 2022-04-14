Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: relaxngcc
Version: 1.12
Release: 19%{?dist}
Summary: RELAX NG Compiler Compiler

License: ASL 1.1

Url: http://relaxngcc.sourceforge.net/en/index.htm

Source0: http://prdownloads.sourceforge.net/relaxngcc/relaxngcc-20031218.zip
Source1: %{name}-build.xml

BuildRequires: ant
BuildRequires: java-devel
BuildRequires: javacc
BuildRequires: jpackage-utils
BuildRequires: msv-msv
BuildRequires: msv-xsdlib
BuildRequires: relaxngDatatype
BuildRequires: isorelax
BuildRequires: xerces-j2
BuildRequires: xml-commons-apis
BuildRequires: dos2unix

Requires: msv-msv
Requires: msv-xsdlib
Requires: relaxngDatatype
Requires: isorelax
Requires: xerces-j2
Requires: xml-commons-apis

BuildArch: noarch


%description
RelaxNGCC is a tool for generating Java source code from a given RELAX NG
grammar. By embedding code fragments in the grammar like yacc or JavaCC, you can
take appropriate actions while parsing valid XML documents against the grammar.


%package javadoc
Summary: Javadoc for %{name}


%description javadoc
This package contains javadoc for %{name}.


%prep

# Prepare the original sources:
%setup -q -n relaxngcc-20031218

# Remove all the binary files:
find . -name '*.class' -delete
find . -name '*.jar' -delete

# Remove the sources that will be generated with JavaCC:
rm src/relaxngcc/javabody/*.java

# Remove to avoid dependency on commons-jelly:
rm src/relaxngcc/maven/ChildAntProjectTag.java

# Some of the sources don't use the correct end of line encoding, so to be
# conservative fix all of them:
find . -type f -exec dos2unix {} \;

# Some of the source files contain characters outside of the ASCII set that
# cause problems when compiling, so make sure that they are translated to
# ASCCI:
sources='
src/relaxngcc/builder/SwitchBlockInfo.java
'
for source in ${sources}
do
  native2ascii -encoding UTF8 ${source} ${source}
done


%build

# Populate the lib directory with references to the jar files required for the
# build:
mkdir lib
build-jar-repository -p lib \
  msv-msv msv-xsdlib relaxngDatatype isorelax javacc

# Put the ant build files in place:
cp %{SOURCE1} build.xml

# Run the ant build:
ant jar javadoc


%install

# Jar files:
mkdir -p %{buildroot}%{_javadir}
install -pm 644 relaxngcc.jar %{buildroot}%{_javadir}/%{name}.jar

# Javadoc files:
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr javadoc/* %{buildroot}%{_javadocdir}/%{name}/.


%files
%{_javadir}/*
%doc src/HOWTO-readAutomata.txt LICENSE.txt readme.txt
%doc doc/*


%files javadoc
%{_javadocdir}/*
%doc LICENSE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Stephen Gallagher <sgallagh@redhat.com> - 1.12-11
- Add BR on java-devel for native2ascii

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 11 2015 Mat Booth <mat.booth@redhat.com> - 1.12-8
- Fix FTBFS rhbz#1107006

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.12-3
- Changed license to ASL 1.1

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.12-2
- Cleanups of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 1.12-1
- Initial packaging
