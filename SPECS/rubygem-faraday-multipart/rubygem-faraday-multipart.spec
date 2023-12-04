%global debug_package %{nil}
%global gem_name faraday-multipart
Summary:        Perform multipart-post requests using Faraday
Name:           rubygem-%{gem_name}
Version:        1.0.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/lostisland/faraday-multipart
Source0:        https://github.com/lostisland/faraday-multipart/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Perform multipart-post requests using Faraday. The Multipart middleware converts a Faraday::Request#body Hash of key/value pairs into a multipart form request.

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.4-1
- Auto-upgrade to 1.0.4 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner
