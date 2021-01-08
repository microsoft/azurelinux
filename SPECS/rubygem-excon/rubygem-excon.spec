%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name excon

Name:           rubygem-excon
Version:        0.78.0
Release:        1%{?dist}
Summary:        Usable, fast, simple HTTP 1.1 for Ruby 
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
Excon was designed to be simple, fast and performant. It works great as a 
general HTTP(s) client and is particularly well suited to usage in API clients.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 0.78.0-1
-   Original version for CBL-Mariner.
-   License verified.
