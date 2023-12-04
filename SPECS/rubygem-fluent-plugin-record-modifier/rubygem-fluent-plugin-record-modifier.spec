%global debug_package %{nil}
%global gem_name fluent-plugin-record-modifier
Summary:        Filter plugin for modifying event record
Name:           rubygem-%{gem_name}
Version:        2.1.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/repeatedly/fluent-plugin-record-modifier
Source0:        https://github.com/repeatedly/fluent-plugin-record-modifier/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluentd
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Filter plugin to modify event record for Fluentd

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.1.1-1
- Auto-upgrade to 2.1.1 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.1.0-2
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 2.1.0-1
- License verified
- Original version for CBL-Mariner
