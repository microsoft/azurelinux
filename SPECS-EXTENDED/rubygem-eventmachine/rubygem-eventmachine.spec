%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name eventmachine

Name:          rubygem-%{gem_name}
Version:       1.2.7
Release:       1%{?dist}
Summary:       Ruby/EventMachine library
License:       MIT
Vendor:	       Microsoft Corporation
Distribution:  Mariner
URL:           http://rubyeventmachine.com
#Source0:       https://github.com/eventmachine/eventmachine/archive/refs/tags/v%{version}.tar.gz
Source0:       %{gem_name}-%{version}.tar.gz
BuildRequires: ruby
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: openssl-devel
BuildRequires: rubygem(test-unit)

%description
EventMachine implements a fast, single-threaded engine for arbitrary network
communications. It's extremely easy to use in Ruby. EventMachine wraps all
interactions with IP sockets, allowing programs to concentrate on the
implementation of network protocols. 

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
* Thu Dec 30 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.2.7-1
- License verified
- Original version for CBL-Mariner
