%global debug_package %{nil}
%global gem_name webrick
Summary:        HTTP server toolkit
Name:           rubygem-%{gem_name}
Version:        1.7.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:	        Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ruby/webrick
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
WEBrick is an HTTP server toolkit that can be configured as an HTTPS server, a proxy server, and a virtual-host server.

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
* Thu Jun 30 2022 Suresh Babu chalamalasetty <schalam@microsoft.com> - 1.7.0-1
- License verified
- Original version for CBL-Mariner
