%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-logger

Name:           rubygem-fluent-logger
Version:        0.9.0
Release:        1%{?dist}
Summary:        fluent logger for ruby
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
Requires:       rubygem-msgpack >= 1.0.0
Requires:       rubygem-msgpack < 2

%description
A structured event logger.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/COPYING
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 0.9.0-1
-   Original version for CBL-Mariner.
-   License verified.
