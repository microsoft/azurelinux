%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name stringio
Summary:        Pseudo `IO` class from/to `String`
Name:           rubygem-stringio
Version:        3.0.1
Release:        1%{?dist}
License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby/stringio
Source0:        https://github.com/ruby/stringio/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(stringio) = %{version}-%{release}

%description
Pseudo IO class from/to String.
This library is based on MoonWolf version written in Ruby.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 21 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.0.1-1
- License verified
- Original version for CBL-Mariner
