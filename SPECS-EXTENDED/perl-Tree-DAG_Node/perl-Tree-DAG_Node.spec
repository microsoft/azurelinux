Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Tree-DAG_Node
Version:        1.31
Release:        8%{?dist}
Summary:        Class for representing nodes in a tree
License:        (GPL+ or Artistic)
URL:            https://metacpan.org/release/Tree-DAG_Node
Source0:        https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Tree-DAG_Node-%{version}.tgz
BuildArch:      noarch
# Module Build ---------------------------------------------------------------
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  sed
# Module Runtime -------------------------------------------------------------
BuildRequires:  perl(File::Slurp::Tiny) >= 0.003
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite -----------------------------------------------------------------
BuildRequires:  perl(File::Spec) >= 3.4
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(Test::More) >= 1.001002
BuildRequires:  perl(Test::Pod) >= 1.48
BuildRequires:  perl(utf8)
# Runtime --------------------------------------------------------------------
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This class encapsulates/makes/manipulates objects that represent nodes in a
tree structure. The tree structure is not an object itself, but is emergent
from the linkages you create between nodes. This class provides the methods
for making linkages that can be used to build up a tree, while preventing you
from ever making any kinds of linkages that are not allowed in a tree (such as
having a node be its own mother or ancestor, or having a node have two
mothers).

%prep
%setup -q -n Tree-DAG_Node-%{version}

# Fix up shellbangs in example scripts
sed -i -e 's|^#!/usr/bin/env perl|#!/usr/bin/perl|' scripts/*.pl

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README scripts/
%{perl_vendorlib}/Tree/
%{_mandir}/man3/Tree::DAG_Node.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.31-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-2
- Perl 5.28 rebuild

* Wed Feb 14 2018 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31
  - Clarify licence issue by changing the reference in the DAG_Node.pm file
    from Artistic V2 to Perl, so it now matches what I preemptively put in
    Makefile.PL and the LICENSE file; Sean Burke has kindly agreed to this
    change (GH#1)
- License changed to GPL+ or Artistic

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30
  - Explicitly escape { and } in a regexp because unescaped { issues a warning
    now and will become a fatal error in Perl 5.32
  - Adopt new repo structure, see:
    https://savage.net.au/Ron/html/My.Workflow.for.Building.Distros.html
- Drop legacy Group: tag
- Simplify find command using -delete

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-2
- Perl 5.24 rebuild

* Tue Mar  1 2016 Paul Howarth <paul@city-fan.org> - 1.29-1
- Update to 1.29
  - No code changes
  - Rework Makefile.PL so File::Spec, File::Temp and Test::More are in
    TEST_REQUIRES (CPAN RT#112568)
  - Expand the SYNOPSIS
  - Update MANIFEST.SKIP to include .gitignore
  - Test::Pod is only a developer dependency

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jul 12 2015 Paul Howarth <paul@city-fan.org> - 1.27-1
- Update to 1.27
  - Remove the line that reads 'use open qw(:std :utf8);' (CPAN RT#105798)
  - Remove Build.PL, ship only Makefile.PL
  - Remove .gitignore from MANIFEST

* Mon Jun 22 2015 Paul Howarth <paul@city-fan.org> - 1.26-4
- Specify all dependencies (#1234366)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-2
- Perl 5.22 rebuild

* Sun Apr 12 2015 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26
  - Fix bug in string2hashref(), which failed on some strings, such as
    {a => 'b, c'}
  - Add t/string2hash.t to test new code

* Mon Mar 23 2015 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25
  - Deleted the undocumented sub _dump_quote(), which butchered Unicode
    characters when it tried to convert ASCII control characters into printable
    strings (on the assumption all data is ASCII); methods that used to call
    _dump_quote() now just output the node's name by calling quote_name(),
    which is discussed next, and undefined names are output as the string
    'undef'
  - Add method quote_name(), which simply returns its input string surrounded
    by single-quotes
  - Add method decode_lol(), which converts the output of tree_to_lol() and
    tree_to_simple_lol() into something that is easy to read
  - Re-order a couple of methods called tree_*(), so that they are in
    alphabetical order
  - Expand the docs for methods tree_to_*(), regarding undefined node names
  - Add scripts/write.tree.pl, which creates the test input file
    t/tree.utf8.attributes.txt (note: this file is now much more complex than
    in previous versions)
  - Add scripts/read.tree.pl, and its output file scripts/read.tree.log; this
    program demonstrates the output produced by various methods
  - Fix the faulty syntax I had used in Build.PL to identify the github repo
  - Delete and re-create github repo after 'git push' failed to upload the new
    version
  - Add LICENSE file to MANIFEST
- Package LICENSE and scripts (as documentation)

* Sun Jan 25 2015 Paul Howarth <paul@city-fan.org> - 1.24-1
- Update to 1.24
  - Clean up discussion in docs of original author's reluctance to allow
    parameters to new()
  - Rewrite bareword filehandles to use a variable (my $fh)
  - Rename github repo from Tree--DAG_Node to Tree-DAG_Node - my new standard;
    update Build.PL and Makefile.PL to match
  - Reformat the docs to be ≤ 100 chars per line - my new standard
  - Change horizontal indentation used by node2string() to add 1 space, so '|'
    lines up underneath the first char of the previous node's name

* Tue Oct 21 2014 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 1.23
  - Change output format when using node2string(), which is called by
    tree2string(); indentation that used to be '|---' is now '|--- ', which
    makes the difference between node names ''/'-', '1'/'-1', etc. much clearer
- Classify buildreqs by usage

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Paul Howarth <paul@city-fan.org> - 1.22-1
- Update to 1.22
  - Switch from File::Slurp to File::Slurp::Tiny (CPAN RT#92976)

* Fri Jan 31 2014 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to 1.20
  - Bump File::Temp version requirement back up to 0.19, as that's the version
    that introduced the newdir() method, as used in the test suite

* Thu Jan 30 2014 Paul Howarth <paul@city-fan.org> - 1.19-1
- Update to 1.19
  - Set pre-req File::Temp version # to 0 (back from 0.2301)

* Thu Sep 19 2013 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to 1.18
  - No changes, code or otherwise, except for the version # in the *.pm, this
    file, and Changelog.ini
  - Somehow a corrupted version got uploaded to search.cpan.org, so I've just
    changed the version # (the file on MetaCPAN was fine)

* Mon Sep 16 2013 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to 1.17
  - Write test temp files in :raw mode as well as utf-8, for MS Windows users
  - Take the opportunity to change all utf8 to utf-8, as per the docs for Encode,
    except for 'use warnings qw(FATAL utf8);', which doesn't accept utf-8 :-(

* Mon Sep  9 2013 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to 1.16
  - Merge patch (slightly modified by me) from Tom Molesworth (CPAN RT#88501):
    - Remove 'use open qw(:std :utf8);' because of its global effect
    - Replace Perl6::Slurp with File::Slurp, using the latter's binmode option
      for the encoding
    - Fix docs where I'd erroneously said File::Slurp didn't support utf8

* Fri Sep  6 2013 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to 1.15
  - Replace Path::Tiny with File::Spec, because the former's list of
    dependencies is soooo long :-( (CPAN RT#88435)
  - Move t/pod.t to xt/author/pod.t
- Explicitly run the author tests

* Thu Sep  5 2013 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to 1.14
  - Document the copy() method
  - Patch the copy() method so it respects the {no_attribute_copy => 1} option
  - Add method read_tree(), for text files; it uses Perl6::Slurp, which
    supports utf8
  - Add methods read_attributes() and string2hashref($s) for use by read_tree()
  - Add t/read.tree.t to test read_tree()
  - Add t/tree.utf8.attributes.txt, in utf8, for use by t/read.tree.t
  - Add t/tree.with.attributes.txt and t/tree.without.attributes.txt for use by
    t/read.tree.t
  - Make Perl 5.8.1 a pre-req so we have access to the utf8 pragma

* Mon Aug 12 2013 Paul Howarth <paul@city-fan.org> - 1.13-1
- Update to 1.13
  - Change the values accepted for the no_attributes option from undef and 1
    to 0 and 1; if undef is used, it becomes 0, so pre-existing code will not
    change behavior, whilst this makes it easier to pass 0 or 1 from the
    command line

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.12-2
- Perl 5.18 rebuild

* Wed Jul  3 2013 Paul Howarth <paul@city-fan.org> - 1.12-1
- Update to 1.12
  - Change text in README referring to licence to match text in body of source,
    since it was in conflict with the Artistic Licence V 2.0
  - Rename CHANGES to Changes as per CPAN::Changes::SPEC
  - Various spelling fixes in the docs

* Mon Feb  4 2013 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - License clarified as Artistic 2.0 (CPAN RT#83088)

* Fri Feb  1 2013 Paul Howarth <paul@city-fan.org> - 1.10-1
- Update to 1.10
  - Look for but don't require Test::Pod ≥ 1.45 (CPAN RT#83077)

* Fri Nov 23 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.09-2
- Update dependencies
- Remove BuildRoot cleaning

* Fri Nov  9 2012 Paul Howarth <paul@city-fan.org> - 1.09-1
- Update to 1.09
  - No code changes
  - For pre-reqs such as strict, warnings, etc., which ship with Perl, set the
    version requirement to 0 (CPAN RT#80663)

* Fri Nov  2 2012 Paul Howarth <paul@city-fan.org> - 1.07-1
- Update to 1.07
  - New maintainer: Ron Savage
  - Pre-emptive apologies for any changes which are not back-compatible; no
    such problems are expected, but the introduction of new methods may
    disconcert some viewers
  - Fix CPAN RT#78858 and audit code for similar problems
  - Fix CPAN RT#79506
  - Rename ChangeLog to CHANGES, and add Changelog.ini
  - Replace all uses of cyclicity_fault() and Carp::croak with die
  - Remove unused methods: decommission_root(), cyclicity_allowed(),
    cyclicity_fault(), inaugurate_root(), no_cyclicity() and _update_links();
    OK - cyclicity_fault() was called once - it just died
  - Add methods: format_node(), hashref2string(), is_root(), node2string(),
    tree2string()
  - Reformat the POD big-time
  - Add Build.PL
  - Re-write Makefile.PL
  - Remove use vars(@ISA $Debug $VERSION), and replace latter 2 with 'our ...'
  - Rename t/00_about_verbose.t to t/about.perl.t
  - Add scripts/cut.and.paste.subtrees.pl (Warning: Some trees get into an
    infinite loop)
  - Add t/cut.and.paste.subtrees.t (Warning: Some trees get into an infinite
    loop)
  - Document the options (discouraged by Sean) supported in the call to
    new($hashref)
- This release by RSAVAGE -> update source URL
- BR: perl(Test::More) and perl(Test::Pod) ≥ 1.00
- Modernize spec file:
  - Drop %%clean section
  - Drop buildroot definition and cleaning
  - Don't use macros for commands
  - Don't need to remove empty directories from the buildroot
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Drop %%defattr, redundant since rpm 4.4

* Mon Oct 29 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-15
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.06-13
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.06-11
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-9
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-8
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.06-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-4
- fix source url

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-3
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-1
- 1.06

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-4
- Rebuild for FC6.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Jul  1 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-2
- Dist tag.

* Thu Dec 30 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.05-0.fdr.1
- Update to 1.05.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.04-0.fdr.1
- First build.
