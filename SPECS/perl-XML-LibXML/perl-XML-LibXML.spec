# Do not invoke thread tests by default because the thread support is broken,
# bug #1224731, CPAN RT#91800
%bcond_with thread_test

Name:           perl-XML-LibXML
# NOTE: also update perl-XML-LibXSLT to a compatible version, see
# https://bugzilla.redhat.com/show_bug.cgi?id=469480
# it might not be needed anymore
# this module is maintained, the other is not
Version:        2.0209
Release:        1%{?dist}
Summary:        Perl interface to the libxml2 library
License:        (GPL+ or Artistic) and MIT
URL:            https://metacpan.org/release/XML-LibXML
Source0:        https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/XML-LibXML-%{version}.tar.gz 
# Fix parsing ampersand entities in SAX interface, CPAN RT#131498,
# posted to the upstream.
Patch0:         XML-LibXML-2.0202-Parse-an-ampersand-entity-in-SAX-interface.patch
# To reduce dependencies replace Alien::Libxml2 with pkg-config
Patch1:         XML-LibXML-2.0206-Use-pkgconfig-instead-of-Alien-Libxml2.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  glibc-common
BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  pkgconfig(libxml-2.0)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(vars)
BuildRequires:  perl(XML::NamespaceSupport)
BuildRequires:  perl(XML::SAX::Base)
BuildRequires:  perl(XML::SAX::DocumentLocator)
BuildRequires:  perl(XML::SAX::Exception)
BuildRequires:  perl(XSLoader)
# Tests
# t/12html.t exhibits ISO-8859-2 charset
BuildRequires:  glibc-iconv
BuildRequires:  perl(Errno)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(locale)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XML::SAX)
BuildRequires:  perl(XML::SAX::ParserFactory)
%if %{with thread_test}
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
%endif
BuildRequires:  perl(URI::file)
BuildRequires:  perl(utf8)
# Author test - Test::CPAN::Changes
# Author test - Test::Pod
# Author test - Test::Kwalitee
# Author test - Test::TrailingSpace
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Data::Dumper)
# Run-require "perl-interpreter" because a triggerin script needs it.
Requires:           perl-interpreter
Requires(preun):    perl-interpreter
# threads and threads::shared are optional
Provides:       perl-XML-LibXML-Common = %{version}
Obsoletes:      perl-XML-LibXML-Common <= 0.13

%{?perl_default_filter}
# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Collector\\)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(Counter)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(Stacker)\s*$
%global __requires_exclude %{__requires_exclude}|^perl\\(TestHelpers)\s*$

%description
This module implements a Perl interface to the GNOME libxml2 library
which provides interfaces for parsing and manipulating XML files. This
module allows Perl programmers to make use of the highly capable
validating XML parser and the high performance DOM implementation.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
# t/12html.t exhibits ISO-8859-2 charset
Requires:       glibc-iconv
Requires:       perl-Test-Harness
%if %{with thread_test}
Requires:       perl(threads)
Requires:       perl(threads::shared)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n XML-LibXML-%{version}
%patch0 -p1
%patch1 -p1
chmod -x *.c
for i in Changes; do
  /usr/bin/iconv -f iso8859-1 -t utf-8 $i > $i.conv && /bin/mv -f $i.conv $i
done
perl -i -pe 's/\r\n/\n/' t/91unique_key.t

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL SKIP_SAX_INSTALL=1 INSTALLDIRS=vendor \
     OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a example t test %{buildroot}%{_libexecdir}/%{name}
for F in example/*.pl t/cpan-changes.t t/11memory.t t/pod.t \
        t/pod-files-presence.t t/release-kwalitee.t t/style-trailing-space.t; do
    rm -f %{buildroot}%{_libexecdir}/%{name}/"$F"
done
perl -i -pe 's{example/(testrun.xml)}{/tmp/$1}' %{buildroot}%{_libexecdir}/%{name}/t/03doc.t
cat > %{buildroot}%{_libexecdir}/%{name}/tests << 'EOF'
#!/bin/sh
unset AUTHOR_TESTING RELEASE_TESTING
cd %{_libexecdir}/%{name} && THREAD_TEST=0%{?with_thread_test:1} exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/tests


%check
unset AUTHOR_TESTING RELEASE_TESTING
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
THREAD_TEST=0%{?with_thread_test:1} make test

%triggerin -- perl-XML-SAX
for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
  %{_bindir}/perl -MXML::SAX -e "XML::SAX->add_parser(q($p))->save_parsers()" \
    2>/dev/null || :
done

%preun
if [ $1 -eq 0 ] ; then
  for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
    %{_bindir}/perl -MXML::SAX -e "XML::SAX->remove_parser(q($p))->save_parsers()" \
      2>/dev/null || :
  done
fi

%files
%license LICENSE
%doc Changes HACKING.txt README TODO
%{perl_vendorarch}/auto/XML
%{perl_vendorarch}/XML
%{_mandir}/man3/*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0209-1
- Auto-upgrade to 2.0209 - Azure Linux 3.0 - package upgrades

* Tue Jul 26 2022 Henry Li <lihl@microsoft.com> - 2.0207-7
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License Verified
- Remove macro usage that does not apply to CBL-Mariner
- Use glibc-iconv as BR and runtime requirements
- Remove epoch which is not supported in Mariner

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0207-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0207-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0207-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 25 2021 Petr Pisar <ppisar@redhat.com> - 1:2.0207-3
- Build-require glibc-gconv-extra for ISO-8859-2 support in tests
- Make tests subpackage noarch

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0207-2
- Perl 5.34 rebuild

* Mon Apr 19 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0207-1
- 2.0207 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0206-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0206-2
- Replace using of Alien::Libxml2 with pkg-config

* Tue Sep 15 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0206-1
- 2.0206 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0205-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0205-2
- Perl 5.32 rebuild

* Mon May 11 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0205-1
- 2.0205 bump

* Wed Mar 18 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0204-1
- 2.0204 bump

* Wed Mar 11 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0203-1
- 2.0203 bump

* Tue Jan 28 2020 Petr Pisar <ppisar@redhat.com> - 1:2.0202-2
- Fix parsing ampersand entities in SAX interface (CPAN RT#131498)

* Mon Jan 13 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0202-1
- 2.0202 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0201-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0201-2
- Perl 5.30 rebuild

* Mon May 27 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0201-1
- 2.0201 bump

* Mon Mar 25 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0200-1
- 2.0200 bump

* Mon Feb 11 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0134-1
- 2.0134 bump

* Wed Feb 06 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0133-1
- 2.0133 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0132-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0132-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0132-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0132-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 30 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0132-1
- 2.0132 bump

* Wed Oct 25 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0131-1
- 2.0131 bump

* Thu Oct 19 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0130-1
- 2.0130 bump

* Wed Sep 20 2017 Petr Pisar <ppisar@redhat.com> - 1:2.0129-8
- Adapt to libxml2-2.9.5 (bug #1489529)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0129-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0129-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Petr Pisar <ppisar@redhat.com> - 1:2.0129-5
- Fix CVE-2017-10672 (use-after-free by controlling the arguments to
  a replaceChild call) (bug #1470205)

* Fri Jul 14 2017 Petr Pisar <ppisar@redhat.com> - 1:2.0129-4
- Rename perl dependency in scriptlets

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1:2.0129-3
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0129-2
- Perl 5.26 rebuild

* Wed Mar 15 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0129-1
- 2.0129 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0128-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jul 25 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0128-1
- 2.0128 bump

* Mon Jul 04 2016 Petr Pisar <ppisar@redhat.com> - 1:2.0126-1
- 2.0126 bump

* Thu Jun 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0125-1
- 2.0125 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0124-2
- Perl 5.24 rebuild

* Mon Feb 29 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0124-1
- 2.0124 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0123-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 07 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0123-1
- 2.0123 bump

* Thu Nov 26 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0122-2
- Rebuild against the latest libxml2

* Tue Sep 01 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0122-1
- 2.122 bump

* Tue Jun 23 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0121-5
- Replace dependency on glibc-headers with gcc (bug #1230489)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0121-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0121-3
- Perl 5.22 rebuild

* Wed May 27 2015 Petr Pisar <ppisar@redhat.com> - 1:2.0121-2
- Disable thread tests because thread support not complete (bug #1224731)

* Mon May 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0121-1
- 2.0121 bump

* Thu Apr 23 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0119-1
- 2.0119 bump

* Mon Feb 09 2015 Petr Pisar <ppisar@redhat.com> - 1:2.0118-1
- 2.0118 bump

* Wed Oct 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0117-1
- 2.0117 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0116-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0116-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0116-1
- 2.0116 bump

* Fri Apr 04 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0115-1
- 2.0115 bump

* Mon Mar 17 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0113-1
- 2.0113 bump

* Mon Mar 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0111-1
- 2.0111 bump

* Mon Feb 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0110-1
- 2.0110 bump

* Thu Jan 02 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0108-1
- 2.0108 bump

* Sun Nov 03 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0107-1
- 2.0107 bump

* Thu Sep 19 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0106-1
- 2.0106 bump

* Tue Sep 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0105-1
- 2.0105 bump

* Mon Sep 02 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0104-1
- 2.0104 bump

* Mon Aug 26 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0103-1
- 2.0103 bump

* Mon Aug 19 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0101-1
- 2.0101 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0019-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1:2.0019-2
- Perl 5.18 rebuild

* Mon Jul 08 2013 Petr Šabata <contyk@redhat.com> - 1:2.0019-1
- 2.0019 bump (typo fixes)

* Wed Jul 03 2013 Petr Pisar <ppisar@redhat.com> - 1:2.0018-3
- Correct changelog entry

* Wed Jul 03 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0018-2
- Specify all dependencies

* Tue May 14 2013 Petr Šabata <contyk@redhat.com> - 1:2.0018-1
- 2.0018 bump; revert the library version requirements

* Mon May 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0017-1
- 2.0017 bump

* Mon Apr 15 2013 Petr Pisar <ppisar@redhat.com> - 1:2.0016-1
- 2.0016 bump (disable XML_PARSE_HUGE by default to prevent from
  CVE-2003-1564, a recursive XML entity expansion leads to memory exhaustion
  in a XML parser)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0014-1
- 2.0014 bump

* Mon Nov 12 2012 Petr Pisar <ppisar@redhat.com> - 1:2.0012-1
- 2.0012 bump

* Thu Nov  8 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:2.0010-2
- fix license field, under MIT is one example

* Mon Nov 05 2012 Petr Šabata <contyk@redhat.com> - 1:2.0010-1
- 2.0010 bumpity

* Tue Oct 23 2012 Petr Šabata <contyk@redhat.com> - 1:2.0008-1
- 2.0008 bump

* Thu Oct 18 2012 Petr Šabata <contyk@redhat.com> - 1:2.0007-1
- 2.0007 bump

* Mon Oct 15 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0006-1
- 2.0006 bump
- Remove bundled library and add BR perl(Devel::CheckLib).

* Mon Aug 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0004-2
- Rebuild for the latest libxml2.

* Thu Aug 09 2012 Petr Šabata <contyk@redhat.com> - 1:2.0004-1
- 2.0004 bump

* Fri Aug 03 2012 Petr Pisar <ppisar@redhat.com> - 1:2.0003-2
- Re-enable 12html test as the bug has been fixed (bug #769537)

* Mon Jul 30 2012 Petr Šabata <contyk@redhat.com> - 1:2.0003-1
- 2.0003 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Petr Pisar <ppisar@redhat.com> - 1:2.0002-2
- Perl 5.16 rebuild

* Tue Jul 10 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0002-1
- 2.0002 bump

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1:2.0001-2
- Perl 5.16 rebuild

* Thu Jun 21 2012 Petr Šabata <contyk@redhat.com> - 1:2.0001-1
- 2.0001 bump

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1:1.99-2
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Šabata <contyk@redhat.com> - 1:1.99-1
- 1.99 bump, test updates

* Mon May 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.98-1
- 1.98 bump

* Wed May 02 2012 Petr Šabata <contyk@redhat.com> - 1:1.97-1
- 1.97 bump

* Mon Mar 19 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.96-1
- 1.96 bump

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 1:1.95-1
- 1.95 bump, tests bugfixes

* Mon Feb 27 2012 Petr Šabata <contyk@redhat.com> - 1:1.93-1
- 1.93 bumpity, minor bugfix

* Thu Feb 23 2012 Petr Pisar <ppisar@redhat.com> - 1:1.92-1
- 1.92 bump
- Declare all dependencies
- Enable thread tests

* Tue Jan 10 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.90-1
- update to 1.90

* Wed Dec 21 2011 Dan Horák <dan[at]danny.cz> - 1:1.88-3
- use better workaround until rhbz#769537 is resolved

* Tue Dec 20 2011 Karsten Hopp <karsten@redhat.com> - 1:1.88-2
- disable tests on ppc as most ppc buildmachines have only 2Gb 
  and the tests run out of memory

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.88-1
- update to 1.88

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1:1.74-2
- Perl mass rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.74-1
- update to 1.74

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.70-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov  5 2010 Paul Howarth <paul@city-fan.org> - 1:1.70-6
- Rebuild for libxml2 2.7.8 in Rawhide
- Move recoding of documentation from %%install to %%prep
- Use %%{?perl_default_filter}
- Use standard %%install idiom

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.70-5
- Mass rebuild with perl-5.12.0

* Fri Jan  8 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-4
- remove BR XML::LibXML::Common

* Mon Nov 30 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-3
- corrected version of obsoletes

* Thu Nov 26 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-2
- 541605 this package now contains XML::LibXML::Common

* Fri Nov 20 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-1
- update to fix 539102

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.69-1
- update to 1.69

* Fri Aug 01 2008 Lubomir Rintel <lkundrak@v3.sk> - 1:1.66-2
- Supress warning about nonexistent file in perl-XML-SAX install trigger

* Mon Jun 23 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:1.66-1
- upgrade to 1.66

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.65-5
- Rebuild for perl 5.10 (again)

* Mon Feb 11 2008 Robin Norwood <rnorwood@redhat.com> - 1:1.65-4
- Build for new perl

* Mon Feb 11 2008 Robin Norwood <rnorwood@redhat.com> - 1:1.65-3
- Resolves: bz#432442
- Use epoch to permit upgrade from 1.62001 -> 1.65

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.65-2
- disable hacks, build normally

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.65-1.1
- rebuild for new perl, first pass, temporarily disable BR: XML::Sax, tests

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 1.65-1
- Update to latest CPAN release: 1.65
- patch0 no longer needed
- various spec file cleanups

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.62001-2.3
- fix stupid test

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.62001-2.2
- add BR: perl(Test::More)

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.62001-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Dec 07 2006 Robin Norwood <rnorwood@redhat.com> - 1.62001-2
- Rebuild

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.62001
- Build latest version from CPAN: 1.62001

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.58-2.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.58-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.58-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.58-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Mar 19 2005 Joe Orton <jorton@redhat.com> 1.58-2
- rebuild

* Sun Apr 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 1.58-1
- #121168
- Update to 1.58.
- Require perl(:MODULE_COMPAT_*).
- Handle ParserDetails.ini parser registration.
- BuildRequires libxml2-devel.
- Own installed directories.

* Fri Feb 27 2004 Chip Turner <cturner@redhat.com> - 1.56-1
- Specfile autogenerated.
