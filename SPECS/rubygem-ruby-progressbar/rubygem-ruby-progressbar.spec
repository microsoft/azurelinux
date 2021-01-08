%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ruby-progressbar

Name:           rubygem-ruby-progressbar
Version:        1.10.1
Release:        1%{?dist}
Summary:        Ruby/ProgressBar is a text progress bar library for Ruby
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
Ruby/ProgressBar is an extremely flexible text progress bar library for 
Ruby. The output can be customized with a flexible formatting system including: 
percentage, bars of various formats, elapsed time and estimated time remaining.

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
*   Wed Jan 06 2021 Henry Li <lihl@microsoft.com> 1.10.1-1
-   Original version for CBL-Mariner.
-   License verified.
