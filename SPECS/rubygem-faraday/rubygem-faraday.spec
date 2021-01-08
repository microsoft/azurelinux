%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name faraday

Name:           rubygem-faraday
Version:        1.1.0
Release:        1%{?dist}
Summary:        HTTP/REST API client library
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.4.0
Requires:       rubygem-ruby2_keywords
Requires:       rubygem-multipart-post >= 1.2
Requires:       rubygem-multipart-post < 3

%description
Faraday is an HTTP client library that provides a common interface over 
many adapters (such as Net::HTTP) and embraces the concept of Rack middleware
when processing the request/response cycle.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 1.1.0-1
-   Original version for CBL-Mariner.
-   License verified.
