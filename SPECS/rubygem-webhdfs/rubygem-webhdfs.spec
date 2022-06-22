%global debug_package %{nil}
%global gem_name webhdfs
Summary:        Ruby client for Hadoop WebHDFS
Name:           rubygem-%{gem_name}
Version:        0.10.2
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/kzk/webhdfs/
Source0:        https://github.com/kzk/webhdfs/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-addressable
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
A client library implementation for Hadoop WebHDFS, and HttpFs, for Ruby

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/COPYING
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.10.2-1
- Update to v0.10.2.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.9.0-1
- License verified
- Original version for CBL-Mariner
