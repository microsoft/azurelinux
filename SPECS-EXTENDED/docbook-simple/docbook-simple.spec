Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: docbook-simple
Version: 1.1
Release: 25%{?dist}
Summary: Simplified DocBook is a small subset of the DocBook XML DTD
License: Freely redistributable without restriction
URL: http://www.oasis-open.org/docbook/xml/simple/
Source0: http://www.docbook.org/xml/simple/1.1/%{name}-%{version}.zip
Source1: %{name}.README.redhat
Source2: %{name}.xml
Source3: %{name}.cat
Source4: LICENSE.PTR
BuildArch: noarch
BuildRequires: unzip
Requires: sgml-common
Requires(post): sed
Requires(post): libxml2 >= 2.4.8
Requires(postun): libxml2 >= 2.4.8
Requires: docbook-dtds

%description
Simplified DocBook is an attempt to provide a proper subset of DocBook
that is simultaneously smaller and still useful. Documents written in
the subset must be 100% legal DocBook documents. This is a subset for
single documents (articles, white papers, etc.), so there's no need
for books or sets, just 'articles'. Simplified DocBook documents are 
viewable in online browsers if styled with CSS. (it's XML not SGML).


%prep
# splatter the files into a version-numbered directory
%setup -q -c -n %{version}

# see http://rpm-devel.colug.net/max-rpm/s1-rpm-inside-macros.html
# setup -c creates the dir then changes to it to expand SOURCE0

%build

%install

rm -rf $RPM_BUILD_ROOT

########## install versioned-numbered directory of dtd files ############

DESTDIR=$RPM_BUILD_ROOT%{_datadir}/xml/docbook/simple
mkdir -p $DESTDIR
cp -a ../%{version} $DESTDIR

########## install package catalogs  ################

XML_CAT_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/xml
mkdir -p $XML_CAT_DIR
install -p -m 644 %{SOURCE2} $XML_CAT_DIR

SGML_CAT_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/sgml
mkdir -p $SGML_CAT_DIR
install -p -m 644 %{SOURCE3} $SGML_CAT_DIR

####### FIXME: must copy README.redhat to source directory ########
#######        for %doc to find it, ${SOURCE1} doesn't work ########

cp -p %{SOURCE1} ./README

cp %{SOURCE4} .

%files
%license LICENSE.PTR
%doc sdocbook.css
%doc README
%dir %{_datadir}/xml/docbook/simple/
%{_datadir}/xml/docbook/simple/%{version}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sgml/docbook-simple.cat
%config(noreplace) %{_sysconfdir}/xml/docbook-simple.xml


%post

##################  XML catalog registration #######################

## Define handy variables ##

ROOT_XML_CATALOG=%{_sysconfdir}/xml/catalog
PKG_XML_CATALOG=%{_sysconfdir}/xml/docbook-simple.xml

#### Root XML Catalog Entries ####
#### Delegate appropriate lookups to package catalog ####

if [ -w $ROOT_XML_CATALOG ]
then
        %{_bindir}/xmlcatalog --noout --add "delegatePublic" \
                "-//OASIS//DTD Simplified" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG

        %{_bindir}/xmlcatalog --noout --add "delegateURI" \
                "http://www.oasis-open.org/docbook/xml/simple/1.1/" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG

  # Next line because some resolvers misinterpret uri entries
        %{_bindir}/xmlcatalog --noout --add "delegateSystem" \
                "http://www.oasis-open.org/docbook/xml/simple/1.1/" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG
fi

####################################################################


#################  SGML catalog registration  ######################

ROOT_SGML_CATALOG=%{_sysconfdir}/sgml/catalog
PKG_SGML_CATALOG=%{_sysconfdir}/sgml/docbook-simple.cat

#### Root SGML Catalog Entries ####
#### "Delegate" appropriate lookups to package catalog ####


############## use install-catalog ######################

if [ -w $ROOT_SGML_CATALOG ]
then
# xmlcatalog deletes OVERRIDE YES directive, use install-catalog instead
#         /usr/bin/xmlcatalog --sgml --noout --add \
#     "/etc/sgml/docbook-simple.cat"

  install-catalog --add \
  "$PKG_SGML_CATALOG" \
  "$ROOT_SGML_CATALOG" 1>/dev/null

# Hack to workaround bug in install-catalog
  sed -i '/^CATALOG.*log\"$/d' $PKG_SGML_CATALOG
  sed -i '/^CATALOG.*log$/d' $PKG_SGML_CATALOG   
fi

####################################################################


# Finally, make sure everything in /etc/*ml is readable!
/bin/chmod a+r  %{_sysconfdir}/sgml/*
/bin/chmod a+r  %{_sysconfdir}/xml/*

%postun
##
## SGML and XML catalogs
##
## Jobs: remove package catalog entries from both root catalogs &
##       remove package catalogs

# remove catalog entries only on removal of package
if [ "$1" = 0 ]; then
  %{_bindir}/xmlcatalog --sgml --noout --del \
     %{_sysconfdir}/sgml/catalog \
     %{_sysconfdir}/sgml/docbook-simple.cat

  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_sysconfdir}/xml/docbook-simple.xml" \
     %{_sysconfdir}/xml/catalog 
fi

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-25
- Removing the explicit %%clean stage.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Ondrej Vasik <ovasik@redhat.com> 1.1-11
- avoid using Fedora in the README file (portability)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 18 2010 Ondrej Vasik <ovasik@redhat.com> - 1.1-7
- post scriptlet requires sed (#593083)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 18 2008 Ondrej Vasik <ovasik@redhat.com> - 1.1-4
- fix loop in post catalog registration(incomplete sed
  coverage) #455680
- fix broken catalogs for package updates
- fix removal of files during updates

* Mon Nov 05 2007 Ondrej Vasik <ovasik@redhat.com> - 1.1-3
- merge review(#225701)
- spec modified to follow guidelines

* Wed Oct 24 2007 Ondrej Vasik <ovasik@redhat.com> - 1.1-2
- rpmlint check
- /etc/ files marked as config, fixed bad requirements
- cosmetic cleanup of spec file

* Thu May 24 2007 Ondrej Vasik <ovasik@redhat.com> - 1.1-1.02
- fixed added error in docbook-simple.xml(wrong catalog version)

* Thu May 24 2007 Ondrej Vasik <ovasik@redhat.com> - 1.1-1
- rebuilt with latest stable upstream release(1.1)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0-2.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Sep 07 2004 Mark Johnson <mjohnson@redhat.com> 1.0-1
- Initial release

