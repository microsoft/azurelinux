%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name bundler
Summary:        manages an application's dependencies
Name:           rubygem-bundler
Version:        1.16.4
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby > 2.1.0
Provides:       rubygem(bundler) = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}

%description
Bundler manages an application's dependencies through its entire life
across many machines, systematically and repeatably.

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
* Thu Mar 11 2021 Henry Li <lihl@microsoft.com> - 1.16.4-5
- Add provides for rubygem(bundler) and rubygem-bundler-doc

*   Thu May 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.16.4-4
-   Removed "sha1" macro.
-   Removed redundant "Provides" tag.
-   License verified.

*   Wed May 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.16.4-3
-   Adding the "%%license" macro.

*   Tue May 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.16.4-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.16.4-1
-   Update to version 1.16.4

*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.16.3-1
-   Initial build
