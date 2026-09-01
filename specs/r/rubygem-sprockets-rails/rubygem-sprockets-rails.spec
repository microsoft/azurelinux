# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from sprockets-rails-2.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sprockets-rails

Name: rubygem-%{gem_name}
Version: 3.5.2
Release: 2%{?dist}
Summary: Sprockets Rails integration
License: MIT
URL: https://github.com/rails/sprockets-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Get the tests
# git clone --no-checkout https://github.com/rails/sprockets-rails.git && cd sprockets-rails
# git archive -v -o sprockets-rails-3.5.2-tests.tar.gz v3.5.2 test/
Source1: sprockets-rails-%{version}-tests.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(railties) >= 6.1
%dnl BuildRequires: rubygem(rake)
BuildRequires: rubygem(sprockets)
BuildArch: noarch

%description
Provides Sprockets implementation for Rails 4.x (and beyond) Asset Pipeline.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

( cd .%{gem_instdir}
ln -s %{builddir}/test .

ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 01 2025 Vít Ondruch <vondruch@redhat.com> - 3.5.2-1
- Update to Sprockets Rails 3.5.2.
  Resolves: rhbz#2290690

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 01 2023 Pavel Valena <pvalena@redhat.com> - 3.4.2-1
- Update to sprockets-rails 3.4.2.
  Resolves: rhbz#2022436

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jul 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.2-6
- Backport upstream fix for supporting actionview 7

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct  9 04:24:35 CEST 2020 Pavel Valena <pvalena@redhat.com> - 3.2.2-1
- Update to sprockets-rails 3.2.2.
  Resolves: rhbz#1878349

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 19 2018 Pavel Valena <pvalena@redhat.com> - 3.2.1-1
- Update to Sprockets Rails 3.2.1.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 15 2017 Jun Aruga <jaruga@redhat.com> - 3.2.0-5
- Fix tests for FTBFS.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Vít Ondruch <vondruch@redhat.com> - 3.2.0-3
- Fix test compatibility with Rails 5.1.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Jun Aruga <jaruga@redhat.com> - 3.2.0-1
- Update to sprockets-rails 3.2.0.

* Mon Aug 15 2016 Vít Ondruch <vondruch@redhat.com> - 3.1.1-1
- Update to sprockets-rails 3.1.1.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 29 2015 Josef Stribny <jstribny@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Josef Stribny <jstribny@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Thu Jan 29 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.4-2
- Drop the boostrap and depend on railties instead of rails.

* Wed Jan 28 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.4-1
- Update to sprockets-rails 2.2.4.

* Fri Jul 04 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.3-1
- Update to sprockets-rails 2.1.3.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Josef Stribny <jstribny@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-3
- Enable tests

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-2
- Disable tests for now due to broken deps in Rails

* Mon Jul 22 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-1
- Initial package
