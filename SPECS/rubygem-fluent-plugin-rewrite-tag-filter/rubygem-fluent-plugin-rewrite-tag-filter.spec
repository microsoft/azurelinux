%global debug_package %{nil}
%global gem_name fluent-plugin-rewrite-tag-filter
Summary:        Fluentd Output filter plugin
Name:           rubygem-%{gem_name}
Version:        2.4.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-rewrite-tag-filter
Source0:        https://github.com/fluent/fluent-plugin-rewrite-tag-filter/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluent-config-regexp-type
Requires:       rubygem-fluentd
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Fluentd Output filter plugin to rewrite tags that matches specified attribute.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.4.0-1
- Update to v2.4.0.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 2.3.0-1
- License verified
- Original version for CBL-Mariner
