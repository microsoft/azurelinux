%global debug_package %{nil}
%global gem_name webrick
Summary:        HTTP server toolkit
Name:           rubygem-%{gem_name}
Version:        1.8.1
Release:        1%{?dist}
License:        BSD
Vendor:	        Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ruby/webrick
Source0:        https://github.com/ruby/webrick/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
WEBrick is an HTTP server toolkit that can be configured as an HTTPS server, a proxy server, and a virtual-host server.
WEBrick features complete logging of both server operations and HTTP access.
WEBrick supports both basic and digest authentication in addition to algorithms not in RFC 2617.
A WEBrick server can be composed of multiple WEBrick servers or servlets to provide differing behavior on a per-host or per-path basis. WEBrick includes servlets for handling CGI scripts, ERB pages, Ruby blocks and directory listings.
WEBrick also includes tools for daemonizing a process and starting a process at a higher privilege level and dropping permissions.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-1
- Auto-upgrade to 1.8.1 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.7.0-1
- License verified
- Original version for CBL-Mariner
