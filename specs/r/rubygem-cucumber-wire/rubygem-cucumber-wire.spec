# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from cucumber-wire-0.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name cucumber-wire

%bcond_with bootstrap

Name: rubygem-%{gem_name}
Version: 6.2.1
Release: 5%{?dist}
Summary: Wire protocol for Cucumber
License: MIT
URL: http://cucumber.io
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone --no-checkout https://github.com/cucumber/cucumber-ruby-wire.git
# git -C cucumber-ruby-wire archive -v -o rubygem-cucumber-wire-6.2.1-features.txz v6.2.1 features/
Source1: %{name}-%{version}-features.txz
# Support quote in backtrace for Ruby 3.4
# https://github.com/cucumber/cucumber-ruby-wire/pull/72
Patch0: rubygem-cucumber-wire-7.0.0-Support-quote-in-backtrace-for-Ruby-3-4.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
%if %{without bootstrap}
# Dependencies for %%check
BuildRequires: rubygem(aruba)
BuildRequires: rubygem(cucumber)
BuildRequires: rubygem(rspec)
%endif
BuildArch: noarch

%description
Wire protocol for Cucumber.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

(
cd %{builddir}
%patch 0 -p1
)

# Relax the dependency.
%gemspec_remove_dep -g cucumber-cucumber-expressions "~> 14.0", ">= 14.0.0"
%gemspec_add_dep -g cucumber-cucumber-expressions ">= 14.0"

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%if %{without bootstrap}
%check
pushd .%{gem_instdir}

rspec -Ilib spec

ln -s %{_builddir}/features features

# Ensure the current version of cucumber-wire is used in place of system one,
# pulled in as a Cucumber dependency.
RUBYOPT="-I$(pwd)/lib" cucumber --format progress --publish-quiet

popd
%endif

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%license %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/spec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Vít Ondruch <vondruch@redhat.com> - 6.2.1-3
- Support quote in backtrace for Ruby 3.4

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Jarek Prokop <jprokop@redhat.com> - 6.2.1-1
- Upgrade to cucumber-wire 6.2.1.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 30 2021 Jarek Prokop <jprokop@redhat.com> - 6.2.0-1
- Relax rubygem-cucumber-cucumber-expressions dependency.
- Update to cucumber-wire 6.2.0.

* Mon Sep 06 2021 Pavel Valena <pvalena@redhat.com> - 6.1.1-1
- Update to cucumber-wire 6.1.1.
  Resolves: rhbz#1867935

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-13
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 Vít Ondruch <vondruch@redhat.com> - 0.0.1-9
- Remove the test suite hack made obsolete by proper fix in rubygem-cucumber.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 06 2018 Vít Ondruch <vondruch@redhat.com> - 0.0.1-7
- Fix compatibility with Cucumber 3.1+

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 21 2017 Vít Ondruch <vondruch@redhat.com> - 0.0.1-3
- Fix Ruby 2.4 compatibility.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Apr 05 2016 Vít Ondruch <vondruch@redhat.com> - 0.0.1-1
- Initial package
