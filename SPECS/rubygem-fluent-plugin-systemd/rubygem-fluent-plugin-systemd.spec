%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-systemd

Name:           rubygem-fluent-plugin-systemd
Version:        1.0.2
Release:        1%{?dist}
Summary:        Reads logs from the systemd journal 
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
Requires:       rubygem-fluentd
Requires:       rubygem-systemd-journal

%description
This is a fluentd input plugin. 
It reads logs from the systemd journal.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENCE
%{gemdir}

%changelog
*   Tue Jan 05 2021 Henry Li <lihl@microsoft.com> 1.0.2-1
-   Original version for CBL-Mariner.
-   License verified.
