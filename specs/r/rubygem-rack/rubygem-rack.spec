# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name rack

Name: rubygem-%{gem_name}
Version: 3.1.19
# Introduce Epoch (related to bug 552972)
Epoch:  1
Release: 1%{?dist}
Summary: A modular Ruby webserver interface
# lib/rack/show_{status,exceptions}.rb contains snippets from Django under BSD license.
License: MIT AND BSD-3-Clause
URL: https://github.com/rack/rack
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rack/rack.git && cd rack/
# git archive -v -o rack-3.1.19-tests.tar.gz v3.1.19 test/
Source1: rack-%{version}-tests.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.4.0
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Rack provides a minimal, modular and adaptable interface for developing
web applications in Ruby. By wrapping HTTP requests and responses in
the simplest way possible, it unifies and distills the API for web
servers, web frameworks, and software in between (the so-called
middleware) into a single method call.


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



%check
( cd .%{gem_instdir}

cp -a %{builddir}/test .

# Avoid minitest-global_expectations in exchange of lot of deprecation warnings.
# https://github.com/rack/rack/pull/1394
mkdir -p test/minitest/global_expectations
echo 'require "minitest/autorun"' > test/minitest/global_expectations/autorun.rb

ruby -Itest -e 'Dir.glob "./test/spec_*.rb", &method(:require)'
)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/SPEC.rdoc

%changelog
* Tue Nov 04 2025 Vít Ondruch <vondruch@redhat.com> - 1:3.1.19-1
- Update to Rack 3.1.19

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Vít Ondruch <vondruch@redhat.com> - 1:3.1.16-1
- Update to Rack 3.1.16
  Resolves: rhbz#2124662
- Denial of service in Content-Disposition parsing (CVE-2022-44571)
  Resolves: rhbz#2164714
  Resolves: rhbz#2164716
- Denial of service in Content-Disposition parsing (CVE-2022-44570)
  Resolves: rhbz#2164719
  Resolves: rhbz#2164721
- Denial of service in Content-Disposition parsing (CVE-2022-44572)
  Resolves: rhbz#2164722
  Resolves: rhbz#2164724
- Denial of service in Multipart MIME parsing (CVE-2023-27530)
  Resolves: rhbz#2176477
  Resolves: rhbz#2176478
- Denial of service in header parsing (CVE-2023-27539)
  Resolves: rhbz#2179649
  Resolves: rhbz#2179651
- Denial of Service Vulnerability in Rack Content-Type Parsing (CVE-2024-25126)
  Resolves: rhbz#2265593
- Possible DoS Vulnerability with Range Header in Rack (CVE-2024-26141)
  Resolves: rhbz#2265594
- Possible Denial of Service Vulnerability in Rack Header Parsing (CVE-2024-26146)
  Resolves: rhbz#2265595
- Possible Log Injection in Rack::CommonLogger (CVE-2025-25184)
  Resolves: rhbz#2345301
- Escape Sequence Injection vulnerability in Rack lead to Possible Log Injection (CVE-2025-27111)
  Resolves: rhbz#2349810
- File Inclusion in Rack::Static (CVE-2025-27610)
  Resolves: rhbz#2351231
- Unbounded-Parameter DoS in Rack::QueryParser (CVE-2025-46727)
  Resolves: rhbz#2364966
- Rack Session Reuse Vulnerability (CVE-2025-32441). Current version
  actually extracts the affected code into rack-session package.
  Resolves: rhbz#2364965

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 20 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:2.2.4-8
- Backport upstream patch for ruby34 hash formatting change
- Add dependency for rubygem(base64) explicitly

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1:2.2.4-7
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 18 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:2.2.4-4
- Backport upstream patch for Regexp.new 3rd argument deprecation
  (needed for ruby 3.3)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 09 2022 Vít Ondruch <vondruch@redhat.com> - 2.2.4-1
- Update to Rack 2.2.4
  Resolves: rhbz#2091121
  Resolves: rhbz#2113698

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 11 2022 Vít Ondruch <vondruch@redhat.com> - 1:2.2.3-8
- Backport Ruby 3.1 / Psych 4.0 support.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  8 2021 Pavel Valena <pvalena@redhat.com> - 1:2.2.3-4
- Fix FTBFS due to WEBrick removed from Ruby 3.0.

* Wed Oct 21 2020 Vít Ondruch <vondruch@redhat.com> - 1:2.2.3-3
- Re-enable test suite.
- Remove rubygem(thin) dependency for good.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 17 2020 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1:2.2.3-1
- Update to Rack 2.2.3

* Mon Feb 17 2020 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1:2.2.2-1
- Update to Rack 2.2.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1:2.1.1-1
- Update to Rack 2.1.1
- This version has no files for tests included 

* Thu Dec 19 2019 Pavel Valena <pvalena@redhat.com> - 1:2.0.8-1
- Update to Rack 2.0.8.
- Change the source URL

* Wed Jul 24 2019 Pavel Valena <pvalena@redhat.com> - 1:2.0.7-1
- Update to Rack 2.0.7.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.0.6-3
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Mon Nov 12 2018 Vít Ondruch <vondruch@redhat.com> - 2.0.6-1
- Update to Rack 2.0.6.

* Mon Sep 24 2018 pvalena <pvalena@redhat.com> - 1:2.0.5-1
- Update to rack 2.0.5.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 15 2018 Vít Ondruch <vondruch@redhat.com> - 1:2.0.4-2
- Exclude test.ru shebang from being mangled.

* Tue Feb 13 2018 Jun Aruga <jaruga@redhat.com> - 1:2.0.4-1
- Update to Rack 2.0.4.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 09 2017 Jun Aruga <jaruga@redhat.com> - 1:2.0.3-2
- Improve bootstrapping logic.
  Ref: https://fedoraproject.org/wiki/Packaging:Guidelines#Bootstrapping
- Fix wrong script interpreter for rpmlint.

* Thu Jun 01 2017 Steve Traylen <steve.traylen@cern.ch> - 1:2.0.3-1
- Update to Rack 2.0.3.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Vít Ondruch <vondruch@redhat.com> - 1:2.0.1-2
- Fix test error caused by rubygem-concurrent-ruby.

* Fri Jul 01 2016 Vít Ondruch <vondruch@redhat.com> - 1:2.0.1-1
- Update to Rack 2.0.1.

* Mon May 02 2016 Jun Aruga <jaruga@redhat.com> - 1:1.6.4-1
- Update to 1.6.4.
- Fix test suite for FTBFS (rhbz#1308069).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Vít Ondruch <vondruch@redhat.com> - 1:1.6.2-1
- Update to Rack 1.6.2.

* Tue Jun 2 2015 Steve Traylen <jstribny@redhat.com> - 1:1.6.1-1
- Update to 1.6.1

* Mon Feb 09 2015 Josef Stribny <jstribny@redhat.com> - 1:1.6.0-1
- Update to 1.6.0

* Thu Sep 25 2014 Steve Traylen <steve.traylen@cern.ch> - 1:1.5.2-4
- Add enable_check flag and disable check for .el7.
- Rely on autorequires and autoprovides.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 05 2014  Josef Stribny <jstribny@redhat.com> - 1:1.5.2-2
- Fix licensing
- Add virtual provide for bundled okjson

* Wed Jul 24 2013 Josef Stribny <jstribny@redhat.com> - 1:1.5.2-1
- Update to rack 1.5.2

* Fri Mar 01 2013 Vít Ondruch <vondruch@redhat.com> - 1:1.4.5-3
- Enable thin test suite.

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 1:1.4.5-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Fri Feb 08 2013 Josef Stribny <jstribny@redhat.com> - 1:1.4.5-1
- Update to Rack 1.4.5.

* Tue Jan 15 2013 Vít Ondruch <vondruch@redhat.com> - 1:1.4.4-1
- Update to Rack 1.4.4.

* Thu Nov 01 2012 Vít Ondruch <vondruch@redhat.com> - 1:1.4.1-2
- Fixed epoch in -doc sub-package.

* Mon Oct 29 2012 Vít Ondruch <vondruch@redhat.com> - 1:1.4.1-1
- Update to Rack 1.4.1.
- Documentation moved into subpackage.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.4.0-2
- Rebuilt for Ruby 1.9.3.

* Thu Jan 05 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.4.0-1
- Update to Rack 1.4.
- Moved gem install to %%prep to be able to apply patches.
- Applied two patches that fix test failures with Ruby 1.8.7-p357.

* Tue Jun 28 2011 Vít Ondruch <vondruch@redhat.com> - 1:1.3.0-1
- Updated to Rack 1.3.
- Fixed FTBFS.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:1.1.0-2
- Epoch 1 for keeping upgrade path from F-12 (related to bug 552972)
- Enable %%check

* Mon Jan  4 2010 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.1.0-1
- New upstream version

* Sun Oct 25 2009 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.0.1-1
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 26 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.0.0-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.9.1-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 09 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-2
- Remove unused macro (#470694)
- Add ruby(abi) = 1.8 as required by package guidelines (#470694)
- Move %%{gem_dir}/bin/rackup to %%{_bindir} (#470694)

* Sat Nov 08 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-1
- Initial package
