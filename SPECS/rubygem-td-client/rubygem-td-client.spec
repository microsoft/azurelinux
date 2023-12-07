%global debug_package %{nil}
%global gem_name td-client
Summary:        Ruby Client Library for Treasure Data
Name:           rubygem-%{gem_name}
Version:        2.0.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://www.treasuredata.com/
Source0:        https://github.com/treasure-data/td-client-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-ruby-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-httpclient
Requires:       rubygem-msgpack < 2
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Ruby Client Library for Treasure Data.

%prep
%setup -q -n %{gem_name}-ruby-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.0-1
- Auto-upgrade to 2.0.0 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.8-1
- Update to v1.0.8.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 1.0.7-1
- License verified
- Original version for CBL-Mariner
