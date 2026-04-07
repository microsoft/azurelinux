# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: docbook-style-xsl
Version: 1.79.2
Release: 25%{?dist}

Summary: Norman Walsh's XSL stylesheets for DocBook XML

License: LicenseRef-DMIT
URL: https://github.com/docbook/xslt10-stylesheets

Provides: docbook-xsl = %{version}
Requires: docbook-dtd-xml
# xml-common was using /usr/share/xml until 0.6.3-8.
Requires: xml-common >= 0.6.3-8
# libxml2 required because of usage of /usr/bin/xmlcatalog
Requires(post): libxml2 >= 2.4.8
Requires(postun): libxml2 >= 2.4.8
# PassiveTeX before 1.21 can't handle the newer stylesheets.
Conflicts: passivetex < 1.21
BuildRequires: make


BuildArch: noarch
Source0: https://github.com/docbook/xslt10-stylesheets/releases/download/release%2F{%version}/docbook-xsl-nons-%{version}.tar.bz2
Source1: %{name}.Makefile
Source2:  https://github.com/docbook/xslt10-stylesheets/releases/download/release%2F{%version}/docbook-xsl-doc-%{version}.tar.bz2


#Avoid proportional-column-width for passivetex (bug #176766).
Patch1: docbook-xsl-pagesetup.patch
#Hard-code the margin-left work around to expect passivetex (bug #113456).
Patch2: docbook-xsl-marginleft.patch
#fix of #161619 - adjustColumnWidths now available
Patch3: docbook-xsl-newmethods.patch
#change a few non-constant expressions to constant - needed for passivetex(#366441)
Patch4: docbook-xsl-non-constant-expressions.patch
#added fixes for passivetex extension and list-item-body(#161371)
Patch5: docbook-xsl-list-item-body.patch
#workaround missing mandir section problem (#727251)
Patch6: docbook-xsl-mandir.patch
#Non-recursive string.subst that doesn't kill smb.conf.5 generation
Patch7: docbook-style-xsl-non-recursive-string-subst.patch
#Fix multilib problems with gtk-doc documentation
#https://github.com/docbook/xslt10-stylesheets/issues/54
Patch8: docbook-style-xsl-1.79.2-fix-gtk-doc-multilib.patch

%description
These XSL stylesheets allow you to transform any DocBook XML document to
other formats, such as HTML, FO, and XHMTL.  They are highly customizable.


%prep
%setup -c -T -n docbook-xsl-%{version}
tar jxf %{SOURCE0}
mv docbook-xsl-nons-%{version}/* .
pushd ..
tar jxf %{SOURCE2}
popd
%patch -P1 -p1 -b .pagesetup
%patch -P2 -p1 -b .marginleft
%patch -P3 -p1 -b .newmethods
%patch -P4 -p1 -b .nonconstant
%patch -P5 -p1 -b .listitembody
%patch -P6 -p1 -b .mandir
%patch -P7 -p2 -b .non-recursive-subst
%patch -P8 -p1 -b .gtk-doc-multilib

cp -p %{SOURCE1} Makefile

# fix of non UTF-8 files rpmlint warnings
for fhtml in $(find ./doc -name '*.html' -type f)
do
  iconv -f ISO-8859-1 -t UTF-8 "$fhtml" -o "$fhtml".tmp
  mv -f "$fhtml".tmp "$fhtml"
  sed -i 's/charset=ISO-8859-1/charset=UTF-8/' "$fhtml"
done

for f in $(find -name "*'*")
do
  mv -v "$f" $(echo "$f" | tr -d "'")
done


%build


%install
DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make install BINDIR=$DESTDIR%{_bindir} DESTDIR=$DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}
cp -a VERSION.xsl $DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}/VERSION.xsl
ln -s xsl-stylesheets-%{version} \
	$DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets

# Don't ship the extensions (bug #177256).
rm -rf $DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets/extensions/*


%files
%doc BUGS
%doc README
%doc TODO
%doc doc
%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}
%{_datadir}/sgml/docbook/xsl-stylesheets


%post
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://cdn.docbook.org/release/xsl-nons/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://cdn.docbook.org/release/xsl-nons/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://cdn.docbook.org/release/xsl-nons/current/" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://cdn.docbook.org/release/xsl-nons/current/" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
#keep the old one sourceforge URIs at least temporarily
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG



%postun
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
   "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
fi

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 23 2023 Ondrej Sloup <osloup@redhat.com> - 1.79.2-20
- Update license tag to the SPDX format

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 David King <amigadave@amigadave.com> - 1.79.2-13
- Fix gtk-doc multilib failures

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 13 2017 Alexander Bokovoy <abokovoy@redhat.com> - 1.79.2-6
- Use non-recursive string.subst to allow building large documents like smb.conf.5

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Ondrej Vasik <ovasik@redhat.com> - 1.79.2-3
- keep old sourceforge entries at least temporarily (#1409587)

* Mon Jan 02 2017 Ondrej Vasik <ovasik@redhat.com> - 1.79.2-2
- update xmlcatalog entries to docbook.org cdn

* Mon Jan 02 2017 Ondrej Vasik <ovasik@redhat.com> - 1.79.2-1
- new upstream release 1.79.2
- upstream moved to github

* Fri Jul 08 2016 Ondrej Vasik <ovasik@redhat.com> - 1.79.1-1
- new upstream release 1.79.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.78.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.78.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.78.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jul 29 2013 Ondrej Vasik <ovasik@redhat.com> 1.78.1-2
- use DMIT (modified MIT) as a license for the
  stylesheets (#988715)

* Mon Mar 18 2013 Ondrej Vasik <ovasik@redhat.com> 1.78.1-1
- new upstream release 1.78.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.78.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Ondrej Vasik <ovasik@redhat.com> 1.78.0-1
- new upstream release 1.78.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.77.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun  5 2012 Ondrej Vasik <ovasik@redhat.com> 1.77.1-2
- ship VERSION.xsl file (#829014)

* Tue Jun  5 2012 Ondrej Vasik <ovasik@redhat.com> 1.77.1-1
- new stable upstream release 1.77.1
- defuzz patches

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep  6 2011 Ondrej Vasik <ovasik@redhat.com> 1.76.1-4
- revert previous change, workaround the mandir links issue
  in buildroot (#727251)

* Mon Aug 29 2011 Ondrej Vasik <ovasik@redhat.com> 1.76.1-3
- make man.output.in.separate.dir "on" by default (#727251)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 02 2010 Ondrej Vasik <ovasik@redhat.com> 1.76.1-1
- new upstream release 1.76.1

* Mon Sep 06 2010 Ondrej Vasik <ovasik@redhat.com> 1.76.0-1
- new upstream release 1.76.0

* Tue May 04 2010 Ondrej Vasik <ovasik@redhat.com> 1.75.2-6
- ship eclipse help stylesheets(#588613)

* Fri Dec 18 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.2-5
- comment patches purpose
- License Copyright only

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.75.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.2-3
- upstream changed changed doc tarball after release
  (empty reference pdf file in old tarball)

* Wed Jul 22 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.2-2
- upstream changed tarballs after release

* Tue Jul 21 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.2-1
- New upstream release 1.75.2

* Thu May 28 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.1-1
- New upstream release 1.75.1

* Mon May 11 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.0-1
- New upstream release 1.75.0
- update marginleft patch

* Wed Mar 11 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.3-1
- New upstream release 1.74.3

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.74.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.2-2
- updated Makefile: do ship .svg images(#486849), xsl
  stylesheets for website, xhtml-1_1, docbook -> epub
  convertor

* Fri Feb 20 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.2-1
- New upstream release 1.74.2

* Wed Feb 18 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.1-1
- New upstream release, removed included patches

* Wed Feb 11 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.0-7
- fix broken varlistentry (#479683)

* Mon Feb 02 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.0-6
- fix improper localization for rtl languages, thanks
  Muayyad Alsadi(#475077)

* Wed Jan 28 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.0-5
- fix xsl stylesheets for rtl languages(#475077)

* Fri Dec 12 2008 Ondrej Vasik <ovasik@redhat.com> 1.74.0-4
- Author_Group "<orgname>" merged between "<surname>"
  and "<surname>" (#473019)

* Wed Aug 06 2008 Kamil Dudka <kdudka@redhat.com> 1.74.0-3
- Rediffed all patches to work with patch --fuzz=0

* Wed Aug 06 2008 Kamil Dudka <kdudka@redhat.com> 1.74.0-2
- Tiny changes in docbook-xsl-newmethods.patch to work with xalan
  (#452867)

* Tue Jun 03 2008 Ondrej Vasik <ovasik@redhat.com> 1.74.0-1
- New upstream release 1.74.0, adapted patches

* Fri Dec 14 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.2-9
- added fixes for passivetex extension and list-item-body
  (#161371)

* Tue Dec 11 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.2-8
- remove entries from xmlcatalog only on removal of package
  (required because of the change with droping release
   -caused drop of catalog entries during update)

* Tue Dec 04 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.2-7
- change a few non-constant expressions to constant that
  could now be handled by passivetex(#366441)

* Mon Dec 03 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.2-6
- fixed docbook-xsl-pagesetup.patch to follow Norman Walsh's
  documentation for nonpassivetex processing(#307001)

* Tue Nov 27 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.2-5
- convert all html files in doc to UTF-8 in prep
  (latest rpmlint gives warnings)
- no longer using release in style-xsl dir(#389231)

* Tue Nov 06 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.2-4
- Merge review(#225704)
- spec file modified to follow guidelines

* Wed Oct 24 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.2-3
- rpmlint check
- fixed License Tag, Requires and some cosmetic issues 

* Fri Sep  7 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.2-2
- Added PreReq of libxml2(#253962)

* Wed Sep  5 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.2-1
- new upstream version

* Thu Aug 30 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.1-2
- removed patch for #249294(included in new version other way)

* Wed Aug 29 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.1-1
- new upstream version(fixing some bugs)
- small new-methods patch change

* Mon Jul 23 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.0-2
- fixed manpages/docbook.xsl failure(Tim Waugh,#249294)

* Mon Jul 23 2007 Ondrej Vasik <ovasik@redhat.com> 1.73.0-1
- update to latest upstream version
- patch changes because of rejects

* Mon Jun 18 2007 Ondrej Vasik <ovasik@redhat.com> 1.72.0-3
- patch fixing #161619 taken from upstream

* Wed Jan 24 2007 Tomas Mraz <tmraz@redhat.com> 1.72.0-2
- Install missing *.ent from common.

* Tue Jan 23 2007 Tim Waugh <twaugh@redhat.com> 1.72.0-1
- 1.72.0.

* Fri Jan 19 2007 Tomas Mraz <tmraz@redhat.com> 1.71.1-2
- Add new wordml and especially highlighting (which is referenced
  from html) subdirs to Makefile.

* Fri Jan 19 2007 Tim Waugh <twaugh@redhat.com> 1.71.1-1
- 1.71.1.  No longer seem to need lists patch.  Removed out of date sp
  patch.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.69.1-5.1
- rebuild

* Tue Jan 24 2006 Tim Waugh <twaugh@redhat.com> 1.69.1-5
- Don't ship docsrc/* (bug #177256).
- Don't ship the extensions (bug #177256).

* Thu Jan 19 2006 Tim Waugh <twaugh@redhat.com> 1.69.1-4
- Better 'lists' patch (bug #161371).

* Thu Jan 19 2006 Tim Waugh <twaugh@redhat.com> 1.69.1-3
- Apply patch to fix simpara manpage output, which asciidoc tends to use
  (bug #175592).

* Tue Jan  3 2006 Tim Waugh <twaugh@redhat.com> 1.69.1-2
- Patches from W. Michael Petullo:
  - Fix lists blocking (bug #161371).
  - Avoid proportional-column-width for passivetex (bug #176766).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Aug 12 2005 Tim Waugh <twaugh@redhat.com> 1.69.1-1
- 1.69.1.

* Mon Jul 18 2005 Tim Waugh <twaugh@redhat.com> 1.69.0-1
- 1.69.0.

* Mon Feb 14 2005 Tim Waugh <twaugh@redhat.com> 1.68.1-1
- 1.68.1.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 1.68.0-1
- 1.68.0.

* Wed Dec  8 2004 Tim Waugh <twaugh@redhat.com> 1.67.2-2
- Prevent expressions in passivetex output from index.xsl (bug #142229).

* Thu Dec  2 2004 Tim Waugh <twaugh@redhat.com> 1.67.2-1
- 1.67.2.
- No longer need nbsp or listblock patches.

* Mon Nov 22 2004 Tim Waugh <twaugh@redhat.com> 1.67.0-3
- Avoid non-ASCII in generated man pages.

* Wed Nov 10 2004 Tim Waugh <twaugh@redhat.com> 1.67.0-1
- 1.67.0.

* Tue Nov  2 2004 Tim Waugh <twaugh@redhat.com> 1.66.1-1
- 1.66.1 (bug #133586).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com> 1.65.1-2
- Fix strange filenames (bug #125311).

* Tue Mar  9 2004 Tim Waugh <twaugh@redhat.com> 1.65.1-1
- 1.65.1.

* Mon Mar  1 2004 Tim Waugh <twaugh@redhat.com> 1.65.0-1
- 1.65.0.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 20 2004 Tim Waugh <twaugh@redhat.com> 1.64.1-6
- Fix last margin-left fix (bug #113456).
- Reduce instances of itemized/ordered lists having misalignments.

* Sun Jan 18 2004 Tim Waugh <twaugh@redhat.com> 1.64.1-5
- And another (bug #113456).

* Thu Jan 15 2004 Tim Waugh <twaugh@redhat.com> 1.64.1-4
- Fixed another instance of bug #113456 in lists layout.

* Wed Jan 14 2004 Tim Waugh <twaugh@redhat.com> 1.64.1-3
- Hard-code the margin-left work around to expect passivetex (bug #113456).

* Wed Dec 24 2003 Tim Waugh <twaugh@redhat.com> 1.64.1-2
- Another manpage fix.

* Fri Dec 19 2003 Tim Waugh <twaugh@redhat.com> 1.64.1-1
- 1.64.1.

* Thu Dec 18 2003 Tim Waugh <twaugh@redhat.com> 1.64.0-2
- Another manpage fix.

* Tue Dec 16 2003 Tim Waugh <twaugh@redhat.com> 1.64.0-1
- 1.64.0.

* Fri Dec 12 2003 Tim Waugh <twaugh@redhat.com> 1.62.4-3
- Use the fr.xml from 1.62.1 (bug #111989).

* Thu Dec 11 2003 Tim Waugh <twaugh@redhat.com> 1.62.4-2
- Manpages fixes.

* Thu Dec 11 2003 Tim Waugh <twaugh@redhat.com> 1.62.4-1
- 1.62.4.
- No longer need hyphens patch.
- Avoid expressions in margin-left attributes, since passivetex does not
  understand them.

* Fri Jul  4 2003 Tim Waugh <twaugh@redhat.com> 1.61.2-2.1
- Rebuilt.

* Fri Jul  4 2003 Tim Waugh <twaugh@redhat.com> 1.61.2-2
- Rebuilt.

* Fri May 23 2003 Tim Waugh <twaugh@redhat.com> 1.61.2-1
- 1.61.2.

* Sun May 18 2003 Tim Waugh <twaugh@redhat.com> 1.61.1-1
- 1.61.1.

* Fri May  9 2003 Tim Waugh <twaugh@redhat.com> 1.61.0-1
- Prevent hyphenation-character confusing passivetex.
- 1.61.0.

* Thu Mar  6 2003 Tim Waugh <twaugh@redhat.com> 1.60.1-1
- 1.60.1.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec  2 2002 Tim Waugh <twaugh@redhat.com> 1.58.1-1
- 1.58.1.
- No longer need marker patch.

* Mon Nov  4 2002 Tim Waugh <twaugh@redhat.com> 1.57.0-2
- Ship profiling directory (bug #77191).

* Tue Oct 22 2002 Tim Waugh <twaugh@redhat.com> 1.57.0-1
- 1.57.0.

* Wed Oct 16 2002 Tim Waugh <twaugh@redhat.com> 1.56.1-1
- 1.56.1.
- Use value-of not copy-of for fo:marker content.
- Conflict with passivetex < 1.21.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May  1 2002 Tim Waugh <twaugh@redhat.com> 1.50.0-1
- 1.50.0.

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.49-1
- 1.49.
- Rebuild in new environment.

* Fri Feb  1 2002 Tim Waugh <twaugh@redhat.com> 1.48-4
- Put URIs instead of pathnames in the XML catalog.

* Thu Jan 17 2002 Tim Waugh <twaugh@redhat.com> 1.48-3
- Back to /usr/share/sgml.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.48-2
- automated rebuild

* Mon Jan  7 2002 Tim Waugh <twaugh@redhat.com> 1.48-1
- 1.48.

* Sat Dec  8 2001 Tim Waugh <twaugh@redhat.com> 1.47-2
- Conflict with PassiveTeX before 1.11.

* Tue Oct 16 2001 Tim Waugh <twaugh@redhat.com> 1.47-1
- 1.47-experimental.

* Tue Oct  9 2001 Tim Waugh <twaugh@redhat.com> 1.45-2
- Fix unversioned symlink.

* Mon Oct  8 2001 Tim Waugh <twaugh@redhat.com> 1.45-1
- XML Catalog entries.
- Move files to /usr/share/xml.

* Mon Oct  1 2001 Tim Waugh <twaugh@redhat.com> 1.45-0.1
- 1.45.
- Built for Red Hat Linux.

* Tue Jun 26 2001 Chris Runge <crunge@pobox.com>
- 1.40

* Sat Jun 09 2001 Chris Runge <crunge@pobox.com>
- added extensions and additional doc
- bin added to doc; the Perl files are for Win32 Perl and so need some
  conversion first

* Fri Jun 08 2001 Chris Runge <crunge@pobox.com>
- Initial RPM (based on docbook-style-dsssl RPM)
- note: no catalog right now (I don't know how to do it; and not sure why
  it is necessary)
