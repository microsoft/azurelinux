%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-rewrite-tag-filter

Name:           rubygem-fluent-plugin-rewrite-tag-filter
Version:        2.3.0
Release:        1%{?dist}
Summary:        Fluentd Output filter plugin
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby > 2.1.0
Requires:       rubygem-fluent-config-regexp-type
Requires:       rubygem-fluentd

%description
Fluentd Output filter plugin to rewrite tags that matches specified attribute.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 2.3.0-1
-   Original version for CBL-Mariner.
-   License verified.
