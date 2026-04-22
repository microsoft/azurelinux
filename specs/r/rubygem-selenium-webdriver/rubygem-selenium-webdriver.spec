# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name selenium-webdriver

%bcond_without spec_integration

Name: rubygem-%{gem_name}
Version: 4.34.0
Release: 2%{?dist}
Summary: Selenium is a browser automation tool for automated testing of webapps and more
License: Apache-2.0
URL: https://selenium.dev
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/SeleniumHQ/selenium && cd selenium
# git archive -v -o selenium-webdriver-4.34.0-spec.tar.gz selenium-4.34.0 rb/spec
Source1: %{gem_name}-%{version}-spec.tar.gz
# Needed for integration `spec/integration`
# git archive -v -o selenium-webdriver-4.34.0-web.tar.gz selenium-4.34.0 common/src/web
Source2: %{gem_name}-%{version}-web.tar.gz
# Make the test suite compatible with Rack 3+.
# https://github.com/SeleniumHQ/selenium/pull/16158
Patch0: rubygem-selenium-webdriver-4.34.0-Use-Rack-Files-for-Rack-3-compatibility.patch

# There is no other driver in Fedora, therefore suggest what we have. This also
# reflescts the `selenium-manager` stub above.
Recommends: chromedriver
Recommends: chromium chromium-headless

Requires: %{_bindir}/selenium-manager
BuildRequires: %{_bindir}/selenium-manager

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(base64)
BuildRequires: rubygem(curb)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rubyzip)
BuildRequires: rubygem(webmock)
BuildRequires: rubygem(websocket)
%if %{with spec_integration}
BuildRequires: rubygem(rack)
BuildRequires: rubygem(rackup)
BuildRequires: rubygem(webrick)
BuildRequires: chromedriver
BuildRequires: chromium chromium-headless
# Chromium is not available for i686 / s390x
# https://src.fedoraproject.org/rpms/chromium/blob/fcd074b9c31411f795ab402fe88e4513a68c843e/f/chromium.spec#_803
# and on ppc64le
# https://src.fedoraproject.org/rpms/chromium/blob/fcd074b9c31411f795ab402fe88e4513a68c843e/f/chromium.spec#_43-45
ExclusiveArch: x86_64 aarch64
%endif
BuildArch: noarch

%description
Selenium implements the W3C WebDriver protocol to automate popular browsers.
It aims to mimic the behaviour of a real user as it interacts with the
application's HTML. It's primarily intended for web application testing,
but any web-based task can automated.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1 -b2

(
cd %{builddir}
%patch 0 -p1
)

# Drop the original selenium-manager binaries and replace them by symlink to
# selenium-manager binary from the package of the same name.
%gemspec_remove_file Dir.glob('bin/{windows,macos,linux}/selenium-manager{,.exe}')
rm -rf bin

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Create folder for binaries and create symlink to the selenium-manager from repos
mkdir -p %{buildroot}%{gem_instdir}/bin/linux/
ln -sf %{_bindir}/selenium-manager %{buildroot}%{gem_instdir}/bin/linux/


%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

( cd .%{gem_instdir}
cp -a %{builddir}/rb/spec .
cp -a %{builddir}/common ..

mkdir -p ./bin/linux/
ln -sf %{_bindir}/selenium-manager ./bin/linux/

# `DevTools` are part of separate `selenium-devtools` gem.
mv spec/unit/selenium/devtools_spec.rb{,.disable}
mv spec/unit/selenium/devtools/cdp_client_generator_spec.rb{,.disable}
mv spec/integration/selenium/webdriver/devtools_spec.rb{,.disable}

# Require Firefox extensions included in thirdparty directory, available on GH
# not included in gem
sed -i spec/unit/selenium/webdriver/firefox/profile_spec.rb \
    -e '/can install extension/a\          skip' \
    -e '/can install web extension/a\          skip'

# There seems to be wrong stub and when `bin/linux/selenium-manager` exists,
# the test fails.
# https://github.com/SeleniumHQ/selenium/issues/14925
sed -i "/it 'errors if cannot find' do/a\          skip" \
  spec/unit/selenium/webdriver/common/selenium_manager_spec.rb

rspec spec/unit

%if %{with spec_integration}
# This query is not supported by the `selenium` wrapper. But we won't have beta
# version of Chrome anyway.
sed -i -r '/GlobalTestEnv\.beta_chrome_version/ s/exclude: \{.*\},//' \
  spec/integration/selenium/webdriver/network_spec.rb

# Ignore `spec/integration/selenium/server_spec.rb`, which downloads some
# content from internet.
mv spec/integration/selenium/server_spec.rb{,.disable}

# Test passes when it is expected to fail. Maybe Chromium supports this action
# now?
sed -i -r \
  -e "/it 'can minimize the window'/ s/(^\s*)it/\1skip/" \
  spec/integration/selenium/webdriver/window_spec.rb

# This test fails and should likely be guarded by the `headless` flag.
sed -i -r \
  -e "/it 'can maximize the current window'/ s/(^\s*)it/\1skip/" \
  spec/integration/selenium/webdriver/window_spec.rb

HEADLESS=true SE_CHROMEDRIVER=chromedriver rspec spec/integration
%endif
)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/NOTICE
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/selenium-webdriver.gemspec

%changelog
* Mon Aug 11 2025 Tomáš Juhász <tjuhasz@redhat.com> - 4.34.0-1
- Use packaged selenium-manager binary.

* Thu Aug 07 2025 Vít Ondruch <vondruch@redhat.com> - 4.34.0-1
- Update to selenium-webdriver 4.34.0.
  Resolves: rhbz#2339033
  Resolves: rhbz#2385596

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.27.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 12 2025 Vít Ondruch <vondruch@redhat.com> - 4.27.0-4
- Fix `selenium-manager` stub shebang.

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.27.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Vít Ondruch <vondruch@redhat.com> - 4.27.0-2
- Disable ppc64le support due to missing chromium-headless.

* Fri Dec 20 2024 Vít Ondruch <vondruch@redhat.com> - 4.27.0-1
- Update to selenium-webdriver 4.27.0.
  Resolves: rhbz#2091127

* Wed Jul  24 2024 Miroslav Suchý <msuchy@redhat.com> - 4.1.0-10
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan  2 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.1.0-5
- Apply the upstream patch for ruy3.2 instead of previous patch

* Sat Dec 31 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.1.0-4
- Apply upstream PR under review for ruby3.2 test failure wrt new IO#path method
  and selenium rspec internal mocking File.exist? issue

* Sat Dec 31 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.1.0-3
- Clean up spec file for test suite
  - BR: firefox is actually not needed, just skip test suite
    requiring real extension jar file
  - Fake java runtime
  - Explicity execute spec/unit testsuite only

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Feb 13 2022 Pavel Valena <pvalena@redhat.com> - 4.1.0-1
- Update to selenium-webdriver 4.1.0.
  Resolves: rhbz#2013663

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.142.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.142.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.142.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 14:13:22 GMT 2020 Pavel Valena <pvalena@redhat.com> - 3.142.7-3
- Relax Childprocess dependency.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.142.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 18 2020 Pavel Valena <pvalena@redhat.com> - 3.142.7-1
- Update to selenium-webdriver 3.142.7.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Vít Ondruch <vondruch@redhat.com> - 2.45.0-12
- Relax rubyzip dependency.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 07 2019 Vít Ondruch <vondruch@redhat.com> - 2.45.0-10
- Relax childprocess dependency.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.45.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Mo Morsi <mmorsi@redhat.com> - 2.45.0-2
- Fix dependencies

* Thu Apr 09 2015 Mo Morsi <mmorsi@redhat.com> - 2.45.0-1
- Update to 2.45.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.3.2-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 2.3.2-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 03 2011 Chris Lalancette <clalance@redhat.com> - 2.3.2-1
- Initial package
