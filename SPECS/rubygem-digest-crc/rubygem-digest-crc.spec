%global debug_package %{nil}
%global gem_name digest-crc
Summary:        A Cyclic Redundancy Check (CRC) library for Ruby.
Name:           rubygem-digest-crc
Version:        0.6.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/postmodern/digest-crc
Source0:        https://github.com/postmodern/digest-crc/archive/refs/tags/v%{version}.tar.gz#/downloads/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-rake < 14.0.0
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Adds support for calculating Cyclic Redundancy Check (CRC) to the Digest module.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE.txt file to buildroot from Source0
cp LICENSE.txt %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.6.1-1
- License verified
- Original version for CBL-Mariner
