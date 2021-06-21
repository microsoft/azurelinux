Summary:	Docbook-xsl-1.79.1
Name:		docbook-style-xsl
Version:	1.79.1
Release:        10%{?dist}
License:	ASL 2.0
URL:		http://www.docbook.org
Source0:	http://downloads.sourceforge.net/docbook/docbook-xsl-%{version}.tar.bz2
Group:		Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Requires:	libxml2
BuildRequires:	libxml2
BuildRequires:  zip
BuildArch:      noarch

%description
The DocBook XML DTD-4.5 package contains document type definitions for
verification of XML data files against the DocBook rule set. These are
useful for structuring books and software documentation to a standard
allowing you to utilize transformations already written for that standard.
%prep
%setup -qn docbook-xsl-%{version}

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
if [ ! -d /etc/xml ]; then install -v -m755 -d /etc/xml; fi &&
if [ ! -f /etc/xml/catalog ]; then
    xmlcatalog --noout --create /etc/xml/catalog
fi &&

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/1.79.1" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
    /etc/xml/catalog &&

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/1.79.1" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
    /etc/xml/catalog &&

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
    /etc/xml/catalog &&

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
    /etc/xml/catalog
%postun
if [ $1 -eq 0 ] ; then
    if [ -f /etc/xml/catalog ]; then
        xmlcatalog --noout --del \
        "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" /etc/xml/catalog
    fi
fi
%files
%defattr(-,root,root)
%license COPYING
/usr/share/xml/docbook/*
%{_docdir}/*

%changelog
* Sat May 09 00:20:40 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.79.1-10
- Added %%license line automatically

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
