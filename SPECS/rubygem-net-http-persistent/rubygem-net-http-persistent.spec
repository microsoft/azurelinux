%global debug_package %{nil}
%global gem_name net-http-persistent
Summary:        Thread-safe persistent connections with Net::HTTP
Name:           rubygem-%{gem_name}
Version:        4.0.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/drbrain/net-http-persistent
Source0:        https://github.com/drbrain/net-http-persistent/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Source1:        net-http-persistent.gemspec
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Manages persistent connections using Net::HTTP including a thread pool for connecting to multiple hosts.

%prep
%setup -q -n %{gem_name}-%{version}
cp %{SOURCE1} .

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/README.rdoc
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.0.2-1
- Auto-upgrade to 4.0.2 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.1.0-1
- .gemspec file taken from upstream master branch (License MIT)
- License verified
- Original version for CBL-Mariner
