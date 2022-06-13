%global debug_package %{nil}
%global gem_name fluent-plugin-record-modifier
Summary:        Filter plugin for modifying event record
Name:           rubygem-fluent-plugin-record-modifier
Version:        2.1.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/repeatedly/fluent-plugin-record-modifier
Source0:        https://github.com/repeatedly/fluent-plugin-record-modifier/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluentd
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Filter plugin to modify event record for Fluentd

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add README.md file to buildroot from Source0
cp README.md %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 2.1.0-1
- License verified
- Original version for CBL-Mariner
