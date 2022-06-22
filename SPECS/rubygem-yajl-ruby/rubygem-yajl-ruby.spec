%global debug_package %{nil}
%global gem_name yajl-ruby
Summary:        A streaming JSON parsing and encoding library for Ruby
Name:           rubygem-yajl-ruby
Version:        1.3.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/brianmario/yajl-ruby
Source0:        https://github.com/brianmario/yajl-ruby/archive/refs/tags/%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
a C binding to the YAJL JSON parsing and generation library.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE file to buildroot from Source0
cp LICENSE %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.3.1-1
- Update to v1.3.1.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.4.1-1
- License verified
- Original version for CBL-Mariner
