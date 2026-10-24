%global debug_package %{nil}
%global gem_name httpclient
Summary:        HTTP accessing library
Name:           rubygem-%{gem_name}
Version:        2.8.3
Release:        2%{?dist}
License:        NAKAMURA, Hiroshi Open Source
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://github.com/nahi/httpclient
Source0:        https://github.com/nahi/httpclient/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         remove-compromised-ca-roots.patch
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
'httpclient' gives something similar to the functionality of 
libwww-perl (LWP) in Ruby.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Oct 23 2026 Jon Slobodzian <joslobo@microsoft.com> - 2.8.3-2
- Remove the affected AAA cross-signing root from all bundled certificate stores.

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.8.3-1
- Update to v2.8.3.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 2.8.2.4-1
- License verified
- Original version for CBL-Mariner
