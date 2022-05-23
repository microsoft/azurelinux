%global debug_package %{nil}
%global gem_name strptime
Summary:        a fast strptime/strftime engine which uses VM
Name:           rubygem-strptime
Version:        0.2.5
Release:        1%{?dist}
License:        NARUSE, Yui Open Source
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/nurse/strptime
Source0:        https://github.com/nurse/strptime/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby

%description
a fast strptime/strftime engine which uses VM.

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
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 0.2.5-1
- License verified
- Original version for CBL-Mariner
