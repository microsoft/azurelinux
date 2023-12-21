%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name thor

Summary:        Thor is a toolkit for building powerful command-line interfaces
Name:           rubygem-%{gem_name}
Version:        1.2.1
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:		    Microsoft Corporation
Distribution:	Mariner
URL:            http://whatisthor.com/
Source0:        https://github.com/rails/thor/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby

%description
Thor is a toolkit for building powerful command-line interfaces.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Mon Feb 28 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.2.1-1
- Update to v1.2.1.
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.1.0-1
- Original version for CBL-Mariner
- License verified
