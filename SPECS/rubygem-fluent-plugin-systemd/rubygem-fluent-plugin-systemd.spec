%global debug_package %{nil}
%global gem_name fluent-plugin-systemd
Summary:        Reads logs from the systemd journal
Name:           rubygem-fluent-plugin-systemd
Version:        1.0.5
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent-plugin-systemd/fluent-plugin-systemd
Source0:        https://github.com/fluent-plugin-systemd/fluent-plugin-systemd/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-fluentd
Requires:       rubygem-systemd-journal
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This is a fluentd input plugin.
It reads logs from the systemd journal.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENCE
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.5-1
- Update to v1.0.5.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.0.2-1
- License verified
- Original version for CBL-Mariner
