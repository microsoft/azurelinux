%global debug_package %{nil}
%global gem_name td-logger
Summary:        Treasure Data logging library
Name:           rubygem-%{gem_name}
Version:        0.3.27
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/treasure-data/td-logger-ruby
Source0:        https://github.com/treasure-data/td-logger-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-ruby-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluent-logger < 2.0
Requires:       rubygem-msgpack < 2.0
Requires:       rubygem-td-client < 2.0
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This gem is a logging library for Treasure Data. The events
logged by this module will be uploaded into the cloud.

%prep
%autosetup -p1 -n %{gem_name}-ruby-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.3.27-2
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 0.3.27-1
- License verified
- Original version for CBL-Mariner
