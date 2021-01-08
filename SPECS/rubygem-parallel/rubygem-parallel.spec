%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name parallel

Name:           rubygem-parallel
Version:        1.20.1
Release:        1%{?dist}
Summary:        Run any kind of code in parallel processes
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.4.0

%description
Run any code in parallel Processes(> use all CPUs) or Threads(> speedup blocking operations).
Best suited for map-reduce or e.g. parallel downloads/uploads.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/MIT-LICENSE.txt
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 1.20.1-1
-   Original version for CBL-Mariner.
-   License verified.
