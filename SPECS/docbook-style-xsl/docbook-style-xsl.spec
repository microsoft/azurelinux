Summary:        Docbook-xsl-1.79.1
Name:           docbook-style-xsl
Version:        1.79.1
Release:        12%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.docbook.org
Source0:        http://downloads.sourceforge.net/docbook/docbook-xsl-%{version}.tar.bz2
BuildRequires:  libxml2
BuildRequires:  zip
Requires:       libxml2
Provides:       docbook-xsl = %{version}-%{release}
Provides:       docbook-xsl-stylesheets = %{version}-%{release}
BuildArch:      noarch

%description
The DocBook XML DTD-4.5 package contains document type definitions for
verification of XML data files against the DocBook rule set. These are
useful for structuring books and software documentation to a standard
allowing you to utilize transformations already written for that standard.

%prep
%setup -q -n docbook-xsl-%{version}

%build
zip -d tools/lib/jython.jar Lib/distutils/command/wininst-6.exe
zip -d tools/lib/jython.jar Lib/distutils/command/wininst-7.1.exe

%install
install -v -m755 -d %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.79.1 &&

cp -v -R VERSION common eclipse epub extensions fo highlighting html \
         htmlhelp images javahelp lib manpages params profiling \
         roundtrip slides template tests tools webhelp website \
         xhtml xhtml-1_1 \
    %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.79.1

pushd %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.79.1
rm extensions/saxon65.jar
rm tools/lib/saxon.jar
rm tools/lib/saxon9-ant.jar
rm tools/lib/saxon9he.jar
ln -s VERSION VERSION.xsl
popd

install -v -m644 -D README \
                    %{buildroot}%{_docdir}/docbook-xsl-%{version}/README.txt &&
install -v -m644    RELEASE-NOTES* NEWS* \
                    %{buildroot}%{_docdir}/docbook-xsl-%{version}

#There is no source code for make check
#%check
#chmod 777 tests -R
#make %{?_smp_mflags} check

%post
if [ ! -d %{_sysconfdir}/xml ]; then install -v -m755 -d %{_sysconfdir}/xml; fi &&
if [ ! -f %{_sysconfdir}/xml/catalog ]; then
    xmlcatalog --noout --create %{_sysconfdir}/xml/catalog
fi &&

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/1.79.1" \
           "%{_datadir}/xml/docbook/xsl-stylesheets-1.79.1" \
    %{_sysconfdir}/xml/catalog &&

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/1.79.1" \
           "%{_datadir}/xml/docbook/xsl-stylesheets-1.79.1" \
    %{_sysconfdir}/xml/catalog &&

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "%{_datadir}/xml/docbook/xsl-stylesheets-1.79.1" \
    %{_sysconfdir}/xml/catalog &&

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "%{_datadir}/xml/docbook/xsl-stylesheets-1.79.1" \
    %{_sysconfdir}/xml/catalog

%postun
if [ $1 -eq 0 ] ; then
    if [ -f %{_sysconfdir}/xml/catalog ]; then
        xmlcatalog --noout --del \
        "%{_datadir}/xml/docbook/xsl-stylesheets-1.79.1" %{_sysconfdir}/xml/catalog
    fi
fi

%files
%defattr(-,root,root)
%license COPYING
%{_datadir}/xml/docbook/*
%{_docdir}/*

%changelog
* Tue Dec 01 2020 Joe Schmitt <joschmit@microsoft.com> - 1.79.1-12
- Provide docbook-xsl-stylesheets.

*   Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 1.79.1-11
-   Provide docbook-xsl

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.79.1-10
-   Added %%license line automatically

*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 1.79.1-9
-   Renaming docbook-xsl to docbook-style-xsl

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.79.1-8
-   Initial CBL-Mariner import from Photon (license: Apache2).

*       Fri Jan 18 2019 Tapas Kundu <tkundu@vmware.com> 1.79.1-7
-       Removed saxon jar files while installing

*	Tue Dec 04 2018 Ashwin H<ashwinh@vmware.com> 1.79.1-6
-       Remove windows installers

*	Fri Aug 18 2017 Rongrong Qiu <rqiu@vmware.com> 1.79.1-5
-	Update make check for bug 1635477

*	Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.79.1-4
-	Fix arch

*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.79.1-3
-	GA - Bump release of all rpms

*       Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  1.79.1-2
-	Fixing spec file to handle rpm upgrade scenario correctly

*       Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 1.79.1-1
-       Updated version.

*       Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.78.1-2
-       Updated group.

*	Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 1.78.1-1
-	Initial build. First version
