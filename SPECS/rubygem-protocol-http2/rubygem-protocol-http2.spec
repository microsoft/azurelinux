%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http2
Summary:        A low level implementation of the HTTP/2 protocol
Name:           rubygem-protocol-http2
Version:        0.13.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
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
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.13.2-1
- License verified
- Original version for CBL-Mariner