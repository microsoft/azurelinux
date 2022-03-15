%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name semantic_puppet

Summary:        Useful tools for working with Semantic Versions
Name:           rubygem-%{gem_name}
Version:        1.0.4
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:	Mariner
URL:            https://github.com/puppetlabs/semantic_puppet
#Source0:        https://github.com/puppetlabs/semantic_puppet/archive/refs/tags/%{version}.tar.gz
Source0:        %{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby

%description
Tools used by Puppet to parse, validate, and compare Semantic Versions and
Version Ranges and to query and resolve module dependencies.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.0.4-1
- Original version for CBL-Mariner
- License verified
