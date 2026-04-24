# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name bundler

# Enable test when building on local.
%bcond_with tests

%global connection_pool_version 2.5.0
%global fileutils_version 1.7.3
%global net_http_persistent_version 4.0.4
%global pub_grub_version 0.5.0
%global securerandom_version 0.4.1
%global thor_version 1.3.2
%global tsort_version 0.2.0
%global uri_version 1.0.3

Name: rubygem-%{gem_name}
Version: 2.6.9
Release: 4%{?dist}
Summary: Library and utilities to manage a Ruby application's gem dependencies
# BSD-2-Clause OR Ruby:
#   lib/bundler/vendor/fileutils
#   lib/bundler/vendor/tsort
#   lib/bundler/vendor/uri
# MIT:
#   lib/bundler/vendor/connection_pool
#   lib/bundler/vendor/net-http-persistent
#   lib/bundler/vendor/pub_brub
#   lib/bundler/vendor/thor
#   lib/rubygems/resolver/molinillo
License: MIT AND (Ruby OR BSD-2-Clause)
URL: https://bundler.io
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rubygems/rubygems/ && cd rubygems
# git archive -v -o bundler-2.6.9-specs.tar.gz bundler-v2.6.9 bundler/spec/ tool/bundler/{rubocop,standard,test}_gems.rb
Source1: %{gem_name}-%{version}-specs.tar.gz
# This revert changes which seems to require some setup prior running specs.
# https://github.com/rubygems/rubygems/issues/8698
Patch0: rubygem-bundler-2.6.9-Revert-changes-in-spec-sectup.patch
# ruby package has just soft dependency on rubygem(io-console), while
# Bundler always requires it.
Requires: rubygem(io-console)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
%if %{with tests}
BuildRequires: ruby-devel
BuildRequires: libyaml-devel
BuildRequires: rubygem(rake)
BuildRequires: rubygem(rspec) >= 3.0
BuildRequires: %{_bindir}/git
BuildRequires: %{_bindir}/man
BuildRequires: %{_bindir}/ps
BuildRequires: gcc
%endif
# https://github.com/bundler/bundler/issues/3647
Provides: bundled(rubygem-connection_pool) = %{connection_pool_version}
Provides: bundled(rubygem-fileutils) = %{fileutils_version}
Provides: bundled(rubygem-net-http-persistent) = %{net_http_persistent_version}
Provides: bundled(rubygem-pub_grub) = %{pub_grub_version}
Provides: bundled(rubygem-securerandom) = %{securerandom_version}
Provides: bundled(rubygem-thor) = %{thor_version}
Provides: bundled(rubygem-tsort) = %{tsort_version}
Provides: bundled(rubygem-uri) = %{uri_version}
BuildArch: noarch

%description
Bundler manages an application's dependencies through its entire life, across
many machines, systematically and repeatably.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

( cd %{builddir}
%patch 0 -p1
)

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

# Man pages are used by Bundler internally, do not remove them!
for n in 5 1; do
  mkdir -p %{buildroot}%{_mandir}/man${n}
  for file in %{buildroot}%{gem_libdir}/bundler/man/*.${n}; do
    base_name=$(basename "${file}")
    cp -a "${file}" "%{buildroot}%{_mandir}/man${n}/${base_name}"
  done
done

%check
( cd .%{gem_instdir}
# Check bundled libraries.
[ `ls lib/bundler/vendor | wc -l` == 8 ]

# connection_pool.
[ "`ruby -e " \
  module Bundler; end; \
  require './lib/bundler/vendor/connection_pool/lib/connection_pool/version'; \
  puts Bundler::ConnectionPool::VERSION"`" \
  == '%{connection_pool_version}' ]

# FileUtils.
[ "`ruby -e " \
  module Bundler; end; \
  require './lib/bundler/vendor/fileutils/lib/fileutils'; \
  puts Bundler::FileUtils::VERSION"`" \
  == '%{fileutils_version}' ]

# PubGrub
[ `ruby -Ilib -e '
  module Bundler; end;
  require "bundler/vendor/pub_grub/lib/pub_grub/version";
  puts Bundler::PubGrub::VERSION'` == '%{pub_grub_version}' ]

# Net::HTTP::Persistent.
[ `ruby -Ilib -e '
  module Bundler; module Persistent; module Net; module HTTP; end; end; end; end
  require "bundler/vendor/net-http-persistent/lib/net/http/persistent"
  puts Gem::Net::HTTP::Persistent::VERSION'` == '%{net_http_persistent_version}' ]

# SecureRandom.
[ `ruby -Ilib -e '
  module Bundler; module Random; end; end;
  require "bundler/vendor/securerandom/lib/securerandom";
  puts Bundler::SecureRandom::VERSION'` == '%{securerandom_version}' ]

# Thor.
[ `ruby -e '
  module Bundler; end;
  require "./lib/bundler/vendor/thor/lib/thor/version"
  puts Bundler::Thor::VERSION'` == '%{thor_version}' ]

# TSort
[ `ruby -Ilib -e '
  module Bundler; end;
  require "bundler/vendor/tsort/lib/tsort";
  puts Bundler::TSort::VERSION'` == '%{tsort_version}' ]

# URI.
[ "`ruby -e "
  module Bundler; end; \
  require './lib/bundler/vendor/uri/lib/uri/version'; \
  puts Bundler::URI::VERSION"`" \
  == '%{uri_version}' ]

# Test suite has to be disabled for official build, since it downloads various
# gems, which are not in Fedora or they have different version etc.
# Nevertheless, the test suite should run for local builds.
%if %{with tests}

cp -a %{builddir}/bundler/spec .
cp -a %{builddir}/tool ..

# This dependency is relevant just to RubyGems. Removing it we can omit
# `BR: libffi-devel`
sed -i '/"fiddle"/ s/^/#/' ../tool/bundler/test_gems.rb

# This test fails due to rubypick.
sed -i '/^    context "when disable_exec_load is set" do$/,/^    end$/ {
  /it "runs" do/a\        skip
}' spec/commands/exec_spec.rb

# Avoid unexpected influence of Fedora specific configuration. This forces
# Ruby to load this empty operating_system.rb instead of operatin_system.rb
# shipped as part of RubyGems.
mkdir -p %{_builddir}/rubygems/rubygems/defaults/
touch %{_builddir}/rubygems/rubygems/defaults/operating_system.rb

# The sources are not stored in Git repository nor they come from Ruby source
# tarball. However, the test suite makes some assumptions based on that. Lets
# try to tweak them.
# 1. Standard Bundler layout is used:
sed -i '/def ruby_core_tarball\?/,/^    end$/ {
  /^    end$/i\      # Hardcode standar Bundler layout\n      return false
}' spec/support/path.rb
# 2. But without Git repo, we can't get hash:
sed -i '/def git_commit_sha\?/a\      return "unknown"' spec/support/build_metadata.rb
# 3. These are checking the Git repository content and would be disabled for Ruby
# tarball, but we change that condition above for different reasons 🙈
mv spec/quality_spec.rb{,.disable}
# 4. This check manpages conent and does not really influence runtime stability.
mv spec/quality_es_spec.rb{,.disable}
# 5. Convince the test suite, that the Ruby repo layout is used. This seems to be
# more suitable then assuming that the Bundler repo is used. `GEM_COMMAND` env
# variable unfortunately brings in another set of assumptions.
sed -i '/\sruby_repo:\s/ s/ruby_repo: .*/ruby_repo: true/' spec/support/filters.rb
# 6. Use the `ruby_core?` test version, so it matches the expectaion without
# making another assumpitons about directory layout.
sed -i '/if Spec::Path.ruby_core?/ s/$/ || true/' spec/commands/version_spec.rb

# We work with released version => change the condition.
# https://github.com/rubygems/rubygems/issues/5926
sed -i '/release.*be_falsey/I s/be_falsey/be_truthy/' spec/bundler/build_metadata_spec.rb

# This test is very specific to directory layouts and it its usefulness
# is mostly for upstream to point out some changes which needs to be included.
sed -i '/it "stays in sync with the rubygems implementation" do/a\    skip' spec/bundler/ci_detector_spec.rb

# Fix the compilation issues likely caused by:
# https://fedoraproject.org/wiki/Changes/PortingToModernC#Use_of_incompatible_pointer_types_without_a_cast
# https://github.com/rubygems/rubygems/issues/8694
sed -i 's/VALUE foo()/VALUE foo(VALUE _)/' spec/install/gemfile/git_spec.rb

# Please note that spec/install/security_policy_spec.rb fails with DEFAULT
# crypto policy. Use `update-crypto-policies --set LEGACY` to make it pass.
# https://github.com/rubygems/rubygems/issues/8693

# The `BUNDLER_GEM_DEFAULT_DIR` is useful to make pass e.g.:
# rspec ./spec/commands/exec_spec.rb:203 # bundle exec with default gems when not specified in Gemfile uses version provided by ruby
#
# It is necessary to require spec_helper.rb explicitly.
# https://github.com/bundler/bundler/pull/5634
RUBYOPT=-I%{_builddir}/rubygems GEM_PATH=%{gem_dir} BUNDLER_GEM_DEFAULT_DIR=%{gem_dir} rspec -rspec_helper spec -f d

%endif

)

%files
%dir %{gem_instdir}
%{_bindir}/bundle
%{_bindir}/bundler
%license %{gem_instdir}/LICENSE.md
%exclude %{gem_instdir}/bundler.gemspec
%{gem_instdir}/exe
%{gem_libdir}
%doc %{gem_libdir}/bundler/man/*
%exclude %{gem_cache}
%{gem_spec}
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Vít Ondruch <vondruch@redhat.com> - 2.6.9-2
- Use proper SPDX identifiers.

* Fri Apr 11 2025 Vít Ondruch <vondruch@redhat.com> - 2.6.9-1
- Update to Bundler 2.6.9.
  Resolves: rhbz#2143547

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 03 2022 Jun Aruga <jaruga@redhat.com> - 2.3.25-1
- Update to Bundler 2.3.25.
  Resolves: rhbz#2132432

* Mon Sep 12 2022 Vít Ondruch <vondruch@redhat.com> - 2.3.22-1
- Update to Bundler 2.3.22.
  Resolves: rhbz#1579087

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Vít Ondruch <vondruch@redhat.com> - 1.16.1-2
- Remove unnecessary executable bit.

* Tue Jan 02 2018 Jun Aruga <jaruga@redhat.com> - 1.16.1-1
- Update to Bundler 1.16.1.

* Mon Nov 06 2017 Jun Aruga <jaruga@redhat.com> - 1.16.0-1
- Update to Bundler 1.16.0.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Vít Ondruch <vondruch@redhat.com> - 1.13.7-1
- Update to Bundler 1.13.7.

* Fri Dec 16 2016 Vít Ondruch <vondruch@redhat.com> - 1.13.6-1
- Update to Bundler 1.13.6.

* Wed Jul 27 2016 Vít Ondruch <vondruch@redhat.com> - 1.12.5-1
- Update to Bundler 1.12.5.

* Fri Apr 08 2016 Vít Ondruch <vondruch@redhat.com> - 1.10.6-3
- Explicitly set rubygem(io-console) dependency.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 12 2015 Vít Ondruch <vondruch@redhat.com> - 1.10.6-1
- Update to Bundler 1.10.6.
- Keep vendored libraries.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 05 2015 Vít Ondruch <vondruch@redhat.com> - 1.7.8-2
- Properly uninstall the vendor directory.

* Tue Dec 09 2014 Vít Ondruch <vondruch@redhat.com> - 1.7.8-1
- Update to Bundler 1.7.8.

* Thu Nov 20 2014 Josef Stribny <jstribny@redhat.com> - 1.7.6-2
- Keep ssl_certs/certificate_manager.rb file (used in tests)
- Correctly add load paths for gems during tests

* Wed Nov 12 2014 Josef Stribny <jstribny@redhat.com> - 1.7.6-1
- Update to 1.7.6

* Tue Nov 11 2014 Josef Stribny <jstribny@redhat.com> - 1.7.4-2
- Use symlinks for vendored libraries (rhbz#1163039)

* Mon Oct 27 2014 Vít Ondruch <vondruch@redhat.com> - 1.7.4-1
- Update to Bundler 1.7.4.
- Add thor and net-http-persistent dependencies into .gemspec.

* Mon Sep 22 2014 Josef Stribny <jstribny@redhat.com> - 1.7.3-1
- Update to 1.7.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 12 2014 Sam Kottler <skottler@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 (BZ #1047222)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.5-1
- Update to Bundler 1.3.5.

* Mon Mar 04 2013 Josef Stribny <jstribny@redhat.com> - 1.3.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to Bundler 1.3.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.1-1
- Update to Bundler 1.2.1.
- Fix permissions on some executable files.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.4-1
- Update to Bundler 1.1.4.

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.21-1
- Rebuilt for Ruby 1.9.3.
- Update to Bundler 1.0.21.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 07 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.15-1
- Updated to Bundler 1.0.15

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.10-1
- Upstream update

* Thu Jan 27 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.9-2
- More concise summary
- Do not remove manpages, they are used internally
- Added buildroot cleanup in clean section

* Mon Jan 24 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.9-1
- Bumped to Bundler 1.0.9
- Installed manual pages
- Removed obsolete buildroot cleanup

* Mon Nov 1 2010 Jozef Zigmund <jzigmund@redhat.com> - 1.0.3-2
- Add ruby(abi) dependency
- Add using macro %%{geminstdir} in files section
- Add subpackage doc for doc files
- Removed .gitignore file
- Removed rubygem-thor from vendor folder
- Add dependency rubygem(thor)

* Mon Oct 18 2010 Jozef Zigmund <jzigmund@redhat.com> - 1.0.3-1
- Initial package
