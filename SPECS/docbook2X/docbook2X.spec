Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           docbook2X
Version:        0.8.8
Release:        37%{?dist}
Summary:        Convert docbook into man and Texinfo

License:        MIT
URL:            http://docbook2x.sourceforge.net/
Source0:        http://downloads.sourceforge.net/docbook2x/docbook2X-%{version}.tar.gz


BuildRequires:  gcc
BuildRequires:  perl-interpreter perl-generators libxslt openjade texinfo %{_bindir}/sgml2xml
# required by the perl -c calls during build
BuildRequires:  perl(XML::SAX::ParserFactory)
# rpmlint isn't happy with libxslt, but we need xsltproc
Requires:       libxslt openjade texinfo %{_bindir}/sgml2xml
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Required by bin/* scripts, who does know why rpmbuild does not generate
# dependencies automatically:
Requires:  perl(Exporter)
Requires:  perl(IO::File)
Requires:  perl(Text::Wrap)
Requires:  perl(vars)
Requires:  perl(XML::SAX::ParserFactory)

%description
docbook2X converts DocBook documents into man pages and Texinfo
documents.


%prep
%setup -q

%build
# to avoid clashing with docbook2* from docbook-utils
%configure --program-transform-name='s/docbook2/db2x_docbook2/'
make %{?_smp_mflags}
rm -rf __dist_html
mkdir -p __dist_html/html
cp -p doc/*.html __dist_html/html


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -c -p'
rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/
rm -f $RPM_BUILD_ROOT%{_infodir}/dir


%files
%doc COPYING README THANKS AUTHORS __dist_html/html/
%{_bindir}/db2x_manxml
%{_bindir}/db2x_texixml
%{_bindir}/db2x_xsltproc
%{_bindir}/db2x_docbook2man
%{_bindir}/db2x_docbook2texi
%{_bindir}/sgml2xml-isoent
%{_bindir}/utf8trans
%dir %{_datadir}/docbook2X
%{_datadir}/docbook2X/VERSION
%dir %{_datadir}/docbook2X/charmaps
%dir %{_datadir}/docbook2X/dtd
%dir %{_datadir}/docbook2X/xslt
%{_datadir}/docbook2X/charmaps/*
%{_datadir}/docbook2X/dtd/*
%{_datadir}/docbook2X/xslt/*
%{_mandir}/man1/*.1*
%{_infodir}/docbook2*


%changelog
* Wed Dec 20 2023 Sindhu Karri <lakarri@microsoft.com> - 0.8.8-37
- Promote package to Mariner Base repo
- Verified license

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.8-36
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.8-33
- Perl 5.30 rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.8-30
- Perl 5.28 rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.8-26
- Perl 5.26 rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.8-24
- Perl 5.24 rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.8-21
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.8.8-20
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Aug 01 2013 Petr Pisar <ppisar@redhat.com> - 0.8.8-16
- Declare script dependencies explicitly

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.8.8-15
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Caolán McNamara <caolanm@redhat.com> - 0.8.8-13
- Resolves: rhbz#872580 license text is MIT-alike rather than BSD
  which fits with the upstream web-site declaration

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.8.8-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.8.8-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8.8-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.8.8-6
- rebuild against perl 5.10.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.8-3
Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.8-2
- Autorebuild for GCC 4.3

* Wed Aug  8 2007 Patrice Dumas <pertusus@free.fr> 0.8.8-1
- update to 0.8.8

* Mon Sep 11 2006 Patrice Dumas <pertusus@free.fr> 0.8.7-2
- correct the perl-XML-SAX to be perl(XML::SAX::ParserFactory)

* Thu May 18 2006 Patrice Dumas <pertusus@free.fr> - 0.8.7-1
- update to 0.8.7

* Fri Feb 17 2006 Patrice Dumas <pertusus@free.fr> - 0.8.6-1
- update to 0.8.6
- drop patch as SGMLSpl.pm is included in the scripts, not distributed
- BR perl-XML-SAX (close 188481)

* Fri Feb 17 2006 Patrice Dumas <pertusus@free.fr> - 0.8.5-2
- rebuild for fc5

* Fri Feb  3 2006 Patrice Dumas <pertusus@free.fr> - 0.8.5-1
- FE submission
