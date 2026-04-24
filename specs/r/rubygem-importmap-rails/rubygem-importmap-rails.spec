# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from importmap-rails-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name importmap-rails

Name: rubygem-%{gem_name}
Version: 1.0.3
Release: 11%{?dist}
Summary: Manage modern JavaScript in Rails without transpiling or bundling
License: MIT
URL: https://github.com/rails/importmap-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# To get the test suite:
# git clone https://github.com/rails/importmap-rails.git --no-checkout
# git -C importmap-rails archive -v -o importmap-rails-1.0.3-tests.txz v1.0.3 test/
Source1: %{gem_name}-%{version}%{?prerelease}-tests.txz

BuildRequires: ruby
BuildRequires: ruby(release)
# Used for sample app
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(mutex_m)
BuildRequires: rubygem(rails)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygems-devel
BuildArch: noarch
# Bundles ES Module Shims
# app/assets/javascripts/es-module-shims.js
Provides: bundled(es-module-shims) = 1.4.1

%description
Use ESM with importmap to manage modern JavaScript in Rails without
transpiling or bundling.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/test

echo 'gem "mutex_m"' >> Gemfile
echo 'gem "rails"' >> Gemfile
echo 'gem "sqlite3"' >> Gemfile

# Test requires network access
mv test/packager_integration_test.rb{,.disable}

export BUNDLE_GEMFILE="$(pwd)/Gemfile"

# Tests require building rails app (currently fails)
echo > test/dummy/config/initializers/assets.rb
mv test/importmap_test.rb{,.disable}

ruby -Ilib:test -rbundler -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/app
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 10 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.3-8
- Add BR: rubygem(mutex_m) explicitly for ruby34

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 13 2022 Pavel Valena <pvalena@redhat.com> - 1.0.3-1
- Initial package
