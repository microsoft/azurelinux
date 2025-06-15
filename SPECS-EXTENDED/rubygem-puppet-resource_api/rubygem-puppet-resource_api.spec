%global gem_name puppet-resource_api
 
Name: rubygem-%{gem_name}
Version: 1.8.18
Release: 1%{?dist}
Summary: This library provides a simple way to write new native resources for puppet
License: Apache-2.0
Vendor:		Microsoft Corporation
Distribution:   Azure Linux
URL: https://github.com/puppetlabs/puppet-resource_api
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
Requires: puppet
BuildArch: noarch

%description
This library provides a simple way to write new native resources for puppet.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

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
rm -rf %{buildroot}%{gem_instdir}/{.gitignore,.rubocop.yml,.travis.yml,appveyor.yml,codecov.yml}
 
# %%check can't run since it requires puppet, but puppet requires this package

%files
%license %{gem_instdir}/LICENSE
%license %{gem_instdir}/NOTICE
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/docs
%{gem_instdir}/puppet-resource_api.gemspec

%changelog
* Thu Dec 05 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.8.18-1
- Update to version 1.8.18
- License verified

* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.8.14-2
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.8.14-1
- Original version for CBL-Mariner
- License verified
