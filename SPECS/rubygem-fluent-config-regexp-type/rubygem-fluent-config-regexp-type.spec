%global debug_package %{nil}
%global gem_name fluent-config-regexp-type
Summary:        The compatibility patch to use regexp type
Name:           rubygem-%{gem_name}
Version:        1.0.0
Release:        2%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/okkez/fluent-config-regexp-type
Source0:        https://github.com/okkez/fluent-config-regexp-type/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluentd
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Fluentd 1.2.0 supports regexp type in config_param.
This gem backports regexp type for config_param.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-2
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.0.0-1
- License verified
- Original version for CBL-Mariner