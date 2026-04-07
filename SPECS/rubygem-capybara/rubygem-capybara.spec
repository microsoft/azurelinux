# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name capybara

Name: rubygem-%{gem_name}
Version: 3.40.0
Release: 3%{?dist}
Summary: Capybara aims to simplify the process of integration testing Rack applications
License: MIT
URL: https://github.com/teamcapybara/capybara
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/teamcapybara/capybara.git --no-checkout && cd capybara
# git archive -v -o capybara-3.40.0-tests.tar.gz 3.40.0 features/
Source1: %{gem_name}-%{version}-tests.tar.gz
# Fix compatibility with Rack::Protection 4.1.0+
# https://github.com/teamcapybara/capybara/pull/2812
Patch0: rubygem-capybara-3.40.0-Disable-Rack-Protection-HostAuthorization-.patch

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(addressable)
BuildRequires: rubygem(selenium-webdriver)
BuildRequires: rubygem(sinatra)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(launchy)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(puma)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(xpath)
BuildRequires: rubygem(rack-test)
BuildRequires: rubygem(mini_mime)
BuildRequires: rubygem(cucumber)
BuildRequires: rubygem(regexp_parser)
BuildRequires: rubygem(matrix)
BuildArch: noarch

%description
Capybara is an integration testing tool for rack based web applications. It
simulates how a user would interact with a website.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%patch 0 -p1

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

%check
( cd .%{gem_instdir}
# Move the tests into place
ln -s %{_builddir}/features features

# Do not collect statistics
sed -i '/^require..selenium_statistics.$/ s/^/#/' spec/spec_helper.rb
sed -i '/SeleniumStatistics/ s/^/#/g' ./spec/spec_helper.rb

rspec spec

# Bundler is not really needed
sed -i "/^require 'bundler/ s/^/#/g" \
  features/support/env.rb

cucumber
)

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/License.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 19 2025 Vít Ondruch <vondruch@redhat.com> - 3.40.0-2
- Fix compatibility with Rack::Protection 4.1.0+

* Wed Mar 19 2025 Vít Ondruch <vondruch@redhat.com> - 3.40.0-1
- Update to Capybara 3.40.0.
  Resolves: rhbz#2260593

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.39.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.39.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.39.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.39.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 21 2023 Pavel Valena <pvalena@redhat.com> - 3.39.2-1
- Update to capybara 3.39.2.
  Resolves: rhbz#2140002

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 25 2022 Vít Ondruch <vondruch@redhat.com> - 3.37.1-1
- Update to Capybara 3.37.1.
  Resolves: rhbz#2082862
  Resolves: rhbz#2113690

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Feb 07 2022 Pavel Valena <pvalena@redhat.com> - 3.36.0-1
- Update to capybara 3.36.0.
  Resolves: rhbz#1920296

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.34.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.34.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 22 10:29:58 CET 2020 Vít Ondruch <vondruch@redhat.com> - 3.34.0-2
- Relax rubygem-regexp_parser dependency.

* Fri Nov 27 05:22:25 CET 2020 Pavel Valena <pvalena@redhat.com> - 3.34.0-1
- Update to capybara 3.34.0.
  Resolves: rhbz#1902089

* Tue Aug 11 03:02:23 GMT 2020 Pavel Valena <pvalena@redhat.com> - 3.33.0-1
- Update to capybara 3.33.0.
  Resolves: rhbz#1668957

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Vít Ondruch <vondruch@redhat.com> - 3.8.1-1
- Update to Capybara 3.8.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 29 2018 Pavel Valena <pvalena@redhat.com> - 3.1.1-1
- Update to capybara 3.1.1.

* Mon May 14 2018 Pavel Valena <pvalena@redhat.com> - 3.1.0-1
- Update to Capybara 3.1.0.

* Fri Mar 02 2018 Vít Ondruch <vondruch@redhat.com> - 2.14.3-4
- Fix compatibility with recent rack-test.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Vít Ondruch <vondruch@redhat.com> - 2.14.3-1
- Remove deprecated Group tags.

* Mon Jun 19 2017 Pavel Valena <pvalena@redhat.com> - 2.14.3-1
- Update to Capybara 2.14.3
- Refresh spec file: remove unnecessary Provides, Requires, use current macros

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 22 2014 Josef Stribny <jstribny@redhat.com> - 2.4.1-1
- Update to capybara 2.4.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Mo Morsi <mmorsi@redhat.com> - 1.1.2-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Mo Morsi <mmorsi@redhat.com> - 1.1.2-1
- update to latest upstream release
- updated to ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 04 2011 Chris Lalancette <clalance@redhat.com> - 1.0.0-2
- Fix the license field to meet the actual license

* Wed Aug 03 2011 Chris Lalancette <clalance@redhat.com> - 1.0.0-1
- Initial package
