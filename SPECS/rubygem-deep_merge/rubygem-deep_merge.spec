%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name deep_merge

Summary:        Merge Deeply Nested Hashes
Name:           rubygem-%{gem_name}
Version:        1.2.1
Release:        3%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:	Mariner
URL:            https://github.com/danielsdeleo/deep_merge
Source0:        https://github.com/danielsdeleo/deep_merge/archive/refs/tags/%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby

%description
Recursively merge hashes.

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
* Thu Dec 21 2023 Sindhu Karri <lakarri@microsoft.com> - 1.2.1-3
- Promote package to Mariner Base repo

* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.2.1-2
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.2.1-1
- Original version for CBL-Mariner
- License verified
