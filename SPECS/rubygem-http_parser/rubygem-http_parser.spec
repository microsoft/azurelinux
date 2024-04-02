%global gem_name http_parser.rb
Summary:        simple callback-based HTTP request/response parser
Name:           rubygem-http_parser
Version:        0.8.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://github.com/tmm1/http_parser.rb
Source0:        https://github.com/tmm1/http_parser.rb/archive/refs/tags/v0.8.0.tar.gz#/http_parser-%{version}.tar.gz
Source1:        http_parser-%{version}-submodules.tar.gz
BuildRequires:  git
BuildRequires:  rubygem-ffi
BuildRequires:  rubygem-json
BuildRequires:  rubygem-rake-compiler
BuildRequires:  rubygem-rspec
BuildRequires:  rubygem-yajl-ruby
BuildRequires:  ruby
Provides:       rubygem(http_parser) = %{version}-%{release}
Provides:       rubygem-http_parser = %{version}-%{release}
# Provide old http_parser.rb
Provides:       rubygem(%{gem_name}) = %{version}-%{release}
Provides:       rubygem-%{gem_name} = %{version}-%{release}


%description
A simple callback-based HTTP request/response parser for writing
http servers, clients and proxies.

%prep
%autosetup -a 1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license LICENSE-MIT
%{gemdir}

%changelog
* Mon Apr 1 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.8.0-1
- Update to 0.8.0 for AZL 3.0.
- change the rubygem name to rubygem-http_parser.

* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.1-2
- Updating naming for 3.0 version of Azure Linux.

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.6.1-1
- Downgrade to v0.6.1.
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 0.8.0-1
- License verified
- Original version for CBL-Mariner
