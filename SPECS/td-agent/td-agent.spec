%define      debug_package %{nil}
%define control_service() (systemctl %{1} %{2})
%define disable_service() (systemctl %{1} %{2})
%define enable_service() (systemctl %{1} %{2})

Summary:        The stable distribution of Fluentd
Name:           td-agent
Version:        4.0.1
Release:        1%{?dist}
License:        ASL 2.0 AND BSD AND MIT AND Jason Evans Open Source
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/fluent-plugins-nursery/td-agent-builder
#Source0:      https://github.com/fluent-plugins-nursery/td-agent-builder/archive/testing-uploading-artifacts3.tar.gz
Source0:        td-agent-builder-testing-uploading-artifacts3.tar.gz
Patch0:         td-agent.patch
BuildRequires:  rubygem-httpclient, rubygem-td-client, rubygem-td
BuildRequires:  rubygem-fluent-plugin-td, rubygem-jmespath, rubygem-aws-partitions
BuildRequires:  rubygem-aws-sigv4, rubygem-aws-sdk-core, rubygem-aws-sdk-kms, rubygem-aws-sdk-sqs
BuildRequires:  rubygem-aws-sdk-s3, rubygem-fluent-plugin-s3, rubygem-webhdfs, rubygem-fluent-plugin-webhdfs
BuildRequires:  rubygem-fluent-plugin-rewrite-tag-filter, rubygem-ruby-kafka, rubygem-fluent-plugin-kafka
BuildRequires:  rubygem-elasticsearch, rubygem-fluent-plugin-elasticsearch, rubygem-prometheus-client
BuildRequires:  rubygem-fluent-plugin-prometheus, rubygem-fluent-plugin-prometheus_pushgateway, rubygem-fluent-plugin-record-modifier
BuildRequires:  rubygem-systemd-journal, rubygem-fluent-plugin-systemd, rubygem-nokogiri, rubygem-msgpack
BuildRequires:  rubygem-cool.io, rubygem-serverengine, rubygem-oj, rubygem-async-http, rubygem-http_parser.rb
BuildRequires:  rubygem-yajl-ruby, rubygem-sigdump, rubygem-tzinfo, rubygem-tzinfo-data, rubygem-strptime
BuildRequires:  rubygem-concurrent-ruby, rubygem-rake, rubygem-mini_portile2, rubygem-rdkafka
BuildRequires:  rubygem-ltsv, rubygem-protocol-http2, rubygem-protocol-http1, rubygem-protocol-http
BuildRequires:  rubygem-async-pool, rubygem-async-io, rubygem-async
BuildRequires:  rubygem-protocol-hpack, rubygem-timers, rubygem-nio4r
BuildRequires:  rubygem-console, rubygem-fiber-local, rubygem-ruby-progressbar
BuildRequires:  rubygem-zip-zip, rubygem-rubyzip, rubygem-td-logger
BuildRequires:  rubygem-parallel, rubygem-hirb, rubygem-fluent-logger
BuildRequires:  rubygem-aws-eventstream, rubygem-addressable, rubygem-public_suffix
BuildRequires:  rubygem-fluent-config-regexp-type, rubygem-digest-crc
BuildRequires:  rubygem-ffi, rubygem-elasticsearch-api, rubygem-elasticsearch-transport
BuildRequires:  rubygem-multi_json, rubygem-faraday, rubygem-ruby2_keywords
BuildRequires:  rubygem-multipart-post, rubygem-excon, rubygem-quantile
BuildRequires:  build-essential
BuildRequires:  git
BuildRequires:  libedit-devel
BuildRequires:  libyaml-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pkg-config
BuildRequires:  ruby
BuildRequires:  sudo
BuildRequires:  systemd
BuildRequires:  tar
BuildRequires:  unzip
BuildRequires:  zlib-devel
BuildRequires:  jemalloc
BuildRequires:  jemalloc-devel
BuildRequires:  rubygem-bundler, rubygem-fluentd
Requires:       libxcrypt
Requires:       rubygem-httpclient, rubygem-td-client, rubygem-td
Requires:       rubygem-fluent-plugin-td, rubygem-jmespath, rubygem-aws-partitions
Requires:       rubygem-aws-sigv4, rubygem-aws-sdk-core, rubygem-aws-sdk-kms, rubygem-aws-sdk-sqs
Requires:       rubygem-aws-sdk-s3, rubygem-fluent-plugin-s3, rubygem-webhdfs, rubygem-fluent-plugin-webhdfs
Requires:       rubygem-fluent-plugin-rewrite-tag-filter, rubygem-ruby-kafka, rubygem-fluent-plugin-kafka
Requires:       rubygem-elasticsearch, rubygem-fluent-plugin-elasticsearch, rubygem-prometheus-client
Requires:       rubygem-fluent-plugin-prometheus, rubygem-fluent-plugin-prometheus_pushgateway, rubygem-fluent-plugin-record-modifier
Requires:       rubygem-systemd-journal, rubygem-fluent-plugin-systemd, rubygem-nokogiri, rubygem-msgpack
Requires:       rubygem-cool.io, rubygem-serverengine, rubygem-oj, rubygem-async-http, rubygem-http_parser.rb
Requires:       rubygem-yajl-ruby, rubygem-sigdump, rubygem-tzinfo, rubygem-tzinfo-data, rubygem-strptime
Requires:       rubygem-concurrent-ruby, rubygem-rake, rubygem-mini_portile2, rubygem-rdkafka
Requires:       rubygem-ltsv, rubygem-protocol-http2, rubygem-protocol-http1, rubygem-protocol-http
Requires:       rubygem-async-pool, rubygem-async-io, rubygem-async
Requires:       rubygem-protocol-hpack, rubygem-timers, rubygem-nio4r
Requires:       rubygem-console, rubygem-fiber-local, rubygem-ruby-progressbar
Requires:       rubygem-zip-zip, rubygem-rubyzip, rubygem-td-logger
Requires:       rubygem-parallel, rubygem-hirb, rubygem-fluent-logger
Requires:       rubygem-aws-eventstream, rubygem-addressable, rubygem-public_suffix
Requires:       rubygem-fluent-config-regexp-type, rubygem-digest-crc
Requires:       rubygem-ffi, rubygem-elasticsearch-api, rubygem-elasticsearch-transport
Requires:       rubygem-multi_json, rubygem-faraday, rubygem-ruby2_keywords
Requires:       rubygem-multipart-post, rubygem-excon, rubygem-quantile
Requires:       rubygem-bundler, rubygem-fluentd
Requires:       ruby
Requires:       jemalloc
Requires:       jemalloc-devel

%description
The stable distribution of Fluentd

%prep
%setup -q -n td-agent-builder-testing-uploading-artifacts3
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
sudo ln -S %{_sbindir}/useradd %{_sbindir}/adduser
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
%{_prefix}/%{_unitdir}/td-agent.service
%{_tmpfilesdir}/td-agent.conf
%{_bindir}/td
%{_sbindir}/td-agent
%{_sbindir}/td-agent-gem
%config(noreplace) %{_sysconfdir}/td-agent/td-agent.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/td-agent
%attr(0755,td-agent,td-agent) %dir %{_localstatedir}/log/td-agent
%attr(0755,td-agent,td-agent) %dir %{_localstatedir}/log/td-agent/buffer
%attr(0755,td-agent,td-agent) %dir %{_sysconfdir}/td-agent
%attr(0755,td-agent,td-agent) %dir %{_sysconfdir}/td-agent/plugin
# NOTE: %{_tmpfilesdir} is available since CentOS 7
%attr(0755,td-agent,td-agent) %dir /tmp/td-agent

%changelog
* Tue Dec 01 2020 Henry Li <lihl@microsoft.com> - 4.0.1-1
- Original version for CBL-Mariner