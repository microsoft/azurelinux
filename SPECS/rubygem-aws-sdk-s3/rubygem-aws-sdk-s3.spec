%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-s3
Summary:        Official AWS Ruby gem for Amazon Simple Storage Service (Amazon S3)
Name:           rubygem-aws-sdk-s3
Version:        1.61.1
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
Requires:       rubygem-aws-sdk-core
Requires:       rubygem-aws-sdk-kms
Requires:       rubygem-aws-sigv4

%description
Official AWS Ruby gem for Amazon Simple Storage Service (Amazon S3)

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 1.61.1-1
- License verified
- Original version for CBL-Mariner