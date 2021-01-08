%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name concurrent-ruby

Name:           rubygem-concurrent-ruby
Version:        1.1.7
Release:        1%{?dist}
Summary:        Modern concurrency tools for Ruby
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 1.9.3

%description
Modern concurrency tools including agents, futures, promises, 
thread pools, supervisors, and more. Inspired by Erlang, 
Clojure, Scala, Go, Java, JavaScript, and classic concurrency patterns. 

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 1.1.7-1
-   Original version for CBL-Mariner.
-   License verified.
