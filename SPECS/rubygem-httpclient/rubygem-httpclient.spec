%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name httpclient

Name:           rubygem-httpclient
Version:        2.8.2.4
Release:        1%{?dist}
Summary:        HTTP accessing library
Group:          Development/Languages
License:        NAKAMURA, Hiroshi Open Source
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
gives something like the functionality of libwww-perl (LWP) in Ruby.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jan 04 2021 Henry Li <lihl@microsoft.com> 2.8.2.4-1
-   Original version for CBL-Mariner.
-   License verified.
