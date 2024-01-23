%global debug_package %{nil}
%global gem_name timers
Summary:        Pure Ruby one-shot and periodic timers
Name:           rubygem-%{gem_name}
Version:        4.3.5
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/timers
Source0:        https://github.com/socketry/timers/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Collections of one-shot and periodic timers, intended for
use with event loops such as async.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Jan 22 2024 Riken Maharjan <rmaharjan@microsoft.com> - 4.3.5-1
- Upgrade to 4.3.5.

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 4.3.2-2
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 4.3.2-1
- License verified
- Original version for CBL-Mariner
