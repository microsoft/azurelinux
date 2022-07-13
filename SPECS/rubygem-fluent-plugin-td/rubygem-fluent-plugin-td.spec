%global debug_package %{nil}
%global gem_name fluent-plugin-td
Summary:        Fluentd plugin for Treasure Data Service
Name:           rubygem-fluent-plugin-td
Version:        1.1.0
Release:        2%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://www.treasuredata.com/
Source0:        https://github.com/treasure-data/fluent-plugin-td/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluentd
Requires:       rubygem-td-client
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This Fluentd output plugin is used to upload
logs to Treasure Data using Treasure Data's REST APIs.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.0-2
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.1.0-1
- License verified
- Original version for CBL-Mariner
