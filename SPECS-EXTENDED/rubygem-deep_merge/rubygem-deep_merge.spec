%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name deep_merge

Summary:        Merge Deeply Nested Hashes
Name:           rubygem-%{gem_name}
Version:        1.2.1
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:		Microsoft Corporation
Distribution:	Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
Recursively merge hashes.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}


%changelog
* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.2.1-1
- Original version for CBL-Mariner
- License verified
