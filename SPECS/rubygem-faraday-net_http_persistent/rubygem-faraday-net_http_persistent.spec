%global debug_package %{nil}
%global gem_name faraday-net_http_persistent
Summary:        Faraday Adapter for NetHttpPersistent
Name:           rubygem-%{gem_name}
Version:        2.1.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/lostisland/faraday-net_http_persistent
Source0:        https://github.com/lostisland/faraday-net_http_persistent/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This gem is a Faraday adapter for the Net::HTTP::Persistent gem.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.1.0-1
- Auto-upgrade to 2.1.0 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner
