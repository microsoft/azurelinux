%global debug_package %{nil}
%global gem_name tzinfo
Summary:        Ruby Timezone Library
Name:           rubygem-%{gem_name}
Version:        2.0.6
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://tzinfo.github.io/
Source0:        https://github.com/tzinfo/tzinfo/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-concurrent-ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
a Ruby library that provides access to time zone data
and allows times to be converted using time zone rules.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.6-1
- Auto-upgrade to 2.0.6 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.4-1
- Update to v2.0.4.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 2.0.2-1
- License verified
- Original version for CBL-Mariner
