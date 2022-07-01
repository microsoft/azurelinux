%define      debug_package %{nil}
%define control_service() (systemctl %{1} %{2})
%define disable_service() (systemctl %{1} %{2})
%define enable_service() (systemctl %{1} %{2})
Summary:        The stable distribution of Fluentd
Name:           td-agent
Version:        4.0.1
Release:        8%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/fluent/fluent-package-builder
#Source0:       https://github.com/fluent/fluent-package-builder/archive/refs/tags/v%{version}.tar.gz
Source0:        fluent-package-builder-%{version}.tar.gz
# td-agent enforces the ruby version used for building in td-agent/config.rb file. 
# Therefore, everytime there's an upgrade in td-agent or ruby, please update this
# patch file to update BUNDLED_RUBY_VERSION and RUBYGEM_VERSION to use the correct ruby
# and rubygem installed in the system. Also update the shared library files of ruby, which contain
# ruby versions in their file names
Patch0:         td-agent.patch
BuildRequires:  build-essential
BuildRequires:  git
BuildRequires:  jemalloc
BuildRequires:  jemalloc-devel
BuildRequires:  libedit-devel
BuildRequires:  libyaml-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pkg-config
BuildRequires:  ruby = 3.1.2
BuildRequires:  rubygem-async-http
BuildRequires:  rubygem-aws-partitions
BuildRequires:  rubygem-aws-sdk-core
BuildRequires:  rubygem-aws-sdk-kms
BuildRequires:  rubygem-aws-sdk-s3
BuildRequires:  rubygem-aws-sdk-sqs
BuildRequires:  rubygem-aws-sigv4
BuildRequires:  rubygem-bigdecimal
BuildRequires:  rubygem-bundler
BuildRequires:  rubygem-cool.io
BuildRequires:  rubygem-elasticsearch
BuildRequires:  rubygem-fluent-plugin-elasticsearch
BuildRequires:  rubygem-fluent-plugin-kafka
BuildRequires:  rubygem-fluent-plugin-prometheus
BuildRequires:  rubygem-fluent-plugin-prometheus_pushgateway
BuildRequires:  rubygem-fluent-plugin-record-modifier
BuildRequires:  rubygem-fluent-plugin-rewrite-tag-filter
BuildRequires:  rubygem-fluent-plugin-s3
BuildRequires:  rubygem-fluent-plugin-systemd
BuildRequires:  rubygem-fluent-plugin-td
BuildRequires:  rubygem-fluent-plugin-webhdfs
BuildRequires:  rubygem-fluentd
BuildRequires:  rubygem-http_parser.rb
BuildRequires:  rubygem-httpclient
BuildRequires:  rubygem-jmespath
BuildRequires:  rubygem-msgpack
BuildRequires:  rubygem-nokogiri
BuildRequires:  rubygem-oj
BuildRequires:  rubygem-prometheus-client
BuildRequires:  rubygem-rdkafka
BuildRequires:  rubygem-ruby-kafka
BuildRequires:  rubygem-serverengine
BuildRequires:  rubygem-sigdump
BuildRequires:  rubygem-systemd-journal
BuildRequires:  rubygem-td
BuildRequires:  rubygem-td-client
BuildRequires:  rubygem-tzinfo
BuildRequires:  rubygem-tzinfo-data
BuildRequires:  rubygem-webrick
BuildRequires:  rubygem-webhdfs
BuildRequires:  rubygem-yajl-ruby
BuildRequires:  sudo
BuildRequires:  systemd
BuildRequires:  tar
BuildRequires:  unzip
BuildRequires:  zlib-devel
Requires:       jemalloc
Requires:       jemalloc-devel
Requires:       libxcrypt
Requires:       ruby = 3.1.2
Requires:       rubygem-async-http
Requires:       rubygem-aws-partitions
Requires:       rubygem-aws-sdk-core
Requires:       rubygem-aws-sdk-kms
Requires:       rubygem-aws-sdk-s3
Requires:       rubygem-aws-sdk-sqs
Requires:       rubygem-aws-sigv4
Requires:       rubygem-bundler
Requires:       rubygem-bigdecimal
Requires:       rubygem-cool.io
Requires:       rubygem-elasticsearch
Requires:       rubygem-fluent-plugin-elasticsearch
Requires:       rubygem-fluent-plugin-kafka
Requires:       rubygem-fluent-plugin-prometheus
Requires:       rubygem-fluent-plugin-prometheus_pushgateway
Requires:       rubygem-fluent-plugin-record-modifier
Requires:       rubygem-fluent-plugin-rewrite-tag-filter
Requires:       rubygem-fluent-plugin-s3
Requires:       rubygem-fluent-plugin-systemd
Requires:       rubygem-fluent-plugin-td
Requires:       rubygem-fluent-plugin-webhdfs
Requires:       rubygem-fluentd
Requires:       rubygem-http_parser.rb
Requires:       rubygem-httpclient
Requires:       rubygem-jmespath
Requires:       rubygem-msgpack
Requires:       rubygem-nokogiri
Requires:       rubygem-oj
Requires:       rubygem-prometheus-client
Requires:       rubygem-rdkafka
Requires:       rubygem-ruby-kafka
Requires:       rubygem-serverengine
Requires:       rubygem-sigdump
Requires:       rubygem-systemd-journal
Requires:       rubygem-td
Requires:       rubygem-td-client
Requires:       rubygem-tzinfo
Requires:       rubygem-tzinfo-data
Requires:       rubygem-webhdfs
Requires:       rubygem-webrick
Requires:       rubygem-yajl-ruby
Requires(pre):  shadow-utils
AutoReq:        no

%description
The stable distribution of Fluentd

%prep
%setup -q -n fluent-package-builder-%{version}
%patch0 -p1

%build

%install
sudo rake build:rpm_config TD_AGENT_STAGING_PATH=%{buildroot}
sudo rake build:all TD_AGENT_STAGING_PATH=%{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1
for man in `find %{buildroot} -type f -wholename '*/man/man[1-9]/*.[1-9]'`; do
    gzip ${man}
done

cd -
mkdir -p %{buildroot}%{_localstatedir}/run/td-agent
mkdir -p %{buildroot}%{_localstatedir}/log/td-agent
mkdir -p %{buildroot}%{_localstatedir}/log/td-agent/buffer
mkdir -p %{buildroot}%{_sysconfdir}/td-agent/plugin
mkdir -p %{buildroot}/tmp/td-agent

%pre
if ! getent group td-agent >/dev/null; then
    %{_sbindir}/groupadd -r td-agent
fi
if ! getent passwd td-agent >/dev/null; then
    %{_sbindir}/adduser -r -g td-agent -d %{_localstatedir}/lib/td-agent -s /sbin/nologin -c 'td-agent' td-agent
fi

%preun
if [ $1 -eq 0 ]; then
  %{control_service stop td-agent}
  %{disable_service disable td-agent}
fi

%post
if [ $1 -eq 1 ]; then
  %{enable_service enable td-agent}
fi
if [ $1 -eq 2 ]; then
  %{control_service condrestart td-agent}
fi
if [ -d "%{_sysconfdir}/prelink.conf.d/" ]; then
  echo "prelink detected. Installing %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf ..."
  if [ ! -f %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf ]; then
      cp -f /opt/td-agent/share/td-agent-ruby.conf %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf
  else
    if [ $(grep '\-b /opt/td-agent/embedded/bin/ruby' -c %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf) -eq 1 ]; then
      echo "old-prelink detected, Update %{_sysconfdir}/prelink.conf ..."
      sed -i"" %{_sysconfdir}/prelink.conf.d/td-agent-ruby.conf -e "s,/embedded/,/,"
    fi
  fi
elif [ -f "%{_sysconfdir}/prelink.conf" ]; then
  if [ $(grep '\-b /opt/td-agent/embedded/bin/ruby' -c %{_sysconfdir}/prelink.conf) -eq 1 ]; then
    echo "old-prelink detected, but %{_sysconfdir}/prelink.conf.d/ does't exist. Update %{_sysconfdir}/prelink.conf ..."
    sed -i"" %{_sysconfdir}/prelink.conf -e "s,/embedded/,/,"
  elif [ $(grep '\-b /opt/td-agent/bin/ruby' -c %{_sysconfdir}/prelink.conf) -eq 0 ]; then
    echo "prelink detected, but %{_sysconfdir}/prelink.conf.d/ does't exist. Adding %{_sysconfdir}/prelink.conf ..."
    echo "-b /opt/td-agent/bin/ruby" >> %{_sysconfdir}/prelink.conf
  fi
fi
sudo systemctl start td-agent

%files
%doc README.md
%license LICENSE
%defattr(-,root,root,-)
/opt/*
/opt/td-agent/share/td-agent.conf.tmpl
%{_tmpfilesdir}/td-agent.conf
%{_bindir}/td
%{_sbindir}/td-agent
%{_sbindir}/td-agent-gem
%{_unitdir}/td-agent.service
%config(noreplace) %{_sysconfdir}/td-agent/td-agent.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/td-agent
%attr(0755,td-agent,td-agent) %dir %{_localstatedir}/log/td-agent
%attr(0755,td-agent,td-agent) %dir %{_localstatedir}/log/td-agent/buffer
%attr(0755,td-agent,td-agent) %dir %{_sysconfdir}/td-agent
%attr(0755,td-agent,td-agent) %dir %{_sysconfdir}/td-agent/plugin
%attr(0755,td-agent,td-agent) %dir /tmp/td-agent

%changelog
*  Thu Jun 23 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.0.1-8
-  Migrate from 1.0 and update ruby version to 3.1.2 in SPEC and patch file.

* Thu Jun 23 2022 Henry Li <lihl@microsoft.com> - 4.0.1-7
- Update Source0 to use the official v4.0.1 release
- Update td-agent.patch to align with the new source code

* Mon Jun 06 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.0.1-6
- Update td-agent.patch due to the upgrade in ruby

* Tue Mar 08 2022 Henry Li <lihl@microsoft.com> - 4.0.1-5
- Update td-agent.patch due to the upgrade in ruby
- Add versioning for ruby in BR and runtime requirement

* Thu Jan 20 2022 Cameron Baird <cameronbaird@microsoft.com> - 4.0.1-4
- Bump release to build and republish with mariner-rpm-macros fix to filter out references to module_info.ld in pkgconfig files

* Wed May 05 2021 Henry Li <lihl@microsoft.com> - 4.0.1-3
- Update patch to use ruby 2.6.7

* Mon Mar 01 2021 Henry Li <lihl@microsoft.com> - 4.0.1-2
- Add shadow-utils as BuildRequires and remove creating the sym link for adduser

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 4.0.1-1
- Initial CBL-Mariner import from Treasure Data (license: Apache2).
- License verified.

* Fri May 22 2020 Masahiro Nakagawa <repeatedly@gmail.com> - 4.0.0.rc1-1
- New upstream release.

* Wed May 06 2020 Takuro Ashie <ashie@clear-code.com> - 3.7.1-1
- New upstream release.

* Tue Apr 07 2020 Hiroshi Hatake <hatake@clear-code.com> - 3.7.0-1
- New upstream release.

* Tue Feb 25 2020 Takuro Ashie <ashie@clear-code.com> - 3.6.0-1
- New upstream release.
