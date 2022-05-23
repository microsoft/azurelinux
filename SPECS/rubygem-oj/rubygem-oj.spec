%global debug_package %{nil}
%global gem_name oj
Summary:        Optimized JSON
Name:           rubygem-oj
Version:        3.13.11
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            http://www.ohler.com/oj/
Source0:        https://github.com/ohler55/oj/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby

%description
A fast JSON parser and Object marshaller as a Ruby gem.

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
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 3.10.6-1
- License verified
- Original version for CBL-Mariner
