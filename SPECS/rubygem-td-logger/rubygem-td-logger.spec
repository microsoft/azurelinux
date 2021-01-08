%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name td-logger

Name:           rubygem-td-logger
Version:        0.3.27
Release:        1%{?dist}
Summary:        Treasure Data logging library
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
Requires:       rubygem-fluent-logger >= 0.5.0
Requires:       rubygem-fluent-logger < 2.0
Requires:       rubygem-msgpack >= 0.5.6
Requires:       rubygem-msgpack < 2.0
Requires:       rubygem-td-client >= 0.8.66
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
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 0.3.27-1
-   Original version for CBL-Mariner.
-   License verified.
