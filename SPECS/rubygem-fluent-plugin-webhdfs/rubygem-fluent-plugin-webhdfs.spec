%global debug_package %{nil}
%global gem_name fluent-plugin-webhdfs
Summary:        Hadoop WebHDFS output plugin for Fluentd
Name:           rubygem-%{gem_name}
Version:        1.5.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-webhdfs
Source0:        https://github.com/fluent/fluent-plugin-webhdfs/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluentd
Requires:       rubygem-webhdfs
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Fluentd output plugin to write data into Hadoop HDFS over WebHDFS/HttpFs.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.5.0-1
- Update to v1.5.0.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.2.4-1
- License verified
- Original version for CBL-Mariner
