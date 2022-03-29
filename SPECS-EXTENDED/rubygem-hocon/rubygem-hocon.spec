%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name hocon

Summary:        A port of the Java Typesafe Config library to Ruby
Name:           rubygem-%{gem_name}
Version:        1.3.1
Release:        2%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:	Mariner
URL:            https://github.com/puppetlabs/ruby-hocon
Source0:        https://github.com/puppetlabs/ruby-hocon/archive/refs/tags/%{version}.tar.gz#/ruby-%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby

%description
A port of the Java Typesafe Config library to Ruby.

%prep
%setup -q -n ruby-%{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.3.1-2
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.3.1-1
- Original version for CBL-Mariner
- License verified
