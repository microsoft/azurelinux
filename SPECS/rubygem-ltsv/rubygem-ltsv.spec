%global debug_package %{nil}
%global gem_name ltsv
Summary:        A Parser / Dumper for LTSV
Name:           rubygem-%{gem_name}
Version:        0.1.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/condor/ltsv
Source0:        https://github.com/condor/ltsv/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby

%description
A Parser / Dumper for Labelled Tab-Separated Values (LTSV).

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
* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 0.1.2-1
- License verified
- Original version for CBL-Mariner
