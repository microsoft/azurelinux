%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http2

Name:           rubygem-protocol-http2
Version:        0.13.2
Release:        1%{?dist}
Summary:        A low level implementation of the HTTP/2 protocol
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.5.0
Requires:       rubygem-protocol-hpack
Requires:       rubygem-protocol-http

%description
Provides a low-level implementation of the HTTP/2 protocol.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 0.13.2-1
-   Original version for CBL-Mariner.
-   License verified.
