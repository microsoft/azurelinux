%global debug_package %{nil}
%global gem_name fluent-plugin-s3
Summary:        Amazon S3 output plugin for Fluentd event collector
Name:           rubygem-fluent-plugin-s3
Version:        1.6.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-s3
Source0:        https://github.com/fluent/fluent-plugin-s3/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-aws-sdk-s3
Requires:       rubygem-aws-sdk-sqs
Requires:       rubygem-fluentd

%description
Amazon S3 output plugin for Fluentd event collector

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.3.0-1
- License verified
- Original version for CBL-Mariner
