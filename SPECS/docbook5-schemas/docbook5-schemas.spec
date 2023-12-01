Summary:        Norman Walsh's schemas (DTD, Relax NG, W3C schema) for Docbook 5.X
Name:           docbook5-schemas
Version:        5.1
Release:        3%{?dist}
License:        Freely redistributable without restriction
URL:            https://docbook.org/
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://www.docbook.org/xml/%{version}/docbook-v%{version}-os.zip
Source0:        %{name}-%{version}.zip
Source1:        https://www.docbook.org/xml/5.0/docbook-5.0.zip

Provides: docbook5-dtd = %{version}-%{release}
Provides: docbook5-rng = %{version}-%{release}
Provides: docbook5-sch = %{version}-%{release}
Provides: docbook5-xsd = %{version}-%{release}

Requires(post):     libxml2 >= 2.4.8
Requires(postun):   libxml2 >= 2.4.8
Requires:           xml-common >= 0.6.3-24
BuildRequires:      perl
BuildRequires:      unzip
BuildRequires:      libxml2 >= 2.4.8

BuildArch: noarch


%description
Docbook 5.X is a complete rewrite of Docbook in RELAX NG and not compatible
with previous Docbook versions. This package contains Relax NG , DTD and W3C
schema for Docbook 5.X. Syntax of those schemas is XML-compliant and is
developed by the OASIS consortium.

%prep
%setup -c -T 
mkdir 5.0
mkdir 5.1

#Unzip Docbook 5.0 specification
cd 5.0
unzip %{SOURCE1}
mv docbook-5.0/* .
#Prepare docs to right place
mv docs/ ../
mv README ../
mv ChangeLog ../
cd ..

#Unzip Docbook 5.1 specification
cd 5.1
unzip %{SOURCE0}
mv schemas/rng .
mv schemas/sch .
mv schemas/catalog.xml .
mv schemas/docbook.nvdl .
cd ..

%build
CATALOG=docbook-5.xml
%{_bindir}/xmlcatalog --create --noout $CATALOG
for v in 5.0
do
  # DTD
  %{_bindir}/xmlcatalog --noout --add "public" \
     "-//OASIS//DTD DocBook XML ${v}//EN" \
     "file://%{_datadir}/xml/docbook5/schema/dtd/${v}/docbook.dtd" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "system" \
     "http://www.oasis-open.org/docbook/xml/${v}/dtd/docbook.dtd" \
     "file://%{_datadir}/xml/docbook5/schema/dtd/${v}/docbook.dtd" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "system" \
     "http://docbook.org/xml/${v}/dtd/docbook.dtd" \
     "file://%{_datadir}/xml/docbook5/schema/dtd/${v}/docbook.dtd" ${CATALOG}
  # XSD
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/xsd/docbook.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/docbook.xsd" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/xsd/docbook.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/docbook.xsd" ${CATALOG}
  # XSD + XInclude
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/xsd/docbookxi.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/docbookxi.xsd" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/xsd/docbookxi.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/docbookxi.xsd" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/xsd/xi.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/xi.xsd" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/xsd/xi.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/xi.xsd" ${CATALOG}
  # XLink + XML
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/xsd/xlink.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/xlink.xsd" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/xsd/xlink.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/xlink.xsd" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/xsd/xml.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/xml.xsd" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/xsd/xml.xsd" \
     "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/xml.xsd" ${CATALOG}
done
for v in 5.0 5.1
do
  # RNG
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/rng/docbook.rng" \
     "file://%{_datadir}/xml/docbook5/schema/rng/${v}/docbook.rng" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/rng/docbook.rng" \
     "file://%{_datadir}/xml/docbook5/schema/rng/${v}/docbook.rng" ${CATALOG}
  # RNG+XInclude
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/rng/docbookxi.rng" \
     "file://%{_datadir}/xml/docbook5/schema/rng/${v}/docbookxi.rng" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/rng/docbookxi.rng" \
     "file://%{_datadir}/xml/docbook5/schema/rng/${v}/docbookxi.rng" ${CATALOG}
  # RNC
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/rnc/docbook.rnc" \
     "file://%{_datadir}/xml/docbook5/schema/rng/${v}/docbook.rnc" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/rng/docbook.rnc" \
     "file://%{_datadir}/xml/docbook5/schema/rng/${v}/docbook.rnc" ${CATALOG}
  # RNC+XInclude
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/rnc/docbookxi.rnc" \
     "file://%{_datadir}/xml/docbook5/schema/rng/${v}/docbookxi.rnc" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/rng/docbookxi.rnc" \
     "file://%{_datadir}/xml/docbook5/schema/rng/${v}/docbookxi.rnc" ${CATALOG}
  # Schematron
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://www.oasis-open.org/docbook/xml/${v}/sch/docbook.sch" \
     "file://%{_datadir}/xml/docbook5/schema/sch/${v}/docbook.sch" ${CATALOG}
  %{_bindir}/xmlcatalog --noout --add "uri" \
     "http://docbook.org/xml/${v}/sch/docbook.sch" \
     "file://%{_datadir}/xml/docbook5/schema/sch/${v}/docbook.sch" ${CATALOG}
done
# ---------------------
# Build XML catalog files for each Schema
for v in 5.0 5.1
do
  for s in rng sch; do
   cat=${v}/${s}/catalog.xml
   %{_bindir}/xmlcatalog --noout --create ${cat}
   case $s in
    sch)
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://docbook.org/xml/${v}/${s}/docbook.${s}" \
       "docbook.${s}" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://www.oasis-open.org/docbook/xml/${v}/${s}/docbook.${s}" \
       "docbook.${s}" ${cat}
     ;;
    rng)
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://docbook.org/xml/${v}/${s}/docbook.${s}" \
       "docbook.${s}" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://www.oasis-open.org/docbook/xml/${v}/${s}/docbook.${s}" \
       "docbook.${s}" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://docbook.org/xml/${v}/${s}/docbookxi.${s}" \
       "docbookxi.${s}" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://www.oasis-open.org/docbook/xml/${v}/${s}/docbookxi.${s}" \
       "docbookxi.${s}" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://docbook.org/xml/${v}/${s}/docbook.rnc" \
       "docbook.rnc" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://www.oasis-open.org/docbook/xml/${v}/${s}/docbook.rnc" \
       "docbook.rnc" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://docbook.org/xml/${v}/${s}/docbookxi.rnc" \
       "docbookxi.rnc" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://www.oasis-open.org/docbook/xml/${v}/${s}/docbookxi.rnc" \
       "docbookxi.rnc" ${cat}
     ;;
   esac
  done
done
for v in 5.0
do
  for s in dtd xsd; do
   cat=${v}/${s}/catalog.xml
   %{_bindir}/xmlcatalog --noout --create ${cat}
   case $s in
    dtd)
     %{_bindir}/xmlcatalog --noout --add "public" \
       "-//OASIS//DTD DocBook XML ${v}//EN" \
       "docbook.dtd" ${cat}
     %{_bindir}/xmlcatalog --noout --add "system" \
       "http://www.oasis-open.org/docbook/xml/${v}/dtd/docbook.dtd" \
       "docbook.dtd" ${cat}
     ;;
    xsd)
     # http://www.oasis-open.org/docbook/xml/5.0/xsd/docbookxi.xsd
     # http://www.oasis-open.org/docbook/xml/5.0/xsd/xlink.xsd
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://docbook.org/xml/${v}/${s}/docbook.${s}" \
       "docbook.${s}" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://www.oasis-open.org/docbook/xml/${v}/${s}/docbook.${s}" \
       "docbook.${s}" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://docbook.org/xml/${v}/${s}/docbookxi.${s}" \
       "docbookxi.${s}" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://www.oasis-open.org/docbook/xml/${v}/${s}/docbookxi.${s}" \
       "docbookxi.${s}" ${cat}
     # XLink + XML:
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://docbook.org/xml/${v}/${s}/xlink.xsd" \
       "xlink.xsd" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://www.oasis-open.org/docbook/xml/${v}/${s}/xlink.xsd" \
       "xlink.xsd" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://docbook.org/xml/${v}/${s}/xml.xsd" \
       "xml.xsd" ${cat}
     %{_bindir}/xmlcatalog --noout --add "uri" \
       "http://www.oasis-open.org/docbook/xml/${v}/${s}/xml.xsd" \
       "xml.xsd" ${cat}
     ;;
   esac
  done
done

%install
DOCBOOK5DIR=%{buildroot}%{_datadir}/xml/docbook5
for v in 5.0 5.1
do
mkdir -p ${DOCBOOK5DIR}/schema/rng/$v
mkdir -p ${DOCBOOK5DIR}/schema/sch/$v
install -m644 $v/rng/* ${DOCBOOK5DIR}/schema/rng/$v
install -m644 $v/sch/* ${DOCBOOK5DIR}/schema/sch/$v
done
mkdir -p ${DOCBOOK5DIR}/schema/dtd/5.0
mkdir -p ${DOCBOOK5DIR}/schema/xsd/5.0
install -m644 5.0/dtd/* ${DOCBOOK5DIR}/schema/dtd/5.0
install -m644 5.0/xsd/* ${DOCBOOK5DIR}/schema/xsd/5.0
mkdir -p %{buildroot}%{_bindir}
install -m755 %{version}/tools/db4-entities.pl %{buildroot}%{_bindir}
mkdir -p ${DOCBOOK5DIR}/stylesheet/upgrade
install -m644 %{version}/tools/db4-upgrade.xsl ${DOCBOOK5DIR}/stylesheet/upgrade

mkdir -p %{buildroot}%{_sysconfdir}/xml
install -m644 docbook-5.xml %{buildroot}%{_sysconfdir}/xml/docbook-5.xml

%post
ROOTCATALOG=%{_sysconfdir}/xml/catalog
if [ -w $ROOTCATALOG ]
then
  for v in 5.0 5.1
  do
  %{_bindir}/xmlcatalog --noout --add "delegatePublic" \
    "-//OASIS//DTD DocBook XML ${v}//EN" \
    "file://%{_datadir}/xml/docbook5/schema/dtd/${v}/catalog.xml" \
    $ROOTCATALOG
  %{_bindir}/xmlcatalog --noout --add "delegateURI" \
    "http://docbook.org/xml/${v}/rng/"  \
    "file://%{_datadir}/xml/docbook5/schema/rng/${v}/catalog.xml" \
    $ROOTCATALOG
  %{_bindir}/xmlcatalog --noout --add "delegateURI" \
    "http://docbook.org/xml/${v}/sch/"  \
    "file://%{_datadir}/xml/docbook5/schema/sch/${v}/catalog.xml" \
    $ROOTCATALOG
   done
  %{_bindir}/xmlcatalog --noout --add "delegateURI" \
    "http://docbook.org/xml/5.0/xsd/"  \
    "file://%{_datadir}/xml/docbook5/schema/xsd/${v}/catalog.xml" \
    $ROOTCATALOG
  %{_bindir}/xmlcatalog --noout --add "delegateSystem" \
    "http://docbook.org/xml/5.0/dtd/" \
    "file://%{_datadir}/xml/docbook5/schema/dtd/${v}/catalog.xml" \
    $ROOTCATALOG
  %{_bindir}/xmlcatalog --noout --add "delegateURI" \
    "http://docbook.org/xml/5.0/dtd/" \
    "file://%{_datadir}/xml/docbook5/schema/dtd/${v}/catalog.xml" \
    $ROOTCATALOG
fi

%postun
if [ "$1" = 0 ]; then
  ROOTCATALOG=%{_sysconfdir}/xml/catalog
  if [ -w $ROOTCATALOG ]
  then
    for v in 5.0 5.1
    do
       %{_bindir}/xmlcatalog --noout --del \
       "file://%{_datadir}/xml/docbook5/schema/rng/${v}/catalog.xml" \
       $ROOTCATALOG
       %{_bindir}/xmlcatalog --noout --del \
       "file://%{_datadir}/xml/docbook5/schema/sch/${v}/catalog.xml" \
       $ROOTCATALOG
     done
      %{_bindir}/xmlcatalog --noout --del \
       "file://%{_datadir}/xml/docbook5/schema/dtd/5.0/catalog.xml" \
       $ROOTCATALOG
      %{_bindir}/xmlcatalog --noout --del \
       "file://%{_datadir}/xml/docbook5/schema/xsd/5.0/catalog.xml" \
       $ROOTCATALOG

  fi
fi

%files
%license 5.1/docbook-v5.1-os.html
%doc docs/* README ChangeLog
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xml/docbook-5.xml
%dir %{_datadir}/xml/docbook5/
%dir %{_datadir}/xml/docbook5/schema
%dir %{_datadir}/xml/docbook5/schema/dtd
%dir %{_datadir}/xml/docbook5/schema/rng
%dir %{_datadir}/xml/docbook5/schema/sch
%dir %{_datadir}/xml/docbook5/schema/xsd
%dir %{_datadir}/xml/docbook5/stylesheet
%dir %{_datadir}/xml/docbook5/stylesheet/upgrade
# Docbook5.0
%{_datadir}/xml/docbook5/schema/dtd/5.0
%{_datadir}/xml/docbook5/schema/rng/5.0
%{_datadir}/xml/docbook5/schema/sch/5.0
%{_datadir}/xml/docbook5/schema/xsd/5.0
# Docbook 5.1
%{_datadir}/xml/docbook5/schema/rng/%{version}
%{_datadir}/xml/docbook5/schema/sch/%{version}
%{_datadir}/xml/docbook5/stylesheet/upgrade/db4-upgrade.xsl
%{_bindir}/db4-entities.pl

%changelog
* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 5.1-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 Ondrej Vasik <ovasik@redhat.com> - 5.1-1
- add Docbook 5.1 (no dtd and xsd schemas provided)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.0-10
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Ondrej Vasik <ovasik@redhat.com> 5.0-8
- rebuild to have latest entry in the changelog

* Mon Feb 02 2009 Ondrej Vasik <ovasik@redhat.com> 5.0-2
- do own /usr/share/xml/docbook5 properly(#483341)

* Thu Nov 13 2008 Ondrej Vasik <ovasik@redhat.com> 5.0-1
- Initial Fedora release