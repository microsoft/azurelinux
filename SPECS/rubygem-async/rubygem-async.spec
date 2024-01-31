%global gem_name async
Summary:        An awesome asynchronous event-driven reactor for Ruby
Name:           rubygem-%{gem_name}
Version:        2.8.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/async
Source0:        https://github.com/socketry/async/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-console
Requires:       rubygem-nio4r
Requires:       rubygem-timers
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Async is a composable asynchronous I/O framework
for Ruby based on nio4r and timers.

%prep
%setup -q -n %{gem_name}-%{version}
%gemspec_clear_signing

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Jan 29 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.8.0-1
- Auto-upgrade to 2.8.0 - Azure Linux 3.0 - package upgrades.
- Restored the debuginfo package.

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.30.2-1
- Update to v1.30.2.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.27.0-1
- License verified
- Original version for CBL-Mariner
