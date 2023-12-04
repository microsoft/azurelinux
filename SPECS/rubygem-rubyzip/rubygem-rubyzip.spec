%global debug_package %{nil}
%global gem_name rubyzip
Summary:        a ruby module for reading and writing zip files
Name:           rubygem-%{gem_name}
Version:        2.3.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/rubyzip/rubyzip
Source0:        https://github.com/rubyzip/rubyzip/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Rubyzip is a ruby library for reading and writing zip files.

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
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.3.2-1
- Auto-upgrade to 2.3.2 - Azure Linux 3.0 - package upgrades

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.3.0-2
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.3.0-1
- License verified
- Original version for CBL-Mariner
