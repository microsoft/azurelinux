%global debug_package %{nil}
%global gem_name bundler
Summary:        manages an application's dependencies
Name:           rubygem-bundler
Version:        2.3.8
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/rubygems/rubygems
Source0:        https://github.com/rubygems/rubygems/archive/refs/tags/bundler-v%{version}.tar.gz#/rubygems-%{gem_name}-v%{version}.tar.gz
BuildRequires:  ruby > 2.1.0
Provides:       rubygem(bundler) = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}

%description
Bundler manages an application's dependencies through its entire life
across many machines, systematically and repeatably.

%prep
%setup -q -n rubygems-%{gem_name}-v%{version}

%build
cd %{gem_name}
gem build %{gem_name}

%install
cd %{gem_name}
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} --bindir %{buildroot}%{_bindir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{_bindir}/bundle
%{_bindir}/bundler
%{gemdir}

%changelog
* Wed May 25 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.3.8-2
- Build bin files.

* Tue Mar 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.3.8-1
- Update to v2.3.8.
- Build from .tar.gz source.

* Thu Mar 11 2021 Henry Li <lihl@microsoft.com> - 1.16.4-5
- Add provides for rubygem(bundler) and rubygem-bundler-doc

* Thu May 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.16.4-4
- Removed "sha1" macro.
- Removed redundant "Provides" tag.
- License verified.

* Wed May 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.16.4-3
- Adding the "%%license" macro.

* Tue May 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.16.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.16.4-1
- Update to version 1.16.4

* Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.16.3-1
- Initial build
