# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%global enable_checks 1

# Generated from deep_merge-1.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name deep_merge

Name: rubygem-%{gem_name}
Version: 1.2.2
Release: 11%{?dist}
Summary: Merge Deeply Nested Hashes
License: MIT
URL: https://github.com/danielsdeleo/deep_merge
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(rubygems) 
BuildRequires: rubygems-devel 
BuildRequires: ruby 
%if 0%{?enable_checks}
BuildRequires: rubygem(minitest) >= 5
BuildRequires: rubygem(test-unit)
%endif

BuildArch: noarch

%description
Recursively merge hashes. 

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%if 0%{?enable_checks}
ruby -Ilib test/test_deep_merge.rb
%endif

%files
%dir %{gem_instdir}

%{gem_libdir}
%exclude %{gem_cache} 
%exclude %{gem_instdir}/CHANGELOG
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/Rakefile
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md 


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Pavel Valena <pvalena@redhat.com> - 1.2.2-1
- Update to deep_merge 1.2.2.
  Resolves: rhbz#2038450

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 Steve Traylen <steve.traylen@cern.ch> - 1.2.1-1
- Update to 1.2.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 23 2017 Steve Traylen <steve.traylen@cern.ch> - 1.1.1-1
- Update to 1.1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-5
- Ensure rubygem(minitest) is > 5 version on fc21.

* Tue Jun 3 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-4
- Include LICENSE file in main package.

* Mon Jun 2 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-3
- Drop usage of testrb and use ruby instead for checks.

* Fri May 30 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-2
- latest ruby guidelines and minitest5 patch

* Wed Feb 12 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-1
- Initial package
