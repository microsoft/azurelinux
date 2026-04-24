# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name shoulda-context

Name: rubygem-%{gem_name}
Version: 2.0.0
Release: 6%{?dist}
Summary: Context framework extracted from Shoulda
License: MIT
URL: https://github.com/thoughtbot/shoulda-context
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Use `File.exist?` instead of removed `File.exists` for Ruby 3.2
# compatibility.
# https://github.com/thoughtbot/shoulda-context/pull/70
Patch0: rubygem-shoulda-context-2.0.0-Use-File-exist.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
Shoulda Context makes it easy to write understandable and maintainable tests
under Minitest and Test::Unit within Rails projects or plain Ruby projects.
It's fully compatible with your existing tests and requires no retooling to
use.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

# Remove /usr/bin/env from shebang so RPM doesn't consider this a dependency
sed -i 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|' exe/convert_to_should_syntax

%gemspec_remove_file -t "test/fake_rails_root/vendor/plugins/.keep"
%gemspec_remove_file "test/fake_rails_root/vendor/plugins/.keep"

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


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/exe -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# No need to depend on git.
sed -i '/git/ s/^/#/' shoulda-context.gemspec

# Create simple test file which satisfies the test suite.
cat << EOF > gemfiles/test.gemfile
source "https://rubygems.org"

gem "minitest"
gem "mocha"
gem "test-unit"

gemspec path: "../"
EOF
BUNDLE_GEMFILE=gemfiles/test.gemfile bundle install --local

# Don't depend on Appraisal gem.
sed -i '/require "appraisal"/ s/^/#/' test/support/current_bundle.rb
sed -i '/assert_appraisal!/ s/^/#/' test/test_helper.rb

# We don't really need pry-byebug.
sed -i '/require "pry-byebug"/ s/^/#/' test/test_helper.rb

# We don't have warnings_logger gem available.
sed -i '/require "warnings_logger"/ s/^/#/' test/test_helper.rb
sed -i '/WarningsLogger/,/^)/ s/^/#/' test/test_helper.rb

# We don't have available snow globe gem, which is required for Rails related
# test cases.
sed -i '/require_relative "support\/rails_application_with_shoulda_context"/ s/^/#/' test/test_helper.rb
mv test/shoulda/railtie_test.rb{,.disable}
mv test/shoulda/rerun_snippet_test.rb{,.disable}

TEST_FRAMEWORK=minitest BUNDLE_GEMFILE=gemfiles/test.gemfile ruby -Ilib:test -rsingleton -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
TEST_FRAMEWORK=test_unit BUNDLE_GEMFILE=gemfiles/test.gemfile ruby -Ilib:test -rsingleton -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/convert_to_should_syntax
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/exe
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Appraisals
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Gemfile.lock
%doc %{gem_instdir}/README.md
%{gem_instdir}/bin
%{gem_instdir}/gemfiles
%{gem_instdir}/Rakefile
%{gem_instdir}/shoulda-context.gemspec
%{gem_instdir}/tasks
%{gem_instdir}/test

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 04 2023 Vít Ondruch <vondruch@redhat.com> - 2.0.0-1
- Update to shoulda-context 2.0.0.
  Resolves: rhbz#1846899

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 01 2023 Vít Ondruch <vondruch@redhat.com> - 1.2.2-15
- Drop jQuery dependency, which is not needed by RoR 5.1+.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Vít Ondruch <vondruch@redhat.com> - 1.2.2-13
- Fix Ruby 3.2 compatibility.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 20 2017 Vít Ondruch <vondruch@redhat.com> - 1.2.2-1
- Update to shoulda-context 1.2.2.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 26 2015 Vít Ondruch <vondruch@redhat.com> - 1.2.1-2
- Fix test suite compatibility with latest Mocha and RoR.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jul 02 2014 Vít Ondruch <vondruch@redhat.com> - 1.2.1-1
- Update to shoulda-context 1.2.1.

* Tue Nov 05 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.6-2
- Update to shoulda-context 1.1.6
- Clean up comments
- Remove unnecessary BR: on ruby
- Exclude developer-only files from binary packages

* Tue Aug 27 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.5-1
- Initial package
