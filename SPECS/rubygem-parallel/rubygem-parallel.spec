%global debug_package %{nil}
%global gem_name parallel
Summary:        Run any kind of code in parallel processes
Name:           rubygem-parallel
Version:        1.23.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://github.com/grosser/parallel
Source0:        https://github.com/grosser/parallel/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Run any code in parallel Processes(> use all CPUs) or Threads(> speedup blocking operations).
Best suited for map-reduce or e.g. parallel downloads/uploads.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license MIT-LICENSE.txt
%{gemdir}

%changelog
* Sat Mar 23 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.23.0-1
- Upgrade to 1.23.0

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.20.1-2
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 1.20.1-1
- License verified
- Original version for CBL-Mariner
