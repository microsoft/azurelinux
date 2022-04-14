Vendor:         Microsoft Corporation
Distribution:   Mariner
# TODO:
# - Install dtdinst's schemas, XSL etc as non-doc and to system catalogs?
# - Drop isorelax and xerces license texts and references to them because
#   our package does not actually contain them?


%global headless -headless


Name:           jing-trang
Version:        20151127
Release:        10%{?dist}
Summary:        Schema validation and conversion based on RELAX NG

License:        BSD
URL:            https://github.com/relaxng/jing-trang
Source0:        https://github.com/relaxng/jing-trang/archive/V%{version}.tar.gz
# Applicable parts submitted upstream:
# https://github.com/relaxng/jing-trang/pull/215
# https://github.com/relaxng/jing-trang/pull/216
Patch0:         0001-Various-build-fixes.patch
# Saxon "HE" doesn't work for this, no old Saxon available, details in #655601
Patch1:         0002-Use-Xalan-instead-of-Saxon-for-the-build-655601.patch
Patch2:         %{name}-20091111-datatype-sample.patch
BuildArch:      noarch

%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires:  ant-trax
%else
BuildRequires:  ant >= 1.8.2
%endif
BuildRequires:  bsh
BuildRequires:  isorelax
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  javacc
BuildRequires:  jpackage-utils
BuildRequires:  qdox
BuildRequires:  relaxngDatatype
BuildRequires:  relaxngDatatype-javadoc
BuildRequires:  testng
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-resolver

%description
%{summary}.

%package     -n jing
Summary:        RELAX NG validator in Java
Requires:       jpackage-utils
Requires:       java%{?headless} >= 1.5.0
Requires:       relaxngDatatype
Requires:       xerces-j2
Requires:       xml-commons-resolver

%description -n jing
Jing is a RELAX NG validator written in Java.  It implements the RELAX
NG 1.0 Specification, RELAX NG Compact Syntax, and parts of RELAX NG
DTD Compatibility, specifically checking of ID/IDREF/IDREFS.  It also
has experimental support for schema languages other than RELAX NG;
specifically W3C XML Schema, Schematron 1.5, and Namespace Routing
Language.

%package     -n trang
Summary:        Multi-format schema converter based on RELAX NG
Requires:       jpackage-utils
Requires:       java%{?headless} >= 1.5.0
Requires:       relaxngDatatype
Requires:       xerces-j2
Requires:       xml-commons-resolver

%description -n trang
Trang converts between different schema languages for XML.  It
supports the following languages: RELAX NG (both XML and compact
syntax), XML 1.0 DTDs, W3C XML Schema.  A schema written in any of the
supported schema languages can be converted into any of the other
supported schema languages, except that W3C XML Schema is supported
for output only, not for input.

%package     -n dtdinst
Summary:        XML DTD to XML instance format converter
Requires:       jpackage-utils
Requires:       java%{?headless} >= 1.5.0

%description -n dtdinst
DTDinst is a program for converting XML DTDs into an XML instance
format.


%prep
%setup -q
rm -r gcj mod/datatype/src/main/org $(find . -name "*.jar")
%patch0 -p1
%patch1 -p1
%patch2 -p1
sed -i -e 's/\r//g' lib/isorelax.copying.txt
# No "old" saxon available in Fedora, and "new" one can be skipped altogether
find . -name "*Saxon*.java" -delete
sed -i -e 's|"\(copying\.txt\)"|"%{_licensedir}/dtdinst/\1"|' \
    dtdinst/index.html
sed -i -e 's|"\(copying\.txt\)"|"%{_licensedir}/trang/\1"|' \
    trang/doc/trang.html trang/doc/trang-manual.html


%build
CLASSPATH=$(build-classpath \
    beust-jcommander xalan-j2 xalan-j2-serializer) \
%ant -Dlib.dir=%{_javadir} -Dbuild.sysclasspath=last dist


%install
rm -rf %{buildroot} *-%{version}

install -d -m 0755 %{buildroot}%{_javadir}

%{__unzip} build/dist/jing-%{version}.zip
install -Dpm 644 jing-%{version}/bin/jing.jar %{buildroot}%{_javadir}
rm -f jing-%{version}/sample/datatype/datatype-sample.jar
%jpackage_script com.thaiopensource.relaxng.util.Driver "" "" jing:relaxngDatatype:xml-commons-resolver:xerces-j2 jing true
mkdir -p jing-%{version}/_licenses
mv jing-%{version}/doc/*copying.* jing-%{version}/_licenses

%{__unzip} build/dist/trang-%{version}.zip
install -pm 644 trang-%{version}/trang.jar %{buildroot}%{_javadir}
%jpackage_script com.thaiopensource.relaxng.translate.Driver "" "" trang:relaxngDatatype:xml-commons-resolver:xerces-j2 trang true

%{__unzip} build/dist/dtdinst-%{version}.zip
install -pm 644 dtdinst-%{version}/dtdinst.jar %{buildroot}%{_javadir}
%jpackage_script com.thaiopensource.xml.dtd.app.Driver "" "" dtdinst dtdinst true

%files -n jing
%license jing-%{version}/_licenses/*
%doc jing-%{version}/{readme.html,doc,sample}
%{_bindir}/jing
%{_javadir}/jing.jar

%files -n trang
%license trang-%{version}/copying.txt
%doc trang-%{version}/*.html
%{_bindir}/trang
%{_javadir}/trang.jar

%files -n dtdinst
%license dtdinst-%{version}/copying.txt
%doc dtdinst-%{version}/*.{html,rng,xsl}
%doc dtdinst-%{version}/{dtdinst.rnc.txt,teixml.dtd.txt,example}
%{_bindir}/dtdinst
%{_javadir}/dtdinst.jar


%changelog
* Wed Nov 03 2021 Muhammad Falak <mwani@microsft.com> - 20151127-10
- Remove epoch from java-devel

* Tue Aug 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20151127-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing not needed "jing-javadoc" subpackage to limit external dependencies.
- Fixing the '%%install' section by creating '%%{buildroot}%%{_javadir}' before populating it.
- Changing BR "java-devel-openjdk" to CBL-Mariner's "java-devel".

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20151127-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20151127-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20151127-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 03 2018 Jan Pokorný <jpokorny+rpm-jing-trang@fedoraproject.org> - 20151127-5
- Do not BuildRequire Saxon anymore

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20151127-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20151127-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Ville Skyttä <ville.skytta@iki.fi> - 20151127-2
- Update to 20151127
- Clean up some obsolete specfile constructs

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20131210-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20131210-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20131210-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Ville Skyttä <ville.skytta@iki.fi> - 20131210-5
- Clean up pre-EL6 specfile constructs

* Wed Sep 16 2015 Ville Skyttä <ville.skytta@iki.fi> - 20131210-4
- Use new upstream github tarball

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131210-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 Ville Skyttä <ville.skytta@iki.fi> - 20131210-2
- Apply upstream BTS patch to fix build with Java 8
- Ship license files as %%license where available

* Mon Jun  9 2014 Ville Skyttä <ville.skytta@iki.fi> - 20131210-1
- Update to 20131210

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091111-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 25 2013 Ville Skyttä <ville.skytta@iki.fi> - 20091111-16
- Fix build and depend on headless JRE on EL7 (Jan Pokorný).

* Fri Oct 25 2013 Ville Skyttä <ville.skytta@iki.fi> - 20091111-15
- Depend on headless JRE where available.

* Mon Aug  5 2013 Ville Skyttä <ville.skytta@iki.fi> - 20091111-14
- BuildRequire ant instead of -trax in non-EL builds.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091111-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091111-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091111-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 20091111-10
- Tweak java-devel build dep for buildability without Java 1.6.
- Fix build classpath with recent TestNG.

* Fri Jun 24 2011 Ville Skyttä <ville.skytta@iki.fi> - 20091111-9
- Apply upstream Saxon >= 9.3 patch (#716177).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091111-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Ville Skyttä <ville.skytta@iki.fi> - 20091111-7
- Put Xalan instead of Saxon in build path (regression in -6).
- Build with OpenJDK.

* Tue Nov 30 2010 Ville Skyttä <ville.skytta@iki.fi> - 20091111-6
- Address more comments/TODO's from #655601:
- Patch test suite generation to use Xalan.
- Include license texts in jing-javadoc.
- Make datatype-sample buildable out of the box, drop prebuilt jar.

* Mon Nov 29 2010 Ville Skyttä <ville.skytta@iki.fi> - 20091111-5
- Simplify doc installation (#655601).

* Sun Nov 28 2010 Ville Skyttä <ville.skytta@iki.fi> - 20091111-4
- First Fedora build, combining my earlier separate jing and trang packages.
