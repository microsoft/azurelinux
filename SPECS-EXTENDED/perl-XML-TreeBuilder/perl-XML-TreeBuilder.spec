Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:	Parser that builds a tree of XML::Element objects
Name:		perl-XML-TreeBuilder
Version:	5.4
Release:	18%{?dist}
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/XML-TreeBuilder
# have to:
#  push the patch upstream
Source:		https://cpan.metacpan.org/modules/by-module/XML/XML-TreeBuilder-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Carp)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(HTML::Element) >= 4.1
BuildRequires:	perl(HTML::Tagset)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XML::Catalog) >= 1.02
BuildRequires:	perl(XML::Parser)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
perl-XML-TreeBuilder is a Perl module that implements a parser
that builds a tree of XML::Element objects.

%prep
%setup -q -n XML-TreeBuilder-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%check
./Build test

%install
%{__rm} -rf $RPM_BUILD_ROOT
./Build pure_install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%files
%doc Changes README
%{_mandir}/man3/*.3pm*
%{perl_vendorlib}/XML/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.4-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 5.4-16
- Updated build dependencies (bug #1588542)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 5.4-14
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 5.4-11
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 5.4-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 5.4-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 5.4-3
- Perl 5.22 rebuild

* Thu May 28 2015 Jitka Plesnikova <jplesnik@redhat.com> - 5.4-2
- Update list of build-requires and requires

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 5.4-1
- Perl 5.20 rebuild

* Wed Aug 6 2014 Rüdiger Landmann <r.landmann@redhat.com> - 5.4-0
- new upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 28 2013 Jeff Fearn <jfearn@redhat.com> - 5.1-0
- Fix entities in attributes only working for root node. RT #89402

* Fri Oct 04 2013 Jeff Fearn <jfearn@redhat.com> - 5.0-0
- Support entity expansion.

* Fri Jan 25 2013 Jeff Fearn <jfearn@redhat.com> - 4.1-0
- Support XML::Parser ParseParamEnt parameter

* Tue Jan 4 2011 Rüdiger Landmann <r.landmann@redhat.com> - 4.0-3
- Add Test::More to build requires

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.0-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jun 21 2010  Jeff Fearn <jfearn@redhat.com> - 4.0-1
- new upstream version.

* Tue Sep 29 2009  Jeff Fearn <jfearn@redhat.com> - 3.09-16
- Stupid man! Don't eat entities :(

* Mon Sep 28 2009  Jeff Fearn <jfearn@redhat.com> - 3.09-15
- Always remove NoExpand and ErrorContext from output

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.09-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Jeff Fearn <jfearn@redhat.com> - 3.09-13
- Remove NoExpand and ErrorContext from output if they aren't set.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.09-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 15 2008 Jeff Fearn <jfearn@redhat.com> - 3.09-11
- Add ErrorContext pass through
- Fix crash on Entity declaration. BZ #461557

* Thu May 29 2008 Jeff Fearn <jfearn@redhat.com> - 3.09-10
- Rebuild for docs

* Fri Jan 18 2008 Jeff Fearn <jfearn@redhat.com> - 3.09-9
- Missed one 3.10

* Fri Jan 18 2008 Jeff Fearn <jfearn@redhat.com> - 3.09-8
- Pretend 3.10 never happened

* Thu Jan 17 2008 Jeff Fearn <jfearn@redhat.com> - 3.09-7
- Trimmed Summary

* Fri Jan 11 2008 Jeff Fearn <jfearn@redhat.com> - 3.09-6
- Fixed test
- Fixed Source URL
- Added %%check

* Tue Jan 08 2008 Jeff Fearn <jfearn@redhat.com> - 3.09-5
- Changed Development/Languages to Development/Libraries

* Tue Jan 08 2008 Jeff Fearn <jfearn@redhat.com> - 3.09-4
- Remove %%doc from man files, used glob
- Simplify XML in filelist
- Remove OPTIMIZE setting from make call
- Change buildroot to fedora style
- Remove unused defines

* Mon Jan 07 2008 Jeff Fearn <jfearn@redhat.com> - 3.09-3
- Tidy spec file

* Wed Dec 12 2007 Jeff Fearn <jfearn@redhat.com> - 3.09-2
- Add dist param
- Add NoExpand to allow entities to pass thru un-expanded

* Fri May 04 2007 Dag Wieers <dag@wieers.com> - 3.09-1
- Initial package. (using DAR)
