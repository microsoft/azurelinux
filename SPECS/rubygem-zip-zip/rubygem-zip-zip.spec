%global debug_package %{nil}
%global gem_name zip-zip
Summary:        a simple adapter to let all your dependencies use RubyZip
Name:           rubygem-%{gem_name}
Version:        0.3
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/orien/zip-zip
Source0:        https://github.com/orien/zip-zip/archive/refs/tags/%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-rubyzip
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
zip-zip provides a simple adapter to let all your dependencies 
use RubyZip.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.3-2
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 0.3-1
- License verified
- Original version for CBL-Mariner
