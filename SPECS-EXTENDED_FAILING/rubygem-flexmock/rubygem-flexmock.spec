Vendor:         Microsoft Corporation
Distribution:   Mariner
%global	gem_name	flexmock

Summary:	Mock object library for ruby
Name:		rubygem-%{gem_name}
Version:	2.3.6
Release:	9%{?dist}
License:	MIT
URL:		https://github.com/doudou/flexmock
Source0:	https://github.com/doudou/flexmock/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:	git
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(minitest) >= 5
BuildRequires:	rubygem(rspec) >= 3
Requires:   ruby(release)
Requires:   ruby(rubygems)
Provides:   rubygem(%{gem_name}) = %{version}-%{release}
BuildArch:  noarch

%description
FlexMock is a simple, but flexible, mock object library for Ruby unit
testing.

%package doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}
find . -name \*.rb | xargs sed -i -e '\@/usr/bin/env@d'
find . -name \*.gem -or -name \*.rb -or -name \*.rdoc | xargs chmod 0644

%install
%gem_install -n %{gem_name}-%{version}.gem

mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
#add lib and rake files to buildroot from Source0
cp -a lib/ %{buildroot}%{gem_instdir}/
cp -a rakelib/ %{buildroot}%{gem_instdir}/

pushd %{buildroot}%{gem_instdir}
rm -rf \
	.autotest .gitignore .togglerc .travis.yml .yardopts \
	Gemfile \
	Rakefile \
	flexmock.blurb \
	flexmock.gemspec \
	install.rb
popd

%check
pushd .%{gem_instdir}

ruby -Ilib:.:test \
	-e 'Dir.glob("test/*_test.rb").each {|f| require f}'
rspec test/rspec_integration/
popd

%files
%license LICENSE.txt
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/rakelib/
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_docdir}/

%changelog
* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.3.6-9
- Build from .tar.gz source.

* Thu Feb 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.6-8
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.6-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct  6  2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.6-1
- 2.3.6

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 17 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.5-1
- 2.3.5

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec  1 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.4-1
- 2.3.4

* Mon Oct 17 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.0-1
- 2.3.0

* Fri Jul 15 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.1-1
- 2.2.1

* Thu May  5 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-1
- 2.1.0

* Wed Apr 13 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.5-1
- 2.0.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.4-1
- 2.0.4

* Wed Dec 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.3-1
- 2.0.3

* Thu Sep 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.2-1
- 2.0.2

* Thu Sep 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.1-1
- 2.0.1

* Thu Sep 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.0-1
- 2.0.0

* Fri Aug 14 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.3-5
- Fix two failing tests, and omit one test currently

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.3-3
- Force to use minitest ver4 for now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.3-1
- 1.3.3

* Wed Aug  6 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.2-1
- 1.3.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-1
- 1.3.1

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.0-3
- Macro / BR / Requires cleanup 

* Wed Feb 27 2013 Josef Stribny <jstribny@redhat.com> - 1.3.0-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.0-1
- 1.3.0

* Tue Jan  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.0-1
- 1.2.0

* Sun Nov  4 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.0-1
- 1.1.0

* Thu Oct 11 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.3-1
- 1.0.3

* Fri Sep 14 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.2-1
- 1.0.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-3
- F-17: rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-1
- 0.9.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.11-2
- Fix typo Provides on main package (bug 674413)

* Sun Oct 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.11-1
- 0.8.11

* Fri Jul 23 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.7-1
- 0.8.7

* Thu Jul 30 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.6-1
- Switch to gem, repackage

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 08 2007 Paul Nasrat <pauln@truemesh.com> - 0.7.1-3
- Fix repoid 

* Wed Nov 07 2007 Paul Nasrat <pauln@truemesh.com> - 0.7.1-2
- Spec cleanups in response to review
- Fix license
- strip out shebangs

* Sun Sep 09 2007 Paul Nasrat <pauln@truemesh.com> - 0.7.1-1
- Initial vesion
