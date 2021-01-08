%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name addressable

Name:           rubygem-addressable
Version:        2.7.0
Release:        1%{?dist}
Summary:        an alternative implementation to the URI implementation that is part of Ruby's standard library
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.0.0
Requires:       rubygem-public_suffix >= 2.0.2
Requires:       rubygem-public_suffix < 5.0

%description
Addressable is an alternative implementation to the URI implementation that is 
part of Ruby's standard library. It is flexible, offers heuristic parsing, 
and additionally provides extensive support for IRIs and URI templates.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 2.7.0-1
-   Original version for CBL-Mariner.
-   License verified.
