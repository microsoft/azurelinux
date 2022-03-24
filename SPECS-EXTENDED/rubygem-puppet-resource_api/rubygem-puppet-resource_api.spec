%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name puppet-resource_api

Summary:        Provides a simple way to write new native resources for puppet
Name:           rubygem-%{gem_name}
Version:        1.8.14
Release:        2%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:		Microsoft Corporation
Distribution:	Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://github.com/puppetlabs/puppet-resource_api/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby

%description
This library provides a simple way to write new native resources for puppet.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.8.14-2
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.8.14-1
- Original version for CBL-Mariner
- License verified
