%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name systemd-journal

Name:           rubygem-systemd-journal
Version:        1.3.3
Release:        1%{?dist}
Summary:        Ruby bindings for reading/writing to the systemd journal 
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 1.9.3
Requires:       rubygem-ffi

%description
Provides the ability to navigate and read entries from the systemd 
journal in ruby, as well as write events to the journal.

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
*   Tue Jan 05 2021 Henry Li <lihl@microsoft.com> 1.3.3-1
-   Original version for CBL-Mariner.
-   License verified.
