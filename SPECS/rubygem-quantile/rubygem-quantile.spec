%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name quantile

Name:           rubygem-quantile
Version:        0.2.1
Release:        1%{?dist}
Summary:        Ruby Implementation of Graham Cormode and S. Muthukrishnan's Effective Computation of Biased Quantiles over Data Streams in ICDE’05
Group:          Development/Languages
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
Ruby Implementation of Graham Cormode and S. Muthukrishnan's Effective Computation of 
Biased Quantiles over Data Streams in ICDE’05.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 0.2.1-1
-   Original version for CBL-Mariner.
-   License verified.
