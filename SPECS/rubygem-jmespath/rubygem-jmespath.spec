%global debug_package %{nil}
%global gem_name jmespath
Summary:        Ruby implementation of JMESPath
Name:           rubygem-%{gem_name}
Version:        1.6.2
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/jmespath/jmespath.rb
Source0:        https://github.com/jmespath/jmespath.rb/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}.rb-%{version}.tar.gz
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
An implementation of JMESPath for Ruby. This implementation supports searching
JSON documents as well as native Ruby data structures.

%prep
%setup -q -n %{gem_name}.rb-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-1
- Auto-upgrade to 1.6.2 - Azure Linux 3.0 - package upgrades

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.6.1-1
- Update to v1.6.1.
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 1.4.0-1
- License verified
- Original version for CBL-Mariner
