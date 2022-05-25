%global debug_package %{nil}
%global gem_name tzinfo-data
Summary:        Timezone Data for TZInfo
Name:           rubygem-%{gem_name}
Version:        1.2022.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://tzinfo.github.io/
Source0:        https://github.com/tzinfo/tzinfo-data/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-tzinfo

%description
a fast strptime/strftime engine which uses VM.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.2019.3-1
- License verified
- Original version for CBL-Mariner
