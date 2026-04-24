# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Visualize XML files with GraphViz
%bcond_without perl_GraphViz_enables_xml

Name:           perl-GraphViz
Version:        2.26
Release: 8%{?dist}
Summary:        Interface to the GraphViz graphing tool
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/GraphViz
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETJ/GraphViz-%{version}.tar.gz
# Normalize shebangs
Patch0:         GraphViz-2.24-Normalize-shebangs-in-examples.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
# graphviz for the "dot" tool
BuildRequires:  graphviz
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp) >= 1.01
BuildRequires:  perl(IPC::Run) >= 0.6
BuildRequires:  perl(lib)
BuildRequires:  perl(Parse::RecDescent) >= 1.965001
BuildRequires:  perl(Time::HiRes) >= 1.51
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(File::Which) >= 1.09
BuildRequires:  perl(Test::More) >= 1.001002
# "dot" command is executed from GraphViz module
Requires:       graphviz
Requires:       perl(Carp) >= 1.01
Requires:       perl(IPC::Run) >= 0.6
Requires:       perl(Parse::RecDescent) >= 1.965001
Requires:       perl(Time::HiRes) >= 1.51

%{?perl_default_filter}
# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Carp|IPC::Run|Parse::RecDescent|Time::HiRes|XML::Twig)\\)$

%description
This Perl module provides an interface to layout and image generation of
directed and undirected graphs in a variety of formats (PostScript, PNG,
etc.) using the "dot", "neato", "twopi", "circo" and "fdp" programs from
the GraphViz project (<http://www.graphviz.org/>).

%if %{with perl_GraphViz_enables_xml}
%package XML
Summary:        Visualize XML as a tree
Requires:       %{name} = %{version}-%{release}
Requires:       perl(Carp) >= 1.01
Requires:       perl(XML::Twig) >= 3.52

%description XML
GraphViz::XML Perl module makes it easy to visualize XML as a tree. XML
elements are represented as diamond nodes, with links to elements within them.
Character data is represented in round nodes.
%endif

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n GraphViz-%{version}
%patch -P0 -p1
find -type f -exec chmod -x {} +

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
mv examples/xml.pl ./

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
perl -i -pe 's{(as_foo.\d)}{/tmp/$1}' %{buildroot}%{_libexecdir}/%{name}/t/foo.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
make test

%files
%license LICENSE
%doc Changes README examples/
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/GraphViz/XML.pm
%{_mandir}/man3/Devel*
%{_mandir}/man3/GraphViz*
%exclude %{_mandir}/man3/GraphViz::XML.*

%if %{with perl_GraphViz_enables_xml}
%files XML
%doc xml.pl
%{perl_vendorlib}/GraphViz/XML.pm
%{_mandir}/man3/GraphViz::XML.*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 06 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-1
- 2.26 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 22 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-1
- 2.25 bump
- Package tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-20
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-17
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-14
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Petr Pisar <ppisar@redhat.com> - 2.24-12
- Remove a useless build dependency on graphviz-devel

* Thu Nov 07 2019 Petr Pisar <ppisar@redhat.com> - 2.24-11
- Modernize a spec file
- Correct dependencies
- Subpackage GraphViz::XML to perl-GrapViz-XML package

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 01 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-1
- 2.24 bump

* Tue Jul 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.22-1
- 2.22 bump

* Mon May 23 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.21-1
- 2.21 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 04 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-1
- 2.20 bump

* Fri Nov 13 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.19-1
- 2.19 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 07 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-2
- Perl 5.22 rebuild

* Thu May 28 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-1
- 2.18 bump

* Wed Nov 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-1
- 2.16 bump
- Modernize spec file

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.14-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 2.14-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 09 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.14-1
- Upstream update.
- Minor spec file brushup.

* Mon Sep 24 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.11-1
- Upstream update.
- Add perl_default_filter.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 2.10-2
- Perl 5.16 rebuild

* Tue Apr 03 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.10-1
- Upstream update.

* Sun Jan 15 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.09-1
- Upstream update.
- Modernize spec-file.
- Reflect Source0-URL having changed.
- Add missing BRs.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.04-7
- Perl mass rebuild

* Tue Apr 19 2011 Paul Howarth <paul@city-fan.org> - 2.04-6
- Don't provide perl(DB)

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.04-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.04-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.04-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 30 2009 Stepan Kasal <skasal@redhat.com> - 2.04-1
- update to 2.04

* Sun Mar 29 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.03-3
- add manual Requires on graphviz (bz 492318)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.03-1
- update to 2.03

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.02-3
- rebuild for new perl

* Thu Apr 19 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.02-2
- bump

* Mon Apr 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 2.02-1
- Specfile autogenerated by cpanspec 1.70.
