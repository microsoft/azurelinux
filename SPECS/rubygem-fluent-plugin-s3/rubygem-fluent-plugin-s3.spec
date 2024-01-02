%global debug_package %{nil}
%global gem_name fluent-plugin-s3
Summary:        Amazon S3 output plugin for Fluentd event collector
Name:           rubygem-%{gem_name}
Version:        1.7.2
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-s3
Source0:        https://github.com/fluent/fluent-plugin-s3/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-aws-sdk-s3
Requires:       rubygem-aws-sdk-sqs
Requires:       rubygem-fluentd
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Amazon S3 output plugin for Fluentd event collector

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.2-1
- Auto-upgrade to 1.7.2 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.6.0-1
- Update to v1.6.0.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.3.0-1
- License verified
- Original version for CBL-Mariner
