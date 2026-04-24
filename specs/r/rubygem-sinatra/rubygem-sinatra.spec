# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name sinatra

%bcond_with bootstrap
%bcond_without tilt_integration_tests

Name: rubygem-%{gem_name}
Version: 4.1.1
Release: 3%{?dist}
Summary: Ruby-based web application framework
License: MIT
URL: http://sinatrarb.com/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/sinatra/sinatra.git && cd sinatra
# git archive -v -o sinatra-4.1.1-test.tar.gz v4.1.1 test/
Source1: %{gem_name}-%{version}-test.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
%if %{without bootstrap}
BuildRequires: rubygem(minitest) > 5
BuildRequires: rubygem(mustermann)
BuildRequires: rubygem(rack)
BuildRequires: rubygem(rack-test)
BuildRequires: rubygem(rack-protection) >= %{version}
BuildRequires: rubygem(rack-session)
BuildRequires: rubygem(rackup)
# Tilt is actually required from base_test
BuildRequires: rubygem(tilt)
%if %{with tilt_integration_tests}
BuildRequires: rubygem(asciidoctor)
BuildRequires: rubygem(builder)
BuildRequires: rubygem(erubi)
BuildRequires: rubygem(haml)
BuildRequires: rubygem(kramdown)
BuildRequires: rubygem(liquid)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(rdiscount)
BuildRequires: rubygem(redcarpet)
BuildRequires: rubygem(slim)
%endif
%endif
Epoch: 1
BuildArch: noarch

%description
Sinatra is a DSL for quickly creating web applications in Ruby with minimal
effort.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

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


# Fix shebangs, though those are examples.
sed -i -e 's|^#!/usr/bin/env ruby|#!/usr/bin/ruby|' \
  %{buildroot}%{gem_instdir}/examples/*.rb
chmod a+x %{buildroot}%{gem_instdir}/examples/*.rb

%if %{without bootstrap}
%check
pushd .%{gem_instdir}
cp -a %{builddir}/test test

# Avoid ActiveSupport dependency, which should not be needed anyway.
sed -i '/active_support/ s/^/#/' test/test_helper.rb

# We can't do integration test
# because we don't ship sinatra-contrib including Sinatra::Runner.
mv test/integration_test.rb{,.disabled}
mv test/integration_async_test.rb{,.disabled}
# These would require additional dependencies, such as Zeitwerk, Puma, etc.
mv test/integration_start_test.rb{,.disabled}

# TODO: Is it worth of testing all the possible template engines integration?
ruby -e 'Dir.glob "./test/*_test.rb", &method(:require)'
popd
%endif

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.yardopts
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/AUTHORS.md
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/MAINTENANCE.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/SECURITY.md
%{gem_instdir}/VERSION
%{gem_instdir}/examples
%{gem_instdir}/sinatra.gemspec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 12 2025 Vít Ondruch <vondruch@redhat.com> - 1:4.1.1-1
- Update to Sinatra 4.1.1.
  Resolves: rhbz#2185968
- Open Redirect Vulnerability in Sinatra via X-Forwarded-Host Header (CVE-2024-21510)
  Resolves: rhbz#2323117

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 18 2024 Vít Ondruch <vondruch@redhat.com> - 3.2.0-1
- Update to Sinatra 3.2.0.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 19 2023 Vít Ondruch <vondruch@redhat.com> - 1:3.0.5-1
- Update to Sinatra 3.0.5.
  Resolves: rhbz#2107692

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Apr 20 2022 Vít Ondruch <vondruch@redhat.com> - 1:2.2.0-2
- Patch the error_highlight test issues.
- Add upstream reference to another test failure.

* Tue Apr 19 2022 Vít Ondruch <vondruch@redhat.com> - 1:2.2.0-1
- Update to Sinatra 2.2.0.
  Resolves: rhbz#2054771

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 Pavel Valena <pvalena@redhat.com> - 1:2.1.0-1
- Update to sinatra 2.1.0.
  Resolves: rhbz#1875978
  Resolves: rhbz#1970606

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 29 2020 Vít Ondruch <vondruch@redhat.com> - 1:2.0.8.1-1
- Update to Sinatra 2.0.8.1.
  Resolves: rhbz#1744278

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 11 2018 Jun Aruga <jaruga@redhat.com> - 1:2.0.3-1
- Update to 2.0.3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 16 2017 Jun Aruga <jaruga@redhat.com> - 1:2.0.0-1
- Update to 2.0.0

* Fri Apr 28 2017 František Dvořák <valtri@civ.zcu.cz> - 1:1.4.8-2
- Update versions of dependencies

* Thu Apr 27 2017 František Dvořák <valtri@civ.zcu.cz> - 1:1.4.8-1
- Update to 1.4.8 (#1417614)
- Ruby 2.4 Fixnum patch merged
- EPEL 7 support

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Vít Ondruch <vondruch@redhat.com> - 1:1.4.7-2
- Fix Ruby 2.4 compatibility.

* Mon Aug 01 2016 Jun Aruga <jaruga@redhat.com> - 1:1.4.7-1
- Update to 1.4.7
- Fix broken dependency for rack 2.x.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Josef Stribny <jstribny@redhat.com> - 1:1.4.6-1
- Update to 1.4.6

* Fri Jul 18 2014 Vít Ondruch <vondruch@redhat.com> - 1:1.4.5-1
- Update to Sinatra 1.4.5.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Michal Fojtik <mfojtik@redhat.com> - 1:1.4.3-1
- Update to 1.4.3

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.3.5-1
- Update to version 1.3.5.
- Run tests again.

* Thu Feb 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.3.4-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb 25 2013 Michal Fojtik <mfojtik@redhat.com> - 1;1.3.4-3
- Rebuild using new rack-protection

* Thu Feb 21 2013 Michal Fojtik <mfojtik@redhat.com> - 1;1.3.4-2
- Fixed rack-protection version

* Thu Feb 21 2013 Michal Fojtik <mfojtik@redhat.com> - 1;1.3.4-1
- Release 1.3.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.3.2-8
- Set %%bootstrap to 0 to allow tests.

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.3.2-7
- Rebuilt for Ruby 1.9.3.
- Introduced %%bootstrap macro to deal with dependency loop.

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-6
- Fixed Epoch once again

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-5
- Added Epoch to -dc subpackage

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-4
- Rebuild for missing -dc subpackage

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-3
- Added missing build requires

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-2
- Added tests
- Added doc subpackage

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-2
- Version bump

* Thu Feb 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.6-1
- Version bump

* Thu Feb 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.0-1
- Version bump

* Thu Feb 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.1.2-3
- Added tilt dependency

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.1.2-1
- Version bump

* Thu Mar 25 2010 Michal Fojtik <mfojtik@redhat.com> - 1.0-1
- Sinatra now uses Tilt for rendering templates
- New helper methods
- New argument to specify the address to bind to
- Speed improvement in rendering templates

* Mon Feb 15 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.4-2
- Downgrade-Release

* Thu Jan 07 2010 Michal Fojtik <mfojtik@redhat.com> - 0.10.1-1
- Version-Release
- Added jp README

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.2-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.2-2
- Fix up documentation list
- Bring tests back
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.2-1
- Package generated by gem2rpm
- Don't ship tests
- Fix up License
