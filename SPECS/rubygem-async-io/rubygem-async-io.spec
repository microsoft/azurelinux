%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-io

Name:           rubygem-async-io
Version:        1.30.1
Release:        1%{?dist}
Summary:        Concurrent wrappers for native Ruby IO & Sockets
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.5.0
Requires:       rubygem-async

%description
Async::IO provides builds on async and provides asynchronous 
wrappers for IO, Socket, and related classes.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 1.30.1-1
-   Original version for CBL-Mariner.
-   License verified.
