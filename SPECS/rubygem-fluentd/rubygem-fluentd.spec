%define      debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluentd
%define gembuilddir %{buildroot}%{gemdir}
Summary:        Fluentd event collector
Name:           rubygem-fluentd
Version:        1.11.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Ruby
URL:            https://www.fluentd.org/
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.4.0
Requires:       rubygem-async-http
Requires:       rubygem-cool.io < 2.0.0
Requires:       rubygem-cool.io >= 1.4.5
Requires:       rubygem-http_parser.rb < 0.7.0
Requires:       rubygem-http_parser.rb >= 0.5.1
Requires:       rubygem-msgpack < 2.0.0
Requires:       rubygem-msgpack >= 1.3.1
Requires:       rubygem-rake < 14
Requires:       rubygem-rake >= 13.0
Requires:       rubygem-serverengine < 3.0.0
Requires:       rubygem-serverengine >= 2.0.4
Requires:       rubygem-sigdump < 0.3
Requires:       rubygem-sigdump >= 0.2.2
Requires:       rubygem-strptime < 1.0.0
Requires:       rubygem-strptime >= 0.2.2
Requires:       rubygem-tzinfo < 3.0
Requires:       rubygem-tzinfo >= 1.0
Requires:       rubygem-tzinfo-data < 2
Requires:       rubygem-tzinfo-data >= 1.0
Requires:       rubygem-yajl-ruby < 2
Requires:       rubygem-yajl-ruby >= 1.0

%description
Fluentd is an open source data collector designed to scale and simplify log
management. It can collect, process and ship many kinds of data in near
real-time.

%prep
%setup -q -T -c

%build

%install
mkdir -p %{gembuilddir}
gem install --local --install-dir %{gembuilddir} --force %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{gembuilddir}/bin/* %{buildroot}/%{_bindir}
rmdir %{gembuilddir}/bin

%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root)
%{_bindir}/fluent-binlog-reader
%{_bindir}/fluent-ca-generate
%{_bindir}/fluent-cat
%{_bindir}/fluent-debug
%{_bindir}/fluent-gem
%{_bindir}/fluent-plugin-config-format
%{_bindir}/fluent-plugin-generate
%{_bindir}/fluentd
%{gemdir}

%doc %{gemdir}/doc/fluentd-1.11.0
%{gemdir}/cache/fluentd-1.11.0.gem
%{gemdir}/specifications/fluentd-1.11.0.gemspec

%changelog
