%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name concurrent-ruby
Summary:        Modern concurrency tools for Ruby
Name:           rubygem-concurrent-ruby
Version:        1.1.10
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby-concurrency/concurrent-ruby
Source0:        https://github.com/ruby-concurrency/concurrent-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         remove_jar.patch
BuildRequires:  git
BuildRequires:  ruby

%description
Modern concurrency tools including agents, futures, promises,
thread pools, supervisors, and more. Inspired by Erlang,
Clojure, Scala, Go, Java, JavaScript, and classic concurrency patterns.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.10-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
