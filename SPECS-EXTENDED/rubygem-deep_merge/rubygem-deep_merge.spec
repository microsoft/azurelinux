 
%global enable_checks 1
 
# Generated from deep_merge-1.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name deep_merge
 
Name: rubygem-%{gem_name}
Version: 1.2.2
Release: 1%{?dist}
Summary: Merge Deeply Nested Hashes
License: MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
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
%license %{gem_instdir}/LICENSE


%changelog
* Thu Dec 05 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.2.2-1
- Update to version 1.2.2

* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.2.1-2
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.2.1-1
- Original version for CBL-Mariner
- License verified
