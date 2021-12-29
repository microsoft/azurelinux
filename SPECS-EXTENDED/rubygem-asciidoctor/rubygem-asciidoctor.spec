%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name asciidoctor

Summary:        A fast, open source AsciiDoc implementation in Ruby
Name:           rubygem-%{gem_name}
Version:        2.0.15
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:	Mariner
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby

%description
A fast, open source AsciiDoc implementation in Ruby.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Dec 28 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.0.15-1
- Original version for CBL-Mariner
- License verified
