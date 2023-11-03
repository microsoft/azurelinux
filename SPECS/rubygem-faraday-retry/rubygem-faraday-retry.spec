%global debug_package %{nil}
%global gem_name faraday-retry
Summary:        Catches exceptions and retries each request a limited number of times
Name:           rubygem-%{gem_name}
Version:        2.2.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/lostisland/faraday-retry
Source0:        https://github.com/lostisland/faraday-retry/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(%{gem_name}) = %{version}-%{release}
AutoReq:        no

%description
The Retry middleware automatically retries requests that fail due to intermittent client or server errors (such as network hiccups). By default, it retries 2 times and handles only timeout exceptions. It can be configured with an arbitrary number of retries, a list of exceptions to handle, a retry interval, a percentage of randomness to add to the retry interval, and a backoff factor. The middleware can also handle the Retry-After header automatically when configured with the right status codes (see below for an example).

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Fri Nov 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.2.0-1
- Auto-upgrade to 2.2.0 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.1-1
- License verified
- Original version for CBL-Mariner
