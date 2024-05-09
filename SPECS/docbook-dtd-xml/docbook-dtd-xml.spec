Summary:        Docbook-xml-4.5
Name:           docbook-dtd-xml
Version:        4.5
Release:        11%{?dist}
License:        MIT
URL:            https://www.docbook.org
Source0:        https://docbook.org/xml/4.5/docbook-xml-%{version}.zip
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Requires:       libxml2
BuildRequires:  libxml2
BuildRequires:  unzip
BuildArch:      noarch

%description
The DocBook XML DTD-4.5 package contains document type definitions for
verification of XML data files against the DocBook rule set. These are
useful for structuring books and software documentation to a standard
allowing you to utilize transformations already written for that standard.
%prep
%setup -c -T
unzip %{SOURCE0}
if [ `id -u` -eq 0 ]; then
  chown -R root.root .
  chmod -R a+rX,g-w,o-w .
fi
%build
%install
install -v -d -m755 %{buildroot}/usr/share/xml/docbook/docbook-xml-%{version}
install -v -d -m755 %{buildroot}/etc/xml
chown -R root:root .
cp -v -af docbook.cat *.dtd ent/ *.mod %{buildroot}/usr/share/xml/docbook/docbook-xml-%{version}

%post
if [ ! -e /etc/xml/docbook ]; then
    xmlcatalog --noout --create /etc/xml/docbook
fi &&
xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V4.5//EN" \
    "https://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML CALS Table Model V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/calstblx.dtd" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/soextblx.dtd" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbpoolx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbhierx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML HTML Tables V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/htmltblx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbnotnx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbcentx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbgenent.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "rewriteSystem" \
    "https://www.oasis-open.org/docbook/xml/4.5" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "rewriteURI" \
    "https://www.oasis-open.org/docbook/xml/4.5" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5" \
    /etc/xml/docbook

if [ ! -e /etc/xml/catalog ]; then
    xmlcatalog --noout --create /etc/xml/catalog
fi &&
xmlcatalog --noout --add "delegatePublic" \
    "-//OASIS//ENTITIES DocBook XML" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog &&
xmlcatalog --noout --add "delegatePublic" \
    "-//OASIS//DTD DocBook XML" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog &&
xmlcatalog --noout --add "delegateSystem" \
    "https://www.oasis-open.org/docbook/" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog &&
xmlcatalog --noout --add "delegateURI" \
    "https://www.oasis-open.org/docbook/" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog

for DTDVERSION in 4.1.2 4.2 4.3 4.4
do
  xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V$DTDVERSION//EN" \
    "https://www.oasis-open.org/docbook/xml/$DTDVERSION/docbookx.dtd" \
    /etc/xml/docbook
  xmlcatalog --noout --add "rewriteSystem" \
    "https://www.oasis-open.org/docbook/xml/$DTDVERSION" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5" \
    /etc/xml/docbook
  xmlcatalog --noout --add "rewriteURI" \
    "https://www.oasis-open.org/docbook/xml/$DTDVERSION" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5" \
    /etc/xml/docbook
  xmlcatalog --noout --add "delegateSystem" \
    "https://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog
  xmlcatalog --noout --add "delegateURI" \
    "https://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog
done

%preun
if [ $1 -eq 0 ] ; then
    if [ -f /etc/xml/catalog ]; then
        xmlcatalog --noout --del \
        "file:///etc/xml/docbook" /etc/xml/catalog
    fi
    if [ -f /etc/xml/docbook ]; then
        xmlcatalog --noout --del \
        "file:///usr/share/xml/docbook/docbook-xml-4.5" /etc/xml/docbook

        for DTDVERSION in 4.1.2 4.2 4.3 4.4 %{version}
        do
            xmlcatalog --noout --del \
            "https://www.oasis-open.org/docbook/xml/$DTDVERSION/docbookx.dtd" /etc/xml/docbook
        done

        for file in `find /usr/share/xml/docbook/%{name}-%{version}/*.dtd -printf "%f\n"`
        do
            xmlcatalog --noout --del \
            "file:///usr/share/xml/docbook/docbook-xml-4.5/$file" /etc/xml/docbook
        done

        for file in `find /usr/share/xml/docbook/%{name}-%{version}/*.mod -printf "%f\n"`
        do
            xmlcatalog --noout --del \
            "file:///usr/share/xml/docbook/docbook-xml-4.5/$file" /etc/xml/docbook
        done
    fi
fi

%files
%defattr(-,root,root)
/usr/share/xml/docbook/docbook-xml-%{version}
/etc/xml

%changelog
*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 4.5-11
-   Renaming docbook-xml to docbook-dtd-xml
*   Thu Apr 16 2020 Nick Samson <nisamson@microsoft.com> 4.5-10
-   Updated Source0, URL. Removed sha1. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.5-9
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 4.5-8
-   Remove libxml2-python from requires.
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.5-7
-   Fix arch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.5-6
-   GA - Bump release of all rpms
*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  4.5-5
-   Fixing spec file to handle rpm upgrade scenario correctly
*   Thu Mar 10 2016 XIaolin Li <xiaolinl@vmware.com> 4.5.1-4
-   Correct the local folder name.
*   Mon Jul 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.5.1-3
-   Updated dependencies.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 4.5.1-2
-   Updated group.
*   Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 4.5-1
-   Initial build. First version
