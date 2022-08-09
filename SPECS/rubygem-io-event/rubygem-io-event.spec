%global gem_name io-event
Summary:        An event loop
Name:           rubygem-%{gem_name}
Version:        1.0.7
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/io-event
Source0:        https://github.com/socketry/io-event/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(io-event) = %{version}-%{release}

%description
An event loop

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add README.md file to buildroot from Source0
cp README.md %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/README.md
%{gemdir}

%changelog
* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.7-1
- License verified
- Original version for CBL-Mariner
