%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-kms

Name:           rubygem-aws-sdk-kms
Version:        1.30.0
Release:        1%{?dist}
Summary:        Official AWS Ruby gem for AWS Key Management Service (KMS)
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby
Requires:       rubygem-aws-sdk-core
Requires:       rubygem-aws-sigv4

%description
Official AWS Ruby gem for AWS Key Management Service (KMS)

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 1.30.0-1
-   Original version for CBL-Mariner.
-   License verified.
