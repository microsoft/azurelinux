%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http_parser.rb

Name:           rubygem-http_parser.rb
Version:        0.6.0
Release:        1%{?dist}
Summary:        simple callback-based HTTP request/response parser
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
A simple callback-based HTTP request/response parser for writing 
http servers, clients and proxies.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE-MIT
%{gemdir}

%changelog
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 0.6.0-1
-   Original version for CBL-Mariner.
-   License verified.
