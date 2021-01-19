%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name td-logger
Summary:        Treasure Data logging library
Name:           rubygem-td-logger
Version:        0.3.27
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
Requires:       rubygem-fluent-logger < 2.0
Requires:       rubygem-msgpack < 2.0
Requires:       rubygem-td-client < 2.0

%description
This gem is a logging library for Treasure Data. The events
logged by this module will be uploaded into the cloud.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 0.3.27-1
- License verified
- Original version for CBL-Mariner