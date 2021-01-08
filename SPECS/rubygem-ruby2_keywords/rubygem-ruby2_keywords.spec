%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ruby2_keywords

Name:           rubygem-ruby2_keywords
Version:        0.0.2
Release:        1%{?dist}
Summary:        Shim library for Module#ruby2_keywords
Group:          Development/Languages
License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
Provides empty Module#ruby2_keywords method, for the forward 
source-level compatibility against ruby2.7 and ruby3.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 0.0.2-1
-   Original version for CBL-Mariner.
-   License verified.
