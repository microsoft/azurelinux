%global debug_package %{nil}
%global gem_name fluentd
Summary:        Fluentd event collector
Name:           rubygem-%{gem_name}
Version:        1.16.2
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Ruby
URL:            https://www.fluentd.org/
Source0:        https://github.com/fluent/fluentd/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         file-list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-async-http
Requires:       rubygem-cool.io < 2.0.0
Requires:       rubygem-http_parser.rb < 0.7.0
Requires:       rubygem-msgpack < 2.0.0
Requires:       rubygem-rake < 14
Requires:       rubygem-serverengine < 3.0.0
Requires:       rubygem-sigdump < 0.3
Requires:       rubygem-strptime < 1.0.0
Requires:       rubygem-tzinfo < 3.0
Requires:       rubygem-tzinfo-data < 2
Requires:       rubygem-yajl-ruby < 2
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Fluentd is an open source data collector designed to scale and simplify log
management. It can collect, process and ship many kinds of data in near
real-time.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}%{gemdir} --bindir %{buildroot}%{_bindir} %{gem_name}-%{version}.gem

%files
%defattr(-, root, root)
%{_bindir}/fluent-binlog-reader
%{_bindir}/fluent-ca-generate
%{_bindir}/fluent-cap-ctl
%{_bindir}/fluent-cat
%{_bindir}/fluent-ctl
%{_bindir}/fluent-debug
%{_bindir}/fluent-gem
%{_bindir}/fluent-plugin-config-format
%{_bindir}/fluent-plugin-generate
%{_bindir}/fluentd
%{gemdir}
%doc %{gemdir}/doc/fluentd-%{version}
%{gemdir}/cache/fluentd-%{version}.gem
%{gemdir}/specifications/fluentd-%{version}.gemspec

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.16.2-1
- Auto-upgrade to 1.16.2 - Azure Linux 3.0 - package upgrades

* Wed Nov 9 2022 Ahmed Badawi <ahmedbadawi@microsoft.com> - 1.14.6-2
- Add patch to fix CVE-2022-39379

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.14.6-1
- Update to v1.14.6.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.11.0-1
- License verified
- Original version for CBL-Mariner
