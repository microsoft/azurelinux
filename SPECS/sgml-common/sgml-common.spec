%global xmlxsdver 2009/01

Summary: 		Common SGML catalog and DTD files
Name: 			sgml-common
Version: 		0.6.3
Release: 		57%{?dist}
License: 		GPLv3

BuildArch: 		noarch

#Actually - there is no homepage of this project, on that URL
#page you could get complete ISO 8879 listing as was on the
#old page - only part of it is included in sgml-common package.
URL: 			http://www.w3.org/2003/entities/
Vendor: 		Microsoft Corporation
Distribution: 	Mariner
Source0: 		https://sourceware.org/ftp/docbook-tools/new-trials/SOURCES/%{name}-%{version}.tgz
# Following 4 from openjade/pubtext - same maintainer as in SGML-common, so up2date:
Source1: 		xml.dcl
Source2: 		xml.soc
Source3: 		html.dcl
Source4: 		html.soc
Source5: 		xml.xsd
Source6: 		xmldsig-core-schema.xsd
Source7: 		XMLSchema.dtd
Source8: 		datatypes.dtd
Source9: 		sgmlwhich.1
Source10: 		sgml.conf.5

Patch0: sgml-common-umask.patch
Patch1: sgml-common-xmldir.patch
Patch2: sgml-common-quotes.patch

BuildRequires: libxml2
BuildRequires: automake
Requires: %{_bindir}/basename

%description
The sgml-common package contains a collection of entities and DTDs
that are useful for processing SGML, but that don't need to be
included in multiple packages.  Sgml-common also includes an
up-to-date Open Catalog file.

%package -n xml-common
Summary: Common XML catalog and DTD files
License: GPL+
Requires(pre): %{_bindir}/xmlcatalog

%description -n xml-common
The xml-common is a subpackage of sgml-common which contains
a collection XML catalogs that are useful for processing XML,
but that don't need to be included in main package.

%prep
%setup -q
%patch0 -p1 -b .umask
%patch1 -p1 -b .xmldir
%patch2 -p1 -b .quotes

# replace bogus links with files
automakedir=`ls -1d /usr/share/automake* | head -n +1`
for file in COPYING INSTALL install-sh missing mkinstalldirs; do
   rm $file
   cp -p $automakedir/$file .
done

%build
%configure

%install
rm -rf %{buildroot}
make install DESTDIR="%{buildroot}" htmldir='%{_datadir}/doc' INSTALL='install -p'
mkdir %{buildroot}%{_sysconfdir}/xml
mkdir -p %{buildroot}%{_sysconfdir}/sgml/docbook
mkdir -p %{buildroot}%{_datadir}/sgml/docbook
# Touch SGML catalog
touch %{buildroot}%{_sysconfdir}/sgml/catalog
# Create an empty XML catalog.
XMLCATALOG=%{buildroot}%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --create $XMLCATALOG
# ...and add xml.xsd in it
for type in system uri ; do
	for path in 2001 %{xmlxsdver} ; do
		%{_bindir}/xmlcatalog --noout --add $type \
			"http://www.w3.org/$path/xml.xsd" \
			"file://%{_datadir}/xml/xml.xsd" $XMLCATALOG
	done
	# Add xmldsig-core-schema.xsd to catalog
	%{_bindir}/xmlcatalog --noout --add $type \
		"http://www.w3.org/TR/xmldsig-core/xmldsig-core-schema.xsd" \
		"file://%{_datadir}/xml/xmldsig-core-schema.xsd" $XMLCATALOG
done
# Now put the common DocBook entries in it
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//ENTITIES DocBook XML" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//DTD DocBook XML" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"ISO 8879:1986" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegateSystem" \
	"http://www.oasis-open.org/docbook/" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegateURI" \
	"http://www.oasis-open.org/docbook/" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
for public in "-//W3C//DTD XMLSchema 200102//EN" "-//W3C//DTD XMLSCHEMA 200102//EN" ; do
	%{_bindir}/xmlcatalog --noout --add "public" \
		"$public" \
		"file://%{_datadir}/xml/XMLSchema.dtd" $XMLCATALOG
done
%{_bindir}/xmlcatalog --noout --add "system" \
	"http://www.w3.org/2001/XMLSchema.dtd" \
	"file://%{_datadir}/xml/XMLSchema.dtd" $XMLCATALOG

# Also create the common DocBook catalog
%{_bindir}/xmlcatalog --noout --create \
	%{buildroot}%{_sysconfdir}/sgml/docbook/xmlcatalog
ln -sf %{_sysconfdir}/sgml/docbook/xmlcatalog\
	%{buildroot}%{_datadir}/sgml/docbook/xmlcatalog

rm -f %{buildroot}%{_datadir}/sgml/xml.dcl
install -p -m0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} \
	%{buildroot}%{_datadir}/sgml
rm -rf %{buildroot}%{_datadir}/xml/*
install -p -m0644 %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} \
	%{buildroot}%{_datadir}/xml
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man5
install -p -m0644 %{SOURCE9} %{buildroot}%{_mandir}/man1
install -p -m0644 %{SOURCE10} %{buildroot}%{_mandir}/man5

# remove installed doc file and prepare installation with %%doc
rm %{buildroot}%{_datadir}/doc/*.html
rm -rf __dist_doc/html/
mkdir -p __dist_doc/html/
cp -p doc/HTML/*.html __dist_doc/html/


%pre -n xml-common
if [ $1 -gt 1 ] && [ -e %{_sysconfdir}/xml/catalog ]; then
	for type in system uri ; do
		for path in 2001 %{xmlxsdver} ; do
			%{_bindir}/xmlcatalog --noout --add $type \
				"http://www.w3.org/$path/xml.xsd" \
				"file://%{_datadir}/xml/xml.xsd" \
				%{_sysconfdir}/xml/catalog
		done
		%{_bindir}/xmlcatalog --noout --add $type \
			"http://www.w3.org/TR/xmldsig-core/xmldsig-core-schema.xsd" \
			"file://%{_datadir}/xml/xmldsig-core-schema.xsd" %{_sysconfdir}/xml/catalog
	done
	for public in "-//W3C//DTD XMLSchema 200102//EN" "-//W3C//DTD XMLSCHEMA 200102//EN" ; do
		%{_bindir}/xmlcatalog --noout --add "public" \
			"$public" \
			"file://%{_datadir}/xml/XMLSchema.dtd" %{_sysconfdir}/xml/catalog
	done
fi

%files
%license COPYING
%doc __dist_doc/html/ AUTHORS NEWS ChangeLog README
%dir %{_sysconfdir}/sgml
%config(noreplace) %{_sysconfdir}/sgml/sgml.conf
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %{_sysconfdir}/sgml/catalog
%dir %{_datadir}/sgml
%dir %{_datadir}/sgml/sgml-iso-entities-8879.1986
%{_datadir}/sgml/sgml-iso-entities-8879.1986/*
%{_datadir}/sgml/xml.dcl
%{_datadir}/sgml/xml.soc
%{_datadir}/sgml/html.dcl
%{_datadir}/sgml/html.soc
%{_bindir}/sgmlwhich
%{_bindir}/install-catalog
%{_mandir}/man8/install-catalog.8*
%{_mandir}/man1/sgmlwhich.1*
%{_mandir}/man5/sgml.conf.5*

%files -n xml-common
%dir %{_sysconfdir}/xml
%dir %{_sysconfdir}/sgml
%dir %{_sysconfdir}/sgml/docbook
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xml/catalog
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sgml/docbook/xmlcatalog
%dir %{_datadir}/sgml
%dir %{_datadir}/sgml/docbook
%{_datadir}/sgml/docbook/xmlcatalog
%dir %{_datadir}/xml
%{_datadir}/xml/xml.xsd
%{_datadir}/xml/xmldsig-core-schema.xsd
%{_datadir}/xml/XMLSchema.dtd
%{_datadir}/xml/datatypes.dtd

%changelog
* Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.3-57
- Fixing invalid source URL.
- License verified.

* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 0.6.3-56
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 05 2018 Ondrej Vasik <ovasik@redhat.com> - 0.6.3-51
- add basic manpages for sgml.conf(5) and sgmlwhich(1) (#1612272)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Jan Pazdziora <jpazdziora@redhat.com> - 0.6.3-49
- Package and catalog xmldsig-core-schema.xsd, XMLSchema.dtd, and datatypes.dtd

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 31 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.6.3-47
- Use /usr/bin instead of /bin in Requires

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 15 2014 Ondrej Vasik <ovasik@redhat.com> 0.6.3-42
- add /etc/sgml ownership to xml-common subpackage (#1173925)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Ondrej Vasik <ovasik@redhat.com> 0.6.3-38
- get rid of the explicit automake14 requirement

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 30 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.6.3-35
- Include xml.xsd in xml-common (#750073).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 12 2010 Ondrej Vasik <ovasik@redhat.com> 0.6.3-33
- ship COPYING file with both sgml-common and xml-common
- ship documentation with xml-common

* Fri Jan 15 2010 Ondrej Vasik <ovasik@redhat.com> 0.6.3-32
- Merge review #226415: remove unapplied patches, remove
  versioned BR

* Wed Nov 11 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.3-31
- apply quotes patch once again (accidently deleted in Nov07-#533058)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.3-29
- do own /etc/sgml/catalog

* Tue May 19 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.3-28
- do not provide explicit url for xml-common subpackage,
  fix trailing spaces
- add Requires: /bin/basename (#501360)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 07 2008 Ondrej Vasik <ovasik@redhat.com> 0.6.3-26
- /etc/sgml/docbook dir now owned by package(#458230)
- get rid off fuzz in patches

* Tue Jul 01 2008 Ondrej Vasik <ovasik@redhat.com> 0.6.3-25
- mark xmlcatalog config(noreplace) to prevent overwriting
  of the content, move it to sysconfdir and make symlink for
  it to silence rpmlint

* Mon Jun 30 2008 Ondrej Vasik <ovasik@redhat.com> 0.6.3-24
- mark catalog files as (not md5 size mtime) for verify to
  prevent info about changed files (#453271)

* Thu Nov 22 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.3-23
- Another MergeReview improvements(provided by Patrice Dumas)
- copy Automake-1.4 files instead of rerunning autotools,
- better preserving timestamps, better handling of documentation
- improved XML-common description

* Thu Nov 15 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.3-22
- Merge Review(226415)
- changed: License Tag, using RPM macros instead of hardcoded
  dirs, summary ended with dot, added URL, removed CHANGES
  file as obsolete, preserved timestamps and some other cosmetic
  changes
- no longer shipping old automake tarball, fixed issue with man8_DATA,
  BuildRequire:Automake,Autoconf again(see MergeReview discussion)

* Mon May 28 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.3-21
- Fixed broken URL (changed to XML entity declarations) (bug #237726)
- Rebuilt

* Tue May 15 2007 Tim Waugh <twaugh@redhat.com> 0.6.3-20
- Added dist tag.
- Fixed summary.
- Removed build dependency on autoconf/automake.

* Tue Oct 24 2006 Tim Waugh <twaugh@redhat.com> 0.6.3-19
- Removed stale URL (bug #210848).

* Mon Jun 12 2006 Tim Waugh <twaugh@redhat.com> 0.6.3-18
- Build requires automake and autoconf (bug #194709).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 22 2004 Than Ngo <than@redhat.com> 0.6.3-17
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec  8 2003 Tim Waugh <twaugh@redhat.com> 0.6.3-15
- Patch from Ville Skyttä <ville.skytta@iki.fi> (bug #111625):
  - Include /usr/share/xml in xml-common.
  - Own /usr/share/sgml and /usr/share/xml.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Oct 23 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-13
- Ship the installed documentation.
- Don't install files not packaged.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 24 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-10
- Ship {xml,html}.{dcl,soc} (bug #63500, bug #62980).
- Work around broken tarball packaging.

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-9
- Rebuild in new environment.

* Thu Jan 17 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-8
- Back to /usr/share/sgml.  Now install docbook-dtds.
- Use a real install-sh, not the symlink shipped in the tarball.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 0.6.3-7
- automated rebuild

* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-6
- Don't create a useless empty catalog.
- Don't try to put install things outside the build root.
- Build requires a libxml2 that actually works.

* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-4
- Use (and handle) catalog files with quotes in install-catalog.

* Thu Nov  1 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-3
- Create default XML Catalog at build time, not install time.

* Fri Oct  5 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-2
- Move XML things into /usr/share/xml, and split them out into separate
  xml-common package.

* Mon Oct  1 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-1
- 0.6.3.  Incorporates oldsyntax and quiet patches.
- Make /etc/sgml/sgml.conf noreplace.
- Own /etc/sgml, various other directories (bug #47485, bug #54180).

* Wed May 23 2001 Tim Waugh <twaugh@redhat.com> 0.5-7
- Remove execute bit from data files.

* Mon May 21 2001 Tim Waugh <twaugh@redhat.com> 0.5-6
- install-catalog needs to make sure that it creates world-readable files
  (bug #41552).

* Wed Mar 14 2001 Tim Powers <timp@redhat.com> 0.5-5
- fixed license

* Wed Jan 24 2001 Tim Waugh <twaugh@redhat.com>
- Make install-catalog quieter during normal operation.

* Tue Jan 23 2001 Tim Waugh <twaugh@redhat.com>
- Require textutils, fileutils, grep (bug #24719).

* Wed Jan 17 2001 Tim Waugh <twaugh@redhat.com>
- Require sh-utils.

* Mon Jan 15 2001 Tim Waugh <twaugh@redhat.com>
- Don't play so many macro games.
- Fix typo in install-catalog patch.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Change group.
- Install by hand (man/en/...).  Use %%{_mandir}.
- Use %%{_tmppath}.
- Make install-catalog fail silently if given the old syntax.
- Add CHANGES file.
- Change Copyright: to License:.
- Remove Packager: line.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Based on Eric Bischoff's new-trials packages.
