%if ! (0%{?rhel})
%{bcond_without perl_File_Find_Object_Rule_enables_optional_test}
%else
%{bcond_with perl_File_Find_Object_Rule_enables_optional_test}
%endif

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-File-Find-Object-Rule
Version:        0.0313
Release:        10%{?dist}
Summary:        Alternative interface to File::Find::Object
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/File-Find-Object-Rule
Source0:        https://cpan.metacpan.org/modules/by-module/File/File-Find-Object-Rule-%{version}.tar.gz#/perl-File-Find-Object-Rule-%{version}.tar.gz
Patch0:         File-Find-Object-Rule-0.0310-shellbang.patch
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Module::Build) >= 0.28
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::XSAccessor)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find::Object)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Number::Compare)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::Glob)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Script Runtime
BuildRequires:  perl(File::Spec::Functions)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::TreeCreate)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
# Dependencies
# (none)

%description
File::Find::Object::Rule is a friendlier interface to File::Find::Object. It 
allows you to build rules that specify the desired files and directories.

%prep
%setup -qn File-Find-Object-Rule-%{version}

# Avoid use of /usr/bin/env
%patch -P 0

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
./Build test

%files
%license LICENSE
%doc Changes Changes.F-F-R README
%{_bindir}/findorule
%{perl_vendorlib}/File/
%{_mandir}/man1/findorule.1*
%{_mandir}/man3/File::Find::Object::Rule.3*
%{_mandir}/man3/File::Find::Object::Rule::Extending.3*
%{_mandir}/man3/File::Find::Object::Rule::Procedural.3*

%changelog
* Wed Apr 09 2025 Archana Shettigar <v-shettigara@microsoft.com> - 0.0313-10
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0313-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0313-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0313-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0313-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0313-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0313-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.0313-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0313-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 27 2021 Paul Howarth <paul@city-fan.org> - 0.0313-1
- Update to 0.0313
  - Split File::TreeCreate off to its own distribution

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0312-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.0312-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0312-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0312-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.0312-3
- Perl 5.32 rebuild

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 0.0312-2
- BR: perl(blib) for t/00-compile.t and t/findorule.t

* Tue Jan 28 2020 Paul Howarth <paul@city-fan.org> - 0.0312-1
- Update to 0.0312
  - Rebuild for order of 'NAME' and 'VERSION' sections in the generated POD
    documentation (VERSION used to appear before NAME)

* Mon Aug 26 2019 Paul Howarth <paul@city-fan.org> - 0.0311-1
- Update to 0.0311
  - Moved the VCS repo to https://github.com/shlomif/perl-file-find-object-rule

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0310-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.0310-2
- Perl 5.30 rebuild

* Sat Apr  6 2019 Paul Howarth <paul@city-fan.org> - 0.0310-1
- Update to 0.0310
  - Fully qualified shebang for findorule
  - Enable tidyall in dist.ini
- Add patch to avoid use of /usr/bin/env in findorule
- Extra tests moved to xt/ so drop build dependencies for them

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0309-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0309-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.0309-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.0309-2
- Perl 5.28 rebuild

* Wed Jun 20 2018 Paul Howarth <paul@city-fan.org> - 0.0309-1
- Update to 0.0309
  - Apply spelling fixes patch from Debian (CPAN RT#125635)

* Thu May 24 2018 Paul Howarth <paul@city-fan.org> - 0.0307-1
- Update to 0.0307
  - Convert to Dist-Zilla
- Switch upstream from search.cpan.org to metacpan.org

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0306-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0306-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.0306-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.0306-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0306-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 12 2016 Paul Howarth <paul@city-fan.org> - 0.0306-1
- Update to 0.0306
  - Made the trailing space tests RELEASE_TESTING only

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.0305-8
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.0305-7
- Perl 5.24 rebuild

* Mon Feb 29 2016 Paul Howarth <paul@city-fan.org> - 0.0305-6
- Classify buildreqs by usage
- Make %%files list more explicit
- Use %%license

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0305-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0305-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.0305-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.0305-2
- Perl 5.20 rebuild

* Sun Jun 08 2014 Christopher Meng <rpm@cicku.me> - 0.0305-1
- Update to 0.0305

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0304-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 13 2014 Christopher Meng <rpm@cicku.me> - 0.0304-1
- Update to 0.0304

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0303-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Christopher Meng <rpm@cicku.me> - 0.0303-1
- Initial Package.
