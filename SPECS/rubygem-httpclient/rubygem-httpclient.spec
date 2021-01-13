%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name httpclient
Summary:        HTTP accessing library
Name:           rubygem-httpclient
Version:        2.8.2.4
Release:        1%{?dist}
License:        NAKAMURA, Hiroshi Open Source
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
'httpclient' gives something similar to the functionality of 
libwww-perl (LWP) in Ruby.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 2.8.2.4-1
- License verified
- Original version for CBL-Mariner