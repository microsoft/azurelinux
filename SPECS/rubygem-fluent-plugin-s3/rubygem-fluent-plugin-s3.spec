%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-s3
Summary:        Amazon S3 output plugin for Fluentd event collector
Name:           rubygem-fluent-plugin-s3
Version:        1.3.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby > 2.1.0
Requires:       rubygem-aws-sdk-s3
Requires:       rubygem-aws-sdk-sqs
Requires:       rubygem-fluentd

%description
Amazon S3 output plugin for Fluentd event collector

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
