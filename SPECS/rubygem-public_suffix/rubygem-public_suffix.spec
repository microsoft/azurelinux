%global debug_package %{nil}
%global gem_name public_suffix
Summary:        Domain name parser for Ruby based on the Public Suffix List
Name:           rubygem-%{gem_name}
Version:        4.0.6
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://simonecarletti.com/code/publicsuffix-ruby/
Source0:        https://github.com/weppos/publicsuffix-ruby/archive/refs/tags/v%{version}.tar.gz#/publicsuffix-ruby-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
PublicSuffix is a Ruby domain name parser based on the Public Suffix List.

%prep
%autosetup -p1 -n publicsuffix-ruby-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 4.0.6-2
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 4.0.6-1
- License verified
- Original version for CBL-Mariner
