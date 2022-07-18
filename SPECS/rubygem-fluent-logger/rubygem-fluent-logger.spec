%global debug_package %{nil}
%global gem_name fluent-logger
%global gems_version 3.1.0
Summary:        fluent logger for ruby
Name:           rubygem-fluent-logger
Version:        0.9.0
Release:        2%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-logger-ruby
Source0:        https://github.com/fluent/fluent-logger-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-ruby-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-msgpack < 2
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
A structured event logger.

%prep
%autosetup -p1 -n %{gem_name}-ruby-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} --bindir %{buildroot}%{_prefix}/lib/ruby/gems/%{gems_version}/bin/ %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/COPYING
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.9.0-2
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 0.9.0-1
- License verified
- Original version for CBL-Mariner
