%global debug_package %{nil}
%global gem_name tzinfo
Summary:        Ruby Timezone Library
Name:           rubygem-tzinfo
Version:        2.0.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://tzinfo.github.io/
Source0:        https://github.com/tzinfo/tzinfo/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Requires:       rubygem-concurrent-ruby

%description
a Ruby library that provides access to time zone data
and allows times to be converted using time zone rules.

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
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 2.0.2-1
- License verified
- Original version for CBL-Mariner
