Vendor:         Microsoft Corporation
Distribution:   Mariner
# Generated from rdoc-3.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rdoc

Name: rubygem-%{gem_name}
Version: 6.1.1
Release: 3%{?dist}
Summary: RDoc produces HTML and command-line documentation for Ruby projects
# OFL: lib/rdoc/generator/template/darkfish/css/fonts.css
License: GPLv2 and Ruby and MIT and OFL
URL: https://ruby.github.io/rdoc
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rdoc/rdoc.git && cd rdoc
# git archive -v -o rdoc-6.1.1-tests.tar.xz v6.1.1 test/
Source1: %{gem_name}-%{version}-tests.tar.xz
# Fix ruby_version abuse. Keep this in sinc with ruby-2.3.0-ruby_version.patch
# applied in ruby package.
# https://bugs.ruby-lang.org/issues/11002
Patch0: rubygem-rdoc-5.1.0-ruby_version.patch
Requires: rubygem(irb)
Requires: rubygem(io-console)
Requires: rubygem(json)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest) >= 5
BuildRequires: rubygem(did_you_mean)
# Execute Rake integration test cases.
BuildRequires: rubygem(rake)
Provides: rdoc = %{version}-%{release}
Provides: ri = %{version}-%{release}
BuildArch: noarch

%description
RDoc produces HTML and command-line documentation for Ruby projects.
RDoc includes the +rdoc+ and +ri+ tools for generating and displaying
documentation from the command-line.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/exe -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
cp -a %{_builddir}/test test

# Avoid Bundler dependency.
sed -i '/bundler/ s/^/#/' test/minitest_helper.rb

DONT_USE_BUNDLER_FOR_GEMDEPS=true RUBYOPT=-Ilib ruby -Itest -e 'Dir.glob "./test/**/test_*.rb", &method(:require)' -- -v
popd

%files
%dir %{gem_instdir}
%{_bindir}/rdoc
%{_bindir}/ri
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE.rdoc
%license %{gem_instdir}/LEGAL.rdoc
%{gem_instdir}/exe
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.rdoc
%doc %{gem_instdir}/CVE-2013-0256.rdoc
%doc %{gem_instdir}/Example*
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/RI.rdoc
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/TODO.rdoc
%{gem_instdir}/appveyor.yml
%{gem_instdir}/bin
%{gem_instdir}/rdoc.gemspec

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1.1-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Vít Ondruch <vondruch@redhat.com> - 6.1.1-1
- Update to RDoc 6.1.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 11 2018 Vít Ondruch <vondruch@redhat.com> - 6.0.3-2
- Add missing rubygem(json) dependency (rhbz#1565960).

* Tue Apr 03 2018 Vít Ondruch <vondruch@redhat.com> - 6.0.3-1
- Update to RDoc 6.0.3.

* Thu Mar 22 2018 Vít Ondruch <vondruch@redhat.com> - 6.0.2-1
- Update to RDoc 6.0.2.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Vít Ondruch <vondruch@redhat.com> - 5.1.0-2
- Fix the RI path (rhbz#1458131).

* Fri Feb 24 2017 Vít Ondruch <vondruch@redhat.com> - 5.1.0-1
- Update to RDoc 5.1.0.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 09 2016 Vít Ondruch <vondruch@redhat.com> - 4.2.2-2
- Fix broken links to assets.

* Mon May 23 2016 Vít Ondruch <vondruch@redhat.com> - 4.2.2-1
- Update to RDoc 4.2.2.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 08 2014 Vít Ondruch <vondruch@redhat.com> - 4.1.1-2
- Add missing IRB dependency.

* Mon Jul 07 2014 Vít Ondruch <vondruch@redhat.com> - 4.1.1-1
- Update to RDoc 4.1.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 29 2013 Vít Ondruch <vondruch@redhat.com> - 4.0.1-1
- Update to RDoc 4.0.1.

* Tue Mar 26 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-100
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to RDoc 4.0.0

* Wed Feb 06 2013 Josef Stribny <jstribny@redhat.com> - 3.12.1-2
- Encoding issue is still unresolved in upstream.

* Wed Feb 06 2013 Josef Stribny <jstribny@redhat.com> - 3.12.1-1
- Update to version 3.12.1

* Thu Sep 06 2012 Vít Ondruch <vondruch@redhat.com> - 3.12-5
- Fix the location of Ruby documentation (rhbz#854418).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 02 2012 Vít Ondruch <vondruch@redhat.com> - 3.12-3
- Add missing obsolete (rhbz#809007).

* Mon Feb 13 2012 Vít Ondruch <vondruch@redhat.com> - 3.12-2
- Add missing IRB dependency.

* Tue Feb 07 2012 Vít Ondruch <vondruch@redhat.com> - 3.12-1
- Rebuilt for Ruby 1.9.3.
- Updated to RDoc 3.12.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Mo Morsi <mmorsi@redhat.com> - 3.8-2
- Fixes for fedora compliance

* Mon Jan 10 2011 mo morsi <mmorsi@redhat.com> - 3.8-1
- Initial package
