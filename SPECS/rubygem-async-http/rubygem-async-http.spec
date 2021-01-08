%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-http
Summary:        A HTTP client and server library
Name:           rubygem-async-http
Version:        0.50.13
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby > 2.1.0
Requires:       rubygem-async
Requires:       rubygem-async-io
Requires:       rubygem-async-pool
Requires:       rubygem-protocol-http
Requires:       rubygem-protocol-http1
Requires:       rubygem-protocol-http2

%description
An asynchronous client and server implementation of HTTP/1.0,
HTTP/1.1 and HTTP/2 including TLS. Support for streaming requests
and responses.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
