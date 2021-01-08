%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-config-regexp-type

Name:           rubygem-fluent-config-regexp-type
Version:        1.0.0
Release:        1%{?dist}
Summary:        The compatibility monkey patch to use regexp type
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
Requires:       rubygem-fluentd

%description
Fluentd 1.2.0 supports regexp type in config_param. 
This gem backports regexp type for config_param.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 1.0.0-1
-   Original version for CBL-Mariner.
-   License verified.
