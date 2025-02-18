%global	majorver	3.13.2
#%%global	preminorver	.rc6
%global	rpmminorver	.%(echo %preminorver | sed -e 's|^\\.\\.*||')
%global	fullver	%{majorver}%{?preminorver}

%global	baserelease	1

%global	gem_name	rspec-mocks

%bcond_with bootstrap

%undefine __brp_mangle_shebangs

Summary:	RSpec's 'test double' framework (mocks and stubs)
Name:		rubygem-%{gem_name}
Version:	%{majorver}
Release:	%{?preminorver:0.}%{baserelease}%{?preminorver:%{rpmminorver}}%{?dist}

# SPDX confirmed
License:	MIT
URL:		http://github.com/rspec/rspec-mocks
Source0:	https://rubygems.org/gems/%{gem_name}-%{fullver}.gem
# %%{SOURCE2} %%{name} %%{version}
Source1:	rubygem-%{gem_name}-%{version}-full.tar.gz
Source2:	rspec-related-create-full-tarball.sh

BuildRequires:	rubygems-devel
%if %{without bootstrap}
# rspec
BuildRequires:	rubygem(rspec)
BuildRequires:	rubygem(rake)
%if %{undefined rhel}
# cucumber
BuildRequires:	rubygem(aruba)
BuildRequires:	rubygem(cucumber)
BuildRequires:	rubygem(minitest)
%endif
BuildRequires:	git
%endif
BuildArch:	noarch

%description
rspec-mocks provides a test-double framework for rspec including support
for method stubs, fakes, and message expectations.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version} -b 1

# Cucumber 7 syntax change
sed -i cucumber.yml -e "s|~@wip|not @wip|"
sed -i features/support/disallow_certain_apis.rb -e "s|~@allow-old-syntax|not @allow-old-syntax|"

gem specification %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# cleanups
rm -f %{buildroot}%{gem_instdir}/{.document,.yardopts}

%check
%if %{with bootstrap}
# Don't do actual check
exit 0
%endif

%if %{defined rhel}
# avoid aruba dep on RHEL, but tests fail if files are removed entirely
echo -n > spec/integration/rails_support_spec.rb
echo -n > spec/support/aruba.rb
%else
# Don't call bundler
sed -i spec/integration/rails_support_spec.rb \
	-e 's|bundle exec rspec|rspec|'
%endif

# library_wide_checks.rb needs UTF-8
LANG=C.UTF-8
export RUBYLIB=$(pwd)/lib
rspec spec/

%if 0%{?rhel}
# Don't do cucumber test
exit 0
%endif
export CUCUMBER_PUBLISH_QUIET=true
cucumber

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
* Thu Oct 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.13.2-1
- 3.13.2

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 09 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.13.1-1
- 3.13.1

* Thu Apr 18 2024 Jun Aruga <jaruga@redhat.com> - 3.13.0-2
- Remove unused thread_order build dependency

* Fri Feb 09 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.13.0-1
- 3.13.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.6-1
- 3.12.6

* Sat Apr  1 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.5-1
- 3.12.5

* Tue Mar 14 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.4-1
- 3.12.4

* Thu Mar 09 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.12.3-2
- Disable unwanted dependencies in RHEL builds

* Thu Feb 16 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.3-1
- 3.12.3

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec  2 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.0-3
- Backport upstream reviewing patch for ruby32 ruby2_keywords treatment change

* Thu Nov  3 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.0-2
- On Fedora 37, remove "Display keyword hashes" feature for now
  (On Fedora 38, this is effective)

* Thu Oct 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.0-1
- 3.12.0

* Wed Oct 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.11.2-1
- 3.11.2

* Mon Oct  3 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.11.1-2
- Backport upstream patch for ruby32 wrt method reference changes

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr  7 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.11.1-1
- 3.11.1

* Thu Feb 10 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.11.0-1
- 3.11.0

* Sun Jan 30 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.3-1
- 3.10.3

* Sun Jan 30 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.2-3
- BR: rubygem(rake) for check

* Thu Jan 20 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.2-2
- Execute cucumber test

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb  1 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.2-1
- 3.10.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 29 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.1-1
- 3.10.1

* Fri Dec 11 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.0-1
- Enable tests again

* Fri Dec 11 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.0-0.1
- 3.10.0
- Once disable test for bootstrap

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan  2 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.1-1
- 3.9.1

* Tue Dec 10 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.0-2
- Enable tests again

* Tue Dec 10 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.0-0.1
- 3.9.0
- Once disable test for bootstrap

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.1-1
- 3.8.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 13 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.0-1
- Enable tests again

* Wed Dec 12 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.0-0.1
- 3.8.0
- Once disable test for bootstrap

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.7.0-3.2
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.1-3
- Backport patch to fix test failure with ruby 2.5

* Tue Feb 13 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.1-2
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

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Vít Ondruch <vondruch@redhat.com> - 3.5.0-2
- Fix Ruby 2.4 compatibility.

* Sun Jul 24 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-1
- Enable tests again

* Sat Jul 23 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-0.1
- 3.5.0
- Once disable tests

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-1
- 3.4.1

* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-2
- Enable tests again

* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-1
- 3.4.0
- Once disable tests

* Wed Aug 12 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-3
- Enable thread_order dependent tests

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-2
- Enable tests again

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-1
- 3.3.2
- Once disable tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-1
- 3.2.1

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.0-2
- Enable tests again

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.0-1
- 3.2.0
- Once disable tests

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.3-2
- Enable tests

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.3-1
- 3.1.3
- Once disable tests

* Fri Aug 15 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.4-1
- 3.0.4

* Thu Aug 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.3-1
- 3.0.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.6-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.6-1
- 2.14.6

* Tue Feb  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.5-1
- 2.14.5

* Thu Oct 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.4-1
- 2.14.4

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.3-2
- Enable test suite again

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.3-1
- 2.14.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 12 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.1-1
- 2.13.1

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.0-2
- Enable test suite again

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.0-1
- 2.13.0

* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 2.12.2-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.2-1
- 2.12.2

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.1-2
- Enable test suite again

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.1-1
- 2.12.1

* Thu Oct 11 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.11.3-1
- 2.11.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

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
