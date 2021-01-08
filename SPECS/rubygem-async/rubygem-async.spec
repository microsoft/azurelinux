%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async

Name:           rubygem-async
Version:        1.27.0
Release:        1%{?dist}
Summary:        An awesome asynchronous event-driven reactor for Ruby
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.5.0
Requires:       rubygem-console
Requires:       rubygem-nio4r
Requires:       rubygem-timers

%description
Async is a composable asynchronous I/O framework 
for Ruby based on nio4r and timers.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 1.27.0-1
-   Original version for CBL-Mariner.
-   License verified.
