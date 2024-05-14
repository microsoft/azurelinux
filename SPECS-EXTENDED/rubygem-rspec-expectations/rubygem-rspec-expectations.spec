Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global	majorver	3.12.0
%global	fullver	%{majorver}%{?preminorver}

%global	gem_name	rspec-expectations

%global	need_bootstrap_set	0

%undefine __brp_mangle_shebangs

Summary:	RSpec expectations (should and matchers)
Name:		rubygem-%{gem_name}
Version:	%{majorver}
Release:	1%{?dist}

License:	MIT
URL:		https://github.com/rspec/rspec-expectations
Source0:	https://github.com/rspec/rspec-expectations/archive/refs/tags/v%{version}.tar.gz#/rubygem-%{gem_name}-%{version}.tar.gz

#BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
%if 0%{?need_bootstrap_set} < 1
BuildRequires:	rubygem(rspec)
# Some features in expectations needs this
BuildRequires:	rubygem(rspec-support) >= 3.9.3
BuildRequires:	rubygem(minitest) >= 5
BuildRequires:	git
%endif
BuildArch:		noarch

%description
rspec-expectations adds `should` and `should_not` to every object and includes
RSpec::Matchers, a library of standard matchers.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.


%prep
%autosetup -S git -n %{gem_name}-%{version}

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# cleanups
rm -f %{buildroot}%{gem_instdir}/{.document,.yardopts}

%if 0%{?need_bootstrap_set} < 1
%check
LANG=C.UTF-8
ruby -rrubygems -Ilib/ -S rspec spec/
%endif

%files
%dir	%{gem_instdir}

%license	%{gem_instdir}/LICENSE.md
%doc	%{gem_instdir}/Changelog.md
%doc	%{gem_instdir}/README.md

%{gem_instdir}/lib/

%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%{gem_docdir}

%changelog
* Mon Nov 28 2022 Muhammad Falak <mwani@microsoft.com> - 3.12.0-1
- Switch to build from .tar.gz
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.9.2-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sat May  9 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.2-1
- 3.9.2

* Sun Apr 19 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.1-1
- 3.9.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 10 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.0-2
- Enable tests again

* Tue Dec 10 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.0-0.1
- 3.9.0
- Once disable test for bootstrap

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.4-1
- 3.8.4

* Wed Apr 24 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.3-1
- 3.8.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 13 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.2-1
- Enable tests again

* Wed Dec 12 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.2-0.1
- 3.8.2
- Once disable test for bootstrap

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.7.0-3.2
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.0-3
- Backport upstream patch to fix test failure on ruby 25

* Tue Feb 13 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.0-2
- ruby 2.5 drops -rubygems usage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.0-1
- Enable tests again

* Mon Nov 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.0-0.1
- 3.7.0
- Once disable tests

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat May  6 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.0-1
- Enable tests again

* Sat May  6 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.0-0.1
- 3.6.0
- Once disable tests

* Tue Feb 21 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-3
- Always use full tar.gz for installed files and
  keep using gem file for gem spec (ref: bug 1425220)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Vít Ondruch <vondruch@redhat.com> - 3.5.0-2
- Fix Ruby 2.4 compatibility.

* Sun Jul 24 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-1
- Enable tests again

* Sat Jul 23 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-0.1
- 3.5.0
- Once disable tests

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-2
- Enable tests again

* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-1
- 3.4.0
- Once disable tests

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.1-2
- Enable tests again

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.1-1
- 3.3.1
- Once disable tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-1
- 3.2.1

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.0-2
- Enable tests again

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.0-1
- 3.2.0
- Once disable tests

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-2
- Enable tests

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-1
- 3.1.2
- Once disable tests

* Fri Aug 15 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.4-1
- 3.0.4

* Thu Aug 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.3-1
- 3.0.3

* Thu Aug 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.5-4
- Clearner way to specify minitest 4.x

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.5-3
- Backport temporarily be_truthy matchers and so on

* Thu Jun 26 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.5-2
- Force to use minitest 4.x, 5.x is too dangerous now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.5-1
- 2.14.5

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.4-1
- 2.14.4

* Fri Sep 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.3-1
- 2.14.3

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.2-2
- Enable test suite again

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.2-1
- 2.14.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.0-2
- Enable test suite again

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.0-1
- 2.13.0

* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 2.12.1-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.1-2
- Enable test suite again

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.1-1
- 2.12.1

* Thu Oct 11 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.11.3-1
- 2.11.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.8.0-2
- Require (diff-lcs) again

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.8.0-1
- 2.8.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-1
- 2.6.0

* Tue May 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-0.3.rc6
- 2.6.0 rc6

* Tue May  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org>
- And enable check on rawhide

* Tue May  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-0.1.rc4
- 2.6.0 rc4

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org>
- And enable check on rawhide

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.5.0-2
- Cleanups

* Thu Feb 17 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.5.0-1
- 2.5.0

* Fri Nov 05 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- Initial package
