# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Don't ship Java extensions in Fedora as they are not compiled from the source
# Shipping sources instead of binary jars was requested by
# https://lists.oasis-open.org/archives/docbook-apps/201408/msg00008.html
# Sources available in the docbook stylesheets svn repository, but not packaged.
%bcond extensions 0

Name: docbook5-style-xsl
Version: 1.79.2
Release: 25%{?dist}

Summary: Norman Walsh's XSL stylesheets for DocBook 5.X

# Package is licensed as MIT/X (http://wiki.docbook.org/topic/DocBookLicense),
# some .js files under ./slides/browser/ are licensed MPLv1.1
# Automatically converted from old format: MIT and MPLv1.1 - review is highly recommended.
License: LicenseRef-Callaway-MIT AND LicenseRef-Callaway-MPLv1.1
URL: https://github.com/docbook/xslt10-stylesheets

Provides: docbook-xsl-ns = %{version}
# xml-common was using /usr/share/xml until 0.6.3-8.
Requires: xml-common >= 0.6.3-8
# libxml2 required because of usage of /usr/bin/xmlcatalog
Requires(post): libxml2 >= 2.4.8
Requires(postun): libxml2 >= 2.4.8
Conflicts: passivetex < 1.21

BuildArch: noarch
Source0: https://github.com/docbook/xslt10-stylesheets/releases/download/release%2F{%version}/docbook-xsl-%{version}.tar.bz2

%description
These XSL namespace aware stylesheets allow you to transform any
DocBook 5 document to other formats, such as HTML, manpages, FO,
XHMTL and other formats. They are highly customizable. For more
information see W3C page about XSL.

%if %{with extensions}
%package extensions
Summary: Norman Walsh's XSL stylesheets extensions for DocBook 5.X
# Package is licensed as MIT/X (http://wiki.docbook.org/topic/DocBookLicense),
# some .js files under ./slides/browser/ are licensed MPLv1.1
# Automatically converted from old format: MIT and ASL 2.0 - review is highly recommended.
License: LicenseRef-Callaway-MIT AND Apache-2.0
Requires: docbook-xsl-ns = %{version}
# Provide an alternative to removed JAR files via Fedora Packages
# lucene-core.jar (lucene-core-3.0.0.jar), lucene-analysis-common.jar (lucene-analyzers-3.0.0.jar)
Requires: lucene-core lucene-analysis-common
# ant-apache-xalan2.jar (xalan27.jar)
Requires: ant-apache-xalan2
# tagsoup.jar (tagsoup-1.2.1.jar)
Requires: tagsoup

%description extensions
This package contains Java extensions for XSL namespace aware stylesheets.
%endif

%prep
%setup -q -n docbook-xsl-%{version}

# Remove .gitignore files
rm -rf $(find -name '.gitignore' -type f)

# Remove ant buildsystem
find . -name build.xml -delete

# Remove binary JAR files
rm -f extensions/*.jar
rm -fr tools/

# Make ruby scripts executable
chmod +x epub/bin/dbtoepub

# Remove misc
rm slides/slidy/scripts/slidy.js.gz
rm roundtrip/template.dot

%build

%install
DESTDIR=$RPM_BUILD_ROOT
mkdir -p $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version
cp -a [[:lower:]]* $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version/
cp -a VERSION $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version/VERSION.xsl
ln -s VERSION.xsl \
$DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version/VERSION
ln -s xsl-ns-stylesheets-%{version} \
 $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets

# Don't ship install shell script.
rm -rf $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets/install.sh

%files
%doc BUGS
%doc README COPYING
%doc TODO NEWS
%doc RELEASE-NOTES.*
%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}
%{_datadir}/sgml/docbook/xsl-ns-stylesheets
%exclude %{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}/extensions

%if %{with extensions}
%files extensions
%doc extensions/README.txt extensions/LICENSE.txt
%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}/extensions
%endif

%post
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://cdn.docbook.org/release/xsl/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://cdn.docbook.org/release/xsl/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://cdn.docbook.org/release/xsl/current/" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://cdn.docbook.org/release/xsl/current/" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG

%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl-ns/current" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl-ns/current" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG

%postun
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
   "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
fi

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 1.79.2-22
- convert license to SPDX

* Tue Jul 23 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.79.2-21
- Drop unused tools directory
- Limit Java dependency to extensions subpackage

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 29 2024 Ondrej Sloup <osloup@redhat.com> - 1.79.2-19
- Remove binary JAR files and replace them with available dependencies (rhbz#2260534)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Ondrej Vasik <ovasik@redhat.com> - 1.79.2-2
- keep the old sourceforge URI rewrites at least temporarily

* Mon Jan 02 2017 Ondrej Vasik <ovasik@redhat.com> - 1.79.2-1
- new upstream release 1.79.2
- upstream moved to github, switch online content to docbook CDN

* Fri Jul 08 2016 Ondrej Vasik <ovasik@redhat.com> - 1.79.1-1
- new upstream release 1.79.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.78.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.78.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 05 2014 Ondrej Vasik <ovasik@redhat.com> 1.78.1-6
- Don't ship Java extensions on Fedora until compiled from
  sources

* Wed Jul 16 2014 Ondrej Vasik <ovasik@redhat.com> 1.78.1-5
- fix the extensions inclusion

* Wed Jul 16 2014 Ondrej Vasik <ovasik@redhat.com> 1.78.1-4
- include extensions in extensions subpackage (#1084491)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.78.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.78.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Ondrej Vasik <ovasik@redhat.com> 1.78.1-1
- new upstream release 1.78.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.78.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Ondrej Vasik <ovasik@redhat.com> 1.78.0-2
- resolve missing VERSION.xsl (#891459)

* Thu Dec 20 2012 Ondrej Vasik <ovasik@redhat.com> 1.78.0-1
- new upstream release 1.78.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.77.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Ondrej Vasik <ovasik@redhat.com> 1.77.1-1
- new upstream release 1.77.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 02 2010 Ondrej Vasik <ovasik@redhat.com> 1.76.1-1
- new upstream release 1.76.1

* Mon Sep 06 2010 Ondrej Vasik <ovasik@redhat.com> 1.76.0-1
- new upstream release 1.76.0

* Tue Feb 23 2010 Ondrej Vasik <ovasik@redhat.com> 1.75.2-4
- fix the licenses, use better URL

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.75.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.2-2
- upstream changed tarballs after release

* Tue Jul 21 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.2-1
- new upstream release 1.75.2

* Thu May 28 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.1-1
- new upstream release 1.75.1

* Mon May 11 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.0-1
- new upstream release 1.75.0

* Wed Mar 11 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.3-1
- new upstream release 1.74.3

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.74.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.2-1
- new upstream release 1.74.2

* Wed Feb 18 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.1-1
- new upstream release 1.74.1

* Fri Feb 13 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.0-2
- Ship VERSION file (#485297) , ship RELEASE-NOTES

* Mon Nov 10 2008 Ondrej Vasik <ovasik@redhat.com> 1.74.0-1
- Initial Fedora release
